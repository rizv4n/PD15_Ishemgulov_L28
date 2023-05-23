from rest_framework import serializers

from ads.validators import AgeVerificationValidator, EmailValidator
from authentication.models import User


class UserCreateSerializer(serializers.ModelSerializer):
    birthday = serializers.DateField(validators=[AgeVerificationValidator()])
    email = serializers.EmailField(validators=[EmailValidator()])

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validate_data):
        user = super().create(validate_data)

        user.set_password(user.password)
        user.save()

        return user
