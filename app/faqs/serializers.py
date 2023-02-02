from rest_framework import serializers

from faqs.models import FAQ


class FAQSerializer(serializers.ModelSerializer):
    answer = serializers.SerializerMethodField()

    def get_answer(self, faq):
        return faq.answer.html

    class Meta:
        model = FAQ
        fields = ('question', 'answer')
