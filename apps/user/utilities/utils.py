import os
import random

from django.core.mail import EmailMessage
from dotenv import load_dotenv
from twilio.rest import Client

from apps.user.customs.authentications import (
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
)

# from apps.user.models import User

load_dotenv()


def get_tokens_for_user(user):
    # refresh = RefreshToken.for_user(user)
    # access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)
    id = decode_refresh_token(refresh_token)
    refresh_access_token = create_access_token(id)

    return {
        "refresh": refresh_token,
        "access": refresh_access_token,
    }


class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data["subject"],
            body=data["body"],
            from_email=os.getenv("EMAIL_HOST_USER"),
            to=[data["to_email"]],
        )
        print(email)
        email.send()


def send_otp_via_phone(mobile):
    print("mobile ----- >>>>", mobile)
    account_sid = os.getenv("account_sid")
    auth_token = os.getenv("auth_token")
    client = Client(account_sid, auth_token)
    phone_number = mobile
    my_otp = random.randint(1111, 9999)
    client.messages.create(
        body=f"Hi,Welcome to NVC CRM ,{my_otp} is your one time password to proceed on NuVu. Do not share your OTP with anyone.",
        from_=os.getenv("twilio_no"),
        to=f"{phone_number}",
    )
    return my_otp


def genrate_otp():
    my_otp = random.randint(1111, 9999)
    return my_otp
