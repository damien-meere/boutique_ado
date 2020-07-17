from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm


def checkout(request):
    bag = request.session.get('bag', {})
    # If there's nothing in the bag just add a simple error message.
    # And redirect back to the products page. This will prevent people
    # from manually accessing the URL by typing /checkout
    if not bag:
        messages.error(request, "This is nothing in your bag")
        return redirect(reverse('products'))

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51H5v9oII1DOczrG4xAuFZE9jU7t1d7fop6wRBE7Yuw6aMx1stP9VSlb7DQpFSLEZTIK9VhxdBafOkegGlOB5NXCZ00QaagRrTW',
        'client_secret': 'test client secret',
    }

    return render(request, template, context)
