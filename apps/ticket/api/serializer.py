from rest_framework import serializers

from apps.ticket.models import (  # TeamMembers,; FAQ,; RCA,; Attachment,; Comment,; CompanyProductItem,; CompanyTicketInstallationItemStatus,; Document,; FeedBack,; FileUpload,; FTCForm,; InstallationaProblemStatus,; Item,; LastStatus,; Notification,; # Product,; ProductProblemType,; RCACategory,; RCADepartment,; ServiceReport,; ServiceReportPart,
    FAQ,
    RCA,
    CompanyTicketInstallationItemStatus,
    CustomerWiseItem,
    Engineer,
    FeedBack,
    FTCForm,
    Installation,
    InstallationaProblemStatus,
    Item,
    ItemProblemType,
    ItemSpare,
    LastStatus,
    Notification,
    OtherService,
    RCACategory,
    RCADepartment,
    Repair,
    ReturnSpare,
    ReturnSpareDetail,
    SalesInquiry,
    Service,
    ServiceReport,
    ServiceReportPart,
    SpareDetail,
    Spares,
    Ticket,
    Document,
    InstallationReport,
    InstallationReportPart

)
from apps.user.api.serializer import CustomerUserSerializer, PhoneNumebrSerializer
from apps.user.models import PhoneNumber


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        # fields = [
        #     "name",
        #     "phone_number",
        #     "customer_address",
        #     "query_type",
        #     "customer_email",
        #     ""
        # ]
        fields = "__all__"


class TicketDepthSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        # fields = [
        #     "name",
        #     "phone_number",
        #     "customer_address",
        #     "query_type",
        #     "customer_email",
        #     ""
        # ]
        fields = "__all__"
        depth = 2


class InstallationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Installation
        fields = "__all__"


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = "__all__"


class SalesInquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesInquiry
        fields = "__all__"


class OtherServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtherService
        fields = "__all__"


class SparesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spares
        fields = "__all__"


class SparesDepthSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spares
        fields = "__all__"
        depth = 1


# class CommentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Comment
#         fields = "__all__"


# # class DocumentSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = Document
# #         fields = "__all__"


# class CompanyProductItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CompanyProductItem
#         fields = "__all__"


# class CompanyProductItemDepthSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CompanyProductItem
#         fields = "__all__"
#         depth = 1


# # class ProductDepthSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = Product
# #         fields = "__all__"
# #         depth = 1


# class AttachmentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Attachment
#         fields = "__all__"


# # class TeamMemberSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = TeamMembers
# #         fields = "__all__"


# class UploadFIleSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = FileUpload
#         fields = "__all__"


# class TicketStatusSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Ticket
#         fields = "__all__"


class EnginnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Engineer
        fields = "__all__"
        depth = 1

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["engineer_fk"] = CustomerUserSerializer(
            instance.engineer_fk, context={"request": self.context.get("request")}
        ).data
        # print("DATA", data["engineer_fk"])
        return data


class EnginnerWithoutDepthSerializer(serializers.ModelSerializer):
    class Meta:
        model = Engineer
        fields = "__all__"


class LastStatusDepthSerializer(serializers.ModelSerializer):
    class Meta:
        model = LastStatus
        fields = "__all__"
        depth = 1


class LastStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = LastStatus
        fields = "__all__"


class FeedBackSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedBack
        fields = "__all__"


# class FeedBackDepthSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = FeedBack
#         fields = "__all__"
#         depth = 1


class RCACategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RCACategory
        fields = "__all__"


class RCADepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = RCADepartment
        fields = "__all__"


class RCASerializer(serializers.ModelSerializer):
    rca_department = RCADepartmentSerializer(read_only=True, many=True).data

    class Meta:
        model = RCA
        fields = ("id", "category", "rca_suggestion", "rca_department", "ticket_fk")


# class ItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Item
#         fields = "__all__"


# class ItemDepthSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Item
#         fields = "__all__"
#         depth = 1


class InstallationProblemStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstallationaProblemStatus
        fields = "__all__"
        depth = 1


class RepairServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repair
        fields = "__all__"


class NotificationSeralizer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"


class ServiceReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceReport
        fields = "__all__"


class ServiceReportDepthSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceReport
        fields = "__all__"
        depth = 1


class ServiceReportPartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceReportPart
        fields = "__all__"


class ServiceReportPartDepthSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceReportPart
        fields = "__all__"
        depth = 1


# # class ProductQRSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = Product
# #         fields = "__all__"


class DocumentProductSerializer(serializers.ModelSerializer):
    # file = serializers.SerializerMethodField()
    class Meta:
        model = Document
        fields = "__all__"

    @property
    def get_file(self, document):
        request = self.context.get("request")
        photo_url = document.file.url
        return request.build_absolute_uri(photo_url)


# class DocumentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Document
#         fields = "__all__"


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = "__all__"


class FTCFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = FTCForm
        fields = "__all__"


# class ProductProblemTypeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProductProblemType
#         fields = "__all__"


class SpareDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpareDetail
        fields = "__all__"


class CustomerWiseItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerWiseItem
        fields = "__all__"
        depth = 1


class CustomerWiseItemWithoutDepthSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerWiseItem
        fields = "__all__"


class CompanyTicketInstallationItemStatusSerializers(serializers.ModelSerializer):
    class Meta:
        model = CompanyTicketInstallationItemStatus
        fields = "__all__"


class DepthCompanyTicketInstallationItemStatusSerializers(serializers.ModelSerializer):
    class Meta:
        model = CompanyTicketInstallationItemStatus
        fields = "__all__"
        depth = 1


class TicketInstallationItemStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyTicketInstallationItemStatus
        fields = "__all__"


class AllDateFieldSerializer(serializers.Serializer):
    ticket = serializers.IntegerField()
    customer_wise_item = serializers.IntegerField()


class ItemProblemTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemProblemType
        fields = "__all__"


class ItemSpareSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemSpare
        fields = "__all__"


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = "__all__"


class ReturnSpareSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReturnSpare
        fields = "__all__"


class ReturnSpareDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReturnSpareDetail
        fields = "__all__"


class InstallationReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstallationReport
        fields = "__all__"


class InstallationReportDepthSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstallationReport
        fields = "__all__"
        depth = 1


class InstallationReportPartSerializer(serializers.ModelSerializer):

    class Meta:
        model = InstallationReportPart
        fields = "__all__"

class InstallationReportPartDepthSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstallationReportPart
        fields = "__all__"
        depth = 1
