# # from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.ticket.api.views import (  # AssignTicketApi,; DocumentDeleteApi,; EnginnerTicketCountApi,; ProductApi,; UnAssignTicketApi,; ClientTicketApi,; ClientTicketCountApi,; CloseTicketApi,; CommentApi,; CompanyItemStatusChangeApi,; CompleteTicketApi,; DocumentApi,; EngineerAssignApi,; EngineerOnSiteAPI,; EngineerServiceEditApi,; EngineerTicketApi,; EngineerTicketCountApi,; FAQApi,; FeedBackApi,; FileUploadApi,; FTCFormApi,; InProgressTicketApi,; InstallationProblemStatusApi,; ItemStatusChangeApi,; LaststatusAPI,; NotificationApi,; OnCallTicketApi,; PendingTicketApi,; ProductApi,; ProductProblemTypeApi,; ProductQRApi,; ProductWiseItem,; RCAApi,; RCACategoryApi,; RCADepartmentApi,; ServiceReportApi,; ServiceReportCustomerVerifyApi,; SiteApi,; TicketActionApi,; TicketCustomerActionApi,; TicketListApi,; VisitAndCloseTicketApi,; VisitAndScheduleTicketApi,; WaitingForSparesTicketApi,; WebCompanyProductItemApi,; WebCustomerFormApi,; WebTicketApi,; ProductProblemTypeApi
    ClientTicketCountApi,
    ALLDateFieldsAPI,
    ClientTicketApi,
    CustomerWiseItemApi,
    EngineerAssignApi,
    EngineerOnSiteAPI,
    EngineerTicketApi,
    EngineerTicketCountApi,
    FAQApi,
    FeedBackApi,
    FTCFormApi,
    InstallationItemStatusChangeApi,
    InstallationProblemStatusApi,
    ItemProblemTypeApi,
    ItemQRApi,
    ItemWiseSpare,
    LaststatusAPI,
    NotificationApi,
    ProductApi,
    RCAApi,
    RCACategoryApi,
    RCADepartmentApi,
    ReadyToPackApi,
    ResendOTPServiceReportApi,
    ReturnSpareConfirmApi,
    ServiceReportApi,
    ServiceReportCustomerVerifyApi,
    SiteApi,
    SpareStatusChangeAPI,
    SpareTicketConfirm,
    TicketActionApi,
    TicketApi,
    TicketCustomerActionApi,
    TicketListApi,
    UserWiseSpare,
    InstalationReportApi,
    InstalationReportCustomerVerifyApi,
    PackSlipWiseItemAPI,
)

router = DefaultRouter()

router.register(
    "customer_wise_item", CustomerWiseItemApi, basename="Customer Wise Item API"
)

router.register(
    "Installation_item_status",
    InstallationItemStatusChangeApi,
    basename="Item Status API",
)
# router.register(
#     "company_item_status",
#     CompanyItemStatusChangeApi,
#     basename="Company Item Status ChangeApi",
# )

# router.register(
#     "web_company_product", WebCompanyProductItemApi, basename="Company Product API"
# )
router.register("engineer_ticket", EngineerTicketApi, basename="Engineer Ticket API")
router.register("last_status", LaststatusAPI, basename="Last Status Api")
router.register(
    "engineer_ticket_count", EngineerTicketCountApi, basename="Engineer Ticket Count API"
)
# router.register("web_ticket", WebTicketApi, basename="Web Ticket API")
# router.register(
#     "web_customer_form", WebCustomerFormApi, basename="Web Customer Form API"
# )
router.register("create_ticket", TicketApi, basename="Ticket API")
# router.register("comment", CommentApi, basename="Comment API")
# # router.register("product", ProductApi, basename="product API")
# # router.register("document", DocumentDeleteApi, basename="Document Delete API")
# router.register("file_upload", FileUploadApi, basename="FIle Upload")
# router.register("pending_status", PendingTicketApi, basename="Pending Status")
# router.register("on_call_status", OnCallTicketApi, basename="OnCall Status")
# router.register(
#     "visit_and_close_status", VisitAndCloseTicketApi, basename="VisitAndClose Status"
# )
# router.register(
#     "waiting_for_spares_status",
#     WaitingForSparesTicketApi,
#     basename="WaitingForSpares Status",
# )
# router.register(
#     "visit_and_schedule_status",
#     VisitAndScheduleTicketApi,
#     basename="VisitAndSchedule Status",
# )
router.register("customer_product_item", ProductApi, basename="Product API")
router.register("ticket_action", TicketActionApi, basename="Ticket Action API")

# router.register("in_progress_status", InProgressTicketApi, basename="InProgress Status")
# router.register("complete_status", CompleteTicketApi, basename="Complete Status")
# router.register("close_status", CloseTicketApi, basename="Close Status")
# # router.register("assign_ticket", AssignTicketApi, basename="Assign Ticket List")
# # router.register("unassign_ticket", UnAssignTicketApi, basename="un Assign Ticket List")
# router.register(
#     "enginner_ticket_count", EnginnerTicketCountApi, basename="Enginner ticket count"
# )
router.register(
    "client_ticket_count", ClientTicketCountApi, basename="Client ticket count"
)
# router.register(
#     "engineer_service", EngineerServiceEditApi, basename="Engineer Service Update API"
# )

router.register(
    "resend_otp_service_report",
    ResendOTPServiceReportApi,
    basename="ResendOTPServiceReportApi",
)

router.register("client_ticket", ClientTicketApi, basename="Client ticket")
router.register(
    "installation_problem_status",
    InstallationProblemStatusApi,
    basename="Installation Problem Status",
)
router.register("rca", RCAApi, basename="RCA API")
router.register("rca_category", RCACategoryApi, basename="RCA Category API")
router.register("rca_department", RCADepartmentApi, basename="RCA Department API")
router.register("notification", NotificationApi, basename="Notification Api")
router.register("site", SiteApi, basename="Site Checkin Checkout API")
router.register("engineer_onsite", EngineerOnSiteAPI, basename="Engineer On Site API")
router.register("engineer_assign", EngineerAssignApi, basename="Engineer Assign API")
router.register(
    "service_report_verify",
    ServiceReportCustomerVerifyApi,
    basename="Service Report customer verify API",
)
router.register(
    "Installation_report_verify",
    InstalationReportCustomerVerifyApi,
    basename="Installation Report customer verify API",
)
router.register("Service_report", ServiceReportApi, basename="Service Report Api")
router.register("installation_report", InstalationReportApi, basename="Installation Report Api")
router.register(
    "spare_ticket_confirm", SpareTicketConfirm, basename="Spare Ticket Confirm"
)

router.register(
    "ticket_customer_action", TicketCustomerActionApi, basename="reopen Ticket API"
)
router.register("feedback", FeedBackApi, basename="FeedBack API")
router.register("product_qr", ItemQRApi, basename="Product QR API")
# router.register("document", DocumentApi, basename="Document API")
router.register("faq", FAQApi, basename="FAQ API")
router.register("ftc", FTCFormApi, basename="FTC Form API")
router.register("item_problem_type", ItemProblemTypeApi, basename="McAlarm Api")
router.register("item_wise_spare", ItemWiseSpare, basename="Item Wise Spare Api")
router.register("ticket_list", TicketListApi, basename="All Ticket Api")

router.register("all_date_fields", ALLDateFieldsAPI, basename="ALL Date Fields API")
router.register(
    "status_change", SpareStatusChangeAPI, basename="Spare Status Change API"
)
router.register("user_wis_spare", UserWiseSpare, basename="User Wise Spare api")
router.register("ready_to_pack", ReadyToPackApi, basename="Ready To Pack api")
router.register(
    "return_spare_confirm", ReturnSpareConfirmApi, basename="Return Spare Confirm Api"
)
router.register(
    "pack_wise_item", PackSlipWiseItemAPI, basename="Packing Slip wise Customer wise Item list"
)


urlpatterns = [] + router.urls
