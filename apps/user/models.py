from django.contrib.auth.models import AbstractBaseUser
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models.signals import post_save, post_init
from apps.user.customs.managers import UserManager
from apps.user.utilities.choices import UserRoleChoices
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.hashers import check_password


class CustomerUser(AbstractBaseUser):
    """
    User model
    """

    CardCode = models.CharField(_("Card Code"), max_length=50, null=True, blank=True)
    CardName = models.CharField(_("Card Name"), max_length=100)
    CardType = models.CharField(_("Card Type"), max_length=100, null=True, blank=True)
    GroupCode = models.CharField(_("Group Code"), max_length=50, null=True, blank=True)
    E_Mail = models.EmailField(
        _("E_Mail"), max_length=255, unique=True, null=True, blank=True
    )
    mobile_number = PhoneNumberField(_("Phone"), unique=True, null=True, blank=True)
    # mobile = PhoneNumberField(_("Mobile Number"), null=True, blank=True, unique=True)
    password = models.CharField(_("Password"), max_length=200)
    user_image = models.ImageField(
        _("User Image"),
        null=True,
        blank=True,
        upload_to="media/user",
        default="media/user/user_318-159711.png",
    )
    user_role = models.PositiveSmallIntegerField(
        _("User Role"), choices=UserRoleChoices.choices, default=3
    )
    is_staff = models.BooleanField(_("Staff Status"), default=False)
    is_superuser = models.BooleanField(_("Superuser Status"), default=False)
    fcm_token = models.TextField(_("Fcm Token"), null=True, blank=True)
    is_active = models.BooleanField(_("Superuser Status"), default=True)
    # status = models.CharField(
    #     _("User Status"),
    #     choices=StatusChoices.choices,
    #     max_length=10,
    #     default="pending",
    # )
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)
    last_login = models.DateTimeField(
        _("Last Login"), auto_now=False, auto_now_add=False, blank=True, null=True
    )
    objects = UserManager()
    USERNAME_FIELD = "E_Mail"
    REQUIRED_FIELDS = ["CardName", "password", "user_role"]
    # zip_code = models.CharField(_("Zip Code"), max_length=50)
    # company = models.ForeignKey(
    #     "user.Company",
    #     verbose_name=_("Company FK"),
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     blank=True,
    # )
    changed_user_role = models.DateTimeField(default=now)
    mobile_verify = models.BooleanField(_("Mobile Number Verify"), default=False)
    email_verify = models.BooleanField(_("Email Verify"), default=False)
    # mobile_otp = models.IntegerField(_("Mobile OTP"), default=0)
    is_pass_changed = models.BooleanField(_("Password Changed"), default=False)

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    def __str__(self):
        return str(self.E_Mail)

    # @classmethod
    # def post_create(cls, sender, instance, created, *args, **kwargs):
    #     if created:
    #         instance.save()

    def save(self, *args, **kwargs):
        print(self.pk)
        if not self.pk:
            print("password : ---------->>>", self.password)
            self.set_password(self.password)
            print("---------->>>", self.password)

        elif self.password != self.__class__.objects.get(pk=self.pk).password:
            # print(check_password(self.password))
            # elif self.password != check_password(self.password):
            print(self.__class__.objects.get(pk=self.pk).password)
            self.set_password(self.password)
        super().save(*args, **kwargs)

    # def post_init_create(sender, instance, *args, **kwargs):
    # # Check if the instance is a new one (not retrieved from the database)
    #     if not instance.pk:
    #         instance.set_password(instance.password)
    #         instance.save()


# post_save.connect(CustomerUser.post_create, sender=CustomerUser)


class Address(models.Model):
    customer_user = models.ForeignKey(
        "user.CustomerUser", verbose_name=_("Customer User"), on_delete=models.CASCADE
    )
    Address = models.TextField(_("Address"), null=True, blank=True)
    Street = models.CharField(_("Street"), max_length=200, null=True, blank=True)
    Block = models.CharField(_("Block"), max_length=200, null=True, blank=True)
    ZipCode = models.CharField(_("Zip Code"), max_length=50, null=True, blank=True)
    City = models.CharField(_("City"), max_length=50, null=True, blank=True)
    # Country = models.CharField(_("Country"), max_length=50)
    # State = models.CharField(_("State"), max_length=100)
    Building = models.CharField(_("Building"), max_length=100, null=True, blank=True)
    # AddressType = models.CharField(_("Address Type"), max_length=100)
    StreetNo = models.CharField(_("StreetNo"), max_length=50, null=True, blank=True)
    # Ntnlty = models.CharField(_("Ntnlty"), max_length=100)
    Country = models.ForeignKey(
        "user.Country",
        verbose_name=_("Country FK"),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    States = models.ForeignKey(
        "user.States",
        verbose_name=_("State FK"),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    district = models.ForeignKey(
        "user.District",
        verbose_name=_("District FK"),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    # city = models.CharField(_("City"), max_length=50)
    # pincode = models.CharField(_("PinCode"), max_length=50)
    is_active = models.BooleanField(_("Is Active"), default=True)
    # place = models.CharField(_("Place"), choices=PlaceChoice.choices, max_length=50)
    is_default = models.BooleanField(_("IS Selected"), default=False)

    def __str__(self):
        return str(self.Address)


class PhoneNumber(models.Model):
    customer_user = models.ForeignKey(
        "user.CustomerUser", verbose_name=_("Customer User"), on_delete=models.CASCADE
    )
    phone = PhoneNumberField(_("Phone"), unique=True)
    is_default = models.BooleanField(_("Is Default"), default=False)
    is_active = models.BooleanField(_("Is Active"), default=True)
    is_verified = models.BooleanField(_("Is Verified"), default=False)

    def __str__(self):
        return str(self.phone)


class Email(models.Model):
    customer_user = models.ForeignKey(
        "user.CustomerUser", verbose_name=_("Customer User"), on_delete=models.CASCADE
    )
    E_Mail = models.EmailField(_("E_Mail"), max_length=255, null=True, blank=True, unique=True)


class Country(models.Model):
    country = models.CharField(max_length=256)

    def __str__(self):
        return str(self.country)


class States(models.Model):
    country_fk = models.ForeignKey(
        Country,
        verbose_name=_("country FK"),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="state",
    )
    states = models.CharField(max_length=100)

    def __str__(self):
        return str(self.states)


class District(models.Model):
    state_fk = models.ForeignKey(
        States,
        verbose_name=_("state FK"),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="state",
    )
    district = models.CharField(max_length=100)

    def __str__(self):
        return str(self.district)


class AppVersion(models.Model):
    android_version = models.CharField(
        _("Android Version"), max_length=50, null=True, blank=True
    )
    ios_version = models.CharField(
        _("IOS Version"), max_length=50, null=True, blank=True
    )
    is_android_force_update = models.BooleanField(_("Android force update"))
    is_ios_force_update = models.BooleanField(_("IOS force update"))
    android_updated_url = models.CharField(
        _("Android updated url"), max_length=50, null=True, blank=True
    )
    ios_updated_url = models.CharField(
        _("IOS updated url"), max_length=50, null=True, blank=True
    )
    title = models.CharField(_("Change title"), max_length=50, null=True, blank=True)
    desc = models.TextField(_("Change description"), null=True, blank=True)

    def __str__(self):
        return str(self.android_version)
