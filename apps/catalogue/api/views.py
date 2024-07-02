from django.shortcuts import render

# Create your views here.
import datetime
import logging
import os
from dateutil.parser import parse

from dotenv import load_dotenv

from apps.ticket.api.serializer import (
    CustomerWiseItemWithoutDepthSerializer,
    ItemSerializer,
)

load_dotenv()

import pandas as pd

# import xlwt
# from django.apps import apps
from django.contrib.auth import authenticate
from django.contrib.sessions.backends.db import SessionStore

# from django.db import models as Models
# from django.db.models import DateField, ForeignKey, Q
# from django.http import HttpResponse
from drf_yasg.utils import swagger_auto_schema
from phonenumber_field.phonenumber import PhoneNumber as pn
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from apps.user.customs.viewsets import CustomViewSet, CustomViewSetFilter
from apps.catalogue.models import (
    Catalogue,
    Visitor
)
from apps.catalogue.api.serializer import (
    VisitorSerializer,
    VisitorSerializerWithDepth
)

class RegisterVisitor(CustomViewSet):
    authentication_classes = []
    serializer_class = VisitorSerializer
    queryset = Visitor.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, context={"user": request.user}
        )
        serializer.is_valid(raise_exception=True)
        registervisitor = serializer.save()
        # data = serializer.data
        data = VisitorSerializerWithDepth(registervisitor).data
        headers = self.get_success_headers(serializer.data)
        response = {
            "message": "Created Succesfully",
            "download_url" : data["catalogue_fk"]["urls"],
            "status": status.HTTP_200_OK,
        }
        return Response(response, status=status.HTTP_201_CREATED, headers=headers)
    