from celery import shared_task
from django.core.mail import EmailMessage
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_notification_email(user_email, message):
    print("function working")
    try:
        email_subject = 'New Notification'
        email_body = message
        email_from = settings.DEFAULT_FROM_EMAIL
        email_to = [user_email]

        email = EmailMessage(
            email_subject,
            email_body,
            email_from,
            email_to,
        )
        email.send()
        print("worked")
    except Exception as e:
        print(f'Email sending failed: {e}')




