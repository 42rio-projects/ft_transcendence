import os
from twilio.rest import Client


def send_twilio_code(to, channel):
    account_sid = os.environ["TWILIO_ACCOUNT_SID"]
    auth_token = os.environ["TWILIO_AUTH_TOKEN"]
    service_sid = os.environ["TWILIO_SERVICE_SID"]
    client = Client(account_sid, auth_token)

    verification = client.verify.v2.services(
        service_sid).verifications.create(to=to, channel=channel)

    return verification.status


def check_twilio_code(to, code):
    account_sid = os.environ["TWILIO_ACCOUNT_SID"]
    auth_token = os.environ["TWILIO_AUTH_TOKEN"]
    service_sid = os.environ["TWILIO_SERVICE_SID"]
    client = Client(account_sid, auth_token)

    verification_check = client.verify.v2.services(
        service_sid).verification_checks.create(to=to, code=code)

    return verification_check.status
