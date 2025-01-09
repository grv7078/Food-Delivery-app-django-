# from django.shortcuts import render, redirect
# from django.contrib import messages
# from .forms import RestaurantForm

# def add_restaurant(request):
#     if request.method == 'POST':
#         form = RestaurantForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Restaurant added successfully!')
#             return redirect('add_restaurant')  # Redirect back to the same page to show the message
#     else:
#         form = RestaurantForm()
#     return render(request, 'add_restaurant.html', {'form': form})


from django.shortcuts import render, get_object_or_404, redirect
from .models import MenuItem
from .forms import MenuItemForm

def add_menu_item(request):
    if request.method == 'POST':
        form = MenuItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('menu_item_list') 
    else:
        form = MenuItemForm()
    return render(request, 'restaurant/add_menu_item.html', {'form': form})

def update_menu_item(request, pk):
    menu_item = get_object_or_404(MenuItem, pk=pk)
    if request.method == 'POST':
        form = MenuItemForm(request.POST, instance=menu_item)
        if form.is_valid():
            form.save()
            return redirect('menu_item_list')
    else:
        form = MenuItemForm(instance=menu_item)
    return render(request, 'restaurant/update_menu_item.html', {'form': form})

def delete_menu_item(request, pk):
    menu_item = get_object_or_404(MenuItem, pk=pk)
    if request.method == 'POST':
        menu_item.delete()
        return redirect('menu_item_list')
    return render(request, 'restaurant/delete_menu_item.html', {'menu_item': menu_item})

def menu_item_list(request):
    menu_items = MenuItem.objects.all()
    return render(request, 'restaurant/menu_item_list.html', {'menu_items': menu_items})




from .models import Restaurant, MenuItem, Order, OrderItem
from .forms import OrderForm
from decimal import Decimal

def place_order(request, restaurant_id):
    restaurant = Restaurant.objects.get(id=restaurant_id)

    if request.method == 'POST':
        form = OrderForm(request.POST)

        if form.is_valid():
            # Validate availability
            menu_items = form.cleaned_data['menu_items']
            unavailable_items = [item for item in menu_items if not item.available]
            if unavailable_items:
                return render(request, 'place_order.html', {'form': form, 'restaurant': restaurant, 'error': 'Some items are unavailable.'})

            # Calculate total cost
            total_cost = Decimal(0)
            for item in menu_items:
                total_cost += item.price * form.cleaned_data['quantity']

            # Create the order
            order = form.save(commit=False)
            order.restaurant = restaurant
            order.total_cost = total_cost
            order.save()

            # Save OrderItems
            for item in menu_items:
                OrderItem.objects.create(order=order, menu_item=item, quantity=form.cleaned_data['quantity'], price=item.price)

            return redirect('order_success') 

    else:
        form = OrderForm()

    return render(request, 'place_order.html', {'form': form, 'restaurant': restaurant})


def order_success(request):
    return render(request, 'order_success.html')



from django.db.models import Sum, Count, F, Avg
from django.utils.timezone import now
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Restaurant, MenuItem, Order, OrderItem
from .serializers import RevenueSerializer, PopularMenuItemSerializer, DeliveryTimeSerializer

class TotalRevenueView(APIView):
    def get(self, request):
        revenue_data = Order.objects.values('restaurant__name').annotate(
            total_revenue=Sum('total_cost')
        )
        serializer = RevenueSerializer(revenue_data, many=True)
        return Response(serializer.data)

class PopularMenuItemsView(APIView):
    def get(self, request):
        popular_items = OrderItem.objects.values('menu_item__name').annotate(
            order_count=Count('menu_item')
        ).order_by('-order_count')[:10]  # Top 10 most popular items
        serializer = PopularMenuItemSerializer(popular_items, many=True)
        return Response(serializer.data)

class AverageDeliveryTimeView(APIView):
    def get(self, request):
        delivery_times = Order.objects.annotate(
            delivery_duration=F('order_date') - now()
        ).aggregate(
            average_delivery_time=Avg('delivery_duration')
        )
        serializer = DeliveryTimeSerializer(delivery_times)
        return Response(serializer.data)


from django.shortcuts import render
from .models import MenuItem

def menu_item_list(request):
    menu_items = MenuItem.objects.all()
    return render(request, 'restaurant/menu_item.html', {'menu_items': menu_items})





from django.http import JsonResponse
from .models import OrderTracking
from .firebase_utils import send_push_notification_to_user

def place_order(request):
    order = OrderTracking.objects.create(user=request.user)
   
    user_device_token = request.user.profile.device_token  # Adjust based on your user profile model

    send_push_notification_to_user(
        user_device_token,
        "Order Confirmation",
        f"Your order {order.id} has been placed successfully!"
    )

    return JsonResponse({"message": "Order placed", "order_id": order.id})


from django.http import JsonResponse
from .models import OrderTracking
from .firebase_utils import send_order_status_update  # Assuming this function exists

def update_order_status(request, order_id):
    try:
        # Fetch the order by its ID
        order = OrderTracking.objects.get(id=order_id)
    except OrderTracking.DoesNotExist:
        return JsonResponse({"message": "Order not found"}, status=404)
    
    new_status = request.GET.get('status')

    # Validate if the provided status is correct
    if new_status in dict(OrderTracking.STATUS_CHOICES):
        order.status = new_status
        order.save()

        user_device_token = order.user.profile.device_token  # Adjust based on your user profile model

        # Check if device token exists
        if user_device_token:
            # Send the order status update push notification
            send_order_status_update(user_device_token, order.id, order.get_status_display())
        else:
            return JsonResponse({"message": "User's device token not found"}, status=400)

        return JsonResponse({"message": "Order status updated", "status": order.status})

    return JsonResponse({"message": "Invalid status"}, status=400)


from django.http import JsonResponse
from django.db.models import Sum
from .models import Restaurant

def total_revenue_per_restaurant(request):
    revenue_data = Restaurant.objects.annotate(total_revenue=Sum('ordertracking__amount')).values('name', 'total_revenue')

    return JsonResponse({"data": list(revenue_data)})


from django.db.models import Count
from .models import MenuItem

def most_popular_menu_items(request):
    popular_items = MenuItem.objects.annotate(order_count=Count('orderitem')).order_by('-order_count')

    # Prepare the data to return
    popular_items_data = popular_items.values('name', 'order_count')

    return JsonResponse({"data": list(popular_items_data)})


from datetime import timedelta
from django.db.models import Avg
from django.utils.timezone import now
from .models import OrderTracking

def average_order_delivery_time(request):
    delivered_orders = OrderTracking.objects.filter(status='DELIVERED')
    avg_delivery_time = delivered_orders.aggregate(avg_time=Avg('updated_at' - 'created_at'))
    if avg_delivery_time['avg_time']:
        avg_time_minutes = avg_delivery_time['avg_time'].total_seconds() / 60  # in minutes
    else:
        avg_time_minutes = 0

    return JsonResponse({"average_delivery_time_minutes": avg_time_minutes})
