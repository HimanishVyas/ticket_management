from django.db import models
from django.utils.translation import gettext_lazy as _


class StatusChoices(models.TextChoices):
    ACTIVE = "active", _("Active")
    PENDING = "pending", _("Pending")
    DEACTIVE = "deactive", _("Deactive")


class UserRoleChoices(models.IntegerChoices):
    ADMIN = 1, _("Admin")
    CLIENT = 2, _("Client")
    ENGINEER = 3, _("Enginner")
    REGION_IN_CHARGE = 4, _("Region in charge")
    HQ_IN_CHARGE = 5, _("HQ in charge")
    REGION_TEAM = 6, _("Region Team")
    HQ_TEAM = 7, _("HQ Team")
    CALL_UPDATER = 8, _("Call Updater")
    REGION_COORDINATOR = 9, _("Region Coordinator")
    DISPATCH_UPDATER = 10, _("Dispatch Updater")
    COORDINATOR_TEAM = 11, _("Coordinator Team")
    CUSTOMER_OPERATOR = 12, _("Customer Operator")
    CUSTOMER_MANAGER = 13, _("Customer Manager")
    CUSTOMER_OWNER = 14, _("Customer Owaner")
    CUSTOMER_OEM = 15, _("Customer OEM")
    TEL_ENGINEER = 16, _("Tel Engineer")
    VISIT_ENGINEER = 17, _("Visit Engineer")
    REGION_SERVICE_IN_CHARGE = 18, _("Region Service In Charge")
    STORE_UPDATER = 19, _("Store Updater")
    PRODUCTION_UPDATER = 20, _("Production Updater")
    PURCHASE_UPDATER = 21, _("Purchase Updater")
    ASST_MANAGER = 22, _("Asst Manager")
    MANAGER = 23, _("Manager")
    DIRECTOR = 24, _("Director")
    TESTING_IN_CHARGE = 25, _("Testing In Charge")
    QUALITY_MANAGER = 26, _("Quality Manager")
    LOGISTIC_TEAM = 27, _("Logistic Team")


class PlaceChoice(models.TextChoices):
    HOME = "home", _("Home")
    WORK = "work", _("Work")
