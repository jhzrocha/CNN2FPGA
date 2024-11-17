from rest_framework import serializers
from ..vhdlGenerator.models import Music

class MusicSerializer(serializers.ModelSerializer):

    class Meta:

        model = Music
        fields = '__all__'