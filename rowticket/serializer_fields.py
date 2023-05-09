from rest_framework import serializers


class IdentifierField(serializers.CharField):
    def __init__(self, **kwargs):
        kwargs.update({
            'min_length': 10,
            'max_length': 10,
            'allow_blank': False,
            'trim_whitespace': False
        })

        super().__init__(**kwargs)
