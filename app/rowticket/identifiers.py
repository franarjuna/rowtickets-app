from django.conf import settings

from hashids import Hashids
import shortuuid


def generate_random_identifier():
    shortuuid.set_alphabet('abcdefghijklmnopqrstuvwxyz0123456789')

    return shortuuid.random(length=10)


def generate_identifier(model_instance_id, model_name):
    """
    Generate a decryptable hash from the model instance and a custom salt (different salt for each model)

    Using a different salt for each model prevents matching identifier between different model instances
    with the same IDs
    """
    hashids = Hashids(salt=getattr(settings, 'IDENTIFIER_SALTS')[model_name], min_length=10)

    return hashids.encode(model_instance_id)


def decode_identifier(identifier, model_name):
    """
    Decodes a hashed identifier for a particular model
    """
    hashids = Hashids(salt=getattr(settings, 'IDENTIFIER_SALTS')[model_name], min_length=10)

    return hashids.decode(identifier)[0]
