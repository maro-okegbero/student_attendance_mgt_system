"""
utils.py

@Author:    Maro Okegbero
@Date:      June 2, 2021
@Time:      8:29 AM

This module contains a number of utility functions useful throughout the attendance mgt system app!.
No references are made to specific models or views. As a result, they are useful with or
without the application context.
"""
import hashlib
import time
from datetime import datetime
import random
import string

from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail


def token_generator(size=5, chars=string.digits):
    """
    utility function to generate random identification numbers
    """
    return ''.join(random.choice(chars) for x in range(size))


def generate_reference_number():
    """
    generates a unique reference number
    """

    year = datetime.now().year.__str__()
    month = datetime.now().month.__str__()
    x = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(9))
    return "-".join(["AM"] + [year] + [month] + ["".join([x])])


def populate_obj(obj, data):
    """
    Populates an object with the data passed to it

    param obj: Object to be populated
    param data: The data to populate it with (dict)

    returns: obj populated with data


    """
    for name, value in data.items():
        if hasattr(obj, name):
            # print(name, value)
            setattr(obj, name, value)

    return obj


def send_email_verification_pin(**data):
    """
    send user email
    """

    name = data.get("name")
    email = data.get("email")
    pin = data.get("pin")

    if name and email and pin:
        try:
            print("I'm about to send a mail...............................................")
            send_mail(subject="Email verification",
                      html_message=f"<h1>Hi {name},</h1> <p>Welcome to <>. Your verification pin is <b>{pin}</b></p>",
                      message=f"<h1>Hi {name},</h1> <p>Welcome to HelpMe. Your verification pin is <b>{pin}</b></p>",
                      from_email="HelpMe no-reply@tpie.com", recipient_list=[f'{email}'], fail_silently=False)
            print("I have  sent the mail...............................................")
            return
        except Exception as e:
            print(e, "Email Error..................................................")
            pass


def encode_str(chatcter):
    """

    :param chatcter:
    :return:
    """
    import base64

    letters = string.ascii_lowercase
    random_str = ''.join(
        random.choice(letters) for i in range(4))  # adding this random string to make the encoded value more dynamic
    message = chatcter + random_str
    base64_message = base64.b64encode(message.encode("utf-8"))
    return base64_message


def decode_str(chatcter):
    """


    :param chatcter:
    :return:
    """

    import base64
    print(chatcter, "THe character===============================")
    message = str(chatcter) + "=="
    message = base64.b64decode(message).decode("UTF-8", 'ignore')
    print(message[:-4], "the message========================")
    print(type(message), "the message type========================")
    return message[:-4]
