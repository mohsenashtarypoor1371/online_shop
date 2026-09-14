from django.shortcuts import get_object_or_404

from .models import Order, OrderItem


def pending_order(request):
    if request.user.is_authenticated:
            pending = Order.objects.filter(user=request.user,status='pending').last()
            return {'pending':pending}
    else:
        pending = Order.objects.filter(session_key=request.session.session_key,
                                       status='pending').last()
        return {'pending':pending}
