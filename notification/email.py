from django.template import Context
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings


def send_notification_email(name, email, notification):
    context = {
        'name': name,
        'email': email,
        'notification': notification,
    }

    email_subject = 'You have a new notification'
    email_body = render_to_string('email_message.txt', context)

    email = EmailMessage(
        email_subject, email_body,
        settings.DEFAULT_FROM_EMAIL, [email, ],
    )
    return email.send(fail_silently=False)
