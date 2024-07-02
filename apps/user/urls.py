# """user's URL Configuration
# """
from django.shortcuts import render
from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.user.api.views import (  # VeriifyLinkForForgotPasswordApi,; AddressAdminApi,; PhoneNumberAdminApi,; AppVersionApi,; CompanyApi,; CompanyWiseApi,; CreateUserApi,; EmailResetVerifiedApi,; EmailVerifedApi,; ExcelDownloadApi,; ExcelUploadApi,; ForgotPasswordApi,; ProfileApi,; SendMobileOTP,; SignUpApi,; UserListApi,; UserMobileUpdateApi,; VeifyOtpForLoginApi,; VerfiyMobileOtp,; VerfiyMobileOtpUser,; VerifyOTPforForgotApi,; VerifyPasswordApi,
    AddressApi,
    AppVersionApi,
    ChangePasswordApi,
    CompanyWiseApi,
    CountryApi,
    CreateUserApi,
    CustomerApi,
    DistrictApi,
    EmailResetVerifiedApi,
    ExcelUploadApi,
    LoginApi,
    PhoneNumberApi,
    ProfileApi,
    StateApi,
    TestAPI,
    UserListApi,
    VeifyOtpForLoginApi,
    VerfiyMobileOtp,
    # PasswordResetView
)

router = DefaultRouter()
router.register("test", TestAPI, basename="Test APi")
router.register("login", LoginApi, basename="Login API")
# router.register("signup", SignUpApi, basename="Sign Up API")
router.register("change_password", ChangePasswordApi, basename="Change Password API")
router.register("app_version", AppVersionApi, basename="app_version")
# router.register("send_otp", SendMobileOTP, basename="Send Mobile Otp for login")
router.register("profile", ProfileApi, basename="Profile API")
router.register(
    "verfiy_otp_login", VeifyOtpForLoginApi, basename="Verify Mobile Otp for login"
)
# router.register(
#     "verfiy_otp_forgot", VerifyOTPforForgotApi, basename="Verify otp for forgot api"
# )
router.register("engineer_list", UserListApi, basename="User List Api")
router.register("address", AddressApi, basename="Address Api")
router.register("phone_number", PhoneNumberApi, basename="phone Number Api")
router.register("country", CountryApi, basename="Country Api")
router.register("state", StateApi, basename="State Api")
router.register("district", DistrictApi, basename="District Api")
# router.register("user_mobile", UserMobileUpdateApi, basename="User Mobile Update Api")
router.register("customer", CustomerApi, basename="Company Api")
# # router.register(
# #     "phone_number_admin", PhoneNumberAdminApi, basename="Phone Number Admin Api"
# # )
# # router.register("address_admin", AddressAdminApi, basename="Address Admin Api")
router.register(
    "customer_wise_data", CompanyWiseApi, basename="Company Wise Person List"
)
router.register("create_user", CreateUserApi, basename="Create User Api")
router.register("excel_upload", ExcelUploadApi, basename="excel upload")


def upload_file(request):
    return render(request, "upload_excel.html")


urlpatterns = [
                  # path("pass_cng/", PasswordResetView.as_view(), name="pass_cng"),
                  path("upload/", upload_file, name='upload-file'),
                  #     path(
                  #         "forgot_password/",
                  #         ForgotPasswordApi.as_view(),
                  #         name="Forgot Password API",
                  #     ),
                  path("mobile_otp/", VerfiyMobileOtp.as_view(), name="Mobile OTP Verified API"),
                  #     path(
                  #         "verify_link/<id>/<token>/",
                  #         EmailVerifedApi.as_view(),
                  #         name="Email Verified API",
                  #     ),
                  #     path(
                  #         "verify_password/",
                  #         VerifyPasswordApi.as_view(),
                  #         name="Verify Password API",
                  #     ),
                  #     path(
                  #         "verify_mobile_user/",
                  #         VerfiyMobileOtpUser.as_view(),
                  #         name="Verify Mobile User API",
                  #     ),
                  path(
                      "verify_email_user/",
                      EmailResetVerifiedApi.as_view(),
                      name="Verify Mobile User API",
                  ),
                  #     path("excel_download", ExcelDownloadApi.as_view(), name="excel download"),
              ] + router.urls
