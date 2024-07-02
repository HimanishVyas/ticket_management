import datetime
import logging
import os
from dateutil.parser import parse

from dotenv import load_dotenv

from apps.ticket.api.serializer import (
    CustomerWiseItemWithoutDepthSerializer,
    ItemSerializer,
)
from django.contrib.auth.hashers import make_password, check_password

load_dotenv()

import pandas as pd

# import xlwt
# from django.apps import apps
from django.contrib.auth import authenticate
from django.contrib.sessions.backends.db import SessionStore

# from django.db import models as Models
# from django.db.models import DateField, ForeignKey, Q
# from django.http import HttpResponse
from drf_yasg.utils import swagger_auto_schema
from phonenumber_field.phonenumber import PhoneNumber as pn
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet

from apps.ticket.models import CustomerWiseItem, Item

# from apps.ticket.api.serializer import CompanyProductItemDepthSerializer
from apps.user.api.serializer import (  # VeifyOtpForLoginSerializer,; VerifyLinkForForgotSerializer,; AppVersionSerializer,; CompanySerializer,; CountrySeralizer,; DistrictSeralizer,; EmailVerifiedSerializer,; ForgotPasswordSerializer,; MobileNumberSerializer,; PhoneNumebrSerializer,; StateSeralizer,; UserDepthSerializer,; UserListSerializer,; UserRegisterSerializer,; UserSerializer,; VerifyOTPSerializer,; VerifyPasswordSerializer,; CustomerUserWithOutEmailSerializer
    AddressDepthSerializer,
    AddressSerializer,
    AddressWithoutDepthSerializer,
    AppVersionSerializer,
    ChangePasswordSerializer,
    CountrySeralizer,
    CustomerUserDepthSerializer,
    CustomerUserSerializer,
    DistrictSeralizer,
    EmailSerializer,
    ExcelUploadCustomerUserSerializer,
    LoginSerializer,
    PhoneNumebrSerializer,
    ResetPasswordSerializer,
    StateSeralizer,
    UserListSerializer,
    VerifyOTPSerializer,
)
from apps.user.customs.permissions import ExceptDelete, ReadOnly
from apps.user.customs.viewsets import CustomViewSet, CustomViewSetFilter
from apps.user.models import (  # AppVersion,; Company,; Country,; District,; States,; User,
    Address,
    AppVersion,
    Country,
    CustomerUser,
    District,
    Email,
    PhoneNumber,
    States,
)
from apps.user.utilities.utils import (
    Util,
    genrate_otp,
    get_tokens_for_user,
    send_otp_via_phone,
)


# # Create your views here.


class LoginApi(ViewSet):
    authentication_classes = []

    @swagger_auto_schema(
        request_body=LoginSerializer,
        operation_description="User SignUp",
    )
    def create(self, request):
        password = request.data.get("password")
        if request.data.get("phone_number"):
            phone_number = request.data.get("phone_number")
            # otp = send_otp_via_phone(phone_number) # off till tiwilio
            session_data = SessionStore()  # off till tiwilio
            session_data.set_expiry(500)
            session_data["phone"] = phone_number
            # session_data["otp"] = otp
            session_data["otp"] = os.getenv("OTP")
            session_data.create()
            # phone = PhoneNumber.objects.filter(phone=phone_number).first()
            # if not phone:
            #     return Response(
            #         {"message": "phone_number not found"},
            #         status=status.HTTP_400_BAD_REQUEST,
            #     )
            # user = phone.customer_user
            # if phone.customer_user.check_password(password):
            #     if request.data.get("fcm_token"):
            #         user.fcm_token = request.data.get("fcm_token")
            #         user.save()
            #     user_serializer = CustomerUserDepthSerializer(user, context={"request": request})
            #     token = get_tokens_for_user(user)
            #     response = user_serializer.data
            #     response["token"] = token
            #     return Response(response, status=status.HTTP_200_OK)
            # else:
            return Response(
                {
                    "message": "OTP sent Successfully",
                    "session_key": session_data.session_key,
                },
                status=status.HTTP_200_OK,
            )
        if request.data.get("E_Mail"):
            E_Mail = request.data.get("E_Mail")
            customer_user = CustomerUser.objects.filter(E_Mail=E_Mail).first()
            print(customer_user)
            if customer_user:
                if customer_user.check_password(password):
                    if request.data.get("fcm_token"):
                        customer_user.fcm_token = request.data.get("fcm_token")
                        customer_user.save()
                    user_serializer = CustomerUserDepthSerializer(
                        customer_user, context={"request": request}
                    )
                    token = get_tokens_for_user(customer_user)
                    phone_number = PhoneNumber.objects.filter(
                        customer_user=customer_user
                    ).values()
                    response = user_serializer.data
                    response["phone_number"] = phone_number
                    response["token"] = token
                    return Response(response, status=status.HTTP_200_OK)
                else:
                    return Response(
                        {"message": "Password not Match"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            email = Email.objects.filter(E_Mail=E_Mail).first()
            if not email:
                return Response(
                    {"message": "E_Mail not found"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            user = email.customer_user
            if user.check_password(password):
                if request.data.get("fcm_token"):
                    user.fcm_token = request.data.get("fcm_token")
                    user.save()
                user_serializer = CustomerUserDepthSerializer(
                    user, context={"request": request}
                )
                token = get_tokens_for_user(user)
                phone_number = PhoneNumber.objects.filter(customer_user=user).values()
                response = user_serializer.data
                response["phone_number"] = phone_number
                response["token"] = token
                return Response(response, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"message": "E_Mail not found"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # if not user.mobile_verify:
            #     return Response(
            #         {"message": "mobile number is not verified"},
            #         status=status.HTTP_200_OK,
            #    )
        return Response(
            {"message": "E_Mail not found"}, status=status.HTTP_400_BAD_REQUEST
        )


# class SignUpApi(ViewSet):
#     authentication_classes = []

#     @swagger_auto_schema(
#         request_body=UserSerializer,
#         operation_description="User SignUp",
#     )
#     def create(self, request):
#         serializer = UserRegisterSerializer(
#             data=request.data, context={"host": request.META["HTTP_HOST"]}
#         )
#         if serializer.is_valid():
#             user = serializer.save()
#             response = {
#                 "message": "user created , Please check your email and mobile for verification",
#                 "user_id": user.id,
#                 "user_name": user.name,
#                 # "user_phone": str(user.phone),
#                 "user_email": user.email,
#                 "status": status.HTTP_201_CREATED,
#             }
#             return Response(response, status=status.HTTP_201_CREATED)
#         else:
#             return Response(
#                 {"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
#             )


class ChangePasswordApi(ViewSet):
    @swagger_auto_schema(
        request_body=ChangePasswordSerializer,
        operation_description="User SignUp",
    )
    def create(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data, context={"user": request.user}
        )
        serializer.is_valid(raise_exception=True)
        return Response(
            {"message": "password changed succesfully"}, status=status.HTTP_200_OK
        )


class ResetPasswordApi(ViewSet):
    @swagger_auto_schema(
        request_body=ResetPasswordSerializer,
        operation_description="User SignUp",
    )
    def create(self, request):
        serializer = ResetPasswordSerializer(
            data=request.data, context={"user": request.user}
        )
        serializer.is_valid(raise_exception=True)
        return Response(
            {"message": "password changed succesfully"}, status=status.HTTP_200_OK
        )


# class EmailVerifedApi(APIView):
#     authentication_classes = []

#     def get(self, request, id, token):
#         serializer = EmailVerifiedSerializer(
#             data=request.data,
#             context={"id": id, "token": token, "host": request.META["HTTP_HOST"]},
#         )
#         if serializer.is_valid(raise_exception=True):
#             return Response(
#                 {"message": "Account Verified Successfully"}, status=status.HTTP_200_OK
#             )
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerfiyMobileOtp(APIView):
    @swagger_auto_schema(
        request_body=VerifyOTPSerializer, operation_description="Verfiy Mobile Otp"
    )
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # otp = serializer.validated_data["otp"]
        # user = User.objects.filter(id=pk, mobile_otp=otp).first()
        otp = serializer.data.get("otp")
        session_key = serializer.data.get("session_key")
        try:
            s = SessionStore(session_key=session_key)
            session_otp = s["OTP"]
            session_mobile = s["mobile"]
            created = s.get("create", False)
            customer_user = s.get("customer_user")
            new_mobile = s.get("new_mobile")
            craeted_by_customer = s.get("created_by_customer", False)
        except Exception:
            return Response(
                {
                    "message": "your session is expired",
                    "status": status.HTTP_400_BAD_REQUEST,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        print(session_otp)
        if str(otp) != str(session_otp):
            return Response(
                {"message": "otp is not match", "status": status.HTTP_400_BAD_REQUEST},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if created:
            PhoneNumber.objects.create(
                phone=session_mobile,
                is_verified=True,
                customer_user=CustomerUser.objects.filter(id=customer_user).first(),
            )
            return Response(
                {"message": "PhoneNumber Added Successfully"}, status=status.HTTP_200_OK
            )
        else:
            if not craeted_by_customer:
                customer_user = CustomerUser.objects.filter(
                    mobile_number=session_mobile
                ).first()
                if customer_user:
                    customer_user.mobile_number = new_mobile
                    customer_user.save()
                    return Response(
                        {"message": "otp verified successfully"},
                        status=status.HTTP_200_OK,
                    )
            else:
                phone = PhoneNumber.objects.filter(phone=session_mobile).first()
                if phone:
                    if new_mobile:
                        phone.phone = new_mobile
                    phone.is_verified = True
                    phone.save()
                    return Response(
                        {"message": "otp verified successfully"},
                        status=status.HTTP_200_OK,
                    )
        return Response({"message": "otp not match"}, status=status.HTTP_400_BAD_REQUEST)


# class VerfiyMobileOtpUser(APIView):
#     authentication_classes = []

#     @swagger_auto_schema(
#         request_body=VerifyOTPSerializer, operation_description="Verfiy Mobile Otp User"
#     )
#     def post(self, request):
#         serializer = VerifyOTPSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         # otp = serializer.validated_data["otp"]
#         # user = User.objects.filter(id=pk, mobile_otp=otp).first()
#         otp = serializer.data.get("otp")
#         session_key = serializer.data.get("session_key")
#         try:
#             s = SessionStore(session_key=session_key)
#             session_otp = s["OTP"]
#             session_mobile = s["mobile"]
#             old_mobile = s["old_mobile"]
#         except Exception:
#             return Response(
#                 {"message": "your session is expired"},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )
#         print(str(otp) != str(session_otp))
#         if str(otp) != str(session_otp):
#             return Response(
#                 {"message": "otp is not match"}, status=status.HTTP_400_BAD_REQUEST
#             )
#         phone = User.objects.filter(mobile=old_mobile).first()
#         if phone:
#             phone.mobile = session_mobile
#             phone.mobile_verify = True
#             phone.save()
#             return Response(
#                 {"message": "otp verified successfully"}, status=status.HTTP_200_OK
#             )
#         return Response({"message": "otp not match"}, status=status.HTTP_400_BAD_REQUEST)


class EmailResetVerifiedApi(APIView):
    authentication_classes = []

    @swagger_auto_schema(
        request_body=VerifyOTPSerializer, operation_description="Verfiy Mobile Otp User"
    )
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # otp = serializer.validated_data["otp"]
        # user = User.objects.filter(id=pk, mobile_otp=otp).first()
        otp = serializer.data.get("otp")
        session_key = serializer.data.get("session_key")
        try:
            s = SessionStore(session_key=session_key)
            session_otp = s["OTP"]
            session_new_email = s["new_email"]
            session_email = s["email"]
        except Exception:
            return Response(
                {"message": "your session is expired"}, status=status.HTTP_200_OK
            )
        if str(otp) != str(session_otp):
            return Response({"message": "otp is not match"}, status=status.HTTP_200_OK)
        user = CustomerUser.objects.filter(E_Mail=session_email).first()
        print("user----", user, session_email)
        if user:
            user.E_Mail = session_new_email
            user.email_verify = True
            user.save()
            return Response(
                {"message": "otp verified successfully"}, status=status.HTTP_200_OK
            )
        else:
            email = Email.objects.filter(E_Mail=session_email)
            if email.exists():
                email.update(E_Mail=session_new_email)
                return Response(
                    {"message": "otp verified successfully"}, status=status.HTTP_200_OK
                )

        return Response(
            {"message": "E_Mail Not Found"}, status=status.HTTP_400_BAD_REQUEST
        )


# # class ForgotPasswordApi(APIView):
# #     authentication_classes = []

# #     @swagger_auto_schema(
# #         request_body=ForgotPasswordSerializer, operation_description="Forgot Password"
# #     )
# #     def post(self, request):
# #         session_data = SessionStore()
# #         session_data["email"] = request.data.get("email")
# #         session_data["OTP"] = 0000
# #         print(session_data["email"])
# #         session_data.create()
# #         serializer = ForgotPasswordSerializer(
# #             data=request.data,
# #             context={
# #                 "host": request.META["HTTP_HOST"],
# #                 "session_key": session_data.session_key,
# #             },
# #         )
# #         serializer.is_valid(raise_exception=True)
# #         session_data.set_expiry(500)

# #         return Response(
# #             {
# #                 "data": session_data.session_key,
# #                 "message": "Forgot Password linked sent to your mail",
# #             },
# #             status=status.HTTP_200_OK,
# #         )


# # class VerifyPasswordApi(APIView):
# #     """Verify password api for User"""

# #     authentication_classes = []

# #     @swagger_auto_schema(
# #         request_body=VerifyPasswordSerializer,
# #         operation_description="description from swagger_auto_schema via method_decorator",
# #     )
# #     def post(self, request, id, token):
# #         serializer = VerifyPasswordSerializer(
# #             data=request.data, context={"id": id, "token": token}
# #         )
# #         if serializer.is_valid(raise_exception=True):
# #             response = {
# #                 "message": "Password changed successfully",
# #                 "status": status.HTTP_200_OK,
# #             }
# #             return Response(response, status=status.HTTP_200_OK)
# #         response = serializer.errors
# #         response["status"] = status.HTTP_400_BAD_REQUEST
# #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class ForgotPasswordApi(APIView):
#     authentication_classes = []

#     @swagger_auto_schema(
#         request_body=ForgotPasswordSerializer,
#         operation_description="description from swagger_auto_schema via method_decorator",
#     )
#     def post(self, request):
#         data = request.data
#         serializer = ForgotPasswordSerializer(
#             data=data, context={"host": request.META["HTTP_HOST"]}
#         )
#         if serializer.is_valid():
#             response = {
#                 "message": "Your reset password link has been sent to your registered email id",
#                 "status": status.HTTP_200_OK,
#             }
#             return Response(
#                 response,
#                 status=status.HTTP_200_OK,
#             )
#         response = {
#             "message": "Invalid Email",
#             "status": status.HTTP_400_BAD_REQUEST,
#         }
#         return Response(response, status=status.HTTP_400_BAD_REQUEST)

#     # """Verify password api for User"""

#     # authentication_classes = []

#     # # @swagger_auto_schema(
#     # #     request_body=VerifyLinkForForgotSerializer,
#     # #     operation_description="description from swagger_auto_schema via method_decorator",
#     # # )
#     # def get(self, request, id, token):
#     #     serializer = VerifyLinkForForgotSerializer(
#     #         data=request.data, context={"id": id, "token": token}
#     #     )
#     #     session_key = request.GET.get("session_key")
#     #     print("session_key=", session_key)
#     #     session_stored_data = SessionStore(session_key=session_key)
#     #     try:
#     #         session_stored_data["email"]
#     #         session_stored_data["status"] = True
#     #         session_stored_data.save()
#     #         session_stored_data.modified

#     #     except Exception:
#     #         return Response(
#     #             {"message": "Your Link has been expired,Please generate once again"},
#     #             status=status.HTTP_403_FORBIDDEN,
#     #         )

#     #     if serializer.is_valid(raise_exception=True):
#     #         response = {
#     #             "message": "Email verified Successfully",
#     #             "status": status.HTTP_200_OK,
#     #         }
#     #         return Response(response, status=status.HTTP_200_OK)
#     #     response = serializer.errors
#     #     response["status"] = status.HTTP_400_BAD_REQUEST
#     #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class VerifyPasswordApi(APIView):
#     authentication_classes = []

#     @swagger_auto_schema(
#         request_body=VerifyPasswordSerializer,
#         operation_description="description from swagger_auto_schema via method_decorator",
#     )
#     def post(self, request):
#         serializer = VerifyPasswordSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             response = {
#                 "message": "Password changed successfully",
#                 "status": status.HTTP_200_OK,
#             }
#             return Response(response, status=status.HTTP_200_OK)
#         response = serializer.errors
#         response["status"] = status.HTTP_400_BAD_REQUEST
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     # authentication_classes = []

#     # @swagger_auto_schema(
#     #     request_body=VerifyPasswordSerializer, operation_description="Verify Password"
#     # )
#     # def post(self, request):
#     #     serializer = VerifyPasswordSerializer(data=request.data)
#     #     if serializer.is_valid(raise_exception=True):
#     #         response = {
#     #             "message": "Password changed Successfully",
#     #             "status": status.HTTP_200_OK,
#     #         }
#     #         return Response(response, status=status.HTTP_200_OK)
#     #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AppVersionApi(ViewSet):
    authentication_classes = []

    def list(self, request):
        queryset = AppVersion.objects.all()
        serializer = AppVersionSerializer(queryset, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    def retrieve(self, request, pk):
        try:
            version_obj = AppVersion.objects.get(pk=pk)
        except Exception:
            return Response(
                {"data": "version does not exists"}, status=status.HTTP_400_BAD_REQUEST
            )
        serializer = AppVersionSerializer(version_obj)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)


# class SendMobileOTP(ViewSet):
#     authentication_classes = []

#     @swagger_auto_schema(
#         request_body=MobileNumberSerializer,
#         operation_description="Send OTP for Login",
#     )
#     def create(self, request):
#         serializer = MobileNumberSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         mobile = serializer.validated_data.get("mobile")
#         print(mobile)

#         user = User.objects.filter(mobile=mobile).first()
#         print("--------------------------------------->>>>>", user)
#         if user:
#             generated_otp = send_otp_via_phone(user.mobile)
#             print(generated_otp)
#             session_data = SessionStore()
#             session_data.set_expiry(500)
#             session_data["otp"] = generated_otp
#             session_data["mobile"] = str(user.mobile)
#             session_data.create()
#             return Response(
#                 {"message": "successfull", "session_key": session_data.session_key}
#             )
#         return Response(
#             {"message": "user is not registerd"}, status=status.HTTP_400_BAD_REQUEST
#         )


class VeifyOtpForLoginApi(ViewSet):
    authentication_classes = []

    @swagger_auto_schema(
        request_body=VerifyOTPSerializer,
        operation_description="Verify Otp For Login Serializer",
    )
    def create(self, request, *args, **kwargs):
        received_otp = request.data.get("otp")
        session_id = request.data.get("session_id")
        session_stored_data = SessionStore(session_key=session_id)
        try:
            data = session_stored_data["otp"]
            phone = session_stored_data["phone"]
        except Exception:
            return Response(
                {"message": "Your OTP has been expired,Please generate otp once again"},
                status=status.HTTP_403_FORBIDDEN,
            )
        if int(received_otp) == int(data):
            try:
                user = CustomerUser.objects.filter(mobile_number=phone).first()
                if user:
                    pass
                else:
                    user = PhoneNumber.objects.filter(phone=phone).first()
                    if not user:
                        return Response(
                            {"message": "User not Found"},
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                    user = user.customer_user
            except Exception:
                return Response(
                    {"message": "User not found"}, status=status.HTTP_400_BAD_REQUEST
                )

            user_serializer = CustomerUserDepthSerializer(user)
            token = get_tokens_for_user(user)
            phone_number = PhoneNumber.objects.filter(customer_user=user).values()
            response = user_serializer.data
            response["phone_number"] = phone_number
            response["token"] = token
            return Response(response, status=status.HTTP_200_OK)
        return Response(
            {"message": "Please Enter a valid otp"}, status=status.HTTP_400_BAD_REQUEST
        )


class ProfileApi(CustomViewSet):
    serializer_class = CustomerUserSerializer

    # @swagger_auto_schema(
    #     request_body=UserSerializer, operation_description=" USer Profile"
    # )
    def get_queryset(self):
        return CustomerUser.objects.filter(id=self.request.user.id)

    def list(self, request, *args, **kwargs):
        results = self.get_serializer(request.user).data
        print("------------>>>", results)
        print(results["user_role"])
        if results["user_role"] != 3:
            data = AddressSerializer(request.user.address_set.all(), many=True).data
            print("data: ", data)

            if len(data) > 0:
                results["Address"] = data
            data = PhoneNumebrSerializer(
                request.user.phonenumber_set.all(), many=True
            ).data
            if len(data) > 0:
                results["phone_number"] = data

            return Response(results, status=status.HTTP_200_OK)

        else:
            return Response(results, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        session_key = ""
        instance = self.get_object()
        if request.data.__contains__("E_Mail"):
            otp = genrate_otp()
            # request.data["email_verify"] = False
            email = request.data["E_Mail"]
            if CustomerUser.objects.filter(E_Mail=email).exists():
                return Response(
                    {"message": "This is E_Mail ID Aleady Exist"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            body = f"This is one time password {otp} for resetting email id from NuVu conair."
            subject = "Reset Email"
            data = {"subject": subject, "body": body, "to_email": email}
            session_data = SessionStore()
            session_data["OTP"] = otp
            session_data["new_email"] = request.data["E_Mail"]
            session_data["email"] = instance.E_Mail
            session_data.create()
            session_key = session_data.session_key
            Util.send_email(data)

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        if not request.data.__contains__("E_Mail"):
            print(
                'request.data.__contains__("E_Mail"): ',
                request.data.__contains__("E_Mail"),
            )
            self.perform_update(serializer)

            if getattr(instance, "_prefetched_objects_cache", None):
                print(
                    'getattr(instance, "_prefetched_objects_cache", None): ',
                    getattr(instance, "_prefetched_objects_cache", None),
                )
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}

            response = {
                "message": "Updated Succesfully",
                "session_key": session_key,
                "data": serializer.data,
                "status": status.HTTP_200_OK,
            }
            return Response(response, status=status.HTTP_200_OK)

        elif request.data.get("E_Mail"):

            response = {
                "message": "Otp Sent Successful",
                "session_key": session_key,
                "data": serializer.data,
                "status": status.HTTP_200_OK,
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = {
                "message": "Updated Succesfully",
                "data": serializer.data,
                "status": status.HTTP_200_OK,
            }
            return Response(response, status=status.HTTP_200_OK)


# class VerifyOTPforForgotApi(ViewSet):
#     authentication_classes = []

#     # @swagger_auto_schema(
#     #     request_body=VerifyOTPSerializer,
#     #     operation_description="Verify Otp For Forgot Serializer",
#     # )
#     def create(self, request, *args, **kwargs):
#         received_otp = request.data.get("otp")
#         session_id = request.data.get("session_id")
#         session_stored_data = SessionStore(session_key=session_id)
#         try:
#             data = session_stored_data["OTP"]
#             email = session_stored_data["email"]
#         except Exception:
#             return Response(
#                 {"message": "Your OTP has been expired,Please generate otp once again"},
#                 status=status.HTTP_403_FORBIDDEN,
#             )
#         if int(received_otp) == int(data):
#             try:
#                 user = User.objects.get(email=email)
#             except Exception:
#                 return Response(
#                     {"message": "User not found"}, status=status.HTTP_400_BAD_REQUEST
#                 )
#             user_serializer = UserSerializer(user)
#             token = get_tokens_for_user(user)
#             response = user_serializer.data
#             response["token"] = token
#             return Response(response, status=status.HTTP_200_OK)
#         return Response(
#             {"message": "Please Enter a valid otp"}, status=status.HTTP_400_BAD_REQUEST
#         )


class UserListApi(CustomViewSet):
    serializer_class = CustomerUserSerializer
    queryset = CustomerUser.objects.filter(user_role=3)
    permission_classes = [ReadOnly]

    # @swagger_auto_schema(
    #     request_body=UserListSerializer,
    #     operation_description=" User Profile lsit ")


class AddressApi(CustomViewSet):
    serializer_class = AddressDepthSerializer
    permission_classes = [ExceptDelete]

    def get_queryset(self):
        # return self.request.user.address_user.all()
        # serial_no = request.data.get("SerialNo")
        # user = CustomerWiseItem.objects.filter(SerialNo=serial_no).first().customer_user
        return self.request.user.address_set.all()

    def create(self, request, *args, **kwargs):
        self.serializer_class = AddressSerializer
        if request.user.user_role == 2:
            request.data["customer_user"] = request.user.id
        # if not Address.objects.filter(company=request.data["company"]).exists():
        #     request.data["selected"] = True

        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        self.serializer_class = AddressSerializer
        return super().update(request, *args, **kwargs)

    # def update(self, request, *args, **kwargs):
    #     data = request.data
    #     print('data: ', data)


class PhoneNumberApi(CustomViewSetFilter):
    serializer_class = PhoneNumebrSerializer
    permission_classes = [ExceptDelete]

    def get_queryset(self):
        return self.request.user.phonenumber_set.filter(is_verified=True)

    def create(self, request, *args, **kwargs):
        if request.user.user_role == 2:
            request.data["customer_user"] = request.user.id
            # request.data
        # request.data["company"] = request.user.company.id
        if PhoneNumber.objects.filter(phone=request.data.get("phone")).exists():
            return Response(
                {"message": "Phone number is already register"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not PhoneNumber.objects.filter(
                customer_user=request.data["customer_user"]
        ).exists():
            request.data["selected"] = True
        serializer = self.get_serializer(
            data=request.data, context={"user": request.user}
        )
        if serializer.is_valid():
            # serializer.save()
            headers = self.get_success_headers(serializer.data)
            data = serializer.data
            session_data = SessionStore()
            # session_data["OTP"] = send_otp_via_phone(serializer.data["phone"])
            session_data["OTP"] = os.getenv("OTP")
            session_data["mobile"] = serializer.data["phone"]
            session_data["customer_user"] = serializer.data["customer_user"]
            session_data["create"] = True
            session_data.create()
            data["session_key"] = session_data.session_key

            response = {
                "message": "Created Succesfully",
                "data": data,
                "status": status.HTTP_201_CREATED,
            }
            return Response(response, status=status.HTTP_201_CREATED, headers=headers)
        return Response(
            {"message": "Enter a valid phone number."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def update(self, request, *args, **kwargs):
        created_by_customer = False
        if not request.data.get("phone"):
            return Response(
                {"message": "phone field is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if request.user.user_role == 2:
            instance = self.get_object()
            request.data["customer_user"] = request.user.id
            created_by_customer = True

        if not created_by_customer:
            #     if CustomerUser.objects.filter(
            #         mobile_number=request.data.get("phone")
            #     ).exists():
            #         return Response(
            #             {"message": "Phone number is already register"},
            #             status=status.HTTP_400_BAD_REQUEST,
            #         )
            instance = CustomerUser.objects.filter(id=kwargs["pk"]).first()
            print(instance)
            request.data["mobile_number"] = request.data["phone"]
            serializer = CustomerUserSerializer(
                instance, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            data = serializer.data
            session_data = SessionStore()
            session_data["OTP"] = os.getenv("OTP")
            session_data["mobile"] = instance.mobile_number.as_e164
            session_data["new_mobile"] = request.data["phone"]
            session_data["created_by_customer"] = created_by_customer
            session_data.create()
            data["session_key"] = session_data.session_key

            response = {
                "message": "OTP sent Successfully",
                "data": data,
                "status": status.HTTP_200_OK,
            }
            return Response(response, status=status.HTTP_200_OK)

        else:
            if PhoneNumber.objects.filter(phone=request.data.get("phone")).exists():
                return Response(
                    {"message": "Phone number is already register"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            session_data = SessionStore()
            session_data["OTP"] = os.getenv("OTP")
            session_data["mobile"] = instance.phone.as_e164
            session_data["new_mobile"] = request.data["phone"]
            session_data["created_by_customer"] = created_by_customer
            session_data.create()
            data["session_key"] = session_data.session_key

            response = {
                "message": "Updated Succesfully",
                "data": data,
                "status": status.HTTP_200_OK,
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response(
            {"message": "Enter a valid phone number."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def list(self, request, *args, **kwargs):
        results = super().filter_queryset(queryset=self.get_queryset())
        results = self.get_serializer(results, many=True).data
        for res in results:
            phone = pn.from_string(res["phone"])
            res["country_code"] = phone.country_code
            res["phone"] = phone.national_number
        response = {"data": results}
        return Response(response, status=status.HTTP_200_OK)


class CountryApi(CustomViewSet):
    authentication_classes = []
    serializer_class = CountrySeralizer
    queryset = Country.objects.all()


class StateApi(CustomViewSet):
    authentication_classes = []
    serializer_class = StateSeralizer
    queryset = States.objects.all()


class DistrictApi(CustomViewSet):
    authentication_classes = []
    serializer_class = DistrictSeralizer
    queryset = District.objects.all()


# class UserMobileUpdateApi(CustomViewSet):
#     serializer_class = UserSerializer
#     queryset = User.objects.all()

#     def update(self, request, *args, **kwargs):
#         instance = self.get_object()
#         print("instance: ", instance)
#         data = request.data["mobile"]
#         print("data: ", data)
#         if User.objects.filter(mobile=request.data["mobile"]).exists():
#             return Response(
#                 {"message": "Phone number is already register"},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )
#         else:
#             request.data["mobile_verify"] = False
#             serializer = self.get_serializer(instance, data=request.data, partial=True)
#             print("serializer: ", serializer)
#             serializer.is_valid(raise_exception=True)
#             session_data = SessionStore()
#             session_data["OTP"] = send_otp_via_phone(request.data["mobile"])
#             session_data["mobile"] = request.data["mobile"]
#             session_data["old_mobile"] = instance.mobile.as_e164
#             session_data.create()
#             session_key = session_data.session_key

#         if getattr(instance, "_prefetched_objects_cache", None):
#             # If 'prefetch_related' has been applied to a queryset, we need to
#             # forcibly invalidate the prefetch cache on the instance.
#             instance._prefetched_objects_cache = {}

#         response = {
#             "message": "Updated Succesfully",
#             "session_key": session_key,
#             "data": serializer.data,
#             "status": status.HTTP_200_OK,
#         }
#         return Response(response, status=status.HTTP_200_OK)


# # class UserUploadAPI(ViewSet):

# #     def create(self, request):
# #         model_fields = User._meta.get_fields()
# #         field_names = [field.name for field in model_fields if field.concrete]

# #         print(field_names[1:])
# #         df = pd.read_excel(request.FILES["excel_file"])
# #         column_names = df.columns.tolist()
# #         print(df)
# #         if column_names == field_names[1:]:
# #             print(df.to_dict(orient="records"))
# #             serializer = UserSerializer(
# #                 data=df.to_dict(orient="records"), many=True
# #             )
# #             serializer.is_valid(raise_exception=True)
# #             serializer.save()
# #             response = {"message": "ALL DATA HAS BEEN UPLOADED IN DATA BASE"}
# #             return Response(response, status=status.HTTP_200_OK)
# #         else:
# #             # logging.error("field name not same as database")
# #             response = {"message": "field name is not same as database"}
# #             return Response(response, status=status.HTTP_400_BAD_REQUEST)


class CustomerApi(CustomViewSet):
    serializer_class = CustomerUserSerializer
    queryset = CustomerUser.objects.filter(user_role=2)


# # class PhoneNumberAdminApi(CustomViewSetFilter):
# #     serializer_class = PhoneNumebrSerializer

# #     def get_queryset(self, request):
# #         company = request.GET.get("company")
# #         return PhoneNumber.objects.filter(company_id=company)


# # class AddressAdminApi(CustomViewSetFilter):
# #     serializer_class = AddressDepthSerializer

# #     def get_queryset(self, request):
# #         company = request.GET.get("company")
# #         return Address.objects.filter(company_id=company)


class CompanyWiseApi(CustomViewSet):
    serializer_class = UserListSerializer

    def list(self, request, *args, **kwargs):
        customer = request.GET.get("customer")
        data = {}
        # data["person"] = CustomerUserSerializer(
        #     CustomerUser.objects.filter(company__id=company),
        #     many=True,
        #     context={"request": request},
        # ).data
        data["address"] = AddressDepthSerializer(
            Address.objects.filter(customer_user__id=customer), many=True
        ).data
        data["phone_number"] = PhoneNumebrSerializer(
            PhoneNumber.objects.filter(customer_user__id=customer), many=True
        ).data

        response = {"data": data, "status": status.HTTP_200_OK}
        return Response(response, status=status.HTTP_200_OK)


class CreateUserApi(CustomViewSet):
    def create(self, request, *args, **kwargs):
        request.data["user_role"] = 2
        request.data["mobile_verify"] = True
        request.data["email_verify"] = True
        request.data["password"] = "123"
        serializer = CustomerUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            response = {
                "message": "user created",
                "user_id": user.id,
                "user_name": user.full_name,
                "user_email": user.email,
                "status": status.HTTP_201_CREATED,
            }
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )


class ExcelUploadApi(ViewSet):
    authentication_classes = []

    def create(self, request):
        # model_name = request.data.get("model_name")
        # models = {model.__name__: model for model in apps.get_models()}
        # serializers = {
        #     "CustomerUser": CustomerUserDepthSerializer,

        # }
        models = [
            # CustomerUserDepthSerializer,
            # EmailSerializer,
            PhoneNumebrSerializer,
            # AddressWithoutDepthSerializer,
        ]

        # if serializers in models.keys():
        # model = models[serializers]
        # serializer = serializers[serializers]
        # model_fields = model._meta.get_fields()
        # field_names = [field.name for field in model_fields if field.concrete]
        # df = pd.read_excel(request.FILES["excel_file"])
        # customer_data = df.iloc[:, :6]
        # print('customer_data: ', customer_data)

        # email_data = df.iloc[:, 5:6]
        # print('email_data: ', email_data)

        # address_data = df.iloc[:, 7:]
        # print('address_data: ', address_data)

        # customer_data["password"] = "nuvu@2023"
        # customer_data["user_role"] = "2"
        # customer_data["E_Mail"] = 'nuvu@gmail.com'

        # column_names = df.columns.tolist()

        # if column_names == field_names[1:]:

        df = pd.read_excel(request.FILES["excel_file"])
        row = len(df)
        print("row: ----------", row)
        for serializers in models:
            print("serializers: ", serializers)

            # if serializers == CustomerUserDepthSerializer:
            #     serializer = serializers[serializers]

            #     data_df = df.iloc[:, :6]
            #     print('customer_data: -------->>>>>>>', data_df)
            #     data_df["password"] = "nuvu@2023"
            #     data_df["user_role"] = "2"

            #     serializer = serializer(
            #     data=data_df.to_dict(orient="records"), many=True
            #     )

            #     serializer.is_valid(raise_exception=True)
            #     serializer.save()

            # elif serializers == EmailSerializer:
            #     serializer = serializers[serializers]

            #     data_df = df.iloc[:, 5:6]
            #     for n in range(0, row):
            #         card_code = df.iloc[n, 0]
            #         user = CustomerUser.objects.get(CardCode = card_code)
            #         print('user: ', user.id)
            #         # row_count = n + 1
            #         print('row_count: ', n)

            #         data_df.at[n, "customer_user"] = user.id

            #     data_df["customer_user"] = data_df["customer_user"].astype(int)
            #     serializer = serializer(data=data_df.to_dict(orient="records"), many=True)
            #     serializer.is_valid(raise_exception=True)
            #     serializer.save()

            if serializers == PhoneNumebrSerializer:
                serializer = serializers[serializers]

                data_df = df.iloc[:, 6:8]
                for n in range(0, row):
                    card_code = df.iloc[n, 0]
                    user = CustomerUser.objects.get(CardCode=card_code)
                    data_df.at[n, "customer_user"] = user.id

                data_df["customer_user"] = data_df["customer_user"].astype(int)
                print("data_df: --------------------->>>>", data_df)
                serializer = serializer(
                    data=data_df.to_dict(orient="records"), many=True
                )
                serializer.is_valid(raise_exception=True)
                serializer.save()

            # elif serializers == AddressWithoutDepthSerializer:
            #     serializer = serializers[serializers]

            #     data_df = df.iloc[:, 8:]
            #     data_df.drop(["Country","State","district"],axis=1,inplace=True)
            #     print(data_df)
            #     data_df.loc[:,["Address", "Street", "Block", "ZipCode", "City", "Building", "StreetNo"]]
            #     print(data_df)

            #     for n in range(0, row):
            #         card_code = df.iloc[n, 0]
            #         user = CustomerUser.objects.get(CardCode = card_code)
            #         print('user: ', user.id)
            #         # row_count = n + 1
            #         print('row_count: ', n)
            #         data_df.at[n, "customer_user"] = user.id

            #     data_df["customer_user"] = data_df["customer_user"].astype(int)
            #     print( data_df.to_dict(orient="records"))

            #     serializer = serializer(data=data_df.to_dict(orient="records"), many=True)
            #     serializer.is_valid(raise_exception=True)
            #     serializer.save()

            else:
                response = {
                    "message": "requested model_name not found",
                    "Status": status.HTTP_400_BAD_REQUEST,
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            # serializer.is_valid(raise_exception=True)
            # serializer.save()

            # serializer = serializer(
            #     data=data_df.to_dict(orient="records"), many=True
            # )

            # serializer.is_valid(raise_exception=True)
            # serializer.save()
        logging.info("Excel download successfully")
        response = {
            "message": "ALL DATA HAS BEEN UPLOADED IN DATA BASE",
            "Status": status.HTTP_201_CREATED,
        }
        return Response(response, status=status.HTTP_201_CREATED)
        # else:
        #     logging.error("Excel uploading error")
        #     response = {"message": "field name is not same as database"}
        #     return Response(response, status=status.HTTP_400_BAD_REQUEST)


# class ExcelUploadAPI(ViewSet):
#     def create(self, request):
#         pass
# class ExcelDownloadApi(APIView):
#     authentication_classes = []

#     def get(self, request):
#         filter = request.GET.getlist("filter")
#         print("filter: ", filter)
#         model_name = request.GET.get("model_name")
#         print("model_name: ", model_name)
#         response = HttpResponse(content_type="application/ms-excel")
#         response["Content-Disposition"] = f'attachment; filename="{model_name}.xls"'
#         models = {model.__name__: model for model in apps.get_models()}
#         if model_name in models.keys():
#             serializers = {
#                 "Address": AddressSerializer,
#                 "Company": CountrySeralizer,
#                 "Product": CompanyProductItemDepthSerializer,
#             }
#             model = models[model_name]
#             model_fields = model._meta.get_fields()
#             serializer = serializers[model_name]
#             field_names = {
#                 field.name: field.verbose_name
#                 for field in model_fields
#                 if field.concrete
#             }
#             dynamic_model = [
#                 "Address",
#                 "Company",
#                 "Product",
#             ]
#             wb = xlwt.Workbook(encoding="utf-8")
#             ws = wb.add_sheet("Users Data")  # this will make a sheet named Users Data
#             forignkey_fields = {}
#             temp_fields = []
#             for field in model_fields:
#                 if isinstance(field, Models.ForeignKey):
#                     forignkey_fields[field.name] = field
#                     temp_fields.append(field)
#                 if isinstance(field, Models.ManyToManyField):
#                     forignkey_fields[field.name] = field
#                     temp_fields.append(field)
#             if model_name in dynamic_model:
#                 print(temp_fields)
#                 for field in temp_fields:
#                     related_model_field = field.related_model._meta.get_fields()
#                     print(related_model_field)
#                     for related_field in related_model_field:
#                         if isinstance(related_field, Models.ForeignKey):
#                             forignkey_fields[related_field.name] = related_field
#                             temp_fields.append(related_field)
#                         if isinstance(related_field, Models.ManyToManyField):
#                             forignkey_fields[related_field.name] = related_field
#                             temp_fields.append(related_field)

#                 for i in forignkey_fields.keys():
#                     if forignkey_fields[i].verbose_name not in field_names:
#                         field_names[forignkey_fields[i].name] = forignkey_fields[
#                             i
#                         ].verbose_name
#             # rows = model.objects.all().
#             # Sheet header, first row
#             # a = a/0
#             row_num = 0

#             font_style = xlwt.XFStyle()
#             font_style.font.bold = True

#             boolean_mapping = {True: "Yes", False: "No"}

#             kwargs = {}
#             search = request.GET.get("search")
#             columns = field_names
#             print("columns: ", columns)

#             # for col_num in range(len(columns)):
#             #     ws.write(
#             #         row_num, col_num, columns[col_num], font_style
#             #     )  # at 0 row 0 column
#             if filter:
#                 for i in filter:
#                     search = request.GET.get(i)
#                     try:
#                         if isinstance(field, ForeignKey):
#                             model = model._meta.get_field(i).related_model
#                             first_field = model._meta.fields[1].name
#                             filter_by = "{0}__{1}".format(
#                                 f"{i}__{first_field}", "icontains"
#                             )
#                         if isinstance(field, DateField):
#                             filter_by = "{0}__{1}".format(i, "range")
#                             search = search.split(" ")
#                         else:
#                             filter_by = "{0}__{1}".format(i, "icontains")
#                     except Exception as e:
#                         print(e)
#                         filter_by = "{0}__{1}".format(i, "icontains")
#                     kwargs[filter_by] = search

#             # Sheet body, remaining rows
#             rows = model.objects.filter(Q(**kwargs, _connector=Q.OR))
#             data = serializer(rows, many=True).data

#             # return Response(data)
#             col_num = 0
#             for col in data[0].keys() if data else []:
#                 if model_name in dynamic_model:
#                     col = field_names[col]
#                 else:
#                     # col = model._meta.get_field(col).verbose_name
#                     pass

#                 ws.write(row_num, col_num, col, font_style)
#                 col_num += 1
#             # for col in data[0].keys() if data else []:
#             #     col = model._meta.get_field(col).verbose_name
#             #     ws.write(row_num, col_num, col, font_style)
#             #     col_num += 1
#             font_style = xlwt.XFStyle()

#             for row in data:
#                 row_num += 1
#                 col_num = 0
#                 print("dict(row): ", dict(row))
#                 row = dict(row)
#                 for col_name in row.keys():
#                     col = row.get(col_name)
#                     # if col_name in [
#                     #     "region",
#                     #     "state",
#                     #     "substate",
#                     #     "district",
#                     #     "earthquake_zone_type",
#                     #     "security_agency_id",
#                     #     "area",
#                     #     "HSN Master",
#                     # ]:
#                     if forignkey_fields.get(col_name) and col:
#                         print("col", col_name)
#                         print(col)
#                         if isinstance(forignkey_fields.get(col_name), Models.ForeignKey):
#                             related_model = forignkey_fields.get(col_name).related_model
#                             related_instance = related_model.objects.get(id=col)
#                             related_field_name = related_model._meta.fields[1].name
#                             col = getattr(related_instance, related_field_name)

#                         elif isinstance(
#                             forignkey_fields.get(col_name), Models.ManyToManyField
#                         ):
#                             related_model = forignkey_fields.get(col_name).related_model
#                             related_instances = related_model.objects.filter(id__in=col)
#                             related_field_name = related_model._meta.fields[1].name
#                             related_values = [
#                                 getattr(instance, related_field_name)
#                                 for instance in related_instances
#                             ]
#                             col = ", ".join(related_values)
#                     # ... rest of your code ...
#                     # if isinstance(field, models.ForeignKey):
#                     #     related_model = field.related_model
#                     #     related_instance = related_model.objects.get(pk=col)
#                     #     related_field_name = related_model._meta.fields[1].name

#                     # related_query_name = model._meta.get_field(col_name).related_query_name()
#                     # print('related_query_name: ', related_query_name)
#                     # related_manager = getattr(model, related_query_name)
#                     # parent_instance = related_manager.filter(id=col).first()
#                     # parent_instance_values = parent_instance.__dict__
#                     # # Access the first field dynamically
#                     # col = parent_instance_values.get(list(parent_instance_values.keys())[1])
#                     # print('col: ', col)

#                     # Convert True/False to Yes/No if it's a boolean value
#                     if isinstance(col, bool):
#                         col = boolean_mapping.get(col, col)
#                     ws.write(row_num, col_num, str(col), font_style)
#                     col_num += 1
#             # for row in data:
#             #     for col_num in range(len(row)):
#             #         ws.write(row_num, col_num, row[col_num], font_style)

#             wb.save(response)
#             return response
#         logging.info("Excel downloading successfully")
#         return Response(
#             {"message": "this table not found"}, status=status.HTTP_400_BAD_REQUEST
#         )


class TestAPI(CustomViewSetFilter):
    authentication_classes = []

    def get_queryset(self, request):
        return CustomerUser.objects.all()

    serializer_class = ExcelUploadCustomerUserSerializer

    def create(self, request, *args, **kwargs):
        all_serializer = {
            "Item": ItemSerializer,
            "CustomerUser": ExcelUploadCustomerUserSerializer,
            "CustomerWiseItem": CustomerWiseItemWithoutDepthSerializer,
        }
        df = pd.read_excel(request.FILES["excel_file"])
        data = df.to_dict(orient="records")
        model_name = request.data.get("model_name")
        self.serializer_class = all_serializer[model_name]
        if model_name == "CustomerUser":
            customer_user = CustomerUser.objects.filter().first()
            if customer_user:
                customer_user = customer_user.id
            else:
                return Response(
                    {"message": "least one entry needed for Bulk Upload"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            for record in data:
                for key, value in record.items():
                    if pd.isna(value):
                        record[key] = None
            for i in range(len(data)):
                data[i]["password"] = "nuvu@123"
                data[i]["user_role"] = 2

                a = data[i]["E_Mail"].find("/")
                if a > -1:
                    data[i]["email"] = data[i]["E_Mail"].split("/")
                    for j in range(len(data[i]["email"])):
                        data[i]["email"][j] = {
                            "E_Mail": data[i]["email"][j],
                            "customer_user": customer_user,
                        }
                else:
                    data[i]["email"] = [{
                        "E_Mail": data[i]["E_Mail"],
                        "customer_user": customer_user,
                    }]

                # data[i]["email"] = data[i]["E_Mail"].replace(";", ",").split(",")
                # data[i]["email"] = data[i]["E_Mail"]

                if str(data[i]["Phone1"]) == str(data[i]["Phone2"]):
                    Mobile_Number = str(data[i]["Phone1"])
                else:
                    Mobile_Number = str(data[i]["Phone1"]) + "," + str(data[i]["Phone2"])

                data[i]["phone_number"] = Mobile_Number.split(",")

                # data[i]["phone_number"].append(
                #     {
                #         "phone": "+91" + str(data[i]["Phone1"]),
                #         "is_default": True,
                #         "is_verified": True,
                #         "customer_user": customer_user,
                #     }
                # )
                # data[i]["phone_number"].append(
                #     {
                #         "phone": "+91" + str(data[i]["Phone2"]),
                #         "is_default": True,
                #         "is_verified": True,
                #         "customer_user": customer_user,
                #     }
                # )
                data[i]["E_Mail"] = data[i]["E_Mail"].split("/")[0]
                for j in range(len(data[i]["phone_number"])):
                    data[i]["phone_number"][j] = {
                        "phone": "+91" + data[i]["phone_number"][j].replace(" ", ""),
                        "is_default": True,
                        "is_verified": True,
                        "customer_user": customer_user,
                    }
                # for j in range(len(data[i]["email"])):
                #     print("------------>>>hello", j)
                #     data[i]["email"][j] = {
                #         "E_Mail": data[i]["email"][j],
                #         "customer_user": customer_user,
                #     }
                data[i]["address"] = []
                country = Country.objects.filter(country__iexact=data[i]["Country"]).first()
                if country is None:
                    Country.objects.create(country_fk=country, states=data[i]["Country"])
                    country = Country.objects.filter(country__iexact=data[i]["Country"]).first()

                state = States.objects.filter(states__iexact=data[i]["State"]).first()
                if state is None:
                    States.objects.create(country_fk=country, states=data[i]["State"])
                    state = States.objects.filter(states__iexact=data[i]["State"]).first()

                city = District.objects.filter(district__iexact=data[i]["City"]).first()
                if city is None:
                    District.objects.create(state_fk=state, district=data[i]["City"])
                    city = District.objects.filter(district__iexact=data[i]["City"]).first()

                data[i]["address"].append(
                    {
                        "Address": data[i]["Address"],
                        "Street": data[i]["Street"],
                        "Block": data[i]["Block"],
                        "ZipCode": data[i]["ZipCode"],
                        "City": data[i]["City"],
                        "Country": country.id,
                        "States": state.id,
                        "Building": data[i]["Building"],
                        "StreetNo": data[i]["StreetNo"],
                        "district": city.id,
                        "customer_user": customer_user,
                        "is_default": True,
                    }
                )

            # for i in data:
            #     item = Item.objects.get(ItemCode = i["ItemCode"]).id
            #     print(item)
            #     print(CustomerWiseItem.objects.filter(item = item).exists())
            #     if CustomerWiseItem.objects.filter(item = item).exists() == False:
            #         data = [b for b in data if b.get('ItemCode') == i["ItemCode"]]
            #         print("NEW DATA", data)

            #     else:
            #         update_data = [a for a in data if a.get('ItemCode') == i["ItemCode"]]
            #         print("OLD DATA", update_data)
            #         for i in range(len(update_data)):
            #             item = Item.objects.get(ItemCode = update_data[i]["ItemCode"]).id
            #             CustomerWiseItem.objects.filter(item = item).update(
            #                                 SerialNo = update_data[i]["SerialNo"],
            #                                 QTY = update_data[i]["QTY"],
            #                                 InvoiceNo = update_data[i]["InvoiceNo"],
            #                                 InvoiceDate = update_data[i]["InvoiceDate"],
            #                                 packing_slip_no = update_data[i]["PackingShlipNo"],
            #                                 dispach_date = update_data[i]["dispatchDate"],
            #                                 work_order_no = update_data[i]["WorkOrderNumber"]
            #                             )
        elif model_name == "CustomerWiseItem":
            for i in range(len(data)):
                # date_object = datetime.datetime.strptime(
                #     data[i]["InvoiceDate"], "%Y-%m-%d"
                # )
                # date_object = datetime.datetime.strptime(date_object, "%Y-%m-%d").date()
                # data[i]["InvoiceDate"] = date_object.strftime("%Y-%m-%d")

                # date_object = datetime.datetime.strptime(
                #     data[i]["dispach_date"], "%M/%d/%Y"
                # )
                # data[i]["dispach_date"] = date_object.strftime("%Y-%m-%d")
                # dispach_date_object = data[i]["dispatchDate"].strftime("%Y-%m-%d")

                # date_object = parse(dispach_date_object)
                date_object = data[i]["InvoiceDate"].strftime("%Y-%m-%d")
                data[i]["InvoiceDate"] = data[i]["InvoiceDate"].strftime("%Y-%m-%d")

                dispatchDate = data[i]["dispatchDate"].strftime("%Y-%m-%d")
                date_object = datetime.datetime.strptime(dispatchDate, "%Y-%m-%d").date()
                data[i]["dispach_date"] = date_object

                item = Item.objects.filter(ItemCode=data[i]["ItemCode"]).first()
                customer_user = CustomerUser.objects.filter(
                    CardCode=data[i]["CardCode"]
                ).first()
                if customer_user:
                    customer_user = customer_user.id
                else:
                    customer_user = None
                if item:
                    item = item.id
                else:
                    item = None
                data[i]["item"] = item
                data[i]["customer_user"] = customer_user
                data[i]["packing_slip_no"] = data[i]["PackingShlipNo"]
                data[i]["work_order_no"] = data[i]["WorkOrderNumber"]

        # --------------------------------------- Remaning Work ---------------------------------------

        # for i in data:
        #     item = Item.objects.get(ItemCode = i["ItemCode"]).id
        #     print(item)
        #     print(CustomerWiseItem.objects.filter(item = item).exists())
        #     if CustomerWiseItem.objects.filter(item = item).exists() == False:
        #         data = [b for b in data if b.get('ItemCode') == i["ItemCode"]]
        #         print("NEW DATA", data)

        #     else:
        #         update_data = [a for a in data if a.get('ItemCode') == i["ItemCode"]]
        #         print("OLD DATA", update_data)
        #         for i in range(len(update_data)):
        #             item = Item.objects.get(ItemCode = update_data[i]["ItemCode"]).id
        #             CustomerWiseItem.objects.filter(item = item).update(
        #                                 SerialNo = update_data[i]["SerialNo"],
        #                                 QTY = update_data[i]["QTY"],
        #                                 InvoiceNo = update_data[i]["InvoiceNo"],
        #                                 InvoiceDate = update_data[i]["InvoiceDate"],
        #                                 packing_slip_no = update_data[i]["PackingShlipNo"],
        #                                 dispach_date = update_data[i]["dispatchDate"],
        #                                 work_order_no = update_data[i]["WorkOrderNumber"]
        #                             )

        # --------------------------------------- Done Work ---------------------------------------

        # elif model_name == "Item":
        #     for i in data:
        #         if Item.objects.filter(ItemCode = i["ItemCode"]).exists() == False:
        #             data = [b for b in data if b.get('ItemCode') == i["ItemCode"]]
        #             print("NEW DATA", data)
        #         else:
        #             update_data = [a for a in data if a.get('ItemCode') == i["ItemCode"]]
        #             print("OLD DATA", update_data)
        #             for i in range(len(update_data)):
        #                 Item.objects.filter(ItemCode = update_data[i]["ItemCode"]).update(
        #                                     ItemName = update_data[i]["ItemName"],
        #                                     ItemDescription = update_data[i]["ItemDescrition"],
        #                                     FrgnName = update_data[i]["FrgnName"],
        #                                     ItmsGrpCod = update_data[i]["ItmsGrpCod"],
        #                                     CstGrpCode = update_data[i]["CstGrpCode"],
        #                                     ItemType = update_data[i]["ItemType"],
        #                                     Series = update_data[i]["Series"]
        #                                 )
        print("---------------- data : ", data)
        serializer = self.get_serializer(
            data=data, context={"user": request.user}, many=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        response = {
            "message": "Created Successfully",
            "data": serializer.data,
            "status": status.HTTP_201_CREATED,
        }
        return Response(response, status=status.HTTP_201_CREATED, headers=headers)


# !!!!!!!!!!!!!! ----------- use only when nothing works ----------- !!!!!!!!!!!!!!

# class PasswordResetView(APIView):
#     authentication_classes = []
#
#     def post(self, request):
#         print(request.data)
#         E_Mail = request.data["E_Mail"]
#         users = CustomerUser.objects.all()
#         for user in users:
#             # user = CustomerUser.objects.get(E_Mail=mail)
#             # print("before", user.password)
#             # print(request.data["password"])
#             user.set_password(request.data["password"])
#             # CustomerUser.objects.filter(E_Mail=mail).update(password=request.data["password"])
#             user.save()
#             # print("After", user.password)
#             print("-------------------------------------------------------")
#
#         return Response("password reset", status=status.HTTP_200_OK)
