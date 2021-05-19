from datetime import datetime

from django.utils import timezone
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, reverse

from cart.cart import Cart
from coupons.models import Coupon
from coupons.forms import CouponApplyForm


@require_POST
def coupon_apply_view(request):
    cart = Cart(request=request)
    # now = datetime.now()
    now = timezone.now()
    form = CouponApplyForm(request.POST)
    coupon_id = cart.coupon_id
    if form.is_valid():
        code = form.cleaned_data['code']

        arguments = {
            'code__iexact': code,
            'valid_from__lte': now,
            'valid_to__gte': now,
            'active': True,
        }
        coupon = Coupon.objects.filter(**arguments).first()
        if coupon:
            request.session['coupon_id'] = coupon.pk
        else:
            request.session['coupon_id'] = coupon_id
    return redirect(reverse('cart:detail_cart'))


def coupon_delete_view(request):
    try:
        del request.session['coupon_id']
    except KeyError:
        pass
    return redirect(reverse('cart:detail_cart'))
