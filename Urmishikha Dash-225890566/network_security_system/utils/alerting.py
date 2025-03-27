import requests

def send_slack_alert(message):
    webhook_url = "https://hooks.slack.com/services/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"
    payload = {"text": message}
    requests.post(webhook_url, json=payload)

def send_sms_alert(message):
    # Use an SMS API like Twilio
    pass