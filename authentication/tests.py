from django.test import TestCase
from dotenv import load_dotenv
import pyotp
from datetime import datetime,timedelta
from sms import send_sms
from twilio.rest import Client
from twilio.base.exceptions import TwilioException
import os
load_dotenv()


# Create your tests here.


account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
client = Client(account_sid, auth_token)


def update_mobile_send_otp(request):
    message = ""
    totp = pyotp.TOTP(pyotp.random_base32(), interval=60)
    otp = totp.now()
    request.session['otp_secret_key'] = totp.secret
    valid_date = datetime.now() + timedelta(minutes=1)
    request.session['otp_valid_date'] = str(valid_date)
    
    try:
        recipient = request.session['update_mobile']
        message = client.messages.create(
        from_='ADi meals',
        body=f"Thank you for choosing ADi meals. Your one time password is {otp}",
        to=[recipient]
        )
        print(message.sid)
        return message
    except TwilioException as e:
        print(f"TwilioRestException: {e}")
        print(f"Error Code: {e.code}")
        print(f"Error Message: {e.msg}")
    except KeyError:
        pass



def create_mobile_send_otp(request):
    message = ""
    totp = pyotp.TOTP(pyotp.random_base32(), interval=60)
    otp = totp.now()
    request.session['otp_secret_key'] = totp.secret
    valid_date = datetime.now() + timedelta(minutes=1)
    request.session['otp_valid_date'] = str(valid_date)
    
    try:
        recipient = request.session['create_phone_number']
        message = client.messages.create(
        from_='ADi meals',
        body=f"Thank you for choosing ADi meals. Your one time password is {otp}",
        to=[recipient]
        )
        print(message.sid)
        return message
    except TwilioException as e:
        print(f"TwilioRestException: {e}")
        print(f"Error Code: {e.code}")
        print(f"Error Message: {e.msg}")
    except KeyError:
        pass

'''
def update_mobile_send_otp(request):
    message = ""
    totp = pyotp.TOTP(pyotp.random_base32(), interval=60)
    otp = totp.now()
    request.session['otp_secret_key'] = totp.secret
    valid_date = datetime.now() + timedelta(minutes=1)
    request.session['otp_valid_date'] = str(valid_date)
    
    try:
        recipient = request.session['update_mobile']
        return send_sms(
        f"Thank you for choosing ADi meals. Your one time password is {otp}",
        "ADi meals",
        [recipient],
        )
    except KeyError:
        pass



def create_mobile_send_otp(request):
    message = ""
    totp = pyotp.TOTP(pyotp.random_base32(), interval=60)
    otp = totp.now()
    request.session['otp_secret_key'] = totp.secret
    valid_date = datetime.now() + timedelta(minutes=1)
    request.session['otp_valid_date'] = str(valid_date)
    
    try:
        recipient = request.session['create_phone_number']
        return send_sms(
        f"Thank you for choosing ADi meals. Your one time password is {otp}",
        "ADi meals",
        [recipient],
        )
    except KeyError:
        pass'''

