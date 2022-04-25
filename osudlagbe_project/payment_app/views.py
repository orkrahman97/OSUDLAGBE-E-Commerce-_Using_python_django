from django.shortcuts import render, HttpResponseRedirect, redirect
from django.urls import reverse
from django.contrib import messages
#models and forms
from order_app.models import Order, Cart
from payment_app.models import BillingAddress
from payment_app.forms import BillingForm


from django.contrib.auth.decorators import login_required

# for payment
import requests
from sslcommerz_python_api import SSLCSession
from decimal import Decimal
import socket
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@login_required
def checkout(request):
    saved_address = BillingAddress.objects.get_or_create(user=request.user)
    saved_address = saved_address[0]
    print(saved_address)
    form = BillingForm(instance=saved_address)
    if request.method == "POST":
        form = BillingForm(request.POST, instance=saved_address)
        if form.is_valid():
            form.save()
            form = BillingForm(instance=saved_address)
            messages.success(request, f"Shipping Address Saved!")
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    #print(order_qs)
    order_items = order_qs[0].orderitem.all()
    #print(order_items)
    order_total = order_qs[0].get_totals()
    return render(request, 'payment_templates/checkout.html', context={"form":form, "order_items":order_items, "order_total":order_total, "saved_address":saved_address})

@login_required
def payment(request):
    saved_address = BillingAddress.objects.get_or_create(user=request.user)
    saved_address = saved_address[0]
    if not saved_address.is_fully_filled():
        messages.info(request, f"Please complete shipping address!")
        return redirect("payment_app:checkout")

    if not request.user.profile.is_fully_filled():
        messages.info(request, f"Please complete profile details!")
        return redirect("login_app:user_profile")

    store_id = 'ppp61e31eac0f3d0'
    API_key = 'ppp61e31eac0f3d0@ssl'
    mypayment = SSLCSession(sslc_is_sandbox=True, sslc_store_id=store_id, sslc_store_pass=API_key)

    status_url = request.build_absolute_uri(reverse("payment_app:complete"))
    #print(status_url)
    mypayment.set_urls(success_url=status_url, fail_url=status_url, cancel_url=status_url, ipn_url=status_url)

    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order_items = order_qs[0].orderitem.all()
    order_items_count = order_qs[0].orderitem.count()
    order_total = order_qs[0].get_totals()

    mypayment.set_product_integration(total_amount=Decimal(order_total), currency='BDT', product_category='Mixed', product_name=order_items, num_of_item=order_items_count, shipping_method='Courier', product_profile='None')


    current_user = request.user
    mypayment.set_customer_info(name=current_user.profile.fullname, email=current_user.email, address1=current_user.profile.address, address2=current_user.profile.address, city=current_user.profile.city, postcode=current_user.profile.zipcode, country=current_user.profile.country, phone=current_user.profile.phone)

    mypayment.set_shipping_info(shipping_to=current_user.profile.fullname, address=saved_address.address, city=saved_address.city, postcode=saved_address.zipcode, country=saved_address.country)

    response_data = mypayment.init_payment()
    print(response_data)
    return redirect(response_data['GatewayPageURL'])


@csrf_exempt
def complete(request):
    if request.method == 'POST' or request.method == 'post':
        payment_data = request.POST
        print(payment_data)
        status = payment_data['status']

        if status == 'VALID':
            val_id = payment_data['val_id']
            tran_id = payment_data['tran_id']
            messages.success(request,f"Payment Completed Successfully!")
            return HttpResponseRedirect(reverse("payment_app:purchase", kwargs={'val_id':val_id, 'tran_id':tran_id},))
        elif status == 'FAILED':
            messages.warning(request, f"Payment Failed! Please Try Again!")

    return render(request, "payment_templates/complete.html", context={})

@login_required
def purchase(request, val_id, tran_id):
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order = order_qs[0]
    order_id = tran_id
    order.ordered = True
    order.order_id= order_id
    order.paymentId = val_id
    order.save()
    cart_items = Cart.objects.filter(user=request.user, purchased=False)
    for item in cart_items:
        item.purchased = True
        item.save()
    return HttpResponseRedirect(reverse("store_app:home"))

@login_required
def order_view(request):
    try:
        orders = Order.objects.filter(user=request.user, ordered=True)
        context = {"orders": orders}
    except:
        messages.warning(request, "You do no have an active order")
        return redirect("store_app:home")
    return render(request, "payment_templates/order.html", context)