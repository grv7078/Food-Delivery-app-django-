from django.urls import path
from .views import (
    TotalRevenueView, 
    PopularMenuItemsView, 
    AverageDeliveryTimeView,
    menu_item_list,
    add_menu_item,
    update_menu_item,
    delete_menu_item,
    place_order,
    update_order_status,
    total_revenue_per_restaurant,
    most_popular_menu_items,
    average_order_delivery_time,
   
)

urlpatterns = [
    path('menu-items/', menu_item_list, name='menu_item'),
    path('menu-items/add/', add_menu_item, name='add_menu_item'),
    path('menu-items/<int:pk>/update/', update_menu_item, name='update_menu_item'),
    path('menu-items/<int:pk>/delete/', delete_menu_item, name='delete_menu_item'),
    path('restaurants/<int:restaurant_id>/order/', place_order, name='place_order'),
    path('api/revenue/', TotalRevenueView.as_view(), name='total_revenue'),
    path('api/popular-items/', PopularMenuItemsView.as_view(), name='popular_menu_items'),
    path('api/average-delivery-time/', AverageDeliveryTimeView.as_view(), name='average_delivery_time'),
    path('place-order/', place_order, name='place_order'),  # URL for placing an order
    path('update-order-status/<int:order_id>/', update_order_status, name='update_order_status'),

    path('total-revenue/', total_revenue_per_restaurant, name='total_revenue'),
    path('most-popular-menu-items/', most_popular_menu_items, name='most_popular_menu_items'),
    path('average-delivery-time/', average_order_delivery_time, name='average_delivery_time'),

    
]



