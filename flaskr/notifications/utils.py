class NotificationMessage():
    @staticmethod
    def approvedPromotion():
        return "Congratulations! You are now a host. You can now create events."

    @staticmethod
    def declinedPromotion():
        return "Sorry! Your request for promotion is declined."

    @staticmethod
    def ban_user(reason: str):
        return f"You are banned. Reason: {reason}"

    @staticmethod
    def unban_user():
        return "You are unbanned now."

    @staticmethod
    def report_user(first_user_name: str, second_user_name: str):
        return f"{first_user_name} has reported {second_user_name}."

    @staticmethod
    def want_promotion(user_name: str):
        return f"{user_name} wants to be a host."

    @staticmethod
    def complain_resolved_by_ban(name: str):
        return f"Your complain against {name} has been considered. The user is now banned from the service."

    @staticmethod
    def user_banned_by_other_report(name: str):
        return f"The user {name}, you reported is now banned from the service."

    @staticmethod
    def complain_resolved_by_warning(name: str):
        return f"Your complain against {name} has been considered. He is given a warnning."

    @staticmethod
    def warn_user(reason: str):
        return f"You are warned! {reason}"

    @staticmethod
    def complain_not_acceptable(name: str):
        return f"Your complain against {name} has been considered. Sorry, your complain is not acceptable."
    
    @staticmethod
    def pending_payments(name: str):
        return f"{name} has requested for join your event"
    
    @staticmethod
    def approve_event_registration():
        return "You are not approved to join by the host."
    
    @staticmethod
    def declin_event_registration():
        return "Host has delcined your registration."
    
    @staticmethod
    def review_profile(name):
        return f"{name} has reviewed your profile."
