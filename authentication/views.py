from django.core.mail import EmailMessage,send_mail,EmailMultiAlternatives
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import login,logout
from my_site.settings import EMAIL_HOST_USER
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str
from .tokens import generate_token
from .tests import generate_activateorreset_otp,send_generated_otp
from .models import User
from django.contrib.auth.password_validation import UserAttributeSimilarityValidator,CommonPasswordValidator,MinimumLengthValidator,NumericPasswordValidator
from .custom_authentication import EmailorUsernameModelBackend
#from .custom_authentication2 import EmailorUsernameModelBackend
from .forms import EmailReset
from address.models import UserAddress
from django.urls import reverse
from django.db.models import Q
from cart.models import Cart
from datetime import datetime
import pyotp
import os 
import json
from django.http.response import JsonResponse
from address.views import state_and_lga
from django.contrib.sites.models import Site
from dotenv import load_dotenv
from django.contrib.auth.hashers import make_password,check_password
load_dotenv()


# Create your views here..


#forget password view. User input username or email and we search if user exists in our data base.
def forgetpassword(request):
    current_site = get_current_site(request)
    if request.method == "POST":
        try:
            mobile_or_mail = request.POST.get("email_or_mobile").strip()
            if mobile_or_mail.lower():
            
                model = User.objects.get(Q(email=mobile_or_mail) | Q(mobile=mobile_or_mail))

                #Email Password reset
                try: 
                    subject = 'Password reset from Adimeals.com'
                    body = render_to_string('email_confirmation.html',{
                        'name':model.first_name,
                        'domain':current_site.domain,
                        'uid':urlsafe_base64_encode(force_bytes(model.pk)),
                        'token': generate_token.make_token(model),
                        'resetoractivate': 'reset',
                        'otp': generate_activateorreset_otp(request),

                    }) 
                    from_email = EMAIL_HOST_USER
                    to = [model.email]
                    email = EmailMultiAlternatives(
                        subject,
                        body,
                        from_email,
                        to,
                    )
                    email.content_subtype = "html"
                    email.send(fail_silently = True)
                    messages.success(request, f"We have sent RESET PASSWORD link to {model.email} to reset your password!")
                    return redirect('authentication:forgetpassword')
                except Site.DoesNotExist:
                    messages.error(request, "Site does not exist!")
                    return redirect('authentication:forgetpassword')
        except:
            messages.error(request, "User does not exist in our database! Be sure to input a correct email or username.")
            return redirect('authentication:forgetpassword')

    return render(request,'authentication/forgetpassword.html',{})



def otp(request):
    #This view is to verify user phone number after signup or update phone number after login.
    fname = ""
    lname = ""
    email = ""
    mobile = ""
    password = "" 

    try:
        fname = request.session['fname']
        lname = request.session['lname']
        email = request.session['email']
        mobile = request.session['mobile']
        password = request.session['password']
    except KeyError:
        pass
    
    
    if request.method == "POST":
        otp = request.POST.get("otp")
    
        otp_secret = request.session['otp_secret_key']
        valid_date = request.session['otp_valid_date']
        if otp_secret and valid_date is not None:
            valid_date = datetime.fromisoformat(valid_date)
            if valid_date > datetime.now():
                totp = pyotp.TOTP(otp_secret, interval=600)
                verify_totp = totp.verify(otp)
                print(verify_totp)
                if totp.verify(otp):
                    if not request.user.is_authenticated:
                        try:
                            user = User.objects.create_user(first_name=fname,last_name=lname,email=email,mobile=mobile,password=password)
                            user = User.objects.get(email=email)
                        
                            session_user = User.objects.filter(email=request.session.get('email'))
                        
                            if session_user is not None:
                                del request.session['fname']
                                del request.session['lname']
                                del request.session['email']
                                del request.session['mobile']


                            #Daniel, do not forget to set user.is_active = False during deployment.
                            if user.admin:
                                user.is_active = True
                                user.save()
                            else:
                                user.is_active = False
                                user.save()
                        

                            #Email Confirmation
                            try: 
                                subject = 'Email confirmation from Adimeals.com'
                                body = render_to_string('email_confirmation.html',{
                                    'name':user.first_name,
                                    'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                                    'token': generate_token.make_token(user),
                                    'resetoractivate': 'activate',
                                    'otp': generate_activateorreset_otp(request),
                                }) 
                                from_email = EMAIL_HOST_USER
                                to = [user.email]
                                email = EmailMultiAlternatives(
                                    subject,
                                    body,
                                    from_email,
                                    to,
                                )
                                email.content_subtype = "html"
                                email.send(fail_silently = True)

                                del request.session['otp_secret_key']
                                del request.session['otp_valid_date']
                                messages.success(request, "ADi has successfully verified phone number, Check your mail to activate account.")
                                return redirect('authentication:signin')

                            except Site.DoesNotExist:
                                messages.success(request,"Site does not exist.")
                                return redirect('authentication:signup')
                        except ValueError:
                            messages.error(request, "User created!\nCheck your mail to activate account.")
                            return redirect('authentication:signin')
                    else:
                        user = User.objects.get(email=request.user.email)
                        user.mobile = request.session['mobile']
                        user.first_name = request.session['fname']
                        user.last_name = request.session['lname']
                        user.email = request.session['email']
                        user.save()
                        del request.session['mobile']
                        del request.session['fname']
                        del request.session['lname']
                        del request.session['email']
                        del request.session['otp_secret_key']
                        del request.session['otp_valid_date']
                        messages.success(request, "Account updated successfully!")
                        return redirect('authentication:account_info')
                else:
                    messages.error(request, "Invalid one time password")
                    return redirect('authentication:otp')
            else:
                #messages.error(request, "One time password has expired")#This resend another otp to user after it expires.
                send_generated_otp(request)
                messages.success(request,f"We have sent resent another OTP to your whatsapp number at 0{mobile}.")
                return redirect('authentication:otp')
        else:
            messages.error(request, "Ooops! Something went wrong")
            return redirect('authentication:otp')

    return render(request,'authentication/otp.html',{})




def signup(request):
    session_fname = ""
    session_lname = ""
    session_email = ""
    session_mobile = ""

    if request.method == "POST":
        fname = request.POST.get("fname").strip()
        lname = request.POST.get("lname").strip()
        email = request.POST.get("email").strip()
        mobile = request.POST.get("mobile").strip()
        password = request.POST.get("password").strip()
        password2 = request.POST.get("password2").strip()

        def check_mobile(mobile):
            trimmed_mobile = ""
            list_mobile = str(mobile)
            if len(list_mobile) == 10:
                trimmed_mobile = list_mobile
            elif len(list_mobile) == 11:
                trimmed_mobile = list_mobile[1:]
            elif len(list_mobile) < 10 or len(list_mobile) > 11:
                trimmed_mobile = list_mobile

            mobile = "+234" + trimmed_mobile
            
            return mobile
        
        mobile = str(check_mobile(mobile))

        
        try:
            request.session['fname'] = fname
            request.session['lname'] = lname
            request.session['email'] = email
            request.session['password'] = password
            request.session['password2'] = password2
            
            if mobile is not None and len(mobile) == 14:
                request.session['mobile'] = mobile[4:]
            elif len(mobile) < 14 or len(mobile) > 14:
                request.session['mobile'] = mobile[4:]
        except KeyError:
            pass

        email = email.lower()
        password = password.lower()
        password2 = password.lower()

        if User.objects.filter(mobile=mobile):
            messages.error(request, "Phone number already exist!")
            return redirect('authentication:signup')
        
        elif User.objects.filter(email=email):
            messages.error(request, "E-mail already exist!")
            return redirect('authentication:signup')
        
        elif len(mobile) > 14 or len(mobile) < 14:
            messages.error(request, "Phone no either too long or short. Correct phone number!")
            return redirect('authentication:signup')

        elif password != password2:
            messages.error(request, "Passwords do not match!")
            return redirect('authentication:signup')


        elif password:
            try:
                UserAttributeSimilarityValidator().validate(password)
            except:
                messages.error(request,"Password too similar to user attribute provided.\nPlease, try another password!")
                return redirect('authentication:signup')
            try:
                CommonPasswordValidator().validate(password)
            except:     
                messages.error(request,"Password too common and easy.\nPlease, try another password!")
                return redirect('authentication:signup')
            try:
                MinimumLengthValidator().validate(password)
            except:
                messages.error(request,"Only a minimum characters of 8 is allowed.\nPlease, try another password!")
                return redirect('authentication:signup')
            try:
                NumericPasswordValidator().validate(password)
            except:
                messages.error(request,"Numeric only password is not allowed.\nPlease, try another password!")
                return redirect('authentication:signup')
            
        send_generated_otp(request)    
        messages.success(request,f"Let's verify that you truly own the phone number provided.\nWe have sent otp to 0{mobile[4:]}.")
        return redirect('authentication:otp')
    
    else:
        try:  
            session_fname = request.session.get('fname', "")
            session_lname = request.session.get('lname', "") 
            session_email = request.session.get('email', "")
            session_mobile = request.session.get('mobile', "")
            session_password = request.session.get('password', "")
            session_password2 = request.session.get('password2', "")
        except:
            pass
    
    return render(request,'authentication/signup_kunkky.html',{
        'fname':session_fname,
        'lname':session_lname,
        'email':session_email,
        'mobile':session_mobile,
        'password':session_password,
        'password2':session_password2,
    })





def signin(request):
    user_address = ""
    username = ""

    if request.method == "POST":
        username = request.POST.get("username").strip()
        password = request.POST.get("password").strip()
        remember_me = request.POST.get("checkbox")

        def check_if_mobile(username):
            trimmed_username = ""
            if not "@" in username:
                list_username = str(username)
                if len(list_username) == 10:
                    trimmed_username = list_username
                elif len(list_username) == 11:
                    trimmed_username = list_username[1:]
                elif len(username) < 10 or len(list_username) > 11:
                    trimmed_username = list_username

                username = "+234" + trimmed_username
            else:
                username = username
            return username
        
        username = str(check_if_mobile(username))

        try:
            if not "@" in username and len(username) == 14:
                request.session['session_username'] = username[4:]
                request.session['session_password'] = password
            elif "@" in username:
                request.session['session_username'] = username  
                request.session['session_password'] = password
            elif len(username) < 14 or len(username) > 14:
                request.session['session_username'] = username[4:]
                request.session['session_password'] = password
                messages.info(request, "Phone no either too long or short. Correct phone no!")
                return redirect(request.META.get('HTTP_REFERER')) 
        except KeyError:
            pass

        username = username.lower()
        password = password.lower()

        user = EmailorUsernameModelBackend.authenticate(EmailorUsernameModelBackend,
                                                        request,
                                                        username,
                                                        password)
        
        #Daniel, do not forget to add "and user.is_active == True during deployment"
        if user is not None and user.is_active == True:
            if not remember_me:
                request.session.set_expiry(0)
            else:
                request.session.set_expiry(None)
            
            login(request, user)

            
            try:
                cart = Cart.objects.get(session_id=request.session.get('cart_users'),is_paid=False)
                if Cart.objects.filter(user=request.user,is_paid=False).exists():
                    cart.user = None
                    cart.save()
                else:
                    cart.user = request.user
                    cart.save()
            except Cart.DoesNotExist:
                pass
            except KeyError:
                pass

            try:
                user_address = UserAddress.objects.get(user=request.user)
            except UserAddress.DoesNotExist:
                messages.success(request, "You have successfully logged in! Please, kindly create address.")
                return redirect('address:register_address')
 
            if request.user.is_authenticated:
                del request.session['session_username']
                del request.session['session_password']

            if user_address is not None:    
                messages.success(request, "You have successfully logged in")
                try:
                    price_slug = request.session.get('price-slug')
                except KeyError:
                    pass
                if price_slug != None:
                    messages.success(request, "Let's continue from where you stopped...")
                    return redirect(reverse('payments:payment',args=[price_slug[0],price_slug[1]]))
                else:
                    return redirect('food_app:soupbox')
        else:
            messages.error(request, "Bad credentials! or Check your mail to verify account if you have not!")
            return redirect('authentication:signin')

    return render(request,'authentication/signin_kunkky.html',{
        'username':request.session.get('session_username', ""),
        'password':request.session.get('session_password', ""),
        })



def signout(request):

    logout(request)
    messages.success(request, "You have successfully signed out!")
    return redirect('home')



def activate(request, uidb64, token, resetoractivate, otp):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError,user.DoesNotExist):
        user = None

    otp_secret = request.session['otp_secret_key_resetoractivate']  
    valid_date = request.session['otp_valid_date_resetoractivate']
    if otp_secret and valid_date is not None:
        valid_date = datetime.fromisoformat(valid_date)
        if valid_date > datetime.now():
            totp = pyotp.TOTP(otp_secret, interval=86400)
            if totp.verify(otp):
                if user is not None and generate_token.check_token(user, token) and resetoractivate == "activate":
                    user.is_active = True 
                    fname = user.first_name
                    user.save()
                    login(request, user)

                    try:
                        cart = Cart.objects.get(session_id=request.session.get('cart_users'),is_paid=False)
                        if Cart.objects.filter(user=request.user,is_paid=False).exists():
                            cart.user = None
                            cart.save()
                        else:
                            cart.user = request.user
                            cart.save()
                    except Cart.DoesNotExist:
                        pass
                    except KeyError:
                        pass

                    messages.success(request, f"Email verified successfully!")
                    return redirect('address:register_address')
                elif user is not None and generate_token.check_token(user, token) and resetoractivate == "reset":
                    return redirect(reverse('authentication:reset',args=[uid,token]))
                else:
                    return render(request, 'activation_failed.html')                
            else:
                messages.error(request, "Expired link")
                return redirect('authentication:signin')
        else:
            messages.error(request, "Expired link")
            return redirect('authentication:signin')
    else:
        messages.error(request, "Ooops! Something went wrong")
        return redirect('authentication:signin')
        

def account_info(request):
    #This is a view that displays the current information of the user!
    #It displays the username, first name, last name and email. it also gives the user access to edit the account information.
    address = ""
    try:
        address = UserAddress.objects.get(user=request.user)
        mobile = str(address.user.mobile)
        phone_no = f"0{mobile[4:]}"
        
        
    except UserAddress.DoesNotExist:
        messages.info(request, "Please, kindly fill in your address")
        return redirect(reverse('address:register_address'))
    except AttributeError:
        pass
    except Exception as e:
        messages.info(request, "Oooops!! Something went wrong.")
        return redirect(reverse('address:register_address'))

    return render(request,'authentication/account_info.html',{'address':address,'mobile':phone_no})


def edit_account(request):
    #This is a view to edit a user's account information

    #What I did here is, I first of all listed out all the details of the user currently logged in 
    #Then I got all the user inputs from the "Edit info template"
    #After which I got the User object, then inserted each new input from edit info template.

    #Here I added a Phone number form to this view to update phone number

    user_fname = request.user.first_name
    user_lname = request.user.last_name
    user_email = request.user.email
    user_mobile = request.user.mobile

    user = User.objects.get(email=user_email)

    if request.method == "POST":
        fname = request.POST.get("fname").strip()
        lname = request.POST.get("lname").strip()
        email = request.POST.get("email").strip()
        mobile = request.POST.get("mobile").strip()       
    
        email = email.lower()

        
        if User.objects.filter(email=email):
            messages.error(request, "Email has been taken!")
            return redirect('authentication:edit_account')
        elif User.objects.filter(mobile=mobile):
            messages.error(request, "Phone number has been taken!")
            return redirect('authentication:edit_account')
        elif User.objects.filter(first_name=fname):
            messages.error(request, "First name is currently being used!")
            return redirect('authentication:edit_account')
        elif User.objects.filter(last_name=lname):
            messages.error(request, "Last name is currently being used!")
            return redirect('authentication:edit_account')
        elif mobile == request.user.mobile:
            messages.error(request, "Phone number already in use by you! Change number to proceed")
            return redirect('authentication:edit_account')

        if mobile == "":
            mobile = user_mobile
        else:
            if len(mobile) > 11 or len(mobile) < 11:
                messages.error(request, "PHONE NUMBER must be 11 digits!")
                return redirect('authentication:edit_account')
            if fname == "":
                request.session['fname'] = request.user.first_name
            else:
                request.session['fname'] = fname
            
            if lname == "":
                request.session['lname'] = request.user.last_name
            else:
                request.session['lname'] = lname

            if email == "":
                request.session['email'] = request.user.email
            else:
                request.session['email'] = email
            
            if mobile == "":
                request.session['mobile'] = request.user.mobile  
            else:
                request.session['mobile'] = mobile

            send_generated_otp(request)
            messages.success(request,"Let's verify that you truly own the phone number provided.")
            return redirect(reverse('authentication:otp'))

        if fname == "":
            fname = user_fname 
        else:
            user.first_name = fname 
            user.save()
        if lname == "":
            lname = user_lname
        else:
            user.last_name = lname
            user.save()
        if email == "":
            email = user_email
        else:
            user.email = email
            user.save()
            
        messages.success(request, "You have successfully updated your account details!")
        return redirect('authentication:account_info')
    
    
    try:
        user = UserAddress.objects.get(user=request.user)
        if request.method == "POST":
            state = request.POST.get("state")
            division = request.POST.get("division")
            lga = request.POST.get("lga")
            lcda = request.POST.get("lcda")
            street_name = request.POST.get("street_name")
            
            user.state = state
            user.division = division
            user.lga = lga
            user.lcda = lcda
            user.street_name = street_name
            user.save()
            messages.success(request, "You have successfully updated address.")
            return redirect('authentication:account_info')
    except:
        pass
        
    return render(request,'authentication/edit_account.html',{'state_lga':state_and_lga.items()})



def change_address(request):#division
    if request.method == "POST":
        data = json.loads(request.body)
        address_value = data.get('division_id')
        divisions = state_and_lga.get(address_value, {})
        response_data = list(divisions.keys())
        return JsonResponse(response_data, safe=False)
    return JsonResponse({'error': 'Invalid request'}, status=400)


def change_address_division(request):#lga
    if request.method == "POST":
        data = json.loads(request.body)
        division_value = data.get('lga_id')
        selected_state = data.get('state')
        divisions_selsect = state_and_lga.get(selected_state, {})
        lga = divisions_selsect.get(division_value).keys()
        return JsonResponse(list(lga), safe=False)
    return JsonResponse({'error': 'Invalid request'}, status=400)


def change_address_lga(request):#lcda
    if request.method == "POST":
        data = json.loads(request.body)
        lcda = data.get('lcda_id')
        selected_state = data.get('state')
        selected_division = data.get('division')
        lga = data.get('lga')
        state = state_and_lga.get(selected_state, {})
        lcda_list = state.get(selected_division).get(lga)

        return JsonResponse(lcda_list, safe=False)
    return JsonResponse({'error': 'Invalid request'}, status=400)



#This is a view to reset password by e-mail or username when user forgets password 
def password_reset(request, uid=None, token=None):
    try:
        if request.method == "POST":
            password = request.POST.get("password").strip()
            password2 = request.POST.get("password2").strip()

            password = password.lower()
            password2 = password2.lower()

            request.session['password'] = password
            request.session['password2'] = password2
            
            if password != password2:
                messages.error(request,"Passwords do not match!")
                return redirect(reverse('authentication:reset',args=[uid,token]))
            
            try:
                UserAttributeSimilarityValidator().validate(password)
            except:
                messages.error(request,"Password too similar to user attribute provided.\nPlease, try another password!")
                return redirect(reverse('authentication:reset',args=[uid,token]))
            try:
                CommonPasswordValidator().validate(password)
            except:
                messages.error(request,"Password too common and easy.\nPlease, try another password!")
                return redirect(reverse('authentication:reset',args=[uid,token]))
            try:
                MinimumLengthValidator().validate(password)
            except:
                messages.error(request,"Only a minimum characters of 8 is allowed.\nPlease, try another password!")
                return redirect(reverse('authentication:reset',args=[uid,token]))
            try:
                NumericPasswordValidator().validate(password)
            except:
                messages.error(request,"Numeric only password is not allowed.\nPlease, try another password!")
                return redirect(reverse('authentication:reset',args=[uid,token]))
            if not request.user.is_authenticated:
                user = User.objects.get(pk=uid)
            else:
                user = User.objects.get(email=request.user.email)
            current_password = user.password
    
            if check_password(password,current_password):
                messages.error(request, "Old password cannot be used!\nPlease, try a new password.")
                return redirect(reverse('authentication:reset',args=[uid,token]))
            else:
                user.set_password(password)
                user.save()
                del request.session['password']
                del request.session['password2']
                messages.success(request, "You have successfully changed password!")
                return redirect('authentication:signin')
    except AttributeError:
        return redirect('authentication/connection_error.html')
        
    return render(request,'authentication/reset.html',{'password':request.session.get('password', ""),
                                                       'password2':request.session.get('password2', ""),
                                                       })
