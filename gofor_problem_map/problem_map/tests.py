from django.test import TestCase
from django.test import TestCase
from django.test.utils import override_settings
from django.core import mail

# Create your tests here.

@override_settings(EMAIL_BACKEND='anymail.backends.test.EmailBackend')
class SignupTestCase(TestCase):
    # Assume our app has a signup view that accepts an email address...
    def test_sends_confirmation_email(self):
        self.client.post("/account/signup/", {"email": "user@example.com"})

        # Test that one message was sent:
        self.assertEqual(len(mail.outbox), 1)

        # Verify attributes of the EmailMessage that was sent:
        self.assertEqual(mail.outbox[0].to, ["user@example.com"])
        self.assertEqual(mail.outbox[0].tags, ["confirmation"])  # an Anymail custom attr

        # Or verify the Anymail params, including any merged settings defaults:
        self.assertTrue(mail.outbox[0].anymail_send_params["track_clicks"])
