from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail




@shared_task
def send_email_task():
    subject = 'Simple shop subscribe'
    message = 'Hello from simple shop'
    email_from = settings.EMAIL_HOST_USER
    emails_to = ['testartem352@gmail.com', ]

    send_mail(subject, message, email_from, emails_to)
