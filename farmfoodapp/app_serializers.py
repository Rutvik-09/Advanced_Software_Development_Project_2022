from rest_framework import serializers

from farmfoodapp.models import RegisterModel


class RegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=50)  # Required Field
    last_name = serializers.CharField(max_length=50)  # Required Field
    date_of_birth = serializers.DateField()  # Required Field
    email = serializers.EmailField(max_length=50)  # Required Field
    country_code = serializers.CharField(max_length=5, default="+1")  # Optional Field
    phone = serializers.CharField(max_length=15)  # Required Field
    user_password = serializers.CharField(max_length=200)

    def create(self, validated_data):
        return RegisterModel.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        instance.email = validated_data.get('email', instance.email)
        instance.country_code = validated_data.get('country_code', instance.country_code)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.user_password = validated_data.get('user_password', instance.user_password)
        instance.attempts_left = validated_data.get('attempts_left', instance.attempts_left)
        instance.lock = validated_data.get('lock', instance.lock)
        instance.save()
        return instance


# class UserPreferenceSer(serializers.Serializer):
#     user = serializers.PrimaryKeyRelatedField(queryset=RegisterModel.objects.all())
#     pref_fruits = serializers.BooleanField(default=False)
#     pref_veg = serializers.BooleanField(default=False)
#     pref_sea = serializers.BooleanField(default=False)
#     pref_meat = serializers.BooleanField(default=False)
#     pref_organic = serializers.BooleanField(default=False)
