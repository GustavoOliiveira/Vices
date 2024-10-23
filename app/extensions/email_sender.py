import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

api_key = SendGridAPIClient("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")#SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))


def sendgrid_mail(to_emails, subject, html_content):
    sg = api_key
    message = Mail(
        from_email = 'vices4test@gmail.com', # remetente -> sender configurado no site da api (sendgrid)
        to_emails = to_emails,
        subject = subject,
        html_content = html_content)
    try:
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)