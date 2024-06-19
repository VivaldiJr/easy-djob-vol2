import hashlib
import os
from datetime import datetime
import random


def send_firebase_notification(tokens: list, title: str or None, message: str, image_url=None, payload=None):
    try:
        from firebase_admin import messaging
        message = messaging.MulticastMessage(
            notification=messaging.Notification(
                title=title,
                body=message,
                image=image_url,

            ),
            data=payload,
            tokens=tokens,
        )
        response = messaging.send_multicast(message)
        print(response)
        return True
    except Exception as e:
        print("Firebase Send Notification Exceptio ", e)
        return False


def random_token(length=40, prefix="", cicles=8, number=False):
    rbytes = ""
    for i in range(cicles):
        rbytes += "{}".format(str(hashlib.sha1(os.urandom(length)).hexdigest()))
    now = datetime.now().timestamp()
    return "{}".format(random.randint(10 ** (length - 1), 10 ** length - 1)) if number else "{}{}{}".format(prefix, rbytes, now)
