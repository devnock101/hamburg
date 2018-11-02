"""
Scheduled Jobs
"""
import logging
import os
import sendgrid
from sendgrid.helpers.mail import Mail, Email, Content
from django.core.management.base import BaseCommand
from hamburg_api.dataapi import DataGetter
from hamburg_api.models import EmailAlertModel

LOGGER = logging.getLogger(__name__)

class Command(BaseCommand):
    """Command Scheduler class for sending email alerts"""

    def handle(self, *args, **options):
        """send email"""
        data = DataGetter.get_email_alert_data()
        done = []
        for row in data:
            sendgrid_client = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
            from_email = Email(os.environ['SENDER_EMAIL'])
            to_email = Email(row['email'])
            subject = "Hamburg alert for {}".format(row['movie_name'])
            content = Content("text/plain", "{} is releasing on {}".format(row['movie_name'],\
                    row['release_date']))
            mail = Mail(from_email, subject, to_email, content)
            response = sendgrid_client.client.mail.send.post(request_body=mail.get())
            if response.status_code == 202:
                done.append(row['id'])

        EmailAlertModel.objects.filter(id__in=done).update(done=True)
