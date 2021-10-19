from rest_framework import serializers

from .models import User

class RegistrationSerializer(serializers.ModelSerializer):

    # set confirm password field
    password2 = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True
    )

    class Meta:
        model = User
        fields = ['email', 'full_name', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def save(self):
        user = User(
            email=self.validated_data['email'],
            full_name=self.validated_data['full_name'],
        )

        # check if passwords match return error if not
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError(
                {'password': 'Passwords must match!'}
            )

        # set password and save user
        user.set_password(password)
        user.save()
        return user