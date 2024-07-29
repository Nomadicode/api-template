from django.core.mail import EmailMessage
from django.template import Context
from django.template.loader import get_template

def send_email_template(subject, template_name, recipients, from_email="no-reply@nomadicode.com", *args, **kwargs):
    email_template = get_template(f"emails/{template_name}.html")
    
    context = kwargs

    html_message = email_template.render(context)

    mail = EmailMessage(
        subject=subject,
        body=html_message,
        from_email=from_email,
        to=recipients,
        reply_to=(from_email, )
    )
    mail.content_subtype = "html"
    return mail.send()