import django
from django.conf import settings
from django.core.mail import send_mail
from django.core.mail.backends.smtp import EmailBackend

def send_invitation_email(suject,content,target):
    send_mail(
        suject,
        content,
        'MatrixRequirementTracker@gmail.com',
        target,
        auth_user='MatrixRequirementTracker',
        auth_password='matrix2014',

        connection=EmailBackend(
            host='smtp.gmail.com',
            port=587,
            username='MatrixRequirementTracker',
            password='matrix2014',
            use_tls=True
        )
    )
