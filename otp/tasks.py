from ehyzmat.celery import app
from datetime import datetime, timedelta
from otp.models import OTP


@app.task
def otp_task():
    nonexpiredotp = OTP.objects.filter(is_expired=False)
    print("Checking OTP expired times...")
    for i in nonexpiredotp:
        otp_date = (i.expired_at+timedelta(hours=5)).replace(tzinfo=None)
        if otp_date <= datetime.now():
            i.is_expired = True
            i.save()
    print("Process done.")