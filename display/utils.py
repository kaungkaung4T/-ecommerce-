from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six

class Token(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return six.text_type(user.id)+six.text_type(timestamp)+six.text_type(user.profile.is_verified)

token_email = Token()