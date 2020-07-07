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
        'order_form': order_form
    }

    return render(request, template, context)
