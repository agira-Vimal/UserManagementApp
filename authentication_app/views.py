from django.http import HttpResponse,HttpResponseForbidden,JsonResponse
from django.shortcuts import redirect, render ,get_object_or_404
from authentication_app.forms import CustomUserForm, UserProfileForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required,user_passes_test
from django.core.mail import send_mail
from .models import *
import secrets
import os
from dotenv import load_dotenv
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse
load_dotenv()


def home_page(request):
    return render(request, "auth_app/index.html")


otp = os.getenv("OTP")


def register_page(request):
    form = CustomUserForm()
    if request.method == "POST":
        # print(request.POST)
        form = CustomUserForm(request.POST)
        # print(form)
        if form.is_valid():
            username = request.POST.get("username")
            email = request.POST.get("email")
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username is already taken.")
                return render(request, "auth_app/register.html", {"form": form})
            if User.objects.filter(email=email).exists():
                messages.error(request, "Email ID is already taken.")
                return render(request, "auth_app/register.html", {"form": form})
            global otp
            otp = secrets.randbelow(999999)
            subject = f"Welcome {username}"
            message = f"""Thank You for choosing Our Application!
Here is your One Time Password for Verification\nOne Time Password:{otp}"""
            from_email = "iamvimal107@gmail.com"
            recipient_list = [request.POST.get("email")]
            send_mail(subject, message, from_email, recipient_list)
            # form.save()
            # messages.success(request,"Registration Success You can Login Now..!")
            return render(
                request,
                "auth_app/email_verify.html",
                {"original_otp": otp, "form": form},
            )
    return render(request, "auth_app/register.html", {"form": form})


def email_verify(request):
    form = CustomUserForm()
    if request.method == "POST":
        recieved_otp = request.POST.get("otp")
        original_otp = request.POST.get("original_otp")
        if recieved_otp and original_otp:
            form = CustomUserForm(request.POST)
            if recieved_otp == original_otp and form.is_valid():
                form.save()
                messages.success(request, "Registration Success You can Login Now..!")
                return redirect("/login")
            else:
                messages.error(request, "Invalid OTP!")
                return render(
                    request,
                    "auth_app/email_verify.html",
                    {"form": form, "original_otp": otp},
                )
        else:
            form = CustomUserForm(request.POST)
            messages.error(request, "Please Provide OTP!")
            return render(request, "auth_app/email_verify.html", {"form": form})

    return render(request, "auth_app/email_verify.html", {"form": form})


def login_page(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method == "POST":
            name = request.POST.get("username")
            pwd = request.POST.get("password")
            if not name or not pwd:
                messages.error(request, "Please Fill All the Field")
                return render(request,"auth_app/login.html",{"name":name})
            if not (
                User.objects.filter(username=name).exists()
                or User.objects.filter(email=name).exists()
            ):
                messages.error(request, "User not Exists.Try to SignUp First!")
                return redirect("/login")
            if "@" in name:
                existing_user = User.objects.get(email=name)
                user = authenticate(
                    request, username=existing_user.username, password=pwd
                )
                print(user)
                if user is None:
                    messages.error(request, "Invalid Email or Password!  ")
                    return render(request,"auth_app/login.html",{"name":name})
                else:
                    login(request, user)
                    messages.success(request, "Logged in Successfully")
                    return render(request, "auth_app/index.html")
            else:
                user = authenticate(request, username=name, password=pwd)
                if user is None:
                    messages.error(request, "Invalid Username or Password!  ")
                    return render(request,"auth_app/login.html",{"name":name})
                else:
                    login(request, user)
                    messages.success(request, "Logged in Successfully")
                    return render(request, "auth_app/index.html")

        return render(request, "auth_app/login.html")


@login_required
def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Logged out Successfully")
    return redirect("/")


@login_required
def changed_password(request):
    messages.success(
        request,
        "Password Changed Succesfully!Try to Logout and Login with New Password!",
    )
    return redirect("/")


@login_required
def update_user_profile(request):
    current_user = UserProfile.objects.get(user__id=request.user.id)
    form = UserProfileForm(request.POST or None,instance=current_user)
    if request.method=="POST":
        form = UserProfileForm(request.POST or None,request.FILES,instance=current_user)
        if form.is_valid():
            form.save()
            messages.success(request, "User Info Updated Successfully!!")
            return redirect("/user_profile_page")
    default_profile_picture_url = '/static/images/user_profile.jpg'
    profile_picture= current_user.profile_picture.url if current_user.profile_picture else default_profile_picture_url
   
    context= {
        'username':request.user.username,
        'email':request.user.email,
        'profile_picture':profile_picture,
        'form':form
    }

    return render(request, "auth_app/update_user_page.html", context)


# if request.method=="POST":

#     user_profile = UserProfile.objects.select_related('user').get(user=request.user)

#     default_profile_picture_url = '/images/default_user_pic.jpg'
#     context = {
#         'username': request.user.username,
#         'email': request.user.email,
#         'surname': user_profile.surname or 'No Data added',
#         'phone_number': user_profile.phone_number or 'No Data added',
#         'address_line_1': user_profile.address_line_1 or 'No Data added',
#         'address_line_2': user_profile.address_line_2 or 'No Data added',
#         'postcode': user_profile.postcode or 'No Data added',
#         'state': user_profile.state or 'No Data added',
#         'country': user_profile.country or 'No Data added',
#         'profile_picture': user_profile.profile_picture.url if user_profile.profile_picture else default_profile_picture_url,
#     }


# return render(request, 'auth_app/user_profile_page.html', context)
@login_required
def user_profile_page(request):
    user_profile=UserProfile.objects.select_related('user').get(user=request.user)
    default_profile_picture_url = '/static/images/user_profile.jpg'
    context = {
        'username': request.user.username,
        'email': request.user.email,
        'surname': user_profile.surname or 'No Data added',
        'phone_number': user_profile.phone_number or 'No Data added',
        'address_line_1': user_profile.address_line_1 or 'No Data added',
        'address_line_2': user_profile.address_line_2 or 'No Data added',
        'postcode': user_profile.postcode or 'No Data added',
        'state': user_profile.state or 'No Data added',
        'country': user_profile.country or 'No Data added',
        'profile_picture': user_profile.profile_picture.url if user_profile.profile_picture else default_profile_picture_url,
    }
    return render(request,"auth_app/user_profile_page.html",context)

# def is_superuser(user):
#     return user.is_superuser

# @user_passes_test(is_superuser,login_url='/login')

@login_required
def dashboard(request):
    if not request.user.is_superuser:
        messages.error(request, "Only Admins Can Access this Feature!!")
        return redirect('/')

    user_profiles = UserProfile.objects.select_related('user')

    # Get the username from the query parameters
    username = request.GET.get('username', '')

    if username:
        # Perform a case-insensitive search for UserProfile based on the provided username
        user_profiles = user_profiles.filter(user__username__icontains=username)

    # Paginate the user profiles
    page = request.GET.get('page', 1)
    paginator = Paginator(user_profiles, 1)  # Show 1 profiles per page

    try:
        users_data = paginator.page(page)
    except PageNotAnInteger:
        users_data = paginator.page(1)
    except EmptyPage:
        users_data = paginator.page(paginator.num_pages)

    num_pages = range(1, users_data.paginator.num_pages + 1)

    if not user_profiles.exists():
        messages.error(request, f"No user found with the username containing {username}")

    return render(request, 'auth_app/dashboard.html', {'users_data': users_data, 'num_pages': num_pages, 'searched_username': username})


@login_required
def edit_profile(request,user_id):
    if request.user.is_superuser:
        current_user = UserProfile.objects.get(user__id=user_id)
        form=UserProfileForm(request.POST or None,request.FILES or None,instance=current_user)  
        
        if request.method=='POST':
            if form.is_valid():
                form.save()
                messages.success(request,"Edited Successfully!!")
                return redirect('/dashboard')
        default_profile_picture_url = '/static/images/user_profile.jpg'
        profile_picture= current_user.profile_picture.url if current_user.profile_picture else default_profile_picture_url
        context={
            'username':current_user.user.username,
            'email':current_user.user.email,
            'profile_picture':profile_picture,
            "form":form
        }
        return render(request,"auth_app/update_user_page.html",context)
    else:
        messages.error(request,"Only Admins Can Access this Feature!!")
        return redirect('/')
    
# @user_passes_test(is_superuser)
@login_required
def delete_profile(request, user_id):
    if request.user.is_superuser:
        try:
            user_profile = UserProfile.objects.get(user__id=user_id)
            user_profile.user.delete()
            messages.success(request, "User Deleted Successfully!!")
            return redirect("/dashboard")
        except UserProfile.DoesNotExist:
            messages.error(request, "User not found.")
            return redirect('/')
    else:
        messages.error(request, "Only Admins Can Access this Feature!!")
        return redirect('/')
# def permission_denied(request, exception=None):
#     if request.user.is_authenticated:
#         messages.error(request, 'Only Admins can Access this Feature!!')
#         return redirect('/dashboard')
#     else:
#         return render(request, 'auth_app/403.html', status=403)
