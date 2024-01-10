from rest_framework import serializers
from account.models import User
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        # fields='__all__'
        fields=['Id_no','FirstName','LastName','Gender','phone_no','stream','collage','Department','Year_of_Student','Campus','Emergency_responder_name','Emergency_responder_address','Emergency_responder_phone_no','Disability']