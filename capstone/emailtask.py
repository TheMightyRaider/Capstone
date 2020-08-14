from celery import shared_task
from django.core.mail import send_mail
from decouple import config

@shared_task
def send_email_task(sent_time):
        # Sending a Mail
        subject='Unknown Face detected'
        message='Unknown face appeared at: '+sent_time
        email_from=config('EMAIL_HOST_USER')
        recipient_list=['s.sanjay2016@vitstudent.ac.in']
        send_mail(subject,message,email_from,recipient_list)
        return None