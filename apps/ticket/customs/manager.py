from django.db import models
from rest_framework import serializers


class TicketManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
