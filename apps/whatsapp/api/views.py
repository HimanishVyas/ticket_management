# from django.shortcuts import render
import json
import os

import dotenv

# import requests
# import requests
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# from rest_framework.response import Response
# from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet

from apps.whatsapp.customs.function import sendwhatsappMessage

# from apps.whatsapp.customs.whatsapp_bot_flow import MessageGenerator
from apps.whatsapp.customs.whatsapp_bot_flow_v2 import MessageGenerator as MG

# from rest_framework.decorators import authentication_classes
# import os
# from multiprocessing import process


dotenv.load_dotenv()


# Create your views here.
class WhatsappBotApi(ViewSet):
    authentication_classes = []

    def list(self, request):
        mobile = request.GET.get("mobile")
        msg = request.GET.get("msg")
        reply = MG(mobile=mobile, msg=msg)
        return HttpResponse(reply)


@csrf_exempt
def webhook(request):
    if request.method == "GET":
        mode = request.GET["hub.mode"]
        token = request.GET["hub.verify_token"]

        challenge = request.GET["hub.challenge"]
        if mode == "subscribe" and token == os.getenv("VERIFY_TOKEN"):
            return HttpResponse(challenge, status=200)
        else:
            return HttpResponse("error", status=403)

    if request.method == "POST":
        data = json.loads(request.body)
        if "object" in data and "entry" in data:
            if data["object"] == "whatsapp_business_account":
                try:
                    for entry in data["entry"]:
                        # phoneNumber = entry["changes"][0]["value"]["metadata"][
                        #     "display_phone_number"
                        # ]
                        # phoneId = entry["changes"][0]["value"]["metadata"][
                        #     "phone_number_id"
                        # ]
                        # profileName = entry["changes"][0]["value"]["contacts"][0][
                        #     "profile"
                        # ]["name"]
                        # whatsAppId = entry["changes"][0]["value"]["contacts"][0]["wa_id"]
                        # fromId = entry["changes"][0]["value"]["messages"][0]["from"]
                        # messageId = entry["changes"][0]["value"]["messages"][0]["id"]
                        # timestamp = entry["changes"][0]["value"]["messages"][0][
                        #     "timestamp"
                        # ]
                        # text = entry["changes"][0]["value"]["messages"][0]["text"][
                        #     "body"
                        # ]

                        mobile = entry["changes"][0]["value"]["messages"][0]["from"]
                        msg = entry["changes"][0]["value"]["messages"][0]["text"]["body"]
                        message_time = entry["changes"][0]["value"]["messages"][0][
                            "timestamp"
                        ]

                        reply = MG(mobile=mobile, msg=msg)

                        sendwhatsappMessage(mobile, reply)
                except Exception:
                    pass

        return HttpResponse("success", status=200)
        # print("---------------------->>",reply)
        # # phoneNumber = [
        # #     "919724946042"
        # # ]  # enter the number you wanta to recive masseage
        # # message = 'Im a whats app support centre of nuvu conair How can i help you?'
        # print("----->>>", text)
        # if text.lower() in ["hi", "hello", "ram ram", "radhe radhe"]:
        #     message = (
        #         "hi "
        #         + profileName
        #         + " Select anyone option on below this..\n 1.Installatio\n 2.Service\n 3.Spare\n 4.Sales Inquir\n 5.Others \n\n ENTER ONLY NUMBERS"
        #     )

        # if text == "1":
        #     message = "1.Please Enter Work Order No."

        # if text in ["123", "456", "789", "100", "111", "200"]:
        #     message = "2.Packing slip No."

        # if text in ["a123", "a456", "ab12"]:
        #     message = "thanks for providing info"
