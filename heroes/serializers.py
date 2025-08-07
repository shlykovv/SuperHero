from rest_framework import  serializers

from heroes.models import HeroModel


class HeroSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeroModel
        fields = '__all__'
