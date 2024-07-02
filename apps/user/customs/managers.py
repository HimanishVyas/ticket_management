import datetime

from django.contrib.auth.models import BaseUserManager
from django.db import models

from apps.user.customs.querysets import SoftDeletionQuerySet

# from django.db.models.query import QuerySet


class SoftDeletionManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop("alive_only", True)
        super(SoftDeletionManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        if self.alive_only:
            return SoftDeletionQuerySet(self.model).filter(deleted_at=None)
        return SoftDeletionQuerySet(self.model)

    def hard_delete(self):
        return self.get_queryset().hard_delete()


class UserManager(BaseUserManager):
    def create_user(
        self,
        E_Mail,
        user_role=9,
        password=None,
        CardName=None,
        user_image=None,
        *args,
        **kwargs,
    ):
        if not E_Mail:
            raise ValueError("User must have an email address")
        if super().get_queryset().filter(E_Mail=self.normalize_email(E_Mail)):
            raise ValueError("User with this email address already exists")
        user = self.model(
            E_Mail=self.normalize_email(E_Mail),
            CardName=CardName,
            password=password,
            user_role=user_role,
            user_image=user_image,
            last_login=datetime.datetime.now(),
            *args,
            **kwargs,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        E_Mail,
        password=None,
        CardName=None,
        user_role=1,
    ):
        user = self.create_user(
            E_Mail,
            password=password,
            user_role=1,
            CardName=CardName,
        )
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def create(self, **kwargs):
        return self.model.objects.create_user(**kwargs)

    # def get_queryset(self) -> QuerySet:
    #     QuerySet = super().get_queryset().annotate(
    #         email=models.Case(
    #             models.When(email='mittal.nayar@tecblic.com', then=""),
    #             default='password',
    #             output_field=models.CharField()
    #         )
    #     )

    #     return QuerySet
