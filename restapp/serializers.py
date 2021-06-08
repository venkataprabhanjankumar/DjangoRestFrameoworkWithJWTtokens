from rest_framework import serializers
from .models import Products
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email")


class ProductsSerializer(serializers.ModelSerializer):
    productName = serializers.CharField(required=False)
    productCategory = serializers.CharField(required=False)
    productCount = serializers.IntegerField(required=False)

    class Meta:
        model = Products
        fields = ("productName", "productCategory", "productCount")
