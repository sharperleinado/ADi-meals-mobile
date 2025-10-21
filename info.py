import os
from dotenv import load_dotenv
load_dotenv()


#zoho credentials
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.zoho.com'
EMAIL_HOST_USER = os.getenv('ZOHO_EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('ZOHO_EMAIL_HOST_USER')
EMAIL_PORT = 587


#gmail credentials
#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#EMAIL_USE_TLS = True
#EMAIL_HOST = 'smtp.gmail.com'
#EMAIL_HOST_USER = 
#EMAIL_HOST_PASSWORD = 
#EMAIL_PORT = 587


#mail trap credentials
#EMAIL_HOST = 'sandbox.smtp.mailtrap.io'
#EMAIL_HOST_USER = os.getenv('MAILTRAP_EMAIL_HOST_USER')
#EMAIL_HOST_PASSWORD = os.getenv('MAILTRAP_EMAIL_HOST_PASSWORD')
#EMAIL_PORT = '2525'