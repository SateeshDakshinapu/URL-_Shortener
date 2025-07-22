import re
import random
import string

def validate_url(url):
    pattern = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Za-z0-9-]+\.)+[A-Za-z]{2,6})'  # domain...
        r'(?:/?|[/?]\S+)$'
    )
    return re.match(pattern, url) is not None

def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))
