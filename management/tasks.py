from celery import shared_task
from django.core.mail import EmailMessage
from django.conf import settings


@shared_task
def send_notification_email(user_email, message):
    """
    Celery task to send a notification email to the user.

    Parameters:
    - user_email: The email address of the recipient.
    - message: The content of the notification email.

    The task sends an email to the specified user with the given message.
    The email subject is set to 'New Notification', and the sender's email is retrieved from Django settings.
    """
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
    except Exception as e:
        print(f'Email sending failed: {e}')




