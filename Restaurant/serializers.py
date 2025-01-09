from rest_framework import serializers
from .models import Restaurant, MenuItem, Order, OrderItem

class RevenueSerializer(serializers.Serializer):
    restaurant_name = serializers.CharField()
    total_revenue = serializers.DecimalField(max_digits=10, decimal_places=2)

class PopularMenuItemSerializer(serializers.Serializer):
    item_name = serializers.CharField()
    order_count = serializers.IntegerField()

class DeliveryTimeSerializer(serializers.Serializer):
    average_delivery_time = serializers.DurationField()
