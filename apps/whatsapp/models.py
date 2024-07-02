import re

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from apps.ticket.utilities.choices import QueryTypeChoice, InstallationDropDownChoice, ServiceDropDownChoice


def validate_phone_number(value):
    if not re.match(r"^[\d\-\s]+$", value):
        raise ValidationError(
            "Invalid phone number. Phone numbers can only contain digits, dashes, and spaces."
        )


# Create your models here.
# class WhatsappTempData(models.Model):
#     mobile = PhoneNumberField(_("Phone Number"), unique=True)

#     key = ArrayField(
#         models.CharField(null=True, blank=True, max_length=100), null=True, blank=True
#     )
#     ticket_type = models.IntegerField(_("Ticket Type"), blank=True, null=True)
#     field_number = models.IntegerField(_("Field Number"), blank=True, null=True)
#     msg_step = models.IntegerField(_("MSG Step"), default=0)
#     data = ArrayField(
#         models.CharField(null=True, blank=True, max_length=100), null=True, blank=True
#     )


# class MessageTracking(models.Model):
#     mobile = PhoneNumberField(_("Phone Number"))
#     msg_step = models.IntegerField(_("MSG Step"),default=0)


class Ticket(models.Model):
    current_mobile_no = PhoneNumberField(_("Phone Number Field"), unique=True)
    is_saved = models.BooleanField(_("Is Saved"), default=False)
    ticket_type = models.PositiveSmallIntegerField(
        _("Query Type"),
        choices=QueryTypeChoice.choices,
        null=True,
        blank=True,
        validators=[MaxValueValidator(6), MinValueValidator(1)],
    )
    # mobile_no = models.CharField(_("Phone number"), max_length=15)
    # address = models.TextField(_("Address "))
    # is_guest = models.BooleanField(_("Is Guest"), default=True)
    # customer_fk = models.ForeignKey(
    #     "user.user",
    #     verbose_name=_("User FK"),
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     blank=True,
    # )

    # mobile_no = models.CharField(max_length=20, null=True, blank=True)

    mobile_no = models.CharField(
        max_length=20, null=True, blank=True, validators=[validate_phone_number]
    )

    address = models.TextField(null=True, blank=True)

    create_more_time = models.BooleanField(_("Created More Time"), default=False)

    # ticket_status = models.CharField(
    #     _("Ticket Status"),
    #     choices=TicketStatusChoices.choices,
    #     max_length=50,
    #     default="pending",
    # )
    # raise_date = models.DateField(_("Raise Date"), auto_now_add=True)
    # ticket_close_date = models.DateField(_("Ticket Close Date"), null=True, blank=True)
    # ticket_assign_date = models.DateField(_("Ticket Assign Date"), null=True, blank=True)
    # company_product_item = models.ForeignKey(
    #     "ticket.CompanyProductItem",
    #     verbose_name=_("CompanyProductItem FK"),
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     blank=True,
    # )
    # company = models.ForeignKey(
    #     "user.Company", verbose_name=_("Company FK"), on_delete=models.CASCADE
    # )
    # is_ftc_ticket = models.BooleanField(_("IS FTC Ticket"), default=False)

    def __str__(self):
        return str(self.id)


class Installation(models.Model):
    ticket_fk = models.OneToOneField(
        Ticket,
        verbose_name=_("Ticket FK"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ticket_installation",
    )
    work_order_no = models.CharField(
        _("Work Order No"), null=True, blank=True, max_length=50
    )
    packing_slip_no = models.CharField(
        _("Packing Slip No"), null=True, blank=True, max_length=50
    )
    receive_in_good_condition = models.BooleanField(
        _("Received in Good Condition"),
        null=True,
        blank=True,
    )
    equipement_brief = models.TextField(
        _("Equipement Brief"),
        null=True,
        blank=True,
    )
    product_trial_readliness_date = models.DateField(
        _("Product Trial Date"), null=True, blank=True
    )
    # pre_installation_checklist = models.CharField(
    #     _("Pre Installation Checklist"),
    #     choices=PreInstallationChecklistChoice.choices,
    #     max_length=50,
    #     default="pending",
    # )
    # pending = models.BooleanField(
    #     _("Pending"),
    #     null=True,
    #     blank=True,
    # )
    # ready = models.BooleanField(
    #     _("Ready"),
    #     null=True,
    #     blank=True,
    # )
    # during_enginner_visit = models.BooleanField(
    #     _("During Engineer Visit"), null=True, blank=True
    # )
    # not_understood_list = models.BooleanField(
    #     _("Not Understood List"),
    #     null=True,
    #     blank=True,
    # )
    # further_guideliness_needed = models.BooleanField(
    #     _("Further Guideliness Needed"), null=True, blank=True
    # )

    installation_drop_down = models.CharField(_("Installation drop down"),
                                              choices=InstallationDropDownChoice.choices, default=None, null=True,
                                              blank=True)

    # address = models.TextField(_("Address"))

    def __str__(self):
        return str(self.id)


class WhatsappMsg(models.Model):
    key = models.CharField(_("Whatsapp Key"), max_length=50)
    msg = models.TextField(_("message description"))

    def __str__(self) -> str:
        return self.key


class SalesInquiry(models.Model):
    ticket_fk = models.OneToOneField(
        Ticket,
        verbose_name=_("Ticket FK"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    inquiry_brief = models.TextField(
        _("Inquiry Brief"),
        null=True,
        blank=True,
    )
    process_type = models.CharField(
        _("Process Type"),
        max_length=50,
        null=True,
        blank=True,
    )
    max_kg = models.IntegerField(
        _("MAX KG"),
        null=True,
        blank=True,
    )

    def __str__(self):
        return str(self.id)


class OtherService(models.Model):
    ticket_fk = models.OneToOneField(
        Ticket,
        verbose_name=_("Ticket FK"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    equipment_name = models.CharField(
        _("Eqipment Name"), max_length=50, null=True, blank=True
    )
    query_brief = models.TextField(
        _("Query brief"),
        null=True,
        blank=True,
    )

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
    )
    SerialNo = models.CharField(_("Serial No"), max_length=100, null=True, blank=True)
    # machine_name = models.CharField(_("Machine Name"), max_length=80)
    # machine_sr_no = models.CharField(_("Machine Sr No"), max_length=50)
    # machine_model_no = models.CharField(_("Machine Model No"), max_length=50)
    courier_name = models.CharField(
        _("Courier Name"),
        max_length=50,
        null=True,
        blank=True,
    )
    # courier_mobile_no = PhoneNumberField(
    #     _("Courier Mobile Number"),
    #     null=True,
    #     blank=True,
    # )
    courier_mobile_no = models.CharField(
        max_length=20, validators=[validate_phone_number]
    )

    def __str__(self):
        return str(self.id)


class Service(models.Model):
    ticket_fk = models.OneToOneField(
        Ticket,
        verbose_name=_("Ticket FK"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    SerialNo = models.CharField(_("Serial No"), max_length=100, null=True, blank=True)
    # equipement_name = models.CharField(_("Equipment Name"), max_length=50)
    # equipment_sr_no = models.CharField(_("Equipment SR No"), max_length=50)
    # equipment_model_no = models.CharField(_("Equipment Model No"), max_length=50)
    problem_brief = models.TextField(_("Problem Brief"), null=True, blank=True)
    # production_status = models.CharField(
    #     _("Production Status"),
    #     choices=ProductionStatusChoice.choices,
    #     max_length=50,
    #     default="pending",
    # )
    # temporary_running = models.BooleanField(
    #     _("Temporary Running"),
    #     null=True,
    #     blank=True,
    # )
    # running_with_rejection = models.BooleanField(
    #     _("Running with Rejection"), null=True, blank=True
    # )
    # breakdown = models.BooleanField(
    #     _("BreakDown"),
    #     null=True,
    #     blank=True,
    # )
    service_drop_down = models.CharField(_("Service drop down"),
                                         choices=ServiceDropDownChoice.choices, default=None, null=True,
                                         blank=True)

    def __str__(self):
        return str(self.id)


class SpareDetail(models.Model):
    ticket_fk = models.ForeignKey(
        Ticket, verbose_name=_("Spares FK"), on_delete=models.CASCADE
    )

    part_name = models.CharField(_("Part Name"), max_length=100, null=True, blank=True)
    part_desciption = models.TextField(_("Part Description"), null=True, blank=True)
    qunatity = models.IntegerField(_("Quantity"), null=True, blank=True)
    add_another_record = models.BooleanField(
        _("Add Another Part"), null=True, blank=True
    )
