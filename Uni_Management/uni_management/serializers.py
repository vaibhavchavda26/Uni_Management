from rest_framework import serializers
from django.contrib.auth.models import User


from .models import Principal, User, Teachers, Students

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class PrincipalSerializer(serializers.Serializer):
    class Meta:
        model = Principal
        fields = '__all__'

class TeacherSerializer(serializers.Serializer):
    class Meta:
        model = Teachers
        fields = '__all__'

class StudentSerializer(serializers.Serializer):
    class Meta:
        model = Students
        fields = '__all__'
