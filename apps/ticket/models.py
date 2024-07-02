from datetime import datetime
from io import BytesIO

import qrcode
from django.contrib.postgres.fields import ArrayField
from django.core.files import File

# # from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

# # from apps.user.models import User
from django.db.models.signals import post_save
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from PIL import Image, ImageDraw

# from apps.ticket.customs.manager import TicketManager
from apps.ticket.utilities.choices import (  # PreInstallationChecklistChoice,; InstallationStatusItemChoice,; RCACategoryChoice,; RCADepartmentChoice,; ProductionStatusChoice,; FTCChoice,; WarrantyChoices,
    CheckMatType,
    DepartmentStatusChoices,
    DispacherStatusChoices,
    FaqTypeChoices,
    FilterCondtion,
    PriorityChoice,
    QueryTypeChoice,
    ReturnSpareStatusChoices,
    ServicePartAction,
    SparesStatusChoices,
    TicketStatusChoices,
    TicketTypeChoice,
    InstallationStatusItemChoice,
    McTypeChoices
)


# # from apps.user.models import User

# # from datetime import datetime


# # Create your models here.
# class FileUpload(models.Model):
#     file = models.FileField(_("File Upload"), upload_to="media/ticket", max_length=100)

#     def __str__(self):
#         return str(self.id)


class Ticket(models.Model):
    ticket_number = models.CharField(
        _("Ticket Id"), max_length=100, unique=True, blank=True, null=True
    )
    customer_fk = models.ForeignKey(
        "user.CustomerUser",
        verbose_name=_("User FK"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    call_count = models.IntegerField(_("Call Count"), default=0)
    mobile_no_fk = models.ForeignKey(
        "user.PhoneNumber",
        verbose_name=_("Phone Number"),
        on_delete=models.SET_NULL,
        related_name="ticket_phone",
        null=True,
        blank=True,
    )
    address_fk = models.ForeignKey(
        "user.Address",
        verbose_name=_("Address"),
        on_delete=models.SET_NULL,
        related_name="ticket_address",
        null=True,
        blank=True,
    )
    is_guest = models.BooleanField(_("Is Guest"), default=False)
    mobile_no = models.CharField(_("Phone number"), max_length=15, null=True, blank=True)
    address = models.TextField(_("Address "), null=True, blank=True)
    email = models.EmailField(_("Email"), max_length=254, null=True, blank=True)
    region = models.CharField(_("Region"), max_length=254, null=True, blank=True)
    ticket_type = models.PositiveSmallIntegerField(
        _("Query Type"), choices=QueryTypeChoice.choices
    )
    priority = models.CharField(
        _("Ticket Priority"),
        choices=PriorityChoice.choices,
        max_length=10,
        default="low",
    )
    assigned_by = models.ForeignKey(
        "user.CustomerUser",
        verbose_name=_("Assign By FK"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_by_user",
    )
    ticket_status = models.CharField(
        _("Ticket Status"),
        choices=TicketStatusChoices.choices,
        max_length=50,
        default="pending",
    )
    raise_date = models.DateField(_("Raise Date"), auto_now_add=True)
    ticket_close_date = models.DateField(_("Ticket Close Date"), null=True, blank=True)
    ticket_assign_date = models.DateField(_("Ticket Assign Date"), null=True, blank=True)
    customer_wise_item = models.ManyToManyField(
        "ticket.CustomerWiseItem",
        verbose_name=_("Customer Wise Item FK"),
        null=True,
        blank=True,
    )
    spare_ticket_id = models.IntegerField(_("Spare Ticket ID"), null=True, blank=True)
    # company = models.ForeignKey(
    #     "user.Company", verbose_name=_("Company FK"), on_delete=models.CASCADE
    # )
    is_ftc_ticket = models.BooleanField(_("IS FTC Ticket"), default=False)

    @classmethod
    def post_create(cls, sender, instance, created, *args, **kwargs):
        if created:
            id_string = str(instance.id)
            ticket_type = {1: "I", 2: "S", 3: "P", 4: "E", 5: "O", 6: "R"}
            instance.ticket_number = (
                    ticket_type[instance.ticket_type]
                    + id_string
                    + str(datetime.today().year)
            )
            instance.save()

    def __str__(self):
        return str(self.id)


post_save.connect(Ticket.post_create, sender=Ticket)


class Engineer(models.Model):
    check_in_timestamp = ArrayField(
        models.DateTimeField(_("Check IN"), null=True, blank=True), null=True, blank=True
    )
    check_out_timestamp = ArrayField(
        models.DateTimeField(_("Check Out"), null=True, blank=True),
        null=True,
        blank=True,
    )
    # checkout_text = models.TextField(_("Check Out Text"), null=True, blank=True)
    engineer_fk = models.ForeignKey(
        "user.CustomerUser",
        verbose_name=_("Engineer FK"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="enginner_fk_user",
    )
    visit_date = ArrayField(
        models.DateField(_("Visit Date"), null=True, blank=True), null=True, blank=True
    )
    # next_visit_date = models.DateField(_("Next Visit Date"), null=True, blank=True)
    ticket_fk = models.ForeignKey(
        "ticket.Ticket",
        verbose_name=_("Ticket Fk"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ticket_engineer",
    )
    is_assign = models.BooleanField(_("Is Assign"), default=True)
    site_check_in = models.BooleanField(_("Site Check In"), default=False)
    longitude = models.FloatField(_("Longitude"), null=True, blank=True)
    letitude = models.FloatField(_("Longitude"), null=True, blank=True)

    def __str__(self):
        return str(self.ticket_fk)


class Installation(models.Model):
    ticket_fk = models.OneToOneField(
        Ticket,
        verbose_name=_("Ticket FK"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ticket_installation",
    )
    work_order_no = models.CharField(_("Work Order No"), max_length=50)
    packing_slip_no = models.CharField(_("Packing Slip No"), max_length=50)
    receive_in_good_condition = models.BooleanField(_("Received in Good Condition"))
    equipement_brief = models.TextField(_("Equipement Brief"))
    product_trial_readliness_date = models.DateField(
        _("Product Trial Date"), default=now
    )
    # pre_installation_checklist = models.CharField(
    #     _("Pre Installation Checklist"),
    #     choices=PreInstallationChecklistChoice.choices,
    #     max_length=50,
    #     default="pending",
    # )
    pending = models.BooleanField(_("Pending"), default=False)
    ready = models.BooleanField(_("Ready"), default=False)
    during_enginner_visit = models.BooleanField(
        _("During Engineer Visit"), default=False
    )
    not_understood_list = models.BooleanField(_("Not Understood List"), default=False)
    further_guideliness_needed = models.BooleanField(
        _("Further Guideliness Needed"), default=False
    )

    # address = models.TextField(_("Address"))

    def __str__(self):
        return str(self.id)


class SalesInquiry(models.Model):
    ticket_fk = models.OneToOneField(
        Ticket,
        verbose_name=_("Ticket FK"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ticket_sales_inquiry",
    )
    inquiry_brief = models.TextField(_("Inquiry Brief"))
    process_type = models.CharField(_("Process Type"), max_length=50)
    max_kg = models.IntegerField(_("MAX KG"))

    def __str__(self):
        return str(self.id)


class Spares(models.Model):
    ticket_fk = models.OneToOneField(
        Ticket,
        verbose_name=_("Ticket FK"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ticket_spares",
    )
    # equipement_name = models.CharField(_("Name"), max_length=50)
    # equipement_model_no = models.CharField(_("Model Name"), max_length=50)
    # equipement_sr_no = models.CharField(_("SR No"), max_length=50)
    courier_name = models.CharField(
        _("Courier Name"), max_length=50, null=True, blank=True
    )
    courier_mobile = PhoneNumberField(_("Phone Number"), null=True, blank=True)
    courier_docket_no = models.CharField(
        _("Docket NO"), max_length=50, null=True, blank=True
    )
    document_no = models.CharField(
        _("Document Number"), max_length=50, null=True, blank=True
    )
    dispach_date = models.DateField(_("Dispach Date"), null=True, blank=True)
    is_hq_verified = models.BooleanField(_("Is HQ Verified"), default=False)
    is_region_cordinator_varified = models.BooleanField(
        _("Is Region Coordinator Verified"), default=False
    )
    is_ready_to_pack = models.BooleanField(_("Is Ready to Pack"), default=False)
    is_store_updator_verified = models.BooleanField(
        _("Is Store Updator Verified"), default=False
    )
    hq_user_fk = models.ForeignKey(
        "user.CustomerUser",
        verbose_name=_("HQ FK"),
        related_name="hq_spares_user",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    region_co_user_fk = models.ForeignKey(
        "user.CustomerUser",
        verbose_name=_("Region CO FK"),
        related_name="region_spares_user",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    production_user_fk = models.ForeignKey(
        "user.CustomerUser",
        verbose_name=_("Production FK"),
        related_name="production_spares_user",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    purchase_user_fk = models.ForeignKey(
        "user.CustomerUser",
        verbose_name=_("Purchase FK"),
        related_name="purchase_spares_user",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    store_user_fk = models.ForeignKey(
        "user.CustomerUser",
        verbose_name=_("Store Updator FK"),
        related_name="store_spares_user",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    dispacher_user_fk = models.ForeignKey(
        "user.CustomerUser",
        verbose_name=_("Dispacher FK"),
        related_name="dispacher_spares_user",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    logistic_user_fk = models.ForeignKey(
        "user.CustomerUser",
        verbose_name=_("Logistic FK"),
        related_name="logistic_spares_user",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    dispacher_status = models.CharField(
        _("Dispacher Status"),
        choices=DispacherStatusChoices.choices,
        max_length=50,
        null=True,
        blank=True,
    )

    def __str__(self):
        return str(self.id)


class SpareDetail(models.Model):
    spare = models.ForeignKey(
        "ticket.Spares", verbose_name=_("Spares FK"), on_delete=models.CASCADE
    )
    part_name = models.CharField(_("Part Name"), max_length=100)
    part_desciption = models.TextField(_("Part Description"))
    qunatity = models.IntegerField(_("Quantity"))
    spare_status = models.CharField(
        _("Spare Status"),
        choices=SparesStatusChoices.choices,
        max_length=100,
        null=True,
        blank=True,
    )
    department_status = models.CharField(
        _("Department Status"),
        choices=DepartmentStatusChoices.choices,
        max_length=100,
        null=True,
        blank=True,
    )


class SpareBox(models.Model):
    spare = models.ForeignKey(
        "ticket.Spares", verbose_name=_("Spares FK"), on_delete=models.CASCADE
    )
    box_size = models.IntegerField(_("Box Size"), null=True, blank=True)
    box_quantity = models.IntegerField(_("Box Size"), null=True, blank=True)
    box_weight = models.IntegerField(_("Box Size"), null=True, blank=True)


class Service(models.Model):
    ticket_fk = models.OneToOneField(
        Ticket,
        verbose_name=_("Ticket FK"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ticket_service",
    )
    # equipement_name = models.CharField(_("Equipment Name"), max_length=50)
    # equipment_sr_no = models.CharField(_("Equipment SR No"), max_length=50)
    # equipment_model_no = models.CharField(_("Equipment Model No"), max_length=50)
    problem_brief = models.TextField(_("Problem Brief"))
    # production_status = models.CharField(
    #     _("Production Status"),
    #     choices=ProductionStatusChoice.choices,
    #     max_length=50,
    #     default="pending",
    # )
    temporary_running = models.BooleanField(_("Temporary Running"), default=False)
    running_with_rejection = models.BooleanField(_("Running with rejection"), default=False)
    breakdown = models.BooleanField(_("Breakdown"), default=False)

    def __str__(self):
        return str(self.id)


class OtherService(models.Model):
    ticket_fk = models.OneToOneField(
        Ticket,
        verbose_name=_("Ticket FK"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ticket_other",
    )
    equipment_name = models.CharField(_("Eqipment Name"), max_length=50)
    quary_brief = models.TextField(_("Quary brief"))

    # ticket_no = models.IntegerField(_("Ticket No"))
    # customer_name = models.CharField(_("Customer Name"), max_length=50)
    # serial_no = models.IntegerField(_("Serial No"))
    # equipment_serial_no = models.IntegerField(_("Equipment Serial No"))
    # equipment_model_no = models.IntegerField(_("Equipment Model No"))
    # part_name = models.CharField(_("Part Name"), max_length=100)
    # part_desciption = models.TextField(_("Part Description"))
    # qunatity = models.IntegerField(_("Quantity"))

    def __str__(self):
        return str(self.id)


class Repair(models.Model):
    ticket_fk = models.OneToOneField(
        Ticket,
        verbose_name=_("Ticket FK"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ticket_repair",
    )
    # machine_name = models.CharField(_("Machine Name"), max_length=80)
    # machine_sr_no = models.CharField(_("Machine Sr No"), max_length=50)
    # machine_model_no = models.CharField(_("Machine Model No"), max_length=50)
    courier_name = models.CharField(_("Courier Name"), max_length=50)
    courier_mobile_no = PhoneNumberField(_("Courier Mobile Number"))
    invert_number = models.CharField(
        _("Invert Number"), max_length=50, null=True, blank=True
    )
    date = models.DateField(_("Date"), null=True, blank=True)
    verify_from_store_updater = models.BooleanField(
        _("Verify From Store Updator"), default=False
    )

    def __str__(self):
        return str(self.id)


# class Attachment(models.Model):
#     ticket_fk = models.ForeignKey(
#         Ticket,
#         verbose_name=_("Ticket FK"),
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#     )
#     file = models.URLField(_("File url"))

#     def __str__(self):
#         return str(self.id)


# # class TeamMembers(models.Model):
# #     user_fk = models.ForeignKey(
# #         User, verbose_name=_("User FK"), on_delete=models.SET_NULL
# #     )
# #     ticket_fk = models.ForeignKey(
# #         Ticket, verbose_name=_("Ticket FK"), on_delete=models.SET_NULL
# #     )
# #     check_in_timestamp = models.DateTimeField(
# #         _("Check IN"), auto_now=False, auto_now_add=False
# #     )
# #     check_out_timestamp = models.DateTimeField(
# #         _("Check Out"), auto_now=False, auto_now_add=False
# #     )
# #     checkout_text = models.TextField(_("Check Out Text"), null=True, blank=True)
# #     last_status = models.TextField(_("Last Status"), null=True, blank=True)

# #     visit_date = models.DateField(_("Visit Date"), auto_now=False, auto_now_add=False)
# #     next_visit_date = models.DateField(
# #         _("Next Visit Date"), auto_now=False, auto_now_add=False
# #     )


# class Review(models.Model):
#     ticket_fk = models.ForeignKey(
#         Ticket,
#         verbose_name=_("Ticket FK"),
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#     )
#     user_fk = models.ForeignKey(
#         "user.User",
#         verbose_name=_("User FK"),
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#     )
#     email = models.EmailField(_("Email Field"), max_length=254)
#     name = models.CharField(_("Name"), max_length=50)
#     phone = PhoneNumberField(_("Phone Number Field"))

#     def __str__(self):
#         return str(self.id)


# class Comment(models.Model):
#     comment_text = models.TextField(_("Comment text"))
#     ticket_fk = models.ForeignKey(
#         Ticket,
#         verbose_name=_("Ticket FK"),
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#     )
#     user_fk = models.ForeignKey(
#         "user.User",
#         verbose_name=_("User FK"),
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#     )
#     parent_fk = models.ForeignKey(
#         "self",
#         verbose_name=_("Parent FK"),
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#     )
#     like_count = models.IntegerField(_("Like Count"))
#     timestamp = models.DateTimeField(_("Timestamp"), auto_now=False, auto_now_add=False)

#     def __str__(self):
#         return str(self.id)


# class CustomerRating(models.Model):
#     user_fk = models.ForeignKey(
#         "user.User", verbose_name=_("User FK"), on_delete=models.SET_NULL, null=True, blank=True
#     )
#     ticket_fk = models.OneToOneField(
#         Ticket,
#         verbose_name=_("Ticket FK"),
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#     )
#     rating = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])

#     def __str__(self):
#         return str(self.user_fk)


# class Document(models.Model):
#     document_name = models.CharField(_("Document Name"), max_length=50)
#     document_file = models.FileField(_("Document File"), upload_to=None, max_length=100)


# # class Product(models.Model):
# #     name = models.CharField(_("Product Name"), max_length=50)
# #     description = models.TextField(_("Product Description"), null=True, blank=True)
# #     qr_image = models.ImageField(
# #         _("QR Image"),
# #         upload_to="media/QR",
# #         height_field=None,
# #         width_field=None,
# #         max_length=None,
# #         null=True,
# #         blank=True,
# #     )
# #     model_no = models.CharField(_("Model Number"), max_length=50)
# #     serial_no = models.CharField(_("Model Number"), max_length=50)
# #     is_active = models.BooleanField(_("Is Active"), default=True)
# #     updated_at = models.DateTimeField(_("Updated AT"), auto_now_add=True)
# #     created_at = models.DateTimeField(_("Created AT"), auto_now_add=True)

# #     def __str__(self):
# #         return str(self.name)

# #     @classmethod
# #     def post_create(cls, sender, instance, created, *args, **kwargs):
# #         if created:
# #             qr_image = qrcode.make(instance.id)
# #             qr_offset = Image.new("RGB", (310, 310), "white")
# #             ImageDraw.Draw(qr_offset)
# #             qr_offset.paste(qr_image)
# #             file_name = f"{instance.id}.png"
# #             stream = BytesIO()
# #             qr_offset.save(stream, "PNG")
# #             instance.qr_image.save(file_name, File(stream), save=False)
# #             qr_offset.close()
# #             instance.save()


# class CustomerWiseItem(models.Model):
#     customer_user = models.ForeignKey(
#         "user.CustomerUser", verbose_name=_("Customer User FK"), on_delete=models.CASCADE
#     )
#     item = models.ForeignKey(
#         "ticket.Item", verbose_name=_("Item FK"), on_delete=models.CASCADE
#     )
#     SerialNo = models.CharField(_("Serial No"), max_length=100)


# class CompanyProductItem(models.Model):
#     company = models.ForeignKey(
#         "user.Company", verbose_name=_("Company FK"), on_delete=models.CASCADE
#     )
#     product = models.ForeignKey(
#         "ticket.Product", verbose_name=_("Product FK"), on_delete=models.CASCADE
#     )
#     item = models.ManyToManyField("ticket.Item", verbose_name=_("Item FK"))
#     warranty = models.CharField(
#         _("Warranty"), choices=WarrantyChoices.choices, max_length=50
#     )
#     package_slip_no = models.CharField(_("Package Slip No"), max_length=100)

#     def __str__(self):
#         return str(self.product)


class CompanyTicketInstallationItemStatus(models.Model):
    ticket = models.ForeignKey(
        "ticket.Ticket", verbose_name=_("Ticket FK"), on_delete=models.CASCADE
    )
    customer_wise_item = models.ForeignKey(
        "ticket.CustomerWiseItem", verbose_name=_("Item Name"), on_delete=models.CASCADE
    )
    installation_problem_status = models.ForeignKey(
        "ticket.InstallationaProblemStatus",
        verbose_name=_("Installation Problem Status"),
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return str(self.id)


class FTCForm(models.Model):
    ftc_ticket = models.ForeignKey(
        "ticket.Ticket",
        verbose_name=_("FTC Ticket"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ftc_ticket_user",
    )
    ticket = models.ForeignKey(
        "ticket.Ticket",
        verbose_name=_("Ticket"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ticket_ticket",
    )
    problem_type = models.TextField(_("Problem Type"))
    suggestion = models.TextField(_("Suggestion"), null=True, blank=True)

    def __str__(self):
        return str(self.id)


class RCA(models.Model):
    category = models.ForeignKey(
        "ticket.RCACategory",
        verbose_name=_("RCA Category"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    rca_suggestion = models.TextField(_("RCA Suggestion"))
    rca_department = models.ManyToManyField(
        "ticket.RCADepartment", verbose_name=_("Rca Department FK")
    )
    ticket_fk = models.ForeignKey(
        Ticket,
        verbose_name=_("Ticket FK"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self):
        return str(self.id)


# class ReturnOldSpare(models.Model):
#     ticket_fk = models.ForeignKey(
#         Ticket,
#         verbose_name=_("Ticket FK"),
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#     )
#     add_return_condition = models.CharField(_("Add Return Condition"), max_length=50)

#     def __str__(self):
#         return str(self.id)


# class OldSpareDescription(models.Model):
#     return_old_spare_fk = models.ForeignKey(
#         ReturnOldSpare,
#         verbose_name=_("Return Old Spare FK"),
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#     )
#     item = models.CharField(_("Item"), max_length=50)
#     description = models.TextField(_("Description"))

#     def __str__(self):
#         return str(self.id)


class LastStatus(models.Model):
    ticket = models.ForeignKey(
        Ticket,
        verbose_name=_("Ticket"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    engineer = models.ForeignKey(
        "user.CustomerUser",
        verbose_name=_("Engineer"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    last_status = models.TextField(blank=True, null=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


# # class Item(models.Model):
# #     product = models.ForeignKey(
# #         Product,
# #         verbose_name=_("Product FK"),
# #         on_delete=models.SET_NULL,
# #         null=True,
# #         blank=True,
# #     )
# #     item_name = models.CharField(max_length=50, blank=True, null=True)
# #     item_description = models.TextField(_("Item Description"))
# #     is_active = models.BooleanField(_("Is Active"), default=True)
# #     updated_at = models.DateTimeField(_("Updated AT"), auto_now_add=True)
# #     created_at = models.DateTimeField(_("Created AT"), auto_now_add=True)

# #     def __str__(self):
# #         return str(self.item_name)


class FeedBack(models.Model):
    client = models.ForeignKey(
        "user.CustomerUser",
        verbose_name=_("Client FK"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="customer_feedback",
    )
    engineer = models.ForeignKey(
        "user.CustomerUser",
        verbose_name=_("Engineer FK"),
        on_delete=models.SET_NULL,
        related_name="engineer_feedback",
        null=True,
        blank=True,
    )
    ticket = models.ForeignKey(
        "ticket.Ticket",
        verbose_name=_("Ticket FK"),
        on_delete=models.SET_NULL,
        related_name="ticket_feedback",
        null=True,
        blank=True,
    )
    rank = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])
    feedback_text = models.TextField(_("Feedback Text"), null=True, blank=True)

    def __str__(self):
        return str(self.id)


class InstallationaProblemStatus(models.Model):
    name = models.CharField(
        _("Installation Status"),
        max_length=50,
    )
    type = models.CharField(
        _("Type of Ticket"), choices=TicketTypeChoice.choices, max_length=50
    )

    def __str__(self):
        return str(self.name)


class RCACategory(models.Model):
    name = models.CharField(_("Category"), max_length=50)

    def __str__(self):
        return str(self.name)


class RCADepartment(models.Model):
    rca_department = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return str(self.rca_department)


class Notification(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    date = models.DateField(auto_now_add=True)

    # user_fk = models.ForeignKey(
    #     "user.User",
    #     verbose_name=_("User FK"),
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     blank=True,
    # )

    def __str__(self):
        return str(self.title)


class ServiceReport(models.Model):
    ticket_fk = models.ForeignKey(
        "ticket.Ticket",
        verbose_name=_("Ticket FK"),
        on_delete=models.CASCADE,
        related_name="service_report_ticket",
    )
    due_days = models.IntegerField(_("Due Days"))
    warranty = models.CharField(_("Warranty"), max_length=50)
    customer_name = models.CharField(
        _("Customer Name"), max_length=50
    )  # because customer already included
    equipment_model_no = models.CharField(_("Equipment Model No"), max_length=50)
    equipment_sr_no = models.CharField(_("Equipment SR No"), max_length=50)
    work_order_no = models.CharField(_("Work Order No"), max_length=50)
    repeats = models.IntegerField(_("Repeats"))
    install_date = models.DateField(_("Install Date"))
    start_date = models.DateField(_("Start Date"))
    attend_date = models.DateField(_("Attend Date"))
    close_date = models.DateField(_("Close Date"))
    customer_complain = models.TextField(_("Customer Complain"))
    machine_alarm = models.CharField(_("Machine Alrm"), max_length=200)
    item_problem_type = models.ForeignKey(
        "ticket.ItemProblemType",
        verbose_name=_("Item Problem Type"),
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    electrical_supply = models.CharField(_("Electrical Supply"), max_length=200)
    earthing_neutral = models.CharField(_("Electrical Neutral"), max_length=200)
    pneumatic_supply = models.CharField(_("Electrical Neutral"), max_length=200)
    filter_condition = models.CharField(
        _("Filter Condition"), choices=FilterCondtion.choices, max_length=50
    )
    check_material_type = models.CharField(
        _("Check Material Type"), choices=CheckMatType.choices, max_length=50
    )
    check_machine_type_op = models.CharField(_("Check Machine Type OP"), max_length=50)
    corrective_action = models.CharField(_("Corrective Action"), max_length=50)
    production_trial_observation = models.CharField(
        _("Production Trial Observation"), max_length=50
    )
    # added
    service_chargeable = models.BooleanField(_("Service Chargeable"), default=False)
    pricing = models.CharField(_("Pricing"), max_length=100, null=True, blank=True)
    # date = models.DateField(_("Date"))
    machine_op = models.CharField(_("Machine Type"), max_length=50)
    # add water supply here
    water_supply = models.CharField(_("Water Supply"), max_length=50)
    root_cause = models.CharField(_("Root Cause"), max_length=50)
    training_imparted = models.CharField(_("Training Imparted"), max_length=50)
    verified_by_customer = models.BooleanField(_("Verified By Customer"), default=False)

    def __str__(self):
        return str(self.id)


class ServiceReportPart(models.Model):
    service_report = models.ForeignKey(
        "ticket.ServiceReport",
        verbose_name=_("Service Report"),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    part = models.ForeignKey(
        "ticket.ItemSpare", verbose_name=_("Item Spare FK"), on_delete=models.CASCADE
    )
    action = models.CharField(
        _("Action"), choices=ServicePartAction.choices, max_length=50
    )

    def __str__(self):
        return str(self.service_report)


class FAQ(models.Model):
    title = models.CharField(_("Title"), max_length=50)
    description = models.TextField(_("Description"))
    faq_type = models.CharField(
        _("faq_type"), choices=FaqTypeChoices.choices, max_length=50
    )

    def __str__(self):
        return str(self.title)


class ItemProblemType(models.Model):
    name = models.CharField(max_length=100)
    item = models.ForeignKey(
        "ticket.Item", verbose_name=_("Item FK"), on_delete=models.CASCADE
    )

    def __str__(self):
        return str(self.name)


class Item(models.Model):
    ItemCode = models.CharField(_("Item Code"), max_length=500)
    ItemName = models.CharField(_("Item Name"), max_length=500)
    ItemDescription = models.TextField(_("Item Description"), null=True, blank=True)
    ItemDescription2 = models.TextField(_("Item Description"), null=True, blank=True)
    SalesUOM = models.CharField(_("Sales UOM"), max_length=500, null=True, blank=True)
    FrgnName = models.CharField(_("Frgn Name"), max_length=500, null=True, blank=True)
    ItmsGrpCod = models.CharField(
        _("Itms Grp Cod"), max_length=200, null=True, blank=True
    )
    CstGrpCode = models.CharField(
        _("Cst Grp Code"), max_length=100, null=True, blank=True
    )
    ItemType = models.CharField(_("Item Type"), max_length=200, null=True, blank=True)
    Series = models.CharField(_("Series"), max_length=100, null=True, blank=True)
    qr_image = models.ImageField(
        _("QR Image"),
        upload_to="media/QR",
        height_field=None,
        width_field=None,
        max_length=None,
        null=True,
        blank=True,
    )
    # model_no = models.CharField(_("Model Number"), max_length=50)
    # serial_no = models.CharField(_("Model Number"), max_length=50)
    is_active = models.BooleanField(_("Is Active"), default=True)
    updated_at = models.DateTimeField(_("Updated AT"), auto_now_add=True)
    created_at = models.DateTimeField(_("Created AT"), auto_now_add=True)

    def __str__(self):
        return str(self.ItemName)

    @classmethod
    def post_create(cls, sender, instance, created, *args, **kwargs):
        if created:
            qr_image = qrcode.make(instance.id)
            qr_offset = Image.new("RGB", (310, 310), "white")
            ImageDraw.Draw(qr_offset)
            qr_offset.paste(qr_image)
            file_name = f"{instance.id}.png"
            stream = BytesIO()
            qr_offset.save(stream, "PNG")
            instance.qr_image.save(file_name, File(stream), save=False)
            qr_offset.close()
            instance.save()


post_save.connect(Item.post_create, sender=Item)


class ItemSpare(models.Model):
    item = models.ForeignKey(
        "ticket.Item", verbose_name=_("Item FK"), on_delete=models.CASCADE
    )
    spare_name = models.CharField(_("Spare Name"), max_length=200)


class CustomerWiseItem(models.Model):
    item = models.ForeignKey(
        "ticket.Item", verbose_name=_("Item FK"), on_delete=models.CASCADE
    )
    customer_user = models.ForeignKey(
        "user.CustomerUser", verbose_name=_("Customer User FK"), on_delete=models.CASCADE
    )
    SerialNo = models.CharField(_("Serial No"), max_length=100)
    QTY = models.IntegerField(_("Quantity"))
    InvoiceNo = models.CharField(_("Invoice No"), max_length=50)
    InvoiceDate = models.DateField(_("Invoice Date"), default=now)
    packing_slip_no = models.CharField(_("Packing Slip No"), max_length=50)
    dispach_date = models.DateField(_("Dispach date"), default=now)
    work_order_no = models.CharField(_("Work Order No"), max_length=50)


class ReturnSpare(models.Model):
    ticket_fk = models.OneToOneField(
        "ticket.Ticket",
        verbose_name=_("Ticket FK"),
        on_delete=models.CASCADE,
        related_name="return_spare_ticket",
    )

    courier_name = models.CharField(
        _("Courier Name"), max_length=50, null=True, blank=True
    )
    courier_mobile = PhoneNumberField(_("Phone Number"), null=True, blank=True)
    invert_date = models.DateField(_("Invert Date"), null=True, blank=True)
    invert_number = models.IntegerField(_("Invert Number"), null=True, blank=True)

    def __str__(self):
        return self.id


class ReturnSpareDetail(models.Model):
    returnspare_fk = models.ForeignKey(
        ReturnSpare,
        verbose_name=_("ReturnSpare FK"),
        on_delete=models.CASCADE,
        related_name="return_spare_detail_return_spare",
    )
    return_spare_status = models.CharField(
        _("Return Spare Status"),
        choices=ReturnSpareStatusChoices.choices,
        max_length=20,
        null=True,
        blank=True,
    )
    spares_fk = models.ForeignKey(
        "ticket.Spares", verbose_name=_("Spares FK"), on_delete=models.CASCADE
    )


class Document(models.Model):
    item = models.ForeignKey(Item, verbose_name=_("Item QR"), on_delete=models.CASCADE)
    document = models.FileField(_("PDF File"), upload_to="media/pdf", max_length=100)

    def __str__(self):
        return str(self.item)


# ------------------------Installation Report------------------------

class InstallationReport(models.Model):
    ticket_fk = models.ForeignKey(
        "ticket.Ticket",
        verbose_name=_("Ticket FK"),
        on_delete=models.CASCADE,
        related_name="installation_report_ticket",
    )
    customer_name = models.CharField(
        _("Customer Name"), max_length=50
    )  # because customer already included
    location = models.CharField(_("Location"), max_length=200, null=True, blank=True)
    customer_mc_type = models.CharField(
        _("Customer Mc Type"), choices=McTypeChoices.choices, max_length=100, null=True, blank=True)
    customer_mc = models.CharField(_("Customer Mc"), max_length=50, null=True, blank=True)
    customer_application = models.CharField(_("Customer Application"), max_length=50, null=True, blank=True)
    Customer_mc_max_kg_hr = models.CharField(_("Customer M/c Max Kg/hr "), max_length=50, null=True, blank=True)
    packing_slip_no = models.CharField(_("Packing Slip No"), max_length=50, null=True, blank=True)
    install_date = models.DateField(_("Install Date"), null=True, blank=True)
    start_date = models.DateField(_("Start Date"), null=True, blank=True)
    attend_date = models.DateField(_("Attend Date"), null=True, blank=True)
    close_date = models.DateField(_("Close Date"), null=True, blank=True)
    installation_procedure = models.CharField(_("Installation Procedure"), max_length=200, null=True, blank=True)
    trial_observations = models.CharField(_("Installation Procedure"), max_length=200, null=True, blank=True)
    recommendations = models.CharField(_("Installation Procedure"), max_length=200, null=True, blank=True)
    voltage_ry = models.CharField(_("Voltage RY"), max_length=50, null=True, blank=True)
    voltage_br = models.CharField(_("Voltage BR"), max_length=50, null=True, blank=True)
    voltage_yb = models.CharField(_("Voltage YB"), max_length=50, null=True, blank=True)
    voltage_earth_neutral = models.CharField(_("Voltage Earth-Neutral"), max_length=50, null=True, blank=True)
    air_connection = models.CharField(_("Pneumatic Air"), max_length=50, null=True, blank=True)
    water_connection = models.CharField(_("Water Connection"), max_length=50, null=True, blank=True)
    production_trial_kg_hr = models.CharField(_("Production Trial Kg/hr"), max_length=50, null=True, blank=True)
    production_quality = models.CharField(_("Production Quality"), max_length=50, null=True, blank=True)

    # verified_by_customer = models.BooleanField(_("Verified By Customer"), default=False)
    # added
    # service_chargeable = models.BooleanField(_("Service Chargeable"))
    # pricing = models.CharField(_("Pricing"), max_length=100)

    def __str__(self):
        return str(self.id)


class InstallationReportPart(models.Model):
    Installation_report = models.ForeignKey(
        "ticket.InstallationReport",
        verbose_name=_("Installation Report"),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    item = models.ForeignKey(
        "ticket.Item", verbose_name=_("Item FK"), on_delete=models.CASCADE
    )
    installation_problem_status = models.ForeignKey(
        "ticket.InstallationaProblemStatus",
        verbose_name=_("Installation Problem Status"),
        on_delete=models.CASCADE,
    )

    serial_no = models.CharField(verbose_name="SerialNo", max_length=500, null=True, blank=True)

    # action = models.CharField(
    #     _("Installation Status"), choices=InstallationStatusItemChoice.choices, max_length=100
    # )

    def __str__(self):
        return str(self.id)
