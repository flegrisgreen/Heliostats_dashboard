import json
import os
from datetime import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from appFuncs import client


email_count = 0

def config_test(message):
    data = message
    status = None
    config_data = None

    # Check battery levels
    if float(data['battery']) < 6 and float(data['battery']) > 5:
        # Warn that battery levels are low
        print('Warning: battery level for helio {} is low'.format(data["helio_id"]))
        status = {'status': 'Warning'}
        data.update(status)
        # TODO: Add a stackdriver warning
    elif float(data['battery']) < 5:
        # Reset heliostat
        status = {'status': 'Bad'}
        data.update(status)
        config_data = {"Reset": True, "helio_id": data.get('helio_id')}  # Note, parameters must be in double quotes for JSON package decoding
        helio_id = data.get('helio_id')
        # Note, there is no limit on the number of emails that can be sent per day
        c = email_count
        send_mail(helio_id, c)
    else:
        # Battery levels good, do nothing
        status = {'status': 'Good'}
        data.update(status)
        return 'OK', 200

    # Publish config message if there is config data
    if config_data is not None:
        config_data_json = json.dumps(config_data).encode('utf-8')  # convert dictionary to byte object
        config_topic = 'projects/test-project-254608/topics/configuration'
        client.publish(config_topic, config_data_json)
        # print('Helio {} has been reset'.format(data['helio_id']))

    return 'OK', 200


def send_mail(helio_id, c):

    # TODO: Implement a daily e-mail cap per heliostat
    # TODO: The current limiting system must still be tested

    time_now = int(datetime.utcnow().timestamp())
    if c < 1:

        message = Mail(
            from_email=os.environ.get('EMAIL_FROM'),
            to_emails=os.environ.get('EMAIL_TO'),
            subject='Heliostat ' + helio_id + ' warning',
            plain_text_content='Heliostat' + helio_id + ' is non-responsive.')

        try:
            sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            response = sg.send(message)
            time_sent = int(datetime.utcnow().timestamp())
            c = c + 1
            global email_count
            email_count = c
            # print(message)
        except Exception as e:
            print(e)

    if time_now > (time_sent+86400):  # + 86400 is 24 hours later
        email_count = 0

    return 'OK', 200
