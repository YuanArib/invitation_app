from rest_framework import serializers
from .models import Template

class create_template(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = ("owner", "id_global", "male_name", "female_name", "date", "img")