from rest_framework import serializers
from task.models.users import User


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password"]

    def create(self, validated_data):
        user = User(email=validated_data["email"])
        user.set_password(validated_data["password"])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        user = User.objects.filter(email=email, is_active=True).first()
        if not user or not user.check_password(password):
            raise serializers.ValidationError("Invalid credentials")
        attrs["user"] = user
        return attrs
