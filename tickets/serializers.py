from rest_framework import serializers
from .models import Movie , Guest, Reservation,Post

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model =Movie
        fields = '__all__'

class ReservatinoSerailizer(serializers.ModelSerializer):
    class Meta:
        model= Reservation
        fields = '__all__'


class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model =Guest
        fields=['pk','reservations','name','mobile']

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model =Post
        fields='__all__'