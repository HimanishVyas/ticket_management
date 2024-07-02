from django.db import models
from django.utils.translation import gettext_lazy as _


class QueryTypeChoice(models.IntegerChoices):
    INSTALLATION = 1, _("Installation")
    SERVICE = 2, ("Service")
    SPARES = 3, ("Spares")
    SALES_INQUIRY = 4, ("Sales_inquiry")
    OTHERS = 5, ("Others")
    REPAIR = 6, ("Repair")
    RETURN_SPARE = 7, ("Return Spare")


class InstallationDropDownChoice(models.IntegerChoices):
    PENDING = 1, _("Pending")
    READY = 2, ("Ready")
    DURING_ENGINNER_VISIT = 3, ("During engineer visit")
    NOT_UNDERSTOOD_LIST = 4, ("Not understood list")
    FURTHER_GUIDELINES_NEEDED = 5, ("Further guidelines needed")


class ServiceDropDownChoice(models.IntegerChoices):
    TEMPORARY_RUNNING = 1, _("Temporary Running")
    RUNNING_WITH_REJECTION = 2, ("Running With Rejection")
    BREAKDOWN = 3, ("Breakdown")


class PriorityChoice(models.TextChoices):
    LOW = "low", ("Low")
    MEDIUM = "medium", ("Medium")
    HIGH = "high", _("High")


class PreInstallationChecklistChoice(models.TextChoices):
    PENDING = "pending", _("Pending")
    READY = "ready", _("Ready")
    DURING_ENGG_VISIT = "during_engg_visit", _("During Engg Visit")
    NOT_UNDERSTOOD_LIST = "not_understood_list", _("Not Understood List")
    FURTHER_TECH_GUIDANCE_NEED = "further_tech_guidence_need", _(
        "Further Tech Guidance Need"
    )


class ProductionStatusChoice(models.TextChoices):
    TEMPORARY_RUNNIG = "temporary_running", _("Temporary Running")
    RUNNIG_WITH_REJECTION = "running_with_rejection", _("Running With Rejection")
    BREAKDOWN = "breakdown", _("Breakdown")


class TicketStatusChoices(models.TextChoices):
    WAITING = "waiting", _("Waiting")
    PENDING = "pending", _("Pending")
    ON_CALL = "on_call", _("On Call")
    WAITING_FOR_SPARES = "waiting_for_spares", _("Waiting For Spares")
    SCHEDULE = "schedule", _("Schedule")
    # IN_PROGRESS = "in_progress", ("In Progress")
    COMPLETE = "complete", _("Complete")
    CLOSE = "close", _("Close")


class FTCChoice(models.TextChoices):
    OPEN = "open", _("Open")
    CLOSE = "close", _("Close")
    UNDEROBSERVATION = "underobservation", _("Under Observation")


class RCACategoryChoice(models.TextChoices):
    PART_FAILURE = "part_failure", _("part failure")
    MAINTENANCE = "maintenance", _("Maintenance")
    PERFORMANCE = "performance", _("Performance")
    MISCELLENEOUS = "miscelleneous", _("Miscelleneous")
    CUSTOMERSIDE_PROBLEM = "customerside_problem", _("Customerside Problem")
    INADEQUATE_TRAINING = "inadequate_training", _("Inadequate Training")
    QUALITY_ISSUE = "quality_issue", _("Quality Issue")
    APPLICATION_MISMATCH = "application_mismatch", _("Application Mismatch")
    TRANS_DAMAGE = "trans_damage", _("Trans Damage")
    DESIGN_DEFECT = "design_defect", _("Design Defect")
    POOR_WORKMANSHIP = "poor_workmanship", _("Poor Workmanship")
    SHORT_SUPPLY = "short_supply", _("Short Supply")
    WRONG_SUPPLY = "wrong_supply", _("Wrong Supply")
    PRODUCTION_ASSEM = "production_assem", _("Production Assem")
    ADITIONAL_REQIREMENT = "aditional_reqirement", _("Aditional Reqirement")
    CUSTOMER_APPLACTION = "customer_applaction", _("Customer Applaction")
    PREVENTIVE_MAINT = "preventive_maint", _("Preventive Maint")


class RCADepartmentChoice(models.TextChoices):
    ELECTRICAL_DESIGN = "electrical_design", _("electrical_design")
    SERVICE = "Service", _("Service")
    PURCHASE = "purchase", _("purchase")
    STORE_DEPARTMENT = "store_department", _("store_department")
    PRODUCTION = "production", _("production")
    SALES = "sales", _("sales")
    FABRICATION = "fabrication", _("fabrication")
    CUSTOMER_SIDE = "customer_side", _("customer_side")
    QUALITY = "quality", _("quality")
    APP_DEPARTMENT = "app_department", _("app_department")


class InstallationStatusItemChoice(models.TextChoices):
    APPLICATION_MISMATCH = "application_mismatch", _("Application Miss Match")
    CUSTOMER_APPLACTION = "customer_applaction", _("Customer Applaction")
    CUSTOMERSIDE_PROBLEM = "customerside_problem", _("Customerside Problem")
    DESIGN_DEFECT = "design_defect", _("Design Defect")
    POOR_WORKMANSHIP = "poor_workmanship", _("Poor Workmanship")
    PRODUCTION_ASSEM = "production_assem", _("Production Assem")
    QUALITY_ISSUE = "quality_issue", _("Quality Issue")
    SHORT_SUPPLY = "short_supply", _("Short Supply")
    TRANS_DAMAGE = "trans_damage", _("Trans Damage")
    WRONG_SUPPLY = "wrong_supply", _("wrong_supply")
    UNPACKED = "unpacked", _("Unpacked")
    SUBASSEMBLY_DONE = "subassembly_done", _("Subassembly Done")
    ERECTION_DONE = "erection_done", _("Erection Done")
    SUPPLY_UTILITY_CONNECTED = "supply_utility_connected", _("Supply Utility Connected")
    NOLOAD_TRIAL_DONE = "noload_trial_done", _("Noload Trial Done")
    JOB_TRIAL_DONE = "job_trial_done", _("Job Trial Done")
    WAITING_FOR_OEM = "waiting_for_oem_m/c", _("Waiting for OEM m/c")
    WAITING_FOR_CUSTOMER_SUPPLY_UTILITIES = "waiting_for_customer_supply_utilities", _(
        "Waiting for Customer Supply Utilities"
    )
    WAITING_FOR_ROW_MATERIAL = "waiting_for_row_material", _("Waiting for Row Material")
    WAITING_FOR_JOB_TRIAL = "waiting_for_job_trial", _("Waiting for Job Trial")


class TicketTypeChoice(models.TextChoices):
    FTC = "ftc", _("FTC")
    NORMAL = "normal", _("Normal")


class ServicePartAction(models.TextChoices):
    ADJUST = "adjust", _("Adjust")
    REPAIR = "repair", _("Repair")
    REPLACE = "replace", _("Replace")
    CLEAN = "clean", _("Clean")


class FilterCondtion(models.TextChoices):
    OK = "ok", _("Ok")
    NOT_CLEAN = "not clean", _("Not Clean")
    DAMAGE = "damage", _("Damage")


class CheckMatType(models.TextChoices):
    VIRGIN = "virgin", _("Virgin")
    REGRIND = "regrind", _("Regrind")
    FILER_TYPE_DUSTY = "filer type dusty", _("FILER Type Dusty")
    POWDER_FREE_FLOW = "powder free flow", _("Powder Free Flow")
    FLAKES = "flakes", _("Flakes")
    MASTER_BATCH = "master batch", _("Master BATCH")
    MICRO_MASTER_BATCH = "micro master batch", _("Micro Master Batch")
    REGRIND_BIG_PIECE = "regrind big piece", _("REGRIND Big Piece")
    FLAKES_REGRIND_BIG_PIECE = "flakes regrind big piece", _("Flakes REGRIND Big Piece")
    POWDER_STICKY_TYPE = "powder sticky type", _("Powder Sticky Type")


class FaqTypeChoices(models.TextChoices):
    ENGINEER = "engineer", _("Engineer")
    CUSTOMER = "customer", _("Customer")


class WarrantyChoices(models.TextChoices):
    IN = "in", _("In")
    OUT = "out", _("Out")


class SparesStatusChoices(models.TextChoices):
    SHORTAGE = "shortage", _("Shortage")
    GATHERING_FOR_ASSEMBLY = "gathering_for_assembly", _("Gathering For Assembly")
    OVER_TO_ASSEMBLY = "over_to_assembly", _("Over To Assembly")
    READY_TO_PACK = "ready_to_pack", _("Ready To Pack")
    PURCHASE_SCHEDULING = "purchase_scheduling", _("Purchase Scheduling")
    PRODUCTION_SCHEDULING = "production_scheduling", _("Production Scheduling")
    SOURCING = "sourcing", _("Sourcing")
    ORDERED = "ordered", _("Ordered")
    RECEIVED = "received", _("Received")
    ASSEMBLING = "assembling", _("Assembling")
    TESTING = "testing", _("Testing")
    HANDED_OVER_TO_STORE = "handed_over_to_store", _("Handed Over To Store")


class DispacherStatusChoices(models.TextChoices):
    OLD_OUTSTANDING = "old_outstanding", _("Old Outstanding")
    FREIGHT_CONFIRMATION = "freight_confirmation", _("Freight Confirmation")
    PAYMENT_PENDING = "payment_pending", _("Payment Pending")
    CREDIT_TERMS = "credit_terms", _("Credit Terms")
    SERVICE_HOLD = "service_hold", _("Service Hold")
    CANCEL_ORDER = "cancel_order", _("Cancel Order")
    OK_TO_DISPATCH = "ok_to_dispatch", _("Ok To Dispatch")


class ReturnSpareStatusChoices(models.TextChoices):
    OK = "ok", _("Ok")
    XY = "xy", _("XY")
    FAULTY = "faulty", _("Faulty")
    REPAIRING = "repairing", _("Repairing")


class DepartmentStatusChoices(models.TextChoices):
    BAY1 = "bay1", _("Bay1")
    BAY2 = "bay2", _("Bay2")
    BAY3 = "bay3", _("Bay3")
    FAB154 = "fab154", _("Fab154")
    ELECTRICAL = "electrical", _("Electrical")


class McTypeChoices(models.TextChoices):
    IMM = "IMM", _("IMM")
    Blow = "Blow", _("Blow")
    Pipe = "Pipe", _("Pipe")
    Sheet = "Sheet", _("Sheet")
    Lamination = "Lamination", _("Lamination")
    WovenSack = "WovenSack", _("WovenSack")
    BlownFilm = "Blown Film", _("Blown Film")
