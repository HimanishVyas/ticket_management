import os

import dotenv
import requests

# from django.conf import settings


def sendwhatsappMessage(phoneNumber, message):
    haders = {"Authorization": os.getenv("WHATSAPP_TOKEN")}

    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": phoneNumber,
        "type": "text",
        "text": {"body": message},
    }
    response = requests.post(os.getenv("WHATSAPP_URL"), headers=haders, json=payload)
    ans = response.json()
    return ans


# phoneNumber = 919724946042
# message = "otp"
# sendwhatsappMessage(phoneNumber, message)
