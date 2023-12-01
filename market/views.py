import stripe
from django.conf import settings
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView

from .models import Item, ItemInOrder


def item(request, item_id):
    template = 'item.html'
    item = get_object_or_404(Item, pk=item_id)
    context = {
        'item': item,
    }
    return render(request, template, context)


def order(request, order_id):
    template = 'order.html'
    items = ItemInOrder.objects.filter(order__id=order_id)
    total_price = sum([item.item.price for item in items])
    context = {
        'items': items,
        'total_price': total_price
    }
    return render(request, template, context)


@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


@csrf_exempt
def buy_item(request, item_id):
    if request.method == 'GET':
        item = Item.objects.get(id=int(item_id))
        domain_url = 'http://localhost:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',  # noqa
                cancel_url=domain_url + 'cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        "price_data": {
                            "currency": item.currency,
                            "unit_amount": item.price,
                            "product_data": {
                                "name": item.name,
                                "description": item.description,
                            },
                        },
                        "quantity": 1,
                    }
                ],
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})


@csrf_exempt
def buy_order(request, total_price):
    if request.method == 'GET':
        domain_url = 'http://localhost:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',  # noqa
                cancel_url=domain_url + 'cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        "price_data": {
                            "currency": "usd",
                            "unit_amount": total_price,
                            "product_data": {
                                "name": 'order',
                            },
                        },
                        "quantity": 1,
                    }
                ],
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})


class SuccessView(TemplateView):
    template_name = 'success.html'


class CancelledView(TemplateView):
    template_name = 'cancelled.html'
