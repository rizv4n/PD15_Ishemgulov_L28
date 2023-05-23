import datetime
from rest_framework import serializers


def calculate_age(value):
    time_d = datetime.date.today() - value
    seconds = datetime.timedelta.total_seconds(time_d)
    float_years = seconds / 31536000
    return round(float_years)


class AgeVerificationValidator:
    def __call__(self, value):
        if calculate_age(value) < 9:
            raise serializers.ValidationError("Аge verification failed")


class EmailValidator:
    def __call__(self, value):
        if "rambler.com" in value:
            return serializers.ValidationError("Email incorrect")

