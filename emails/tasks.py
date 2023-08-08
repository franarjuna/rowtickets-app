from django.conf import settings
from django.core.mail import EmailMultiAlternatives, send_mail as django_send_mail
from django.template.loader import render_to_string


def send_mail(template_name, subject, template_context, recipient, attachments=None):
    #text_template = f'emails/{template_name}.txt'
    html_template = f'emails/{template_name}.html'

    #text_content = render_to_string(text_template, template_context)
    text_content = ''
    html_content = render_to_string(html_template, template_context)

    msg = EmailMultiAlternatives(subject, text_content, settings.EMAILS_FROM, [recipient])
    msg.attach_alternative(html_content, 'text/html')

    if attachments:
        for attachment in attachments:
            msg.attach_file(attachment)

    msg.send(fail_silently=False)
