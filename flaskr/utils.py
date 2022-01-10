from datetime import datetime

from flask_login import current_user


def is_eligable(user):
    if current_user.is_anonymous:
        return None
    if user.profile.banned:
        if user.profile.banned.expire_date > datetime.utcnow():
            return {
                "is_banned": True,
                "message": "Account is banned."
            }
        else:
            user.profile.unban()
            return None
    if not user.is_verified:
        return {
            "is_valid": False,
            "message": "Account is not verified."
        }
    return None
