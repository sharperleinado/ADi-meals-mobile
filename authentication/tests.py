from django.test import TestCase
from dotenv import load_dotenv
import pyotp
from datetime import datetime,timedelta
from twilio.rest import Client
import os
from django.shortcuts import redirect
from sms import send_sms
from django.contrib import messages
from twilio.base.exceptions import TwilioException
load_dotenv()


# Create your tests here.


account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
client = Client(account_sid, auth_token)


def generate_otp(request):
    totp = pyotp.TOTP(pyotp.random_base32(), interval=600)
    otp = totp.now()
    request.session['otp_secret_key'] = totp.secret
    valid_date = datetime.now() + timedelta(minutes=10)
    request.session['otp_valid_date'] = str(valid_date)
    return otp




#This function is to add otp to user creation mail or forget password mail.
def generate_activateorreset_otp(request):
    totp = pyotp.TOTP(pyotp.random_base32(), interval=86400)
    otp = totp.now()
    request.session['otp_secret_key_resetoractivate'] = totp.secret
    valid_date = datetime.now() + timedelta(hours=24)
    request.session['otp_valid_date_resetoractivate'] = str(valid_date)
    return otp



def send_generated_otp(request):
    message = ""
    try:
        recepient = f"+234{request.session['mobile']}"
        #message = client.messages.create(
        #    from_='ADi meals',
        #    body=f"Thank you for choosing ADi meals. Your one time password is {generate_otp(request)}.",
        #    to=[recepient]
        #)

        message = client.messages.create(
            from_='whatsapp:+15558211520',
            content_sid='HX6a5a70792e270b59d50d8962cd03679f',
            content_variables=f'{{"1":"{generate_otp(request)}"}}',
            messaging_service_sid='MGe116e40a44d5f9e02e59777c14762cff',
            to=f"whatsapp:{recepient}"
        )

        print(f"Message SID: {message.sid}")
        print(f"Status: {message.status}")
        print(f"To: {message.to}")
        return message
    except TwilioException as e:
        print(f"TwilioRestException: {e}")
        print(f"Error Code: {e.code}")
        print(f"Error Message: {e.msg}")
    except KeyError:
        pass
    except ConnectionError:
        messages.info(request, "Error while sending OTP, Ensure that you have a working internet")
        return redirect('authentication:edit_account')


'''
def send_generated_otp(request):
    try:
        recipient = request.session['mobile']
        return send_sms(
            f"Thank you for choosing ADi meals. Your one time password is {generate_otp(request)}",
            "ADi meals",
            [recipient],
            )
    except KeyError:
        pass'''


'''
valid_date = datetime.now() + timedelta(minutes=1)
while True:
    time_diff = valid_date - datetime.now()
    if datetime.now() >= valid_date:
        print("Count down reached zero!")
        break
    hours, remainder = divmod(int(time_diff.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    print(f"{hours:02}:{minutes:02}:{seconds:02}", end="\r")
    time.sleep(1)'''

