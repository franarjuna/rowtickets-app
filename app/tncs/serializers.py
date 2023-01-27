from rest_framework import serializers

from tncs.models import TnC


class TnCSerializer(serializers.ModelSerializer):
    content = serializers.SerializerMethodField()

    def get_content(self, tnc):
        return tnc.content.html

    class Meta:
        model = TnC
        fields = ('title', 'content')
