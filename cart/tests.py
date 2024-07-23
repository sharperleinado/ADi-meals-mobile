from django.test import TestCase

# Create your tests here.
'''
cart_pk = CartItemsFood.objects.get(cart=request.user)

        if request.method == "POST":
            payment_method = request.POST.get("paymentMethod")
            print(payment_method)
            if payment_method:
                return redirect(reverse('payments:flutterwave', kwargs={
                    'username': username,
                    'email': address.user.email,
                    'phone_no': phone_no,
                    'price': cart.total_price(),
                    'pk': cart_pk.pk,
                }))'''