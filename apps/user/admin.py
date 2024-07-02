# from django import forms
from django.apps import apps
from django.contrib import admin
from import_export import fields, resources
from import_export.admin import ImportExportModelAdmin

# from django.core.exceptions import ValidationError
from apps.user.models import CustomerUser

# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from django.contrib.auth.models import Group

models = apps.get_app_config("user").get_models()
for model in models:
    admin.site.register(model)

admin.site.unregister(CustomerUser)


# class UserChangeForm(forms.ModelForm):
#     """A form for updating users. Includes all the fields on
#     the user, but replaces the password field with admin's
#     disabled password hash display field.
#     """
#     password = ReadOnlyPasswordHashField()
#     class Meta:
#         model = CustomerUser
#         fields = "__all__"
#     def save(self, commit=True):
#         # Save the provided password in hashed format
#         user = super().save(commit=False)
#         user.set_password(user.password)
#         if commit:
#             user.save()
#             print(user)
#         return user


# class UserAdmin(BaseUserAdmin):
#     # The forms to add and change user instances
#     form = UserChangeForm
#     add_form = UserChangeForm
#     list_display = ["email", "full_name", "company", "is_superuser", "user_role"]
#     list_filter = ["is_superuser"]
#     fieldsets = [
#         (None, {"fields": ["email", "password"]}),
#         (
#             "Personal info",
#             {
#                 "fields": [
#                     "full_name",
#                     "user_image",
#                     "mobile",
#                     "user_role",
#                     "email_verify",
#                     "mobile_verify",
#                 ]
#             },
#         ),
#         ("Permissions", {"fields": ["is_superuser", "is_staff"]}),
#     ]
#     # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
#     # overrides get_fieldsets to use this attribute when creating a user.
#     add_fieldsets = [
#         (
#             None,
#             {
#                 "classes": ["wide"],
#                 "fields": [
#                     "email",
#                     "full_name",
#                     "mobile",
#                     "user_role",
#                     "company",
#                     "password",
#                 ],
#             },
#         ),
#     ]
#     search_fields = ["email"]
#     ordering = ["email"]
#     filter_horizontal = []


# admin.site.register(User, UserAdmin)
# admin.site.unregister(Group)
class CustomerUserResource(resources.ModelResource):
    class Meta:
        model = CustomerUser


class CustomerUserAdmin(ImportExportModelAdmin):
    resource_classes = [CustomerUserResource]


admin.site.register(CustomerUser, CustomerUserAdmin)
