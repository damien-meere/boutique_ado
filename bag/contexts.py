from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product

# Funtion will return a dictionary called context which makes this
# dictionary agailable to all templates across the entire application


def bag_contents(request):

    bag_items = []
    total = 0
    product_count = 0
    # Getting session 'bag' if it already exists. Or initializing it
    # to an empty dictionary if not.
    bag = request.session.get('bag', {})

    # The item data will just be the quantity. But in the case of an
    # item that has sizes the sitem data will be a dictionary of all
    # the items by size.
    for item_id, item_data in bag.items():
        # only want to execute this code if the item has no sizes.
        # Which will be evident by checking whether or not the item
        # data is an integer.
        if isinstance(item_data, int):
            product = get_object_or_404(Product, pk=item_id)
            total += item_data * product.price
            product_count += item_data
            bag_items.append({
                'item_id': item_id,
                'quantity': item_data,
                'product': product,
            })
        else:
            product = get_object_or_404(Product, pk=item_id)
            for size, quantity in item_data['items_by_size'].items():
                total += quantity * product.price
                product_count += quantity
                bag_items.append({
                    'item_id': item_id,
                    'quantity': quantity,
                    'product': product,
                    'size': size,
                })

    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery_delta = 0
    
    grand_total = delivery + total
    
    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }

    return context
