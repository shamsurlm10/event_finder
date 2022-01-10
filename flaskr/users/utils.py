import random

from flask import url_for


def password_reset_key_mail_body(id: int, token: str, expire_time: int):
    return f"""To reset the password please go to the following link.
Reset Link: { url_for("users.reset_password", id=id, token=token, _external=True) }

This link will be expired in {int(expire_time/60)} minutes.
"""

def generate_token(size: int):
    sample_string = 'qwertyuioplkjhgfdsazxcvbnm1234567890'
    result = ''.join((random.choice(sample_string)) for x in range(size)) 
    return result
