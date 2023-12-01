from django.urls import path

from . import views

urlpatterns = [
    path('item/<int:item_id>/', views.item, name='item'),
    path('order/<int:order_id>/', views.order, name='order'),
    path('config/', views.stripe_config),
    path('buy_item/<int:item_id>/', views.buy_item),
    path('buy_order/<int:total_price>/', views.buy_order),
    path('success/', views.SuccessView.as_view()),
    path('cancelled/', views.CancelledView.as_view()),
]
