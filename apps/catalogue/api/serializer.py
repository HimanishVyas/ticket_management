from rest_framework import serializers
from apps.catalogue.models import (
    Catalogue,
    Visitor
)


class VisitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visitor
        fields = "__all__"

class VisitorSerializerWithDepth(serializers.ModelSerializer):
    class Meta:
        model = Visitor
        fields = "__all__"
        depth = 1