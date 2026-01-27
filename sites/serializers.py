# sites/serializers.py
from rest_framework import serializers
from .models import Site

class SiteMapSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source="name")
    color = serializers.SerializerMethodField()

    class Meta:
        model = Site
        fields = (
            "title",
            "latitude",
            "longitude",
            "color",
        )

    def get_color(self, obj):
        if obj.phase == "P1":
            return "green"
        if obj.phase == "P2":
            return "purple"
        return "gray"
