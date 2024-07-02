# import os

# from django.contrib.auth import authenticate
# from django.contrib.auth.tokens import PasswordResetTokenGenerator

# # from django.contrib.sessions.backends.db import SessionStore
# from django.utils.encoding import DjangoUnicodeDecodeError, force_bytes, smart_str
# from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
# from dotenv import load_dotenv

# # from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

# # from apps.user.customs.authentications import decode_access_token
from apps.user.models import (  # AppVersion,; Company,; User,
    Address,
    AppVersion,
    Country,
    CustomerUser,
    District,
    Email,
    PhoneNumber,
    States,
)

# from apps.user.customs.managers import UserManager


# # from apps.user.customs.authentications import decode_access_token
# from apps.user.utilities.utils import Util  # , send_otp_via_phone

# # from django.core.exceptions import ValidationError
# # from django.contrib.sessions.backends.db import SessionStore

# load_dotenv()


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = "__all__"

#     def get_user_image(self, user):
#         request = self.context.get("request")
#         photo_url = user.user_image.url
#         return request.build_absolute_uri(photo_url)

#     def create(self, validated_data):
#         return super().create(validated_data)


class CustomerUserDepthSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerUser
        fields = "__all__"
        depth = 1


# class CustomerUserWithOutEmailSerializer(serializers.ModelSerializer):
#     E_mail = serializers.EmailField(max_length=50, required=False, allow_null=True)
#     class Meta:
#         model = CustomerUser
#         fields = ["CardName", "password", "user_role", "E_mail"]
#         def create_user(self, attrs):
#             E_mail = attrs.get('E_mail')
#             UserManager.create(self, E_mail)


class CustomerUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerUser
        fields = "__all__"


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerUser
        fields = "__all__"


# class UserRegisterSerializer(serializers.ModelSerializer):
#     confirm_password = serializers.CharField()

#     class Meta:
#         model = User
#         fields = [
#             "name",
#             "email",
#             "password",
#             "confirm_password",
#             "zip_code",
#             "company_name",
#             "user_role",
#         ]

#     def validate(self, attrs):
#         password = attrs.get("password")
#         confirm_password = attrs.get("confirm_password")
#         if password != confirm_password:
#             raise serializers.ValidationError(
#                 {"Error": "Passwords and confirm passwords are not match"}
#             )
#         return attrs

#     def create(self, validated_data):
#         validated_data.pop("confirm_password")
#         user = super().create(validated_data)
#         user = User.objects.filter(id=user.id).first()
#         id = urlsafe_base64_encode(force_bytes(user.id))
#         token = PasswordResetTokenGenerator().make_token(user)
#         host = self.context.get("host")
#         link = f"http://{host}/verify_link/" + id + "/" + token + "/"
#         data = {
#             "subject": "Account verification",
#             "body": f"click Following Link for verified your Account {link}",
#             "to_email": user.email,
#         }
#         Util.send_email(data)
#         # send_otp_via_phone(user.phone)
#         print("-------------------------")
#         return user


class LoginSerializer(serializers.Serializer):
    pass
    # password = serializers.CharField(
    #     write_only=True,
    #     required=True,
    #     style={"input_type": "password", "placeholder": "Password"},
    # )


class ChangePasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(style={"input_type": "password"})
    confirm_password = serializers.CharField(style={"input_type": "password"})

    def validate(self, attrs):
        newpassword = attrs.get("new_password")
        confirmpassword = attrs.get("confirm_password")
        user = self.context.get("user")

        # if not user.check_password(oldpassword):
        #     raise serializers.ValidationError({"Error": "old Password didn't Match"})
        if newpassword != confirmpassword:
            raise serializers.ValidationError(
                {"Error": "Passwords and confirm passwords are not match"}
            )
        user.set_password(newpassword)
        user.is_pass_changed = True
        user.save()

        return super().validate(attrs)


class ResetPasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(style={"input_type": "password"})
    new_password = serializers.CharField(style={"input_type": "password"})
    confirm_password = serializers.CharField(style={"input_type": "password"})

    def validate(self, attrs):
        oldpassword = attrs.get("old_password")
        newpassword = attrs.get("new_password")
        confirmpassword = attrs.get("confirm_password")
        user = self.context.get("user")
        if not user.check_password(oldpassword):
            raise serializers.ValidationError({"Error": "old Password didn't Match"})
        if newpassword != confirmpassword:
            raise serializers.ValidationError(
                {"Error": "Passwords and confirm passwords are not match"}
            )
        user.set_password(newpassword)
        user.is_pass_changed = True
        user.save()

        return super().validate(attrs)


# class EmailVerifiedSerializer(serializers.Serializer):
#     def validate(self, attrs):
#         try:
#             id = self.context.get("id")
#             token = self.context.get("token")
#             id = smart_str(urlsafe_base64_decode(id))
#             user = User.objects.get(id=id)
#             # print(id,token)

#             if not PasswordResetTokenGenerator().check_token(user, token):
#                 raise serializers.ValidationError({"message": "Token is Expired"})
#             user.email_verify = True
#             user.save()
#             return super().validate(attrs)
#         except DjangoUnicodeDecodeError:
#             PasswordResetTokenGenerator().check_token(user, token)
#             raise serializers.ValidationError("Token is not valid or Expired")


class VerifyOTPSerializer(serializers.Serializer):
    otp = serializers.CharField()
    session_key = serializers.CharField()

    # def validate(self, attrs):
    #     otp = attrs.get("otp")
    #     session_key = attrs.get("session_key")
    #     try:
    #         s = SessionStore(session_key=session_key)
    #         session_otp = s["OTP"]
    #     except Exception:
    #         raise ValueError({"message": "your session is expired"})

    #     if otp != session_otp:
    #         raise ValueError({"message": "otp is not match"})
    #     return super().validate(attrs)


# # class ForgotPasswordSerializer(serializers.Serializer):
# #     email = serializers.EmailField()

# #     def validate(self, attrs):
# #         user = User.objects.filter(email=attrs.get("email")).first()
# #         if not user:
# #             raise serializers.ValidationError({"msg": "this email is not registerd"})

# #         otp = genrate_otp()
# #         sessions = SessionStore(session_key=self.context.get("session_key"))
# #         sessions["OTP"] = otp
# #         sessions.save()
# #         sessions.modified
# #         data = {
# #             "subject": "Account verification",
# #             "body": f"This is your One Time password {otp} for forgot password",
# #             "to_email": user.email,
# #         }

# #         Util.send_email(data)
# #         return super().validate(attrs)


# class ForgotPasswordSerializer(serializers.Serializer):
#     email = serializers.EmailField()

#     def validate(self, attrs):
#         user = User.objects.filter(email=attrs["email"]).first()
#         if user is None:
#             raise serializers.ValidationError({"message": "this Email id is not found"})
#         id = urlsafe_base64_encode(force_bytes(user.id))
#         token = PasswordResetTokenGenerator().make_token(user)
#         # link = f"http://{str(self.initial_data.get('HTTP_HOST'))}/{id}/{token}/"
#         # host = self.context.get("host")
#         # link = f"http://{host}/verify_password/{id}/{token}/"
#         react_url = os.getenv("REACT_BASE_URL")
#         link = f"{react_url}forgot_email_password?id={id}&token={token}"
#         data = {
#             "subject": "Forgot password",
#             "body": f"click Following Link for Forgot your Password {link}",
#             "to_email": user.email,
#         }
#         Util.send_email(data)

#         return super().validate(attrs)

#     # def validate(self, attrs):
#     #     try:
#     #         id = self.context.get("id")
#     #         token = self.context.get("token")

#     #         id = smart_str(urlsafe_base64_decode(id))
#     #         user = User.objects.get(id=id)
#     #         if not PasswordResetTokenGenerator().check_token(user, token):
#     #             raise serializers.ValidationError(
#     #                 {"Error": "Token is not valid or Expired"}
#     #             )
#     #         # session_data = SessionStore()
#     #         # session_data.set_expiry(500)
#     #         # session_data["email"] = user.email
#     #         # session_data.create()

#     #         # if password != password2:
#     #         #     raise serializers.ValidationError(
#     #         #         {"Error": "Passwords and confirm passwords are not match"}
#     #         #     )
#     #         # user.set_password(password)
#     #         # user.save()
#     #         return super().validate(attrs)
#     #     except DjangoUnicodeDecodeError:
#     #         PasswordResetTokenGenerator().check_token(user, token)
#     #         raise serializers.ValidationError({"Error": "Token is not valid or Expired"})


# class VerifyPasswordSerializer(serializers.Serializer):
#     newpassword = serializers.CharField(style={"input_type": "password"})
#     confirmpassword = serializers.CharField(style={"input_type": "password"})
#     id = serializers.CharField()
#     token = serializers.CharField()

#     def validate(self, attrs):
#         try:
#             password = attrs.get("newpassword")
#             password2 = attrs.get("confirmpassword")
#             id = attrs.get("id")
#             token = attrs.get("token")
#             id = smart_str(urlsafe_base64_decode(id))
#             user = User.objects.get(id=id)
#             if not PasswordResetTokenGenerator().check_token(user, token):
#                 raise serializers.ValidationError(
#                     {"Error": "Token is not valid or Expired"}
#                 )
#             if password != password2:
#                 raise serializers.ValidationError(
#                     {"Error": "Passwords and confirm passwords are not match"}
#                 )
#             user.set_password(password)
#             user.save()
#             return super().validate(attrs)
#         except DjangoUnicodeDecodeError:
#             PasswordResetTokenGenerator().check_token(user, token)
#             raise serializers.ValidationError({"Error": "Token is not valid or Expired"})

#     # newpassword = serializers.CharField(style={"input_type": "password"})
#     # confirmpassword = serializers.CharField(style={"input_type": "password"})
#     # token = serializers.CharField()

#     # def validate(self, attrs):
#     #     password = attrs.get("newpassword")
#     #     password2 = attrs.get("confirmpassword")
#     #     token = attrs.get("token")
#     #     id = decode_access_token(token)
#     #     try:
#     #         user = User.objects.get(id=id)
#     #     except Exception:
#     #         raise serializers.ValidationError(
#     #             {"Error": "Token expired please regenerate otp"}
#     #         )
#     #     if password != password2:
#     #         raise serializers.ValidationError(
#     #             {"Error": "Passwords and confirm passwords are not match"}
#     #         )
#     #     user.password = password
#     #     user.save()
#     #     return super().validate(attrs)


class AppVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppVersion
        fields = "__all__"


# class LoginMobileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = AppVersion
#         fields = "__all__"


# class MobileNumberSerializer(serializers.Serializer):
#     mobile = serializers.CharField()


# # class VeifyOtpForLoginSerializer(serializers.Serializer):
# #     otp = serializers.CharField()
# #     session_id = serializers.CharField()
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"


class AddressDepthSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"
        depth = 1


class AddressWithoutDepthSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"


class PhoneNumebrSerializer(serializers.ModelSerializer):
    # country_code = serializers.CharField(read_only = True)

    class Meta:
        model = PhoneNumber
        fields = "__all__"


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = "__all__"


class CountrySeralizer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"


class StateSeralizer(serializers.ModelSerializer):
    class Meta:
        model = States
        fields = "__all__"


class DistrictSeralizer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = "__all__"


# class CompanySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Company
#         fields = "__all__"


class ExcelUploadCustomerUserSerializer(serializers.ModelSerializer):
    phone_number = PhoneNumebrSerializer(source="phonenumber_set", many=True)
    email = EmailSerializer(source="email_set", many=True)
    address = AddressSerializer(source="address_set", many=True)

    class Meta:
        model = CustomerUser
        fields = "__all__"

    def create(self, validated_data):
        email = list(validated_data.pop("email_set", []))
        phone_number = list(validated_data.pop("phonenumber_set", []))
        address = list(validated_data.pop("address_set", {}))
        email_list = []
        customer_user = super().create(validated_data)
        for i in address:
            i["customer_user"] = customer_user
            Address.objects.create(**i)

        for i in email:
            i["customer_user"] = customer_user
            Email.objects.create(**i)
        for i in phone_number:
            i["customer_user"] = customer_user
            PhoneNumber.objects.create(**i)
        return customer_user
