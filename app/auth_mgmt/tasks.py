from celery import shared_task
from .signals import send_otp

@shared_task()
def handle_otp_email_task(email, otp):
    send_otp.send(sender=None, otp=otp)