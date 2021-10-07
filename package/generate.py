import os
from random import Random

def identity_generator():
    random = Random()
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789!@#$%^&*'
    identity_code=""
    length = len(chars)-1
    for num in range(64):
        identity_code+=chars[random.randint(0,length)]
    return identity_code