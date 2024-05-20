from django.dispatch import receiver
from django.core.signals import request_finished
from django.dispatch import Signal
from rest_framework import status
from rest_framework.response import Response
from .utlis import generate_otp
from decouple import config
import vonage

# Define the custom signal
send_otp = Signal()

# Connect a receiver function to the signal
@receiver(send_otp)
def handle_otp(sender, otp, **kwargs):
    print("Email sent signal received. Message:", otp) 

    print(otp)
    client = vonage.Client(key=config('VONAGE_KEY'), secret=config('VONAGE_SECRET'))
    sms = vonage.Sms(client)
    responseData = sms.send_message(
        {
            "from": "Vonage APIs",
            "to": "9779803366606",
            "text": '\nYour One Time Password(OTP): ' + otp
        }
    )
    if responseData["messages"][0]["status"] == "0":
        response = {
            'status': 'successful',
            'message': 'otp sent',
        }
        return Response(status=status.HTTP_200_OK, data=response)
    response = {
        'status': 'failed',
        'message': f"Message failed with error: {responseData['messages'][0]['error-text']}"
    }
    return Response(status=status.HTTP_200_OK, data=response)