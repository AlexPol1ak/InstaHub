from drf_spectacular.utils import inline_serializer
from rest_framework import serializers

#Фековый сериализатор для представления RetrieveSelfAllUserDataAPIView.
ResponseFakeSerializer = inline_serializer(
    'RetrieveSelfAllUserDataSerializer',
    fields={'id': serializers.IntegerField(),
            'login': serializers.CharField(max_length=20, min_length=5, read_only=True, ),
            'email': serializers.EmailField(max_length=40, read_only=True),
            'first_name': serializers.CharField(max_length=40, read_only=True) ,
            'last_name': serializers.CharField(max_length=40, read_only=True) ,
            'phone_number': serializers.IntegerField(read_only=True),
            'date_birth': serializers.DateField(read_only=True),
            'status': serializers.BooleanField(read_only=True),
            'is_stuff': serializers.BooleanField(read_only=True),
            'is_activ': serializers.BooleanField(read_only=True),
            'date_joined': serializers.DateTimeField(read_only=True),
            'type': serializers.CharField(max_length=20, min_length=5, read_only=True, ),
            'login_inst':serializers.CharField(max_length=20, min_length=5, read_only=True, ),
            'password_inst': serializers.CharField(max_length=20, min_length=5, read_only=True, ),
            }
)

DeactivateUserFakeSerializer = inline_serializer(
        'DeactivateUserAPIView',
        fields={
                'password': serializers.CharField(max_length=20, min_length=5, write_only=True, )
        }
)