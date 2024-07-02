# # from django.shortcuts import render
import os

from apps.ticket.models import Document
from django.contrib.sessions.backends.db import SessionStore
from django.core.mail import EmailMessage
from django.db.models import Q
from django.utils import timezone
from dotenv import load_dotenv
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet

load_dotenv()

from apps.ticket.api.serializer import (  # TeamMemberSerializer,; TicketStatusSerializer,; DocumentSerializer,; ProductDepthSerializer,; ProductSerializer,; TicketDepthSerializer,; FeedBackDepthSerializer,; CompanyProductItemSerializer,; ItemDepthSerializer,; AttachmentSerializer,; CommentSerializer,; CompanyProductItemDepthSerializer,; CompanyTicketInstallationItemStatusSerializers,; DepthCompanyTicketInstallationItemStatusSerializers,; DocumentProductSerializer,; DocumentSerializer,; EnginnerSerializer,; EnginnerWithoutDepthSerializer,; FAQSerializer,; FeedBackSerializer,; FTCFormSerializer,; InstallationProblemStatusSerializer,; ItemSerializer,; LastStatusDepthSerializer,; LastStatusSerializer,; NotificationSeralizer,; ProductProblemTypeSerializer,; # ProductQRSerializer,; RCACategorySerializer,; RCADepartmentSerializer,; RCASerializer,; RepairServiceSerializer,; ServiceReportPartSerializer,; ServiceReportSerializer,; SpareDetailSerializer,; TicketDepthSerializer,; UploadFIleSerializer,
    AllDateFieldSerializer,
    CustomerWiseItemSerializer,
    DepthCompanyTicketInstallationItemStatusSerializers,
    DocumentProductSerializer,
    EnginnerSerializer,
    EnginnerWithoutDepthSerializer,
    FAQSerializer,
    FeedBackSerializer,
    FTCFormSerializer,
    InstallationProblemStatusSerializer,
    InstallationSerializer,
    ItemProblemTypeSerializer,
    ItemSerializer,
    ItemSpareSerializer,
    LastStatusDepthSerializer,
    LastStatusSerializer,
    NotificationSeralizer,
    OtherServiceSerializer,
    RCACategorySerializer,
    RCADepartmentSerializer,
    RCASerializer,
    RepairServiceSerializer,
    ReturnSpareDetailSerializer,
    ReturnSpareSerializer,
    SalesInquirySerializer,
    ServiceReportDepthSerializer,
    ServiceReportPartDepthSerializer,
    ServiceReportPartSerializer,
    ServiceReportSerializer,
    ServiceSerializer,
    SpareDetailSerializer,
    SparesDepthSerializer,
    SparesSerializer,
    TicketDepthSerializer,
    TicketInstallationItemStatusSerializer,
    TicketSerializer,
    InstallationReportSerializer,
    InstallationReportPartSerializer,
    InstallationReportDepthSerializer,
    InstallationReportPartDepthSerializer
)
from apps.ticket.models import (  # ServiceReportPart,; FAQ,; RCA,; Comment,; CompanyProductItem,; CompanyTicketInstallationItemStatus,; Document,; FeedBack,; FileUpload,; FTCForm,; Installation,; InstallationaProblemStatus,; Item,; LastStatus,; Notification,; OtherService,; # Product,; ProductProblemType,; RCACategory,; RCADepartment,; ServiceReport,
    FAQ,
    RCA,
    CompanyTicketInstallationItemStatus,
    CustomerWiseItem,
    Engineer,
    FeedBack,
    FTCForm,
    Installation,
    InstallationaProblemStatus,
    ItemProblemType,
    ItemSpare,
    LastStatus,
    Notification,
    OtherService,
    RCACategory,
    RCADepartment,
    Repair,
    SalesInquiry,
    Service,
    ServiceReport,
    ServiceReportPart,
    SpareBox,
    SpareDetail,
    Spares,
    Ticket,
    Item,
    InstallationReport,
    InstallationReportPart,
)
from apps.ticket.utilities.utils import RequiredFields, render_to_pdf

# # from apps.user.api.serializer import AddressSerializer  # , PhoneNumebrSerializer
from apps.user.customs.permissions import (
    IsAdminUser,
    IsDispatchUpdater,
    IsEngineer,
    IsProductionUpdater,
    IsPurchaseUpdate,
    IsStoreUpdater,
)

# # from apps.user.customs.permissions import ReadOnly
from apps.user.customs.viewsets import CustomViewSet, CustomViewSetFilter
from apps.user.models import CustomerUser


# from apps.user.utilities.swaggers import filter, id, type
# from apps.user.utilities.utils import send_otp_via_phone

# # from apps.ticket.models import Ticket

# # Create your views here.


class TicketApi(CustomViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    authentication_classes = []

    # permission_classes = [IsNotEngineer]

    # @swagger_auto_schema(
    #     request_body=TicketSerializer,
    #     operation_description="Ticket Create",
    # )

    def create(self, request):
        is_guest = request.data.get("is_guest", False)
        if request.data.get("current_ticket"):
            current_ticket = Ticket.objects.filter(
                id=request.data["current_ticket"]
            ).first()
            current_ticket.ticket_status = "waiting_for_spares"
            current_ticket.save()
            request.data["is_guest"] = current_ticket.is_guest
            request.data["customer_fk"] = current_ticket.customer_fk.id
            if current_ticket.is_guest == False:
                request.data["mobile_no_fk"] = current_ticket.mobile_no_fk.id
                request.data["address_fk"] = current_ticket.address_fk.id
            else:
                request.data["address"] = current_ticket.address
                request.data["mobile_no"] = current_ticket.mobile_no
            request.data["customer_wise_item"] = list(
                current_ticket.customer_wise_item.all().values_list("id", flat=True)
            )
        elif is_guest:
            print("-------------HHEHEHEHE IN current_ticket-------------")
            #  Email field add in required fields
            if not request.data.get("mobile_no") or not request.data.get("address") or not request.data.get("email"):
                return Response(
                    {"message": "Mobile number, Address and Email is required for guest User"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            if not request.data.get("mobile_no_fk") or not request.data.get(
                    "address_fk"
            ):
                return Response(
                    {"message": "mobile_no_fk and address_fk is required for is_guest"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        if int(request.data.get("ticket_type")) == 1:
            if is_guest == False:  # Normal case (with out gust user)
                if not request.data.get("packing_slip_no") or not request.data.get("work_order_no"):
                    return Response(
                        {"message": "packing_slip_no and work_order_no Field is mandatory"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                packing_slip_no = request.data.get("packing_slip_no")
                work_order_no = request.data.get("work_order_no")
                customer_wise_item = CustomerWiseItem.objects.filter(
                    packing_slip_no=packing_slip_no,
                    work_order_no=work_order_no
                )
            if is_guest == False:  # Normal case (with out gust user)
                if not customer_wise_item.exists():
                    return Response(
                        {"message": "can't create ticket for this combination of  packing_slip_no and work_order_no"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                request.data["customer_wise_item"] = list(
                    customer_wise_item.values_list("id", flat=True)
                )
                request.data["customer_fk"] = customer_wise_item.first().customer_user.id
                request.data["region"] = customer_wise_item[0].customer_user.GroupCode

            else:  # is gust true
                packing_slip_no = request.data.get("packing_slip_no")
                work_order_no = request.data.get("work_order_no")
                if packing_slip_no and work_order_no:
                    if CustomerWiseItem.objects.filter(
                            packing_slip_no=packing_slip_no,
                            work_order_no=work_order_no
                    ).exists():
                        customer_wise_item = CustomerWiseItem.objects.filter(packing_slip_no=packing_slip_no,
                                                                             work_order_no=work_order_no)
                        request.data["customer_wise_item"] = list(
                            customer_wise_item.values_list("id", flat=True))
                        request.data["customer_fk"] = customer_wise_item.first().customer_user.id
                        request.data["region"] = customer_wise_item[0].customer_user.GroupCode
                else:
                    request.data["customer_wise_item"] = []
                    request.data["customer_fk"] = None
                    request.data["region"] = ""

        elif int(request.data.get("ticket_type")) in [2, 3, 6]:
            if request.data.get("SerialNo"):
                serial_no = request.data.get("SerialNo")
                customer_wise_item = CustomerWiseItem.objects.filter(SerialNo=serial_no)
                if not customer_wise_item.exists():
                    return Response(
                        {"message": "can't create ticket for this SerialNo"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                request.data["customer_wise_item"] = list(
                    customer_wise_item.values_list("id", flat=True)
                )
                request.data["customer_fk"] = customer_wise_item.first().customer_user.id
            else:
                if not request.data.get("customer_wise_item"):
                    return Response(
                        {"message": "Provide customer_wise_item or SerialNo"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                item = request.data.get("customer_wise_item")[0]
                request.data["customer_fk"] = CustomerWiseItem.objects.get(
                    id=item
                ).customer_user.id
        # if int(request.data["ticket_type"]) == 1:
        #     print("im here hona chahiye")
        #     request.data["customer_wise_item"] = 1
        # if request.user.user_role == 2:
        #     # request.data["created_by_customer"] = True
        #     request.data["customer_fk"] = request.user.id
        #     request.data["company"] = request.user.company.id

        ticket_serializer = TicketSerializer(data=request.data)
        if ticket_serializer.is_valid(raise_exception=True):
            # serializer.data.get("")
            pass
        else:
            return Response(ticket_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # if request.user.user_role == 2:
        #     if request.data.get("address"):
        #         data = request.data["address"]
        #         data["user_fk"] = request.user.id
        #         serializer = AddressSerializer(data=data)
        #         if serializer.is_valid(raise_exception=True):
        #             serializer.save()
        #         else:
        #             return Response(
        #                 serializer.errors, status=status.HTTP_400_BAD_REQUEST
        #             )
        ticket_type = ticket_serializer.validated_data["ticket_type"]
        if ticket_type == 1:  # installation
            serializer = InstallationSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                print("---------------")

                print("im here")
                ticket = ticket_serializer.save()
                request.data["ticket_fk"] = ticket.id
                serializer = InstallationSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                # ticket_type = ticket.ticket_type
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif ticket_type == 2:  # Service
            serializer = ServiceSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                ticket = ticket_serializer.save()
                request.data["ticket_fk"] = ticket.id
                # ticket_type = ticket.ticket_type
                serializer = ServiceSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)

                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif ticket_type == 3:  # Spares
            for i in ["spare_detail"]:
                if i not in request.data.keys():
                    return Response(
                        {"message": f"{i} is required"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                if not request.data[i]:
                    return Response(
                        {"message": "spare_detail shouldn't empty"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                for j in ["part_name", "part_desciption", "qunatity"]:
                    for k in request.data[i]:
                        if j not in k.keys():
                            return Response(
                                {"message": f"{j} is required"},
                                status=status.HTTP_400_BAD_REQUEST,
                            )
            serializer = SparesSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                ticket = ticket_serializer.save()
                request.data["ticket_fk"] = ticket.id
                # ticket_type = ticket.ticket_type
                serializer = SparesSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                spare = serializer.save()
                data = request.data["spare_detail"]
                for i in data:
                    i["spare"] = spare.id
                serializer = SpareDetailSerializer(data=data, many=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                if request.data.get("current_ticket"):
                    current_ticket = Ticket.objects.filter(
                        id=request.data["current_ticket"]
                    ).first()
                    current_ticket.spare_ticket_id = ticket.id
                    current_ticket.save()
                    engineer = current_ticket.ticket_engineer.filter(
                        is_assign=True
                    ).first()
                    Engineer.objects.create(
                        ticket_fk=ticket,
                        is_assign=True,
                        engineer_fk=engineer.engineer_fk,
                    )
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif ticket_type == 4:  # Sales_inquiry
            serializer = SalesInquirySerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                ticket = ticket_serializer.save()
                request.data["ticket_fk"] = ticket.id
                # ticket_type = ticket.ticket_type
                serializer = SalesInquirySerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif ticket_type == 5:  # Others
            serializer = OtherServiceSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                ticket = ticket_serializer.save()
                request.data["ticket_fk"] = ticket.id
                serializer = OtherServiceSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                # ticket_type = ticket.ticket_type
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif ticket_type == 6:  # Repair
            serializer = RepairServiceSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                ticket = ticket_serializer.save()
                request.data["ticket_fk"] = ticket.id
                # ticket_type = ticket.ticket_type
                serializer = RepairServiceSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = ReturnSpareSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                ticket = ticket_serializer.save()
                request.data["ticket_fk"] = ticket.id
                # ticket_type = ticket.ticket_type
                if not request.data.get("return_spares_details"):
                    return Response(
                        {"message": "return_spares_details is required fields"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                data = request.data.get("return_spares_details")
                serializer = ReturnSpareDetailSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # if request.data.get("team_member"):
        #     data = request.data["team_member"]
        #     for i in data:
        #         i["ticket_fk"] = ticket.id
        #     serializer = TeamMemberSerializer(data=data, many=True)
        #     if serializer.is_valid(raise_exception=True):
        #         serializer.save()
        # if request.data.get("attachment"):
        #     data = request.data["attachment"]
        #     for i in data:
        #         i["ticket_fk"] = ticket.id
        #     serializer = AttachmentSerializer(data=data, many=True)
        #     if serializer.is_valid(raise_exception=True):
        #         serializer.save()
        return Response(
            {"message": "Ticket Created Successfully", "data": ticket_serializer.data},
            status=status.HTTP_200_OK,
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        print(request.data)
        instance = self.get_object()
        print(instance)
        item_list = []
        for i in range(len(request.data["id"])):
            current_ticket = CustomerWiseItem.objects.get(id=request.data["id"][i])
            print(current_ticket)
            item_list.append(current_ticket.id)
            region = current_ticket.customer_user.GroupCode
            customer_user_after_update = current_ticket.customer_user.id
            print("new customer user fk", customer_user_after_update)
            print("region", region)
        data = {
            "customer_wise_item": item_list,
            "region": region,
            "customer_fk" : customer_user_after_update
        }
        serializer = TicketSerializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        data = {
            "packing_slip_no": request.data["packing_slip_no"],
            "work_order_no": request.data["work_order_no"]
        }
        instance = instance.ticket_installation
        print(instance)
        installation_serializer = InstallationSerializer(instance, data=data, partial=partial)
        installation_serializer.is_valid(raise_exception=True)
        self.perform_update(installation_serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        response = {
            "message": "Updated Succesfully",
            "data": serializer.data,
            "installation_data": installation_serializer.data,
            "status": status.HTTP_200_OK,
        }
        return Response(response, status=status.HTTP_200_OK)


class CustomerWiseItemApi(CustomViewSetFilter):
    serializer_class = CustomerWiseItemSerializer

    def get_queryset(self, request):
        self.response_tag = "customer_wise_item"
        search = request.GET.get("search")
        if request.GET.get("search"):
            return request.user.customerwiseitem_set.filter(
                Q(item__ItemName__icontains=search)
                | Q(SerialNo__icontains=search)
                | Q(item__ItemCode__icontains=search),
            )
        return request.user.customerwiseitem_set.all()


# class CommentApi(CustomViewSet):
#     def list(self, request):
#         try:
#             ticket_fk = request.data["ticket_fk"]
#         except Exception:
#             return Response(
#                 {"message": "ticket_fk field is mandatory"},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )
#         comment = Comment.objects.filter(ticket_fk=ticket_fk, parent_fk__isnull=True)
#         data = CommentSerializer(comment, many=True).data
#         response = {"data": data}
#         return Response(response, status=status.HTTP_200_OK)


# class ReplyApi(ViewSet):
#     def list(self, request):
#         try:
#             ticket_fk = request.data["ticket_fk"]
#         except Exception:
#             return Response(
#                 {"message": "ticket_fk field is mandatory"},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )
#         comment = Comment.objects.filter(ticket_fk=ticket_fk, parent_fk__isnull=False)
#         data = CommentSerializer(comment, many=True).data
#         response = {"data": data}
#         return Response(response, status=status.HTTP_200_OK)


# # class TicketTracking(ViewSet):
# #     def create(self,request):
# # class ProductApi(CustomViewSet):
# #     serializer_class = ProductDepthSerializer
# #     queryset = Product.objects.all()

# #     @swagger_auto_schema(
# #         request_body=ProductDepthSerializer,
# #         operation_description="Product create",
# #     )
# #     def create(self, request):
# #         if request.data.get("document_name") and request.data.get("document_file"):
# #             serializer = DocumentSerializer(data=request.data)
# #             serializer.is_valid(raise_exception=True)
# #             document = serializer.save()
# #             request.data["document_fk"] = document.id

# #         serializer = ProductSerializer(data=request.data)
# #         serializer.is_valid(raise_exception=True)
# #         serializer.save()
# #         response = {
# #             "message": "product added successfully",
# #             "data": serializer.data,
# #             "status": status.HTTP_201_CREATED,
# #         }
# #         return Response(response, status=status.HTTP_201_CREATED)

# #     def destroy(self, request, *args, **kwargs):
# #         instance = self.get_object()
# #         if instance.document_fk:
# #             Document.objects.filter(id=instance.document_fk.id).delete()
# #         self.perform_destroy(instance)
# #         response = {
# #             "message": "Deleted Succesfully",
# #             "data": "deleted",
# #             "status": status.HTTP_200_OK,
# #         }
# #         return Response(response, status=status.HTTP_200_OK)


# # class DocumentDeleteApi(ModelViewSet):
# #     queryset = Document.objects.all()
# #     serializer_class = DocumentSerializer

# #     @swagger_auto_schema(
# #         request_body=DocumentSerializer,
# #         operation_description="",
# #     )
# #     def create(self, request, *args, **kwargs):
# #         if request.data.get("product_id"):
# #             product = Product.objects.filter(id=request.data.get("product_id")).first()
# #         else:
# #             return Response(
# #                 {"message": "product_id field Required"}, status=status.HTTP_400_BAD_REQUEST
# #             )
# #         serializer = self.get_serializer(
# #             data=request.data, context={"user": request.user}
# #         )

# #         serializer.is_valid(raise_exception=True)
# #         document_fk = serializer.save().id
# #         print("------------------", document_fk)
# #         serializer = ProductSerializer(
# #             product, data={"document_fk": document_fk}, partial=True
# #         )
# #         serializer.is_valid(raise_exception=True)
# #         serializer.save()
# #         headers = self.get_success_headers(serializer.data)
# #         response = {
# #             "message": "Created Succesfully",
# #             "data": serializer.data,
# #             "status": status.HTTP_201_CREATED,
# #         }
# #         return Response(response, status=status.HTTP_201_CREATED, headers=headers)

# #     def destroy(self, request, *args, **kwargs):
# #         instance = self.get_object()
# #         self.perform_destroy(instance)
# #         response = {
# #             "message": "Deleted Succesfully",
# #             "data": "deleted",
# #             "status": status.HTTP_200_OK,
# #         }
# #         return Response(response, status=status.HTTP_200_OK)


# class FileUploadApi(CustomViewSet):
#     parser_classes = [MultiPartParser]
#     serializer_class = UploadFIleSerializer
#     queryset = FileUpload.objects.all()

#     # @swagger_auto_schema(
#     #     request_body=UploadFIleSerializer,
#     #     operation_description="File Upload",
#     # )
#     def create(self, request, *args, **kwargs):
#         serializer = UploadFIleSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             response = serializer.data
#             response["status"] = status.HTTP_201_CREATED
#             response["file"] = (
#                 "http://" + request.META["HTTP_HOST"] + serializer.data["file"]
#             )
#             return Response(response, status=status.HTTP_201_CREATED)


# class PendingTicketApi(CustomViewSet):
#     serializer_class = TicketSerializer

#     # @swagger_auto_schema(
#     #     request_body=TicketSerializer,
#     #     operation_description="Pending Ticket list",
#     # )
#     def get_queryset(self):
#         user = self.request.user
#         if user.user_role == 2:
#             queryset = Ticket.objects.filter(
#                 ticket_status="pending", customer_fk=self.request.user
#             )
#         else:
#             queryset = Ticket.objects.filter(ticket_status="pending")
#         return queryset


# class WaitingTicketApi(CustomViewSet):
#     serializer_class = TicketSerializer

#     # @swagger_auto_schema(
#     #     request_body=TicketSerializer,
#     #     operation_description="Witing Ticket list",
#     # )
#     def get_queryset(self):
#         user = self.request.user
#         if user.user_role == 3:
#             pass
#             # queryset = Ticket.objects.filter(ticket_status="waiting", engineer_fk=user)
#         else:
#             queryset = Ticket.objects.filter(ticket_status="waiting")
#         return queryset


# class OnCallTicketApi(CustomViewSet):
#     serializer_class = TicketSerializer

#     # @swagger_auto_schema(
#     #     request_body=TicketSerializer,
#     #     operation_description="On Call Ticket list",
#     # )
#     def get_queryset(self):
#         user = self.request.user
#         if user.user_role == 3:
#             pass
#             # queryset = Ticket.objects.filter(ticket_status="on_call", engineer_fk=user)
#         else:
#             queryset = Ticket.objects.filter(ticket_status="on_call")
#         return queryset


# class VisitAndCloseTicketApi(CustomViewSet):
#     serializer_class = TicketSerializer

#     # @swagger_auto_schema(
#     #     request_body=TicketSerializer,
#     #     operation_description="Visit and Close Ticket List",
#     # )
#     def get_queryset(self):
#         user = self.request.user
#         if user.user_role == 3:
#             queryset = Ticket.objects.filter(
#                 ticket_status="visit_and_close", engineer_fk=user
#             )
#         else:
#             queryset = Ticket.objects.filter(ticket_status="visit_and_close")
#         return queryset


# class WaitingForSparesTicketApi(CustomViewSet):
#     serializer_class = TicketSerializer
#     queryset = Ticket.objects.filter(ticket_status="waiting_for_spares")

#     # @swagger_auto_schema(
#     #     request_body=TicketSerializer,
#     #     operation_description="Waiting For Spares list",
#     # )
#     def get_queryset(self):
#         user = self.request.user
#         if user.user_role == 3:
#             # queryset = Ticket.objects.filter(
#             #     ticket_status="waiting_for_spares", engineer_fk=user
#             # )
#             pass
#         else:
#             queryset = Ticket.objects.filter(ticket_status="waiting_for_spares")
#         return queryset


# class VisitAndScheduleTicketApi(CustomViewSet):
#     serializer_class = TicketSerializer

#     queryset = Ticket.objects.filter(ticket_status="visit_and_schedule")

#     # @swagger_auto_schema(
#     #     request_body=TicketSerializer,
#     #     operation_description="Visit And Schedule",
#     # )
#     def get_queryset(self):
#         user = self.request.user
#         if user.user_role == 3:
#             # queryset = Ticket.objects.filter(
#             #     ticket_status="waiting_for_spares", engineer_fk=user
#             # )
#             pass
#         else:
#             queryset = Ticket.objects.filter(ticket_status="waiting_for_spares")
#         return queryset


# class InProgressTicketApi(CustomViewSet):
#     serializer_class = TicketSerializer

#     # @swagger_auto_schema(
#     #     request_body=TicketSerializer,
#     #     operation_description="In Progress Ticket list",
#     # )
#     def get_queryset(self):
#         queryset = Ticket.objects.filter(customer_fk=self.request.user).exclude(
#             Q(ticket_status="pending")
#             & Q(ticket_status="complete")
#             & Q(ticket_status="close")
#         )
#         return queryset


# class CompleteTicketApi(CustomViewSet):
#     serializer_class = TicketSerializer

#     # @swagger_auto_schema(
#     #     request_body=TicketSerializer,
#     #     operation_description="Complete Ticket list",
#     # )
#     def get_queryset(self):
#         user = self.request.user
#         if user.user_role == 2:
#             queryset = Ticket.objects.filter(
#                 ticket_status="complete", customer_fk=self.request.user
#             )
#         else:
#             queryset = Ticket.objects.filter(ticket_status="complete")
#         return queryset


# class CloseTicketApi(CustomViewSet):
#     serializer_class = TicketSerializer

#     # @swagger_auto_schema(
#     #     request_body=TicketSerializer,
#     #     operation_description="Close Ticket list",
#     # )
#     def get_queryset(self):
#         user = self.request.user
#         if user.user_role == 2:
#             queryset = Ticket.objects.filter(
#                 ticket_status="close", customer_fk=self.request.user
#             )
#         else:
#             queryset = Ticket.objects.filter(ticket_status="close")
#         return queryset


# # class UnAssignTicketApi(CustomViewSet):
# #     serializer_class = TicketSerializer
# #     queryset = Ticket.objects.filter(engineer_fk__isnull=True)


# # class AssignTicketApi(CustomViewSet):
# #     serializer_class = TicketSerializer
# #     queryset = Ticket.objects.filter(engineer_fk__isnull=False)


class EngineerTicketCountApi(ViewSet):
    def list(self, request):
        ticket = Ticket.objects.filter(ticket_engineer__engineer_fk=request.user)
        feedback = FeedBack.objects.filter(
            engineer=request.user, ticket__ticket_engineer__engineer_fk=request.user
        ).count()
        on_call = ticket.filter(ticket_status="on_call").count()
        waiting_for_spares = ticket.filter(ticket_status="waiting_for_spares").count()
        complete_and_close = ticket.filter(
            Q(ticket_status="close") | Q(ticket_status="complete")
        ).count()
        complete = ticket.filter(ticket_status="complete").count()
        close = ticket.filter(ticket_status="close").count()
        visit_and_schedule = ticket.filter(ticket_status="schedule").count()
        waiting = ticket.filter(ticket_status="waiting").count()

        response = {
            "on_call": on_call,
            "waiting_for_spares": waiting_for_spares,
            "complete_and_close": complete_and_close,
            "visit_and_schedule": visit_and_schedule,
            "waiting": waiting,
            "feedback": feedback,
            "complete": complete,
            "close": close,
            "status": status.HTTP_200_OK,
        }

        return Response(response, status=status.HTTP_200_OK)


class ClientTicketCountApi(ViewSet):
    # permission_classes = [IsClient]

    def list(self, request):
        total_tickets = Ticket.objects.all().count()
        ftc = Ticket.objects.filter(is_ftc_ticket=True).count()
        assigned = Ticket.objects.filter().exclude(assigned_by=None).count()
        print(assigned)
        unassigned = Ticket.objects.filter(assigned_by=None).count()
        on_call = Ticket.objects.filter(
            ticket_status="on_call"
        ).count()
        waiting_for_spares = Ticket.objects.filter(
            ticket_status="waiting_for_spares"
        ).count()
        complete_and_close = Ticket.objects.filter(
            Q(ticket_status="complete") | Q(ticket_status="close")
        ).count()
        visit_and_schedule = Ticket.objects.filter(
            ticket_status="schedule"
        ).count()
        waiting = Ticket.objects.filter(
            ticket_status="waiting"
        ).count()
        complete = Ticket.objects.filter(
            ticket_status="complete"
        ).count()
        close = Ticket.objects.filter(
            ticket_status="close"
        ).count()
        response = {
            "all_tickets": total_tickets,
            "ftc_tickets": ftc,
            "assigned_ticket": assigned,
            "unassigned_ticket": unassigned,
            "on_call": on_call,
            "waiting_for_spares": waiting_for_spares,
            "complete_and_close": complete_and_close,
            "visit_and_schedule": visit_and_schedule,
            "waiting": waiting,
            "complete": complete,
            "close": close,
            "status": status.HTTP_200_OK,
        }

        return Response(response, status=status.HTTP_200_OK)


# class AdminTicketCountApi(ViewSet):  # Visit ticket count not done
#     def list(self, request):
#         ticket = Ticket.objects.all()
#         all = ticket.count()
#         on_call = ticket.filter(ticket_status="on_call").count()
#         unassign_ticket = ticket.filter(ticket_status="pending").count()
#         assign_ticket = ticket.filter(ticket_status="waiting").count()
#         waiting_for_spares = ticket.filter(ticket_status="waiting_for_spares").count()
#         schedule = ticket.filter(ticket_status="schedule").count()
#         complete = ticket.filter(ticket_status="complete").count()
#         close = ticket.filter(ticket_status="close").count()
#
#         response = {
#             "all": all,
#             "on_call": on_call,
#             "unassign_ticket": unassign_ticket,
#             "assign_ticket": assign_ticket,
#             "waiting_for_spares": waiting_for_spares,
#             "schedule": schedule,
#             "complete": complete,
#             "close": close,
#             "status": status.HTTP_200_OK,
#         }
#
#         return Response(response, status=status.HTTP_200_OK)


class ProductApi(CustomViewSetFilter):
    serializer_class = CustomerWiseItemSerializer

    def get_queryset(self, request):
        search = request.GET.get("search")
        customer = request.GET.get("customer")
        if request.GET.get("search"):
            print("-----------------------")
            queryset = CustomerWiseItem.objects.filter(
                Q(item__ItemName__icontains=search)
                | Q(SerialNo__icontains=search)
                | Q(Item__ItemCode__icontains=search),
                customer_user=customer,
            )
        else:
            queryset = CustomerWiseItem.objects.filter(customer_user=customer)
            print(queryset)
        return queryset

    def retrieve(self, *args, **kwargs):
        response = {
            "data": self.get_serializer(
                CustomerWiseItem.objects.get(id=kwargs["pk"])
            ).data,
            "status": status.HTTP_200_OK,
        }
        return Response(response, status=status.HTTP_200_OK)

    # def create(self, request, *args, **kwargs):
    #     request.data["company"] = request.user.company.id
    #     return super().create(request, *args, **kwargs)


class ClientTicketApi(CustomViewSet):
    serializer_class = TicketDepthSerializer
    queryset = Ticket.objects.all()

    @swagger_auto_schema(
        manual_parameters=[type, filter],
        operation_description="description from swagger_auto_schema via method_decorator",
    )
    # serializer_class = TicketSerializer
    def list(self, request, *args, **kwargs):
        listModel = {
            1: Installation,
            2: Service,
            3: Spares,
            4: SalesInquiry,
            5: OtherService,
            6: Repair,
        }
        ticket_type = {
            1: "installation",
            2: "service",
            3: "spares",
            4: "sales_inquiry",
            5: "other_service",
            6: "repair",
        }
        ticket_type_str = {
            "installation": 1,
            "service": 2,
            "spares": 3,
            "sales_inquiry": 4,
            "other_service": 5,
            "repair": 6,
        }
        type = request.GET.get("type")
        search = request.GET.get("search")
        filter = request.GET.get("filter")
        kwargs = {}
        if filter:
            kwargs["ticket_type"] = ticket_type_str[filter]
        pending = Ticket.objects.filter(
            customer_fk=request.user, ticket_status="pending"
        ).count()
        in_progress = (
            Ticket.objects.filter(customer_fk=request.user)
            .exclude(
                Q(ticket_status="pending")
                | Q(ticket_status="complete")
                | Q(ticket_status="close")
            )
            .count()
        )
        complete = Ticket.objects.filter(
            customer_fk=request.user, ticket_status="complete"
        ).count()
        close = Ticket.objects.filter(
            customer_fk=request.user, ticket_status="close"
        ).count()

        if search:
            if type == "in_progress":
                ticket = (
                    Ticket.objects.filter(
                        Q(customer_wise_item__item__ItemName__icontains=search)
                        | Q(mobile_no_fk__phone__icontains=search)
                        | Q(mobile_no__icontains=search),
                        customer_fk=request.user,
                        **kwargs,
                    )
                    .exclude(
                        Q(ticket_status="pending")
                        | Q(ticket_status="complete")
                        | Q(ticket_status="close")
                    )
                    .order_by("-id")
                )
            else:
                ticket = Ticket.objects.filter(
                    Q(customer_wise_item__item__ItemName__icontains=search)
                    | Q(mobile_no_fk__phone__icontains=search)
                    | Q(mobile_no__icontains=search),
                    ticket_status=type,
                    customer_fk=request.user,
                    **kwargs,
                ).order_by("-id")

        else:
            if type == "in_progress":
                ticket = (
                    Ticket.objects.filter(customer_fk=request.user, **kwargs)
                    .exclude(
                        Q(ticket_status="pending")
                        | Q(ticket_status="complete")
                        | Q(ticket_status="close"),
                    )
                    .order_by("-id")
                )
            else:
                ticket = Ticket.objects.filter(
                    ticket_status=type, customer_fk=request.user, **kwargs
                ).order_by("-id")
        results = self.get_serializer(ticket, many=True).data
        for i in results:
            data = listModel[i["ticket_type"]].objects.filter(ticket_fk_id=i["id"])
            enginner = Engineer.objects.filter(ticket_fk__id=i["id"], is_assign=True)
            enginner = EnginnerSerializer(
                enginner, many=True, context={"request": request}
            ).data
            i[ticket_type[i["ticket_type"]]] = data.values()
            i["spare_detail"] = SpareDetail.objects.filter(
                spare__id=data.first().id
            ).values()
            # if i["ticket_type"] == 3:
            #     data = SparesSerializer(data,many=True).data
            #     i[ticket_type[i["ticket_type"]]][0] = SpareDetail.objects.filter(spare__id = i[ticket_type[i["ticket_type"]]][0]["id"])
            # else:
            #     i[ticket_type[i["ticket_type"]]] = data.values()

            i["engineer"] = enginner
            feedback = FeedBack.objects.filter(ticket__id=i["id"]).values()
            i["feedback"] = feedback

        response = {
            "ticket_detail": results,
            "count": [
                {
                    "pending": pending,
                },
                {
                    "in_progress": in_progress,
                },
                {
                    "complete": complete,
                },
                {
                    "close": close,
                },
            ],
        }
        return Response(response, status=status.HTTP_200_OK)


class TicketActionApi(ViewSet):
    permission_classes = [IsEngineer]

    def create(self, request):
        id = request.data.get("ticket")
        action = request.data.get("action")
        if action == "on_call":
            ticket = Ticket.objects.get(
                id=id,
            )
            ticket.call_count += 1
            if ticket.ticket_status == "waiting":
                ticket.ticket_status = "on_call"
            ticket.save()
            return Response(
                {"message": "you can call now", "status": status.HTTP_200_OK},
                status=status.HTTP_200_OK,
            )
        elif action == "schedule":
            date = request.data.get("date")
            ticket = Ticket.objects.get(id=id)
            ticket.ticket_status = "schedule"
            ticket.save()
            engineer = Engineer.objects.filter(
                engineer_fk=request.user, ticket_fk=id, is_assign=True
            ).first()
            if engineer.visit_date:
                engineer.visit_date.append(date)
            else:
                engineer.visit_date = [date]
            engineer.save()
            return Response(
                {"message": "visit scheduled", "status": status.HTTP_200_OK},
                status=status.HTTP_200_OK,
            )
        elif action == "decline":
            try:
                ticket = Ticket.objects.get(id=id)
                ticket.ticket_status = "pending"
                ticket.save()
                engineer = ticket.ticket_engineer.filter(
                    engineer_fk=request.user
                ).first()
                engineer.is_assign = False
                engineer.site_check_in = False
                engineer.save()
            except Exception:
                return Response(
                    {"message": "Ticket not declined"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            return Response(
                {"message": "Ticket has been Declined", "status": status.HTTP_200_OK},
                status=status.HTTP_200_OK,
            )
        elif action == "close":
            ticket = Ticket.objects.get(id=id)
            if ticket.ticket_type == 1 and not ticket.is_ftc_ticket:
                try:
                    ftc_ticket = FTCForm.objects.get(ticket=id).ftc_ticket
                    if ftc_ticket.ticket_status != "close":
                        return Response(
                            {"message": "please wait for close the FTC Ticket"},
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                except Exception:
                    pass
            print("before", ticket.ticket_status)
            if ticket.ticket_status == "complete":
                ticket.ticket_close_date = timezone.now().today()
                ticket.ticket_status = "close"
                print(ticket.ticket_status)
            elif ticket.ticket_status == "on_call":
                ticket.ticket_status = "complete"
            else:
                ticket.ticket_status = "complete"
            ticket.save()
            engineer = Engineer.objects.filter(
                ticket_fk=ticket, engineer_fk=request.user
            ).first()
            engineer.is_assign = False
            engineer.site_check_in = False
            engineer.save()
            return Response(
                {
                    "message": "Ticket has been Closed by Engineer",
                    "status": status.HTTP_200_OK,
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {
                "message": "something went wrong",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


# # class ScheduleApi(ViewSet):
# #     permission_classes = [IsEngineer]

# #     def create(self, request):
# #         id = request.data.get("id")
# #         date = request.data.get("date")
# #         ticket = Ticket.objects.get(id=id)
# #         ticket.ticket_status = "schedule"
# #         engineer = Engineer.objects.get(engineer_fk=request.user, ticket_fk=id)
# #         engineer.visit_date = date
# #         engineer.save()
# #         return Response(
# #             {"message": "visit scheduled", "status": status.HTTP_200_OK},
# #             status=status.HTTP_200_OK,
# #         )


# # this APi is for only web application or admin side


# class WebCustomerFormApi(ModelViewSet):
#     queryset = Ticket.objects.all()
#     serializer_class = TicketSerializer


# class WebTicketApi(ModelViewSet):
#     queryset = Ticket.objects.all()
#     serializer_class = TicketSerializer

#     def create(self, request, *args, **kwargs):
#         ticket_id = request.data.get("id")

#         ticket_type = Ticket.objects.filter(id=ticket_id).first().ticket_type
#         if ticket_type == 1:  # installation
#             serializer = InstallationSerializer(data=request.data)
#             if serializer.is_valid(raise_exception=True):
#                 serializer.save()
#             else:
#                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         elif ticket_type == 2:  # Service
#             serializer = ServiceSerializer(data=request.data)
#             if serializer.is_valid(raise_exception=True):
#                 serializer.save()
#             else:
#                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         elif ticket_type == 3:  # Spares
#             serializer = SparesSerializer(data=request.data)
#             if serializer.is_valid(raise_exception=True):
#                 serializer.save()
#             else:
#                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         elif ticket_type == 4:  # Sales_inquiry
#             serializer = SalesInquirySerializer(data=request.data)
#             if serializer.is_valid(raise_exception=True):
#                 serializer.save()
#             else:
#                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         elif ticket_type == 5:  # Others
#             serializer = OtherServiceSerializer(data=request.data)
#             if serializer.is_valid(raise_exception=True):
#                 serializer.save()
#             else:
#                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         else:  # Repair
#             serializer = RepairServiceSerializer(data=request.data)
#             print(serializer)
#             if serializer.is_valid(raise_exception=True):
#                 serializer.save()
#             else:
#                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         # if request.data.get("team_member"):
#         #     data = request.data["team_member"]
#         #     for i in data:
#         #         i["ticket_fk"] = ticket.id
#         #     serializer = TeamMemberSerializer(data=data, many=True)
#         #     if serializer.is_valid(raise_exception=True):
#         #         serializer.save()
#         if request.data.get("attachment"):
#             data = request.data["attachment"]
#             for i in data:
#                 i["ticket_fk"] = ticket_id
#             serializer = AttachmentSerializer(data=data, many=True)
#             if serializer.is_valid(raise_exception=True):
#                 serializer.save()
#         return Response(
#             {"message": "Ticket Created Successfully"}, status=status.HTTP_200_OK
#         )


# class WebCompanyProductItemApi(ViewSet):
#     @swagger_auto_schema(
#         manual_parameters=[id], operation_description="For web Product Listing"
#     )
#     def list(self, request):
#         id = request.GET.get("company")
#         product = CompanyProductItem.objects.filter(company__id=id)
#         # product = Product.objects.filter(user__email=email)
#         data = CompanyProductItemDepthSerializer(product, many=True).data
#         response = {"data": data, "status": status.HTTP_200_OK}
#         return Response(response, status=status.HTTP_200_OK)


# # class EngineerTicketApi(CustomViewSet):
# #     queryset = Ticket.objects.all()
# #     serializer_class = TicketSerializer

# #     # @swagger_auto_schema(
# #     #     request_body=TicketSerializer,
# #     #     operation_description="Ticket Create",
# #     # )
# #     def create(self, request):
# #         if request.user.user_role == 2:
# #             request.data["created_by_customer"] = True
# #             request.data["customer_fk"] = request.user.id

# #         serializer = TicketSerializer(data=request.data)
# #         if serializer.is_valid(raise_exception=True):
# #             # serializer.data.get("")
# #             ticket = serializer.save()
# #             request.data["ticket_fk"] = ticket.id
# #             ticket_type = ticket.ticket_type
# #         else:
# #             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# #         if request.user.user_role == 2:
# #             if request.data.get("address"):
# #                 data = request.data["address"]
# #                 data["user_fk"] = request.user.id
# #                 serializer = AddressSerializer(data=data)
# #                 if serializer.is_valid(raise_exception=True):
# #                     serializer.save()
# #                 else:
# #                     return Response(
# #                         serializer.errors, status=status.HTTP_400_BAD_REQUEST
# #                     )

# #         if ticket_type == 1:  # installation
# #             serializer = InstallationSerializer(data=request.data)
# #             if serializer.is_valid(raise_exception=True):
# #                 serializer.save()
# #             else:
# #                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# #         elif ticket_type == 2:  # Service
# #             serializer = ServiceSerializer(data=request.data)
# #             if serializer.is_valid(raise_exception=True):
# #                 serializer.save()
# #             else:
# #                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# #         elif ticket_type == 3:  # Spares
# #             serializer = SparesSerializer(data=request.data)
# #             if serializer.is_valid(raise_exception=True):
# #                 serializer.save()
# #             else:
# #                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# #         elif ticket_type == 4:  # Sales_inquiry
# #             serializer = SalesInquirySerializer(data=request.data)
# #             if serializer.is_valid(raise_exception=True):
# #                 serializer.save()
# #             else:
# #                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# #         else:  # Others
# #             serializer = OtherServiceSerializer(data=request.data)
# #             if serializer.is_valid(raise_exception=True):
# #                 serializer.save()
# #             else:
# #                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# #         # if request.data.get("team_member"):
# #         #     data = request.data["team_member"]
# #         #     for i in data:
# #         #         i["ticket_fk"] = ticket.id
# #         #     serializer = TeamMemberSerializer(data=data, many=True)
# #         #     if serializer.is_valid(raise_exception=True):
# #         #         serializer.save()
# #         if request.data.get("attachment"):
# #             data = request.data["attachment"]
# #             for i in data:
# #                 i["ticket_fk"] = ticket.id
# #             serializer = AttachmentSerializer(data=data, many=True)
# #             if serializer.is_valid(raise_exception=True):
# #                 serializer.save()
# #         return Response(
# #             {"message": "Ticket Created Successfully"}, status=status.HTTP_200_OK
# #         )


class EngineerTicketApi(CustomViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketDepthSerializer
    permission_classes = [IsEngineer | IsAdminUser]

    # permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        manual_parameters=[type, filter],
        operation_description="description from swagger_auto_schema via method_decorator",
    )
    # serializer_class = TicketSerializer
    def list(self, request, *args, **kwargs):
        listModel = {
            1: Installation,
            2: Service,
            3: Spares,
            4: SalesInquiry,
            5: OtherService,
            6: Repair,
        }
        ticket_type = {
            1: "installation",
            2: "service",
            3: "spares",
            4: "sales_inquiry",
            5: "other_service",
            6: "repair",
        }
        ticket_type_str = {
            "installation": 1,
            "service": 2,
            "spares": 3,
            "sales_inquiry": 4,
            "other_service": 5,
            "repair": 6,
        }
        type = request.GET.get("type")
        search = request.GET.get("search")
        filter = request.GET.get("filter")
        kwargs = {}
        if filter:
            kwargs["ticket_type"] = ticket_type_str[filter]
            if search:
                if type == "feedback":
                    ticket = Ticket.objects.filter(
                        Q(company_product_item__product__name__icontains=search)
                        | Q(mobile_no__phone__icontains=search)
                        | Q(customer_fk__full_name__icontains=search),
                        ticket_feedback__engineer=request.user,
                        **kwargs,
                    ).order_by("-id")
                else:
                    ticket = Ticket.objects.filter(
                        Q(customer_wise_item__item__ItemName__icontains=search)
                        | Q(mobile_no_fk__phone__icontains=search)
                        | Q(mobile_no__icontains=search)
                        | Q(customer_fk__CardName__icontains=search),
                        ticket_status=type,
                        ticket_engineer__engineer_fk=request.user,
                        **kwargs,
                    ).order_by("-id")
            else:
                if type == "feedback":
                    ticket = Ticket.objects.filter(
                        ticket_feedback__engineer=request.user, **kwargs
                    ).order_by("-id")

                else:
                    ticket = Ticket.objects.filter(
                        ticket_status=type,
                        ticket_engineer__engineer_fk=request.user,
                        **kwargs,
                    ).order_by("-id")
        else:
            if type == "feedback":
                ticket = Ticket.objects.filter(
                    ticket_feedback__engineer=request.user, **kwargs
                ).order_by("-id")

            else:
                ticket = Ticket.objects.filter(
                    ticket_status=type,
                    ticket_engineer__engineer_fk=request.user,
                    **kwargs,
                ).order_by("-id")

        results = self.get_serializer(ticket, many=True).data
        print("Result", results)

        for i in results:
            data = listModel[i["ticket_type"]].objects.filter(ticket_fk_id=i["id"])
            print("data: -===========>>>", data)
            enginner = Engineer.objects.filter(
                ticket_fk__id=i["id"], engineer_fk=request.user
            )
            enginner = EnginnerWithoutDepthSerializer(enginner, many=True).data
            i["installation"] = []
            i["service"] = []
            i["spares"] = []
            if i["ticket_type"] == 3:
                i["spare_detail"] = SpareDetail.objects.filter(
                    spare__id=data.first().id
                ).values()
            else:
                i["spare_detail"] = []
            i[ticket_type[i["ticket_type"]]] = data.values()
            if enginner:
                i["engineer"] = enginner
            else:
                i["engineer"] = []
            feedback = FeedBack.objects.filter(
                engineer=request.user, ticket__id=i["id"]
            ).values()
            i["feedback"] = feedback
            ftc = FTCForm.objects.filter(ftc_ticket__id=i["id"]).values()
            i["ftc"] = ftc
            print(i["ticket_type"])

            print("HEHEHEHHHHHHHHHHHH", LastStatus.objects.filter(ticket=i["id"]).exists())
            if LastStatus.objects.filter(ticket=i["id"]).exists():
                i["LastStatus"] = True
            else:
                i["LastStatus"] = False
            # if i["ticket_type"] == 1:
            #     item_stetus = CompanyTicketInstallationItemStatus.objects.filter(
            #         ticket=i["id"]
            #     )

            #     item_stetus = DepthCompanyTicketInstallationItemStatusSerializers(
            #         item_stetus, many=True
            #     ).data
            #     for j, item in enumerate(item_stetus):
            #         if len(item):
            #             i["company_product_item"]["item"][j][
            #                 "item_status"
            #             ] = item_stetus[j]["installation_problem_status"]
            #         else:
            #             i["company_product_item"]["item"][j]["item_status"] = []

            # response = {
            #     "ticket_detail": results,
            # }
            # return Response(response, status=status.HTTP_200_OK)

        response = {
            "ticket_detail": results,
        }
        return Response(response, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        listModel = {
            1: Installation,
            2: Service,
            3: Spares,
            4: SalesInquiry,
            5: OtherService,
            6: Repair,
        }
        query_type = {
            1: "installation",
            2: "service",
            3: "spares",
            4: "sales_inquiry",
            5: "other_service",
            6: "repair",
        }
        id = self.get_object().id
        data = self.get_serializer(self.get_object()).data
        # item = Item.objects.filter(product=self.get_object().product)
        # item = ItemDepthSerializer(item, many=True).data
        # data["product"]["items"] = item
        data["installation"] = []
        data["service"] = []
        data["spares"] = []
        dataa = listModel[self.get_object().ticket_type].objects.filter(ticket_fk_id=id)
        data[query_type[self.get_object().ticket_type]] = dataa.values()
        if self.get_object().ticket_type == 3:
            data["spare_detail"] = SpareDetail.objects.filter(
                spare__id=dataa.first().id
            ).values()
        else:
            data["spare_detail"] = []
        engineer = Engineer.objects.filter(ticket_fk__id=id, engineer_fk=request.user)
        engineer = EnginnerWithoutDepthSerializer(engineer, many=True).data

        data["engineer"] = engineer
        feedback = FeedBack.objects.filter(engineer=request.user, ticket__id=id).values()
        data["feedback"] = feedback
        ftc = FTCForm.objects.filter(ftc_ticket__id=id).values()

        data["ftc"] = ftc
        item_status = CompanyTicketInstallationItemStatus.objects.filter(
            ticket=data["id"]
        )
        item_status = DepthCompanyTicketInstallationItemStatusSerializers(
            item_status, many=True
        ).data
        step = 0
        print(len(item_status))
        print("len ------------->", len(data["customer_wise_item"]))

        for i in item_status:
            print("-------------hello-------------")
            print(data["customer_wise_item"])
            data["customer_wise_item"][step]["item_status"] = i[
                "installation_problem_status"
            ]
            step = step + 1
        for step in range(len(data["customer_wise_item"])):
            for i in item_status:
                if (
                        data["customer_wise_item"][step]["item"]["id"]
                        == i["installation_problem_status"]["id"]
                ):
                    data["customer_wise_item"][step]["item_status"] = i[
                        "installation_problem_status"
                    ]
        for i in data["customer_wise_item"]:
            if not i.get("item_status"):
                i["item_status"] = None

        # else:
        #     data["customer_wise_item"][0]["item_status"] = []

        response = {
            "data": data,
            "status": status.HTTP_200_OK,
        }

        return Response(response, status=status.HTTP_200_OK)


class LaststatusAPI(CustomViewSetFilter):
    serializer_class = LastStatusDepthSerializer

    def get_queryset(self, request):
        id = request.GET.get("id")
        return LastStatus.objects.filter(ticket__id=id).order_by("-id")

    @swagger_auto_schema(
        manual_parameters=[id],
        operation_description="description from swagger_auto_schema via method_decorator",
    )
    def create(self, request, *args, **kwargs):
        request.data["ticket"] = request.data.get("id")
        request.data["engineer"] = request.user.id

        serializer = LastStatusSerializer(
            data=request.data, context={"user": request.user}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = {
            "message": "Created Succesfully",
            "data": serializer.data,
            "status": status.HTTP_201_CREATED,
        }
        return Response(response, status=status.HTTP_201_CREATED)

    # def list(self, request):
    #     try:
    #         ticket_fk = request.data.get("id")
    #     except Exception:
    #         return Response(
    #             {"message": "ticket_fk field is mandatory"},
    #             status=status.HTTP_400_BAD_REQUEST,
    #         )
    #     last_status = LastStatus.objects.filter(ticket=ticket_fk)
    #     data = LastStatusSerializer(last_status, many=True).data
    #     response = {"data": data}
    #     return Response(response, status=status.HTTP_200_OK)


class FeedBackApi(CustomViewSetFilter):
    serializer_class = FeedBackSerializer

    def get_queryset(self, request):
        return FeedBack.objects.filter(engineer=request.user)

    def create(self, request, *args, **kwargs):
        request.data["client"] = request.user.id
        feedback = FeedBack.objects.filter(ticket=request.data.get("ticket")).first()
        if feedback:
            serializer = FeedBackSerializer(
                feedback, data=request.data, context={"user": request.user}
            )
        else:
            serializer = self.get_serializer(
                data=request.data, context={"user": request.user}
            )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        response = {
            "message": "Created Succesfully",
            "data": serializer.data,
            "status": status.HTTP_201_CREATED,
        }
        return Response(response, status=status.HTTP_201_CREATED, headers=headers)


# class ItemStatusChangeApi(ViewSet):
#     def create(self, request):
#         id = request.data.get("id")
#         item = Item.objects.get(id=id)
#         serializer = ItemSerializer(item, data=request.data, partial=True)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response(
#                 {
#                     "message": "Installation status has been updated",
#                     "status": status.HTTP_200_OK,
#                 },
#                 status=status.HTTP_200_OK,
#             )
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InstallationProblemStatusApi(CustomViewSetFilter):
    serializer_class = InstallationProblemStatusSerializer

    def get_queryset(self, request):
        return InstallationaProblemStatus.objects.all()

    def list(self, request, *args, **kwargs):
        print("------------------")
        results = self.get_serializer(self.get_queryset(request), many=True).data
        response = {"installation_status": results}
        return Response(response, status=status.HTTP_200_OK)


class RCAApi(CustomViewSet):
    queryset = RCA.objects.all()
    serializer_class = RCASerializer

    def create(self, request, *args, **kwargs):
        # RCADepartmentSerializer()
        return super().create(request, *args, **kwargs)


# class EngineerServiceEditApi(ModelViewSet):
#     serializer_class = ServiceSerializer

#     def create(self, request, *args, **kwargs):
#         try:
#             id = request.data.get("ticket")
#             service = Ticket.objects.filter(id=id).first().ticket_service
#         except Exception:
#             return Response(
#                 {"message": "ticket not found", "status": status.HTTP_200_OK},
#                 status=status.HTTP_200_OK,
#             )
#         serializer = ServiceSerializer(service, data=request.data, partial=True)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)


# # class DeclineTicketApi(ViewSet):
# #     def create(self, request, *args, **kwargs):
# #         id = request.data.get("ticket")
# #         try:
# #             ticket = Ticket.objects.get(id = id)
# #             ticket.ticket_status = "pending"
# #             ticket.save()
# #             engineer = ticket.ticket_engineer.filter(engineer_fk = request.user).first()
# #             engineer.is_assign = False
# #             engineer.save()
# #         except:
# #             return Response({"message":"Ticket not declined"},status=status.HTTP_400_BAD_REQUEST)
# #         return Response({"message":"Ticket has been Declined"},status=status.HTTP_200_OK)


class RCADepartmentApi(CustomViewSet):
    serializer_class = RCADepartmentSerializer
    queryset = RCADepartment.objects.all()


class RCACategoryApi(CustomViewSet):
    serializer_class = RCACategorySerializer
    queryset = RCACategory.objects.all()


class NotificationApi(CustomViewSetFilter):
    serializer_class = NotificationSeralizer

    def get_queryset(self, request):
        return Notification.objects.filter()

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


# # for checkin and checkout the engineer to the site
class SiteApi(ViewSet):
    def create(self, request):
        id = request.data.get("ticket")
        engineer = Engineer.objects.get(ticket_fk__id=id, is_assign=True)
        if engineer.site_check_in:
            request.data["site_check_in"] = False
            if engineer.check_out_timestamp:
                engineer.check_out_timestamp.append(timezone.now())
            else:
                engineer.check_out_timestamp = [timezone.now()]
            engineer.save()
            msg = "Engineer Check Out"
        else:
            if Engineer.objects.filter(
                    engineer_fk=request.user, site_check_in=True
            ).exists():
                return Response(
                    {"message": "You can't check in right now"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            request.data["site_check_in"] = True
            if engineer.check_in_timestamp:
                engineer.check_in_timestamp.append(timezone.now())
            else:
                engineer.check_in_timestamp = [timezone.now()]
            engineer.save()
            msg = "Engineer check In"
        serializer = EnginnerWithoutDepthSerializer(
            engineer, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": msg, "data": serializer.data, "status": status.HTTP_200_OK},
            status=status.HTTP_200_OK,
        )


class EngineerOnSiteAPI(ViewSet):
    def list(self, request):
        engineer = Engineer.objects.filter(engineer_fk=request.user, site_check_in=True)
        data = []
        for i in engineer:
            data.append(
                {
                    "ticket": i.ticket_fk.id,
                    "ticket_type": i.ticket_fk.ticket_type,
                    "site_check_in": i.site_check_in,
                }
            )
        return Response(
            {"current_ticket": data, "status": status.HTTP_200_OK},
            status=status.HTTP_200_OK,
        )


class EngineerAssignApi(ModelViewSet):
    serializer_class = EnginnerWithoutDepthSerializer

    def create(self, request):
        if (
                not CustomerUser.objects.get(id=request.data.get("engineer_fk")).user_role
                    == 3
        ):
            return Response(
                {
                    "message": "person must be engineer",
                    "status": status.HTTP_400_BAD_REQUEST,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        ticket = Ticket.objects.get(id=request.data["ticket_fk"])
        if ticket.ticket_type in [4, 5, 6]:
            return Response(
                {"message": "Ticket Can't Assign to this Ticket"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if ticket.ticket_status == "pending":
            serializer = EnginnerWithoutDepthSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            ticket.ticket_status = "waiting"
            ticket.assigned_by = request.user
            ticket.save()
            return Response(
                {"message": "Ticket has been Assigned", "status": status.HTTP_200_OK},
                status=status.HTTP_200_OK,
            )
        return Response(
            {
                "message": "Ticket already Assigned",
                "status": status.HTTP_400_BAD_REQUEST,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    def list(self, request, *args, **kwargs):
        queryset = Ticket.objects.filter(
            Q(assigned_by__isnull=True) | Q(assigned_by=request.user)
        )
        data = TicketSerializer(queryset, many=True).data
        return Response(
            {"ticket_details": data, "status": status.HTTP_200_OK},
            status=status.HTTP_200_OK,
        )


class ServiceReportApi(CustomViewSetFilter):
    serializer_class = ServiceReportSerializer

    def get_queryset(self, request):
        customer = request.GET.get("customer")
        product = request.GET.get("product")
        self.response_tag = "service_report"
        return ServiceReport.objects.filter(
            ticket_fk__customer_fk__id=customer,
            ticket_fk__company_product_item__id=product,
        )

    def create(self, request, *args, **kwargs):
        service_report_serializer = ServiceReportSerializer(data=request.data)
        service_report_serializer.is_valid(raise_exception=True)
        service_report = service_report_serializer.save()
        data = request.data["service_report_part"]
        for i in range(len(data)):
            data[i]["service_report"] = service_report.id
        serializer = ServiceReportPartSerializer(data=data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        if service_report.ticket_fk.is_guest:
            mobile = service_report.ticket_fk.mobile_no
        else:
            mobile = service_report.ticket_fk.mobile_no_fk.phone
        session_data = SessionStore()
        # session_data["OTP"] = send_otp_via_phone(mobile)
        session_data["OTP"] = os.getenv("OTP")
        session_data.set_expiry(3000)
        session_data["service_report"] = service_report.id
        session_data.create()

        return Response(
            {
                "message": "Service Report Created",
                "data": service_report_serializer.data,
                "session_data": session_data.session_key,
                "status": status.HTTP_200_OK,
            },
            status=status.HTTP_200_OK,
        )


class ServiceReportCustomerVerifyApi(ViewSet):
    def create(self, request):
        session_key = request.data.get("session_key")
        otp = request.data.get("otp")
        json_data = {}
        try:
            session_data = SessionStore(session_key=session_key)
            session_otp = session_data["OTP"]
            service_report = session_data["service_report"]
        except Exception:
            return Response(
                {"message": "Session Key is expired"}, status=status.HTTP_400_BAD_REQUEST
            )
        if otp != session_otp:
            return Response(
                {"message": "OTP is not match"}, status=status.HTTP_400_BAD_REQUEST
            )
        service_report = ServiceReport.objects.get(id=service_report)
        service_report.verified_by_customer = True
        service_report.save()
        ticket = service_report.ticket_fk
        json_data["server_path"] = request.META.get("HTTP_HOST")
        json_data["ticket_number"] = ticket.ticket_number
        json_data["customer_name"] = ticket.customer_fk.CardName
        json_data["customer_mobile_num"] = ticket.mobile_no_fk
        json_data["enginer_name"] = ticket.ticket_engineer.first().engineer_fk.CardName
        json_data["enginer_email"] = ticket.ticket_engineer.first().engineer_fk.E_Mail
        json_data["enginer_number"] = ticket.ticket_engineer.first().engineer_fk.mobile_number
        service_report_part = ServiceReportPart.objects.filter(
            service_report=service_report
        )
        service_report_part = ServiceReportPartDepthSerializer(
            service_report_part, many=True
        )
        service_report_serializer = ServiceReportDepthSerializer(service_report)
        service_report_data = service_report_serializer.data
        if service_report_data["service_chargeable"] == True:
            json_data["service_chargeable_flag"] = "Yes"
        else:
            json_data["service_chargeable_flag"] = "No"


        json_data["service_report"] = service_report_data
        json_data["service_report_parts"] = service_report_part.data
        pdf = render_to_pdf(
            "service_report.html",
            json_data,
        )
        email = EmailMessage(
            "NuVu Conair Service report ",
            "hello",
            from_email=os.getenv("EMAIL_HOST_USER"),
            # to=list(
            #     service_report.ticket_fk.customer_fk.email_set.all().values_list(
            #         "E_Mail", flat=True
            #     )
            # ),
            # to = ["kinjal@conairgroup.com"]
            to=["himanishvyas.tecblic@gmail.com", "kinjal@conairgroup.com"]

        )
        email.attach("service_report.pdf", pdf.getvalue(), "application/pdf")
        email.send()
        # return pdf
        return Response(
            {"message": "Service report has been verified by customer"},
            status=status.HTTP_200_OK,
        )


class ResendOTPServiceReportApi(ViewSet):
    def create(self, request):
        service_report = request.data.get("service_report")
        service_report = ServiceReport.objects.filter(id=service_report).first()
        if not service_report:
            return Response(
                {"message": "service report not found"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        print(service_report.__dict__)
        if service_report.ticket_fk.is_guest:
            mobile = service_report.ticket_fk.mobile_no
        else:
            mobile = service_report.ticket_fk.mobile_no_fk.phone
        session_data = SessionStore()
        # session_data["OTP"] = send_otp_via_phone(mobile)
        session_data["OTP"] = os.getenv("OTP")
        session_data["service_report"] = service_report.id
        session_data.create()

        print("here")
        return Response(
            {
                "message": "OTP Sent Successfully",
                "session_data": session_data.session_key,
                "status": status.HTTP_200_OK,
            },
            status=status.HTTP_200_OK,
        )


class TicketCustomerActionApi(ViewSet):
    def create(self, request):
        id = request.data.get("ticket")
        action = request.data.get("action")
        if action == "re_open":
            try:
                ticket = Ticket.objects.get(id=id, ticket_status="complete")
            except Exception:
                return Response(
                    {"message": "ticket not valid for re-open"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            ticket.ticket_status = "pending"
            ticket.save()
            return Response(
                {"message": "Ticket re-open Successfully"}, status=status.HTTP_200_OK
            )
        elif action == "close":
            try:
                ticket = Ticket.objects.get(id=id)
            except Exception:
                return Response(
                    {"message": "ticket not Found"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if ticket.ticket_status in [4, 5, 6]:
                if ticket.ticket_status == "complete":
                    ticket.ticket_status = "close"
                    ticket.ticket_close_date = timezone.now().today()
                elif ticket.ticket_status == "pending":
                    ticket.ticket_status = "complete"
                else:
                    ticket.ticket_status = "complete"
                    engineer = Engineer.objects.filter(
                        ticket_fk__id=ticket.id, is_assign=True
                    ).first()
                    engineer.is_assign = False
                    engineer.save()
                ticket.save()
            else:
                if ticket.ticket_status == "complete":
                    engineer = Engineer.objects.filter(
                        ticket_fk__id=ticket.id, is_assign=False
                    ).first()
                    # if engineer is None:
                    #         return Response(
                    #         {"message": "Ticket Can't be closed"}, status=status.HTTP_400_BAD_REQUEST
                    #         )
                    engineer.is_assign = False
                    ticket.ticket_status = "close"
                    engineer.save()
                    ticket.save()
            return Response(
                {"message": "Ticket has been closed"}, status=status.HTTP_200_OK
            )
        return Response({"message": "action not match"}, status=status.HTTP_200_OK)


class ItemQRApi(CustomViewSet):
    serializer_class = ItemSerializer

    queryset = Item.objects.all()

    def retrieve(self, request, *args, **kwargs):
        data = self.get_serializer(self.get_object()).data
        document = Document.objects.filter(item=self.get_object())
        data["document"] = DocumentProductSerializer(
            document, many=True, context={"request": request}
        ).data
        response = {
            "product": data,
            "status": status.HTTP_200_OK,
        }
        return Response(response, status=status.HTTP_200_OK)


# class DocumentApi(CustomViewSetFilter):
#     serializer_class = DocumentSerializer
#     queryset = Document.objects.all()


class FAQApi(CustomViewSetFilter):
    serializer_class = FAQSerializer

    # queryset = FAQ.objects.all()
    def get_queryset(self, request):
        self.response_tag = "faq"
        faq_type = request.GET.get("faq_type")
        return FAQ.objects.filter(faq_type=faq_type)


class FTCFormApi(ViewSet):
    def create(self, request):
        action = request.data.get("action")
        if action == "reject":
            ticket = Ticket.objects.get(id=request.data.get("ticket"))
            if ticket.ticket_type != "installation":
                return Response(
                    {"message": "only installation ticket required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if ticket.is_guest:
                request.data["mobile_no"] = ticket.mobile_no
                request.data["address"] = ticket.address
            else:
                request.data["mobile_no_fk"] = ticket.mobile_no_fk.id
                request.data["address_fk"] = ticket.address_fk.id
            request.data["ticket_type"] = 1
            request.data["customer_wise_item"] = list(
                ticket.customer_wise_item.all().values_list("id", flat=True)
            )
            request.data["is_ftc_ticket"] = True
            request.data["is_guest"] = ticket.is_guest
            request.data["customer_fk"] = ticket.customer_fk.id
            request.data["assigned_by"] = ticket.assigned_by.id
            installation = Installation.objects.get(ticket_fk=ticket)
            serializer = TicketSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            ticket = serializer.save()
            Installation.objects.create(
                ticket_fk=ticket,
                work_order_no=installation.work_order_no,
                packing_slip_no=installation.packing_slip_no,
                receive_in_good_condition=installation.receive_in_good_condition,
                equipement_brief=installation.equipement_brief,
                product_trial_readliness_date=installation.product_trial_readliness_date,
                pending=installation.pending,
                ready=installation.ready,
                during_enginner_visit=installation.during_enginner_visit,
                not_understood_list=installation.not_understood_list,
                further_guideliness_needed=installation.further_guideliness_needed,
            )
            request.data["ftc_ticket"] = ticket.id
            serializer = FTCFormSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                {"message": "FTC Ticket has been Raised"}, status=status.HTTP_201_CREATED
            )

        else:
            serializer = FTCFormSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "FTC form Submited"}, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        ticket = FTCForm.objects.get(ftc_ticket=request.data["ticket"])
        serializer = FTCFormSerializer(ticket, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = {
            "message": "Updated Succesfully",
            "data": serializer.data,
            "status": status.HTTP_200_OK,
        }
        return Response(response, status=status.HTTP_200_OK)


class ItemProblemTypeApi(CustomViewSetFilter):
    serializer_class = ItemProblemTypeSerializer

    def get_queryset(self, request):
        self.response_tag = "item_problem_type"
        item = request.GET.get("item")
        return ItemProblemType.objects.filter(item=item)


class ItemWiseSpare(CustomViewSetFilter):
    serializer_class = ItemSpareSerializer
    authentication_classes = []

    def get_queryset(self, request):
        search = request.GET.get("search")
        if search:
            queryset = ItemSpare.objects.filter(spare_name__icontains=search)
            return queryset
        else:
            # item = request.GET.get("item")
            self.response_tag = "item"
            queryset = ItemSpare.objects.all()
        return queryset


class TicketListApi(CustomViewSetFilter):
    def get_queryset(self):
        return Ticket.objects.all()

    serializer_class = TicketDepthSerializer

    def list(self, request):
        # filter = request.GET.get("filter")

        ticket_type_str = {
            "installation": 1,
            "service": 2,
            "spares": 3,
            "sales_inquiry": 4,
            "other_service": 5,
            "repair": 6,
        }
        q_query = Q()
        # type = request.GET.get("type")
        # search = request.GET.get("search")
        type = request.GET.get("type")
        search = request.GET.get("search")
        filter = request.GET.get("filter")
        kwargs = {}
        user_role = request.user.user_role
        if user_role == 2:
            q_query = Q(customer_fk=request.user)
        if user_role == 5:
            q_query = Q(ticket_spares__hq_user_fk__isnull=True) | Q(
                ticket_spares__hq_user_fk=request.user
            )
            kwargs["ticket_type"] = 3
        if user_role == 9:
            q_query = Q(ticket_spares__region_co_user_fk__isnull=True) | Q(
                ticket_spares__region_co_user_fk=request.user
            )
            kwargs["ticket_type"] = 3
            kwargs["ticket_spares__is_hq_verified"] = True
        if user_role == 19:
            kwargs["ticket_type"] = 3
            kwargs["ticket_spares__is_hq_verified"] = True
            kwargs["ticket_spares__is_region_cordinator_varified"] = True
            q_query = Q(ticket_spares__store_user_fk__isnull=True) | Q(
                ticket_spares__store_user_fk=request.user
            )
        if user_role == 20:
            q_query = Q(ticket_spares__production_user_fk__isnull=True) | Q(
                ticket_spares__production_user_fk=request.user
            )
            kwargs["ticket_type"] = 3
            kwargs["ticket_spares__is_hq_verified"] = True
            kwargs["ticket_spares__is_region_cordinator_varified"] = True
            kwargs["ticket_spares__sparedetail__spare_status__in"] = [
                "gathering_for_assembly",
                "over_to_assembly",
                "assembling",
                "testing",
                "production_scheduling",
            ]
        if user_role == 21:
            q_query = Q(ticket_spares__purchase_user_fk__isnull=True) | Q(
                ticket_spares__purchase_user_fk=request.user
            )
            kwargs["ticket_type"] = 3
            kwargs["ticket_spares__is_hq_verified"] = True
            kwargs["ticket_spares__is_region_cordinator_varified"] = True
            kwargs["ticket_spares__sparedetail__spare_status__in"] = [
                "purchase_scheduling",
                "sourcing",
                "ordered",
                "shortage",
            ]

        if user_role == 10:
            q_query = Q(ticket_spares__dispacher_user_fk__isnull=True) | Q(
                ticket_spares__dispacher_user_fk=request.user
            )

            kwargs["ticket_type"] = 3
        if user_role == 27:
            q_query = Q(ticket_spares__logistic_user_fk__isnull=True) | Q(
                ticket_spares__logistic_user_fk=request.user
            )
            kwargs["ticket_type"] = 3
            kwargs["ticket_spares__is_hq_verified"] = True
            kwargs["ticket_spares__is_region_cordinator_varified"] = True
            kwargs["ticket_spares__is_store_updator_verified"] = True

        if type:
            kwargs["ticket_type"] = ticket_type_str[type]
        if request.GET.get("filter"):
            if filter == "assign":
                if user_role == 1:
                    kwargs["assigned_by"] = request.user
                elif user_role == 5:
                    kwargs["ticket_spares__is_hq_verified"] = True
                elif user_role == 9:
                    kwargs["ticket_spares__is_region_cordinator_varified"] = True
                elif user_role == 19:
                    kwargs["ticket_spares__sparedetail__spare_status__isnull"] = False
                    # kwargs["ticket_spares__is_store_updator_verified"] = True

                if search:
                    queryset = (
                        Ticket.objects.filter(
                            q_query
                            | Q(company_product_item__product__name__icontains=search)
                            | Q(mobile_no__phone__icontains=search)
                            | Q(customer_fk__full_name__icontains=search),
                            **kwargs,
                        )
                        .distinct()
                        .order_by("-id")
                    )
                    print("queryset: with search ----- >>", queryset)
                else:
                    queryset = (
                        Ticket.objects.filter(q_query, **kwargs)
                        # .distinct()
                        .order_by("-id")
                    )

                    print("queryset: without search", queryset.count())
                    print("queryset: without search", queryset)

            elif filter == "unassign":
                if user_role == 1:
                    kwargs["assigned_by__isnull"] = True
                elif user_role == 5:
                    kwargs["ticket_spares__is_hq_verified"] = False
                elif user_role == 9:
                    kwargs["ticket_spares__is_region_cordinator_varified"] = False
                elif user_role == 19:
                    kwargs["ticket_spares__sparedetail__spare_status__isnull"] = True
                    # kwargs["ticket_spares__is_store_updator_verified"] = False
                if search:
                    queryset = (
                        Ticket.objects.filter(
                            q_query
                            | Q(company_product_item__product__name__icontains=search)
                            | Q(mobile_no__phone__icontains=search)
                            | Q(customer_fk__full_name__icontains=search),
                            **kwargs,
                        )
                        .distinct()
                        .order_by("-id")
                    )
                    print("queryset: with search ----- >>", queryset)
                else:
                    queryset = (
                        Ticket.objects.filter(q_query, **kwargs)
                        .distinct()
                        .order_by("-id")
                    )
                    print("queryset: without search", queryset)

            elif filter == "on_call":
                if user_role == 1:
                    kwargs["assigned_by__isnull"] = True
                elif user_role == 5:
                    kwargs["ticket_spares__is_hq_verified"] = False
                elif user_role == 9:
                    kwargs["ticket_spares__is_region_cordinator_varified"] = False
                elif user_role == 19:
                    kwargs["ticket_spares__sparedetail__spare_status__isnull"] = True
                    # kwargs["ticket_spares__is_store_updator_verified"] = False
                if search:
                    queryset = (
                        Ticket.objects.filter(
                            q_query
                            | Q(company_product_item__product__name__icontains=search)
                            | Q(mobile_no__phone__icontains=search)
                            | Q(customer_fk__full_name__icontains=search),
                            ticket_status="on_call",
                            **kwargs,
                        )
                        .distinct()
                        .order_by("-id")
                    )
                else:
                    queryset = (
                        Ticket.objects.filter(q_query, ticket_status="on_call", **kwargs)
                        .distinct()
                        .order_by("-id")
                    )
                    print("queryset: without search", queryset)


            elif filter == "pending":
                if user_role == 1:
                    kwargs["assigned_by__isnull"] = True
                elif user_role == 5:
                    kwargs["ticket_spares__is_hq_verified"] = False
                elif user_role == 9:
                    kwargs["ticket_spares__is_region_cordinator_varified"] = False
                elif user_role == 19:
                    kwargs["ticket_spares__sparedetail__spare_status__isnull"] = True
                    # kwargs["ticket_spares__is_store_updator_verified"] = False
                if search:
                    queryset = (
                        Ticket.objects.filter(
                            q_query
                            | Q(company_product_item__product__name__icontains=search)
                            | Q(mobile_no__phone__icontains=search)
                            | Q(customer_fk__full_name__icontains=search),
                            ticket_status__in=["pending", "on_call", "waiting_for_spares", "schedule"],
                            **kwargs,
                        )
                        .distinct()
                        .order_by("-id")
                    )
                else:
                    queryset = (
                        Ticket.objects.filter(q_query, ticket_status__in=["pending", "on_call", "waiting_for_spares",
                                                                          "schedule"], **kwargs)
                        .distinct()
                        .order_by("-id")
                    )
                    print("queryset: without search", queryset)

            elif filter == "ftc":
                if search:
                    queryset = (
                        Ticket.objects.filter(
                            q_query
                            | Q(company_product_item__product__name__icontains=search)
                            | Q(mobile_no__phone__icontains=search)
                            | Q(customer_fk__full_name__icontains=search),
                            is_ftc_ticket=True,
                            **kwargs,
                        )
                        .distinct()
                        .order_by("-id")
                    )
                    print("queryset: with search ----- >>", queryset)
                else:
                    queryset = (
                        Ticket.objects.filter(q_query, is_ftc_ticket=True, **kwargs)
                        .distinct()
                        .order_by("-id")
                    )
                    print("queryset: without search", queryset)

            elif filter == "close":
                if search:
                    queryset = (
                        Ticket.objects.filter(
                            q_query
                            | Q(company_product_item__product__name__icontains=search)
                            | Q(mobile_no__phone__icontains=search)
                            | Q(customer_fk__full_name__icontains=search),
                            ticket_status="close",
                            **kwargs,
                        )
                        .distinct()
                        .order_by("-id")
                    )
                    print("queryset: with search ----- >>", queryset)
                else:
                    queryset = (
                        Ticket.objects.filter(q_query, ticket_status="close", **kwargs)
                        .distinct()
                        .order_by("-id")
                    )
                    print("queryset: without search", queryset)

            elif filter == "waiting_for_spares":
                if user_role == 1:
                    kwargs["assigned_by__isnull"] = True
                elif user_role == 5:
                    kwargs["ticket_spares__is_hq_verified"] = False
                elif user_role == 9:
                    kwargs["ticket_spares__is_region_cordinator_varified"] = False
                elif user_role == 19:
                    kwargs["ticket_spares__sparedetail__spare_status__isnull"] = True
                    # kwargs["ticket_spares__is_store_updator_verified"] = False
                if search:
                    queryset = (
                        Ticket.objects.filter(
                            q_query
                            | Q(company_product_item__product__name__icontains=search)
                            | Q(mobile_no__phone__icontains=search)
                            | Q(customer_fk__full_name__icontains=search),
                            ticket_status="waiting_for_spares",
                            **kwargs
                        )
                        .distinct()
                        .order_by("-id")
                    )
                else:
                    queryset = (
                        Ticket.objects.filter(q_query, ticket_status="waiting_for_spares", **kwargs)
                        .distinct()
                        .order_by("-id")
                    )
                    print("queryset: without search", queryset)

            elif filter == "visit_and_schedule":
                if user_role == 1:
                    kwargs["assigned_by__isnull"] = True
                elif user_role == 5:
                    kwargs["ticket_spares__is_hq_verified"] = False
                elif user_role == 9:
                    kwargs["ticket_spares__is_region_cordinator_varified"] = False
                elif user_role == 19:
                    kwargs["ticket_spares__sparedetail__spare_status__isnull"] = True
                    # kwargs["ticket_spares__is_store_updator_verified"] = False
                if search:
                    queryset = (
                        Ticket.objects.filter(
                            q_query
                            | Q(company_product_item__product__name__icontains=search)
                            | Q(mobile_no__phone__icontains=search)
                            | Q(customer_fk__full_name__icontains=search),
                            ticket_status="visit_and_schedule",
                            **kwargs
                        )
                        .distinct()
                        .order_by("-id")
                    )
                else:
                    queryset = (
                        Ticket.objects.filter(q_query, ticket_status="visit_and_schedule", **kwargs)
                        .distinct()
                        .order_by("-id")
                    )
                    print("queryset: without search", queryset)
            elif filter == "complete":
                if user_role == 1:
                    kwargs["assigned_by__isnull"] = True
                elif user_role == 5:
                    kwargs["ticket_spares__is_hq_verified"] = False
                elif user_role == 9:
                    kwargs["ticket_spares__is_region_cordinator_varified"] = False
                elif user_role == 19:
                    kwargs["ticket_spares__sparedetail__spare_status__isnull"] = True
                    # kwargs["ticket_spares__is_store_updator_verified"] = False
                if search:
                    queryset = (
                        Ticket.objects.filter(
                            q_query
                            | Q(company_product_item__product__name__icontains=search)
                            | Q(mobile_no__phone__icontains=search)
                            | Q(customer_fk__full_name__icontains=search),
                            ticket_status="complete",
                            **kwargs,
                        )
                        .distinct()
                        .order_by("-id")
                    )
                else:
                    queryset = (
                        Ticket.objects.filter(q_query, ticket_status="complete", **kwargs)
                        .distinct()
                        .order_by("-id")
                    )
                    print("queryset: without search", queryset)

            else:
                queryset = (
                    Ticket.objects.filter(q_query, **kwargs).distinct().order_by("-id")
                )
        else:
            queryset = (
                Ticket.objects.filter(q_query, **kwargs).distinct().order_by("-id")
            )

        results = self.get_serializer(queryset, many=True).data
        for i in results:
            enginner = Engineer.objects.filter(ticket_fk__id=i["id"], is_assign=True)
            enginner_name = EnginnerSerializer(
                enginner, many=True, context={"request": request}
            ).data

            i["enginner"] = enginner_name

            if i["ticket_type"] == 1:
                ticket_dec = Installation.objects.get(
                    ticket_fk__id=i["id"]
                ).equipement_brief
                i["ticket_description"] = ticket_dec

            elif i["ticket_type"] == 2:
                ticket_dec = Service.objects.get(ticket_fk__id=i["id"]).problem_brief
                i["ticket_description"] = ticket_dec

            elif i["ticket_type"] == 3:
                # spare_details = Spares.objects.filter(ticket_fk__id=i["id"]).values()
                spare_details = Spares.objects.filter(ticket_fk__id=i["id"])
                spare = SparesDepthSerializer(
                    spare_details, many=True, context={"request": request}
                ).data
                i["spares"] = spare
                i["ticket_description"] = ""

            elif i["ticket_type"] == 4:
                ticket_dec = SalesInquiry.objects.get(
                    ticket_fk__id=i["id"]
                ).inquiry_brief
                i["ticket_description"] = ticket_dec

            elif i["ticket_type"] == 5:
                ticket_dec = OtherService.objects.get(ticket_fk__id=i["id"]).quary_brief
                i["ticket_description"] = ticket_dec

            else:
                i["ticket_description"] = ""

            ticket = Ticket.objects.get(
                id=i["id"]
            )
            if ticket.ticket_close_date:
                installation_ticket_date = ticket.ticket_close_date
            else:
                installation_ticket_date = ticket.raise_date
            i["installation_date"] = installation_ticket_date

        response = {
            "ticket_detail": results,
        }
        return Response(response)

    def retrieve(self, request, *args, **kwargs):
        listModel = {
            1: Installation,
            2: Service,
            3: Spares,
            4: SalesInquiry,
            5: OtherService,
            6: Repair,
        }
        query_type = {
            1: "installation",
            2: "service",
            3: "spares",
            4: "sales_inquiry",
            5: "other_service",
            6: "repair",
        }
        id = self.get_object().id
        print("id: ", id)
        data = self.get_serializer(self.get_object()).data
        print("data: ", data)
        # item = Item.objects.filter(product=self.get_object().product)
        # item = ItemDepthSerializer(item, many=True).data
        # data["product"]["items"] = item
        data["installation"] = []
        data["service"] = []
        data["spares"] = []
        dataa = listModel[self.get_object().ticket_type].objects.filter(ticket_fk_id=id)
        data[query_type[self.get_object().ticket_type]] = dataa.values()
        filter = {}
        try:
            if self.get_object().ticket_type == 3:
                if request.user.user_role == 20:
                    filter["spare_status__in"] = [
                        "gathering_for_assembly",
                        "over_to_assembly",
                        "assembling",
                        "testing",
                        "production_scheduling",
                    ]
                elif request.user.user_role == 21:
                    filter["spare_status__in"] = [
                        "purchase_scheduling",
                        "sourcing",
                        "ordered",
                        "shortage",
                    ]
                data["spare_detail"] = SpareDetail.objects.filter(
                    spare__id=dataa.first().id, **filter
                ).values()
                print("i am here--->", data["spare_detail"])
                data["spare_box"] = SpareBox.objects.filter(
                    spare__id=dataa.first().id
                ).values()
            else:
                data["spare_detail"] = []
                data["spare_box"] = []
        except Exception:
            return Response(
                {"message": "spare object not found"}, status=status.HTTP_400_BAD_REQUEST
            )
        print("data----------->>", data)
        enginner = Engineer.objects.filter(ticket_fk__id=data["id"], is_assign=True)
        print(f"HAHA ENGINEER ONLY {enginner}")
        enginner_name = EnginnerSerializer(
            enginner, many=True, context={"request": request}
        ).data
        print("enginner_name: from ticket list", enginner_name)

        data["engineer"] = enginner_name
        spare_details = Spares.objects.filter(ticket_fk__id=data["id"])
        spare = SparesDepthSerializer(
            spare_details, many=True, context={"request": request}
        ).data
        data["spares"] = spare
        print(data)
        response = {
            "ticket_detail": data,
        }
        return Response(response)

        # engineer = Engineer.objects.filter(ticket_fk__id=id, engineer_fk=request.user)
        # engineer = EnginnerWithoutDepthSerializer(engineer, many=True).data

        # data["engineer"] = engineer
        # feedback = FeedBack.objects.filter(engineer=request.user, ticket__id=id).values()
        # data["feedback"] = feedback
        # ftc = FTCForm.objects.filter(ftc_ticket__id=id).values()

        # data["ftc"] = ftc
        # item_stetus = CompanyTicketInstallationItemStatus.objects.filter(
        #     ticket=data["id"]
        # )
        # print("item_stetus: ", item_stetus)
        # item_stetus = DepthCompanyTicketInstallationItemStatusSerializers(
        #     item_stetus, many=True
        # ).data
        # if len(item_stetus):
        #     data["company_product_item"]["item"][0]["item_status"] = item_stetus[0][
        #         "installation_problem_status"
        #     ]
        # else:
        #     data["company_product_item"]["item"][0]["item_status"] = []

        # response = {
        #     "data": data,
        #     "status": status.HTTP_200_OK,
        # }

        return Response(response, status=status.HTTP_200_OK)

        # if search:
        #         ticket = Ticket.objects.filter(
        #             Q(company_product_item__product__name__icontains=search)
        #             | Q(mobile_no__phone__icontains=search)
        #             | Q(customer_fk__full_name__icontains=search),
        #             # ticket_engineer__engineer_fk=request.user,
        #             **kwargs,
        #         )
        #         print('ticket: in search', ticket)
        # else:
        #         ticket = Ticket.objects.filter(
        #             **kwargs,
        #             # ticket_engineer__engineer_fk=request.user,
        #         )
        #         print('ticket: ', ticket)

        # results = self.get_serializer(ticket, many=True).data
        # print("Result", results)
        # for i in results:
        #     data = listModel[i["ticket_type"]].objects.filter(ticket_fk_id=i["id"])
        #     print('data: ===========>>>', data)


class InstallationItemStatusChangeApi(CustomViewSet):
    serializer_class = TicketInstallationItemStatusSerializer
    queryset = CompanyTicketInstallationItemStatus.objects.all()

    def create(self, request, *args, **kwargs):
        data = request.data
        print(data)
        ticket = Ticket.objects.get(id=request.data["ticket"])
        if ticket.ticket_type == 1:
            id = CompanyTicketInstallationItemStatus.objects.filter(
                ticket=data["ticket"], customer_wise_item=data["customer_wise_item"]
            )
            print("id:---------------", id)

            if id.exists():
                # id = TicketInstallationItemStatus.objects.filter(
                #     ticket=data["ticket"], item=data["item"]
                # )[0].id
                # item = TicketInstallationItemStatus.objects.get(id=id)
                serializer = TicketInstallationItemStatusSerializer(
                    id.first(), data=request.data, partial=True
                )
                if serializer.is_valid():
                    serializer.save()
                    data = serializer.data
                    return Response(
                        {
                            "message": "Installation status has been updated",
                            "data": data,
                            "status": status.HTTP_200_OK,
                        },
                        status=status.HTTP_200_OK,
                    )
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            else:
                serializer = self.get_serializer(
                    data=request.data, context={"user": request.user}
                )
                if serializer.is_valid():
                    serializer.save()
                    headers = self.get_success_headers(serializer.data)
                    response = {
                        "message": "Created Succesfully",
                        "data": serializer.data,
                        "status": status.HTTP_201_CREATED,
                    }
                    return Response(
                        response, status=status.HTTP_201_CREATED, headers=headers
                    )
                else:
                    response = {
                        "message": "Validtation Error",
                        "status": status.HTTP_403_FORBIDDEN,
                    }
                    return Response(response, status=status.HTTP_403_FORBIDDEN)
        else:
            response = {
                "message": "Not a Valid Ticket",
                "status": status.HTTP_400_BAD_REQUEST,
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


# # class WebTicketApi(CustomViewSet):
# #     queryset = Ticket.objects.all()
# #     serializer_class = TicketSerializer
# #     permission_classes = [IsClient]

# #     # @swagger_auto_schema(
# #     #     request_body=TicketSerializer,
# #     #     operation_description="Ticket Create",
# #     # )

# #     def create(self, request):
# #         if int(request.data["ticket_type"]) == 1:
# #             print("im here hona chahiye")
# #             request.data["product"] = 19
# #         if request.user.user_role == 2:
# #             request.data["created_by_customer"] = True
# #             request.data["customer_fk"] = request.user.id

# #         ticket_serializer = TicketSerializer(data=request.data)
# #         if ticket_serializer.is_valid(raise_exception=True):
# #             # serializer.data.get("")
# #             pass
# #         else:
# #             return Response(ticket_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# #         # if request.user.user_role == 2:
# #         #     if request.data.get("address"):
# #         #         data = request.data["address"]
# #         #         data["user_fk"] = request.user.id
# #         #         serializer = AddressSerializer(data=data)
# #         #         if serializer.is_valid(raise_exception=True):
# #         #             serializer.save()
# #         #         else:
# #         #             return Response(
# #         #                 serializer.errors, status=status.HTTP_400_BAD_REQUEST
# #         #             )
# #         ticket_type = ticket_serializer.validated_data["ticket_type"]
# #         if ticket_type == 1:  # installation
# #             serializer = InstallationSerializer(data=request.data)
# #             if serializer.is_valid(raise_exception=True):
# #                 print("---------------")

# #                 print("im here")
# #                 ticket = ticket_serializer.save()
# #                 request.data["ticket_fk"] = ticket.id
# #                 serializer = InstallationSerializer(data=request.data)
# #                 serializer.is_valid(raise_exception=True)
# #                 # ticket_type = ticket.ticket_type
# #                 serializer.save()
# #             else:
# #                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# #         elif ticket_type == 2:  # Service
# #             serializer = ServiceSerializer(data=request.data)
# #             if serializer.is_valid(raise_exception=True):
# #                 ticket = ticket_serializer.save()
# #                 request.data["ticket_fk"] = ticket.id
# #                 # ticket_type = ticket.ticket_type
# #                 serializer = ServiceSerializer(data=request.data)
# #                 serializer.is_valid(raise_exception=True)

# #                 serializer.save()
# #             else:
# #                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# #         elif ticket_type == 3:  # Spares
# #             for i in ["spare_detail"]:
# #                 if i not in request.data.keys():
# #                     return Response(
# #                         {"message": f"{i} is required"},
# #                         status=status.HTTP_400_BAD_REQUEST,
# #                     )
# #                 if not request.data[i]:
# #                     return Response(
# #                         {"message": "spare_detail shouldn't empty"},
# #                         status=status.HTTP_400_BAD_REQUEST,
# #                     )

# #                 for j in ["part_name", "part_desciption", "qunatity"]:
# #                     for k in request.data[i]:
# #                         if j not in k.keys():
# #                             return Response(
# #                                 {"message": f"{j} is required"},
# #                                 status=status.HTTP_400_BAD_REQUEST,
# #                             )
# #             serializer = SparesSerializer(data=request.data)
# #             if serializer.is_valid(raise_exception=True):
# #                 ticket = ticket_serializer.save()
# #                 request.data["ticket_fk"] = ticket.id
# #                 # ticket_type = ticket.ticket_type
# #                 serializer = SparesSerializer(data=request.data)
# #                 serializer.is_valid(raise_exception=True)
# #                 spare = serializer.save()
# #                 data = request.data["spare_detail"]
# #                 for i in data:
# #                     i["spare"] = spare.id
# #                 serializer = SpareDetailSerializer(data=data, many=True)
# #                 serializer.is_valid(raise_exception=True)
# #                 serializer.save()
# #             else:
# #                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# #         elif ticket_type == 4:  # Sales_inquiry
# #             serializer = SalesInquirySerializer(data=request.data)
# #             if serializer.is_valid(raise_exception=True):
# #                 ticket = ticket_serializer.save()
# #                 request.data["ticket_fk"] = ticket.id
# #                 # ticket_type = ticket.ticket_type
# #                 serializer = SalesInquirySerializer(data=request.data)
# #                 serializer.is_valid(raise_exception=True)
# #                 serializer.save()
# #             else:
# #                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# #         elif ticket_type == 5:  # Others
# #             serializer = OtherServiceSerializer(data=request.data)
# #             if serializer.is_valid(raise_exception=True):
# #                 ticket = ticket_serializer.save()
# #                 request.data["ticket_fk"] = ticket.id
# #                 serializer = OtherServiceSerializer(data=request.data)
# #                 serializer.is_valid(raise_exception=True)
# #                 # ticket_type = ticket.ticket_type
# #                 serializer.save()
# #             else:
# #                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# #         else:  # Repair
# #             serializer = RepairServiceSerializer(data=request.data)
# #             if serializer.is_valid(raise_exception=True):
# #                 ticket = ticket_serializer.save()
# #                 request.data["ticket_fk"] = ticket.id
# #                 # ticket_type = ticket.ticket_type
# #                 serializer = RepairServiceSerializer(data=request.data)
# #                 serializer.is_valid(raise_exception=True)
# #                 serializer.save()
# #             else:
# #                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# #         # if request.data.get("team_member"):
# #         #     data = request.data["team_member"]
# #         #     for i in data:
# #         #         i["ticket_fk"] = ticket.id
# #         #     serializer = TeamMemberSerializer(data=data, many=True)
# #         #     if serializer.is_valid(raise_exception=True):
# #         #         serializer.save()
# #         if request.data.get("attachment"):
# #             data = request.data["attachment"]
# #             for i in data:
# #                 i["ticket_fk"] = ticket.id
# #             serializer = AttachmentSerializer(data=data, many=True)
# #             if serializer.is_valid(raise_exception=True):
# #                 serializer.save()
# #         return Response(
# #             {"message": "Ticket Created Successfully"}, status=status.HTTP_200_OK
# #         )


class ALLDateFieldsAPI(ViewSet):
    def create(self, request):
        serializer = AllDateFieldSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ticket = Ticket.objects.filter(id=serializer.data.get("ticket")).first()
        print("------------->>>", ticket)
        engineer = Engineer.objects.filter(ticket_fk=ticket, is_assign=True).first()
        if not ticket and not engineer and engineer.visit_date is None:
            return Response(
                {"message": "Ticket Not Found or not assigned"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        customer_wise_item = serializer.data.get("customer_wise_item")
        customer_wise_item = CustomerWiseItem.objects.filter(
            id=customer_wise_item
        ).first()
        print("customer_wise_item ------------>>>>>", customer_wise_item)
        Installation_ticket = customer_wise_item.ticket_set.filter(ticket_type=1).first()
        print("Installation_ticket------------------------>>>", Installation_ticket)
        if not customer_wise_item:
            return Response(
                {"message": "item not found"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not Installation_ticket:
            installation_ticket_date = ticket.raise_date
            print("=====================>>>", installation_ticket_date)
        else:
            try:
                if Installation_ticket.ticket_close_date:
                    installation_ticket_date = Installation_ticket.ticket_close_date
                    print("installation_ticket_date in try: ", installation_ticket_date)
                else:
                    installation_ticket_date = ticket.raise_date
                    print("installation_ticket_date in e:", installation_ticket_date)
            except Exception as e:
                print(e)

        repeats = ServiceReport.objects.filter(
            ticket_fk__customer_wise_item=customer_wise_item.id
        ).count()
        response = {
            "installation_date": installation_ticket_date,
            "start_date": ticket.raise_date,
            "attend_date": engineer.visit_date,
            "dispach_date": customer_wise_item.dispach_date,
            "repeats": repeats,
            "work_order_no": customer_wise_item.work_order_no,
        }
        print("response :", response)
        return Response(response, status=status.HTTP_200_OK)


class SpareTicketConfirm(CustomViewSet, RequiredFields):
    required_fields = ["ticket"]

    def create(self, request, *args, **kwargs):
        user_role = request.user.user_role
        print("user_role", user_role)
        multi_serializer = []
        if user_role == 9:
            self.required_fields = ["document_no", "ticket"]
        elif user_role == 5:
            request.data["hq_user_fk"] = request.user.id
            self.required_fields = ["spare_detail", "ticket"]
        elif user_role == 27:
            request.data["logistic_user_fk"] = request.user.id
            self.required_fields = [
                "ticket",
                "courier_name",
                "courier_mobile",
                "courier_docket_no",
                "dispach_date",
            ]
        print(self.required_fields)
        self.check_required_fields(request)
        ticket = request.data.get("ticket")
        try:
            ticket = Ticket.objects.get(id=ticket)
            if ticket.ticket_type != 3:
                raise Exception
        except Exception:
            return Response(
                {"message": "Ticket Not found or not spare ticket"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if user_role == 9:  # region coordinator
            try:
                spare = ticket.ticket_spares
                spare.document_no = request.data.get("document_no")
                spare.is_region_cordinator_varified = True
                spare.region_co_user_fk = request.user
                spare.save()
                return Response(
                    {"message": "region coordinator verified successfully"},
                    status=status.HTTP_200_OK,
                )
            except Exception:
                return Response(
                    {"message": "spare object not found"}, status=status.HTTP_410_GONE
                )
        elif user_role == 5:
            # ticket_serializer = TicketSerializer(ticket,data=request.data)
            # multi_serializer.append(ticket_serializer)
            spare = ticket.ticket_spares
            request.data["is_hq_verified"] = True
            spare_serializer = SparesSerializer(spare, data=request.data, partial=True)
            multi_serializer.append(spare_serializer)
            spare_details = spare.sparedetail_set.all()
            exclude_ids = []
            update_data = []
            create_data = []
            for data in request.data["spare_detail"]:
                if data.get("id"):
                    data["spare"] = spare
                    update_data.append(data)
                    exclude_ids.append(data["id"])
                else:
                    data["spare"] = spare.id
                    create_data.append(data)
            for i in update_data:
                SpareDetail(**i).save()
            spare_detail_create = SpareDetailSerializer(data=create_data, many=True)
            multi_serializer.append(spare_detail_create)
            spare_details.exclude(id__in=exclude_ids).delete()
            serializer_errors = []
            for serializer in multi_serializer:
                if serializer.is_valid():
                    serializer.save()
                else:
                    if hasattr(serializer, "many") and serializer.many:
                        serializer_errors.extend(serializer.errors)
                    else:
                        serializer_errors.append(serializer.errors)
            if serializer_errors:
                combined_errors = {}
                for errors in serializer_errors:
                    if isinstance(errors, dict):
                        combined_errors.update(errors)
                    elif isinstance(errors, list):
                        for error_dict in errors:
                            combined_errors.update(error_dict)
                response = {
                    "message": "Bad request",
                    "data": combined_errors,
                    "status": status.HTTP_400_BAD_REQUEST,
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            # Your remaining create method logic here
            return Response(
                {"message": "HQ incharge ticket verified"}, status=status.HTTP_200_OK
            )
        elif user_role == 27:
            print("here")
            try:
                spare = ticket.ticket_spares
            except Exception:
                return Response(
                    {"message": "spare object not found"}, status=status.HTTP_410_GONE
                )

            print("here")
            if (
                    spare.is_hq_verified
                    and spare.is_region_cordinator_varified
                    and not spare.sparedetail_set.filter()
                    .exclude(spare_status="ready_to_pack")
                    .exists()
            ):
                spare_serializer = SparesSerializer(
                    spare, data=request.data, partial=True
                )
                spare_serializer.is_valid(raise_exception=True)
                spare_serializer.save()
                email = EmailMessage(
                    "NuVu Conair Spare Part Status",
                    "Dear Customer your spares part are now dispached from our site you can track the status from the portal",
                    from_email=os.getenv("EMAIL_HOST_USER"),
                    to=list(
                        ticket.customer_fk.email_set.all().values_list(
                            "E_Mail", flat=True
                        )
                    ),
                )
                email.send()
                return Response(
                    {"message": "Logstic Team form submitted"},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"message": "right now you are not eligible for this action"},
                    status=status.HTTP_423_LOCKED,
                )


class SpareStatusChangeAPI(CustomViewSet, RequiredFields):
    # serializer_class = SpareDetailSerializer
    permission_classes = [
        IsStoreUpdater | IsProductionUpdater | IsPurchaseUpdate | IsDispatchUpdater
    ]

    # queryset = SpareDetail.objects.all()

    def create(self, request, *args, **kwargs):
        if request.user.user_role == 10:
            self.required_fields = ["ticket", "dispacher_status"]
            request.data["dispacher_user_fk"] = request.user.id
            self.check_required_fields(request)
            try:
                spare = Ticket.objects.get(id=request.data.get("ticket")).ticket_spares
            except Exception:
                return Response(
                    {"message": "spare object not found"}, status=status.HTTP_410_GONE
                )
            spare_serializer = SparesSerializer(spare, data=request.data, partial=True)
            spare_serializer.is_valid(raise_exception=True)
            spare_serializer.save()
            return Response(
                {"message": "Dispacher Status has been changed"},
                status=status.HTTP_200_OK,
            )
        self.required_fields = ["data"]
        self.check_required_fields(request)
        data = request.data["data"]
        if request.user.user_role == 19:
            spare_status = [
                "shortage",
                "gathering_for_assembly",
                "over_to_assembly",
                "ready_to_pack",
            ]
            for i in data:
                if i["spare_status"] not in spare_status:
                    return Response(
                        {
                            "massage": "Spare Status Should Be From Shortage, Gathering For Assembly, Over To Assembly, Ready To Pack"
                        },
                        status=status.HTTP_423_LOCKED,
                    )

        elif request.user.user_role == 21:
            spare_status = ["purchase_scheduling", "sourcing", "ordered", "received"]
            for i in data:
                if i["spare_status"] not in spare_status:
                    return Response(
                        {
                            "massage": "Spare Status Should Be From purchase_scheduling, sourcing, ordered, received"
                        },
                        status=status.HTTP_423_LOCKED,
                    )

        elif request.user.user_role == 20:
            spare_status = [
                "assembling",
                "testing",
                "production_scheduling",
                "handed_over_to_store",
            ]
            for i in data:
                if i["spare_status"] not in spare_status:
                    return Response(
                        {
                            "massage": "Spare Status Should Be From Assembling, Testing, Production Scheduling, Handed Over To Store"
                        },
                        status=status.HTTP_423_LOCKED,
                    )

        elif request.user.user_role == 10:
            spare_status = [
                "old_outstanding",
                "freight_confirmation",
                "payment_pending",
                "credit_terms",
                "service_hold",
                "cancel_order",
                "ok_to_dispatch",
            ]
            for i in data:
                if i["spare_status"] not in spare_status:
                    return Response(
                        {
                            "massage": "Spare Status Should Be From Old Outstanding, Freight Confirmation, Payment Pending, Credit Terms, Service Hold, Cancel Order, Ok To Dispatch"
                        },
                        status=status.HTTP_423_LOCKED,
                    )
        else:
            return Response(
                {"massage": "User not allowed"}, status=status.HTTP_400_BAD_REQUEST
            )
        # try:
        for i in data:
            if i.get("department_status"):
                SpareDetail.objects.filter(id=i["id"]).update(
                    spare_status=i["spare_status"],
                    department_status=i.get("department_status"),
                )
            else:
                SpareDetail.objects.filter(id=i["id"]).update(
                    spare_status=i["spare_status"]
                )
        # spare = SpareDetail.objects.filter(id=i["id"]).first().spare

        spare_detail = SpareDetail.objects.filter(id=i["id"]).first()
        print("spare_detail: ", spare_detail)
        spare = spare_detail.spare
        print("spare: ", spare)
        a = spare.dispacher_status
        print("a: ", a)
        state = spare_detail.spare_status
        print(state)
        spare.is_ready_to_pack = True
        if (
                state
                in [
            "shortage",
            "gathering_for_assembly",
            "over_to_assembly",
            "ready_to_pack",
        ]
                and request.user.user_role == 19
        ):
            setattr(spare, "store_user_fk", request.user)
        elif (
                state in ["purchase_scheduling", "sourcing", "ordered", "received"]
                and request.user.user_role == 21
        ):
            setattr(spare, "purchase_user_fk", request.user)
        elif (
                state
                in ["assembling", "testing", "production_scheduling", "handed_over_to_store"]
                and request.user.user_role == 20
        ):
            setattr(spare, "production_user_fk", request.user)
        elif (
                a
                in [
                    "old_outstanding",
                    "freight_confirmation",
                    "payment_pending",
                    "credit_terms",
                    "service_hold",
                    "cancel_order",
                    "ok_to_dispatch",
                ]
                and request.user.user_role == 10
        ):
            setattr(spare, "dispacher_user_fk", request.user)
        spare.save()

        # if (
        #     not SpareDetail.objects.filter(id=i["id"])
        #     .first()
        #     .spare.sparedetail_set.filter()
        #     .exclude(spare_status="ready_to_pack")
        #     .exists()
        # ):
        #     spare.is_ready_to_pack = True
        #     if request.user.user_role == 10:
        #         setattr(spare, "dispacher_user_fk", request.user)
        #     elif request.user.user_role == 21:
        #         setattr(spare, "purchase_user_fk", request.user)
        #     elif request.user.user_role == 20:
        #         setattr(spare, "production_user_fk", request.user)
        #     elif request.user.user_role == 19:
        #         setattr(spare, "store_user_fk", request.user)
        #     spare.save()

        # except Exception:
        #     return Response(
        #         {"message": "id and spare_status is required"},
        #         status=status.HTTP_400_BAD_REQUEST,
        #     )
        return Response(
            {"message": "Spare Status Updated Successfully"},
            status=status.HTTP_200_OK,
        )
        # else:
        #     Response({"massage": "Wrong ID"}, status=status.HTTP_400_BAD_REQUEST)


class UserWiseSpare(CustomViewSet):
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()

    def list(self, request, *args, **kwargs):
        search = request.GET.get("search")
        if request.user.user_role == 2:
            ticket = Ticket.objects.filter(
                customer_fk=request.user, ticket_type=3
            ).order_by("id")

            print("ticket: ", ticket.count(), ticket)
            ticket_serializer = TicketDepthSerializer(ticket, many=True)
            ticket_datas = ticket_serializer.data
            print("ticket_serializer.data: ", len(ticket_serializer.data))
            for ticket_data in ticket_datas:
                print("hiii")
                # user_spares = Spares.objects.filter(ticket_fk=ticket_data["id"]).values()
                user_spares = Spares.objects.filter(ticket_fk=ticket_data["id"])
                print("user_spares: ", user_spares)
                spare = SparesDepthSerializer(
                    user_spares, many=True, context={"request": request}
                ).data
                print("spare: ", spare)
                ticket_data["spares"] = spare

            return Response({"data": ticket_datas}, status=status.HTTP_200_OK)
        elif request.user.user_role == 3:
            print("-------------------HIM-------------------")
            ticket = Ticket.objects.filter(
                ticket_engineer__engineer_fk=request.user, ticket_type=3
            ).order_by("id")
            ticket_serializer = TicketDepthSerializer(ticket, many=True)
            ticket_datas = ticket_serializer.data
            print("ticket_serializer.data: ", len(ticket_serializer.data))
            for ticket_data in ticket_datas:
                print("hiii")
                # user_spares = Spares.objects.filter(ticket_fk=ticket_data["id"]).values()
                user_spares = Spares.objects.filter(ticket_fk=ticket_data["id"])
                print("user_spares: ", user_spares)
                spare = SparesDepthSerializer(
                    user_spares, many=True, context={"request": request}
                ).data
                print("spare: ", spare)
                ticket_data["spares"] = spare
            return Response({"data": ticket_datas}, status=status.HTTP_200_OK)
        return Response(
            {"message": " This User is note Customer"},
            status=status.HTTP_406_NOT_ACCEPTABLE,
        )

    def retrieve(self, *args, **kwargs):
        data = TicketDepthSerializer(self.get_object()).data
        ticket_spare = self.get_object().ticket_spares
        data["spare"] = SparesSerializer(ticket_spare).data
        data["spare"] = SparesDepthSerializer(ticket_spare).data
        data["spare_parts"] = SpareDetailSerializer(
            self.get_object().ticket_spares.sparedetail_set.all(), many=True
        ).data
        response = {
            "data": data,
            "status": status.HTTP_200_OK,
        }
        return Response(response, status=status.HTTP_200_OK)


class RepairTicketConfirm(CustomViewSet, RequiredFields):
    permission_classes = [IsDispatchUpdater | IsStoreUpdater]
    required_fields = ["ticket"]

    def create(self, request, *args, **kwargs):
        user_role = request.user.user_role
        if user_role == 10:
            fields = ["invert_number", "date"]
            self.required_fields.extend(fields)
            self.required_fields(request)
            data = {k: v for k, v in request.data.items() if k in fields}
        elif user_role == 19:
            fields = ["verify_from_store_updater"]
            self.required_fields.extend(fields)
            self.required_fields(request)
            data = {k: v for k, v in request.data.items() if k in fields}

        try:
            ticket = Ticket.objects.get(id=ticket)
            repair = ticket.ticket_repair
        except Exception:
            return Response(
                {"message": "Ticket not Found or it is not repair ticket"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        repair_serializer = RepairServiceSerializer(repair, data=data)
        repair_serializer.is_valid(raise_exception=True)
        repair_serializer.save()
        return Response(
            {"message": "Ticket accepted successfuly"}, status=status.HTTP_200_OK
        )


class ReadyToPackApi(CustomViewSet, RequiredFields):
    required_fields = ["data", "ticket"]
    permission_classes = [IsStoreUpdater]

    def create(self, request, *args, **kwargs):
        self.check_required_fields(request)
        # data = {k: v for k, v in request.data.items() if k in self.required_fields}
        data = request.data
        try:
            ticket = Ticket.objects.get(id=request.data.get("ticket"))
            spares = ticket.ticket_spares
        except Exception:
            return Response(
                {"message": "ticket not found or ticket is not spare type"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if (
                not spares.sparedetail_set.filter()
                        .exclude(spare_status="ready_to_pack")
                        .exists()
        ):
            data["is_store_updator_verified"] = True
            data["store_user_fk"] = request.user.id
            print(data["data"])
            for i in data["data"]:
                SpareBox.objects.create(spare=spares, **i)
            spare_serializer = SparesSerializer(spares, data=data)
            spare_serializer.is_valid(raise_exception=True)
            spare_serializer.save()
            return Response(
                {"message": "box data added successfully"}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"message": "please make all spare_status to ready_to_pack"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ReturnSpareConfirmApi(CustomViewSet, RequiredFields):
    required_fields = ["ticket", "invert_date", "invert_number"]

    def create(self, request, *args, **kwargs):
        if request.user.user_role == 10:
            self.check_required_fields(request)

            try:
                ticket = Ticket.objects.get(id=ticket)
                return_spare = ticket.return_spare_ticket
            except:
                return Response(
                    {"message": "ticket not found or return_spare"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializer = ReturnSpareDetailSerializer(return_spare, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                {"message": "dispacher form added successfully"},
                status=status.HTTP_200_OK,
            )
        return super().create(request, *args, **kwargs)


# ----------------------------Instalation Report----------------------------

class InstalationReportApi(CustomViewSetFilter):
    serializer_class = InstallationReportSerializer

    # def get_queryset(self, request):
    #     customer = request.GET.get("customer")
    #     product = request.GET.get("product")
    #     self.response_tag = "installation_report"
    #     return InstallationReport.objects.filter(
    #         ticket_fk__customer_fk__id=customer,
    #         ticket_fk__company_product_item__id=product,
    #     )

    def create(self, request, *args, **kwargs):
        installation_report_serializer = InstallationReportSerializer(data=request.data)
        installation_report_serializer.is_valid(raise_exception=True)
        installation_report = installation_report_serializer.save()
        ticket_id = request.data["ticket_fk"]
        cus_item = Ticket.objects.filter(id=ticket_id).values("customer_wise_item")
        for i in cus_item:
            item_fk = CustomerWiseItem.objects.filter(id=i["customer_wise_item"]).values("item")[0]
            SerialNo = CustomerWiseItem.objects.filter(id=i["customer_wise_item"]).values("SerialNo")[0]
            CTIIS = CompanyTicketInstallationItemStatus.objects.filter(
                ticket=ticket_id,
                customer_wise_item=i["customer_wise_item"]).values()[0]
            data = CTIIS
            data["installation_problem_status"] = data["installation_problem_status_id"]
            del data["installation_problem_status_id"]
            del data["customer_wise_item_id"]
            del data["id"]
            del data["ticket_id"]
            data["item"] = item_fk["item"]
            data["serial_no"] = SerialNo["SerialNo"]
            data["Installation_report"] = int(installation_report.id)
            serializer = InstallationReportPartSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            print(serializer.validated_data)
            serializer.save()

        # data = request.data["installation_report_part"]
        # for i in range(len(data)):
        #     data[i]["Installation_report"] = installation_report.id
        # serializer = InstallationReportPartSerializer(data=data, many=True)
        # serializer.is_valid(raise_exception=True)
        # serializer.save()
        if installation_report.ticket_fk.is_guest:
            mobile = installation_report.ticket_fk.mobile_no
        else:
            mobile = installation_report.ticket_fk.mobile_no_fk.phone
        session_data = SessionStore()
        # session_data["OTP"] = send_otp_via_phone(mobile)
        session_data["OTP"] = os.getenv("OTP")
        session_data.set_expiry(300)
        session_data["VVV"] = installation_report.id
        session_data.create()

        return Response(
            {
                "message": "Installation Report Created",
                "data": installation_report_serializer.data,
                "session_data": session_data.session_key,
                "status": status.HTTP_200_OK,
            },
            status=status.HTTP_200_OK,
        )


class InstalationReportCustomerVerifyApi(ViewSet):
    def create(self, request):
        session_key = request.data.get("session_key")
        otp = request.data.get("otp")
        json_data = {}
        try:
            session_data = SessionStore(session_key=session_key)
            session_otp = session_data["OTP"]
            Installation_report = session_data["VVV"]
        except Exception:
            return Response(
                {"message": "Session Key is expired"}, status=status.HTTP_400_BAD_REQUEST
            )
        if otp != session_otp:
            return Response(
                {"message": "OTP is not match"}, status=status.HTTP_400_BAD_REQUEST
            )
        installation_report = InstallationReport.objects.get(id=Installation_report)
        installation_report.verified_by_customer = True
        installation_report.save()
        ticket = installation_report.ticket_fk
        json_data["server_path"] = request.META.get("HTTP_HOST")
        json_data["ticket_number"] = ticket.ticket_number
        json_data["customer_name"] = ticket.customer_fk.CardName
        json_data["customer_mobile_num"] = ticket.mobile_no_fk
        json_data["enginer_name"] = ticket.ticket_engineer.first().engineer_fk.CardName
        json_data["enginer_email"] = ticket.ticket_engineer.first().engineer_fk.E_Mail
        json_data["enginer_number"] = ticket.ticket_engineer.first().engineer_fk.mobile_number
        installation_report_part = InstallationReportPart.objects.filter(
            Installation_report=Installation_report
        )
        installation_report_part = InstallationReportPartDepthSerializer(
            installation_report_part, many=True
        )
        installation_report_serializer = InstallationReportDepthSerializer(installation_report)
        installation_report_data = installation_report_serializer.data
        json_data["installation_report"] = installation_report_data
        json_data["installation_report_parts"] = installation_report_part.data
        pdf = render_to_pdf(
            "installation_report.html",
            json_data,
        )
        email = EmailMessage(
            "NuVu Conair Installation report ",
            "hello",
            from_email=os.getenv("EMAIL_HOST_USER"),
            # to=list(
            #     service_report.ticket_fk.customer_fk.email_set.all().values_list(
            #         "E_Mail", flat=True
            #     )
            # ),
            # to = ["kinjal@conairgroup.com"]
            to=["himanishvyas.tecblic@gmail.com", "kinjal@conairgroup.com"]
        )
        # return pdf
        email.attach("Installation_report.pdf", pdf.getvalue(), "application/pdf")
        email.send()
        # return pdf
        return Response(
            {"message": "Installation report has been verified by customer"},
            status=status.HTTP_200_OK,
        )


class PackSlipWiseItemAPI(CustomViewSetFilter):
    serializer_class = CustomerWiseItemSerializer

    def list(self, request, *args, **kwargs):
        packing_slip_no = request.data.get("packing_slip_no")
        work_order_no = request.data.get("work_order_no")
        customer_wise_item = CustomerWiseItem.objects.filter(
            packing_slip_no=packing_slip_no,
            work_order_no=work_order_no
        )
        results = self.get_serializer(customer_wise_item, many=True).data
        response = {
            "data": results
        }
        return Response(response, status=status.HTTP_200_OK)
