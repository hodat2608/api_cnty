from django.contrib.auth.tokens import default_token_generator
from templated_mail.mail import BaseEmailMessage

from djoser import utils
from djoser.conf import settings


class ActivationEmail(BaseEmailMessage):
    template_name = "static/templates/activation.html"

    def get_context_data(self):
        # ActivationEmail can be deleted
        context = super().get_context_data()

        user = context.get("user")
        context["uid"] = utils.encode_uid(user.pk)
        context["token"] = default_token_generator.make_token(user)
        context["url"] = settings.ACTIVATION_URL.format(**context)

        uid = utils.encode_uid(user.pk)
        token = default_token_generator.make_token(user)
        url = settings.ACTIVATION_URL.format(**context)
        print(f'{url}')
        return context
    
class ConfirmationEmail(BaseEmailMessage):
    template_name = "static/templates/confirmation.html"

class PasswordChangedConfirmationEmail(BaseEmailMessage):
    template_name = "static/templates/password_changed_confirmation.html"

class PasswordResetEmail(BaseEmailMessage):
    template_name = "static/templates/password_reset.html"

    def get_context_data(self):
        # PasswordResetEmail can be deleted
        context = super().get_context_data()

        user = context.get("user")
        context["uid"] = utils.encode_uid(user.pk)
        context["token"] = default_token_generator.make_token(user)
        context["url"] = settings.PASSWORD_RESET_CONFIRM_URL.format(**context)

        url = settings.PASSWORD_RESET_CONFIRM_URL.format(**context)
        print(f'{url}')
        return context
    
class UsernameChangedConfirmationEmail(BaseEmailMessage):
    template_name = "static/templates/username_changed_confirmation.html"


class UsernameResetEmail(BaseEmailMessage):
    template_name = "static/templates/username_reset.html"

    def get_context_data(self):
        context = super().get_context_data()

        user = context.get("user")
        context["uid"] = utils.encode_uid(user.pk)
        context["token"] = default_token_generator.make_token(user)
        context["url"] = settings.USERNAME_RESET_CONFIRM_URL.format(**context)
        url = settings.ACTIVATION_URL.format(**context)
        print(f'Đây là url của bạn : {url} ')
        return context
    
