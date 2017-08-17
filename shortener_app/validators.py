from django.core.exceptions import ValidationError
from django.core.validators import URLValidator


def validate_url(url):
    url_validator = URLValidator()
    try:
        url_validator(url)
    except:
        new_url = 'http://' + url
        try:
            url_validator(new_url)
        except:
            raise ValidationError('Invalid URL for this field')
        else:
            return new_url
    else:
        return url


# def validate_dot_com(url):
#     if not 'com' in url:
#         raise ValidationError('Not a valid .com URL')
#     return url