from datetime import datetime

from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, reverse

from coupons.models import Coupon
from coupons.forms import CouponApplyForm


@require_POST
def coupon_apply_view(request):
    now = datetime.now()
    form = CouponApplyForm(request.POST)
    coupon = None
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
        request.session['coupon_id'] = coupon
    return redirect(reverse('cart:detail_cart'))
