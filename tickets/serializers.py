from rest_framework import serializers

from .models import Guest,Reserveration,Movie,Post


class GuestSerializers(serializers.ModelSerializer):
    class Meta:
        model=Guest
        fields=['pk','Reservation','name','mobile']

class MovieSerializers(serializers.ModelSerializer):
    class Meta:
        model=Movie
        fields='__all__'

class ReserverationSerializers(serializers.ModelSerializer):
    class Meta:
        model=Reserveration
        fields='__all__'
class PostSerializers(serializers.ModelSerializer):
    class Meta:
        model=Post
        fields='__all__'