# """user's URL Configuration
# """
from django.shortcuts import render
from django.urls import path
from apps.catalogue.api.views import (
    RegisterVisitor
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("register_visitor", RegisterVisitor, basename="Register Visitor")


urlpatterns = [] + router.urls