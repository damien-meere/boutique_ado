from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.contrib import messages

from products.models import Product
# Create your views here.


def view_bag(request):
    """ View to return shopping bag page"""
    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    # the contents of the shopping 'bag' will persist within the HTTP session
    # maintained between the cliet browser and the django server itself
    bag = request.session.get('bag', {})

    # if the products has a size parameter
    if size:
        # If the item is already in the bag.
        if item_id in list(bag.keys()):
            # check if another item of the same id and same size exists
            if size in bag[item_id]['items_by_size'].keys():
                # increment the quantity for that size
                bag[item_id]['items_by_size'][size] += quantity
                messages.success(request, f'Added Size {size.upper()} {product.name} quantity to {bag[item_id]["items_by_size"][size]}')
            else:
                # otherwise just set it equal to the quantity.
                bag[item_id]['items_by_size'][size] = quantity
                messages.success(request, f'Added Size {size.upper()} {product.name} to your bag')
        else:
            bag[item_id] = {'items_by_size': {size: quantity}}
            messages.success(request, f'Added Size {size.upper()} {product.name} to your bag')
    # if the products has no size parameter
    else:
        # Within the bag dictionary, create a key of the items id and
        # set it equal to the quantity. If the item is already in the bag in
        # other words if there's already a key in the bag dictionary matching
        # this product id, increment its quantity accordingly.
        if item_id in list(bag.keys()):
            bag[item_id] += quantity
            messages.success(request, f'Updated {product.name} quantity to {bag[item_id]}')
        else:
            bag[item_id] = quantity
            messages.success(request, f'Added {product.name} to your bag')

    # overwrite the bag variable in the session with the updated version
    request.session['bag'] = bag
    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """Adjust the quantity of the specified product to the specified amount"""

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    # the contents of the shopping 'bag' will persist within the HTTP session
    # maintained between the cliet browser and the django server itself
    bag = request.session.get('bag', {})

    # If there's a size, we'll need to drill into the items_by_size dictionary,
    # find that specific size and either set its quantity
    # to the updated one or remove it if the quantity submitted is zero.
    if size:
        if quantity > 0:
            bag[item_id]['items_by_size'][size] = quantity
            messages.success(request, f'Added Size {size.upper()} {product.name} quantity to {bag[item_id]["items_by_size"][size]}')
        else:
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
            messages.success(request, f'Removed Size {size.upper()} {product.name} from your bag')
    else:
        if quantity > 0:
            bag[item_id] = quantity
            messages.success(request, f'Updated {product.name} quantity to {bag[item_id]}')
        else:
            bag.pop(item_id)
            messages.success(request, f'Removed {product.name} from your bag')

    # overwrite the bag variable in the session with the updated version
    request.session['bag'] = bag
    return redirect(reverse('view_bag'))


def remove_from_bag(request, item_id):
    """Remove the item from the shopping bag"""
    try:
        product = get_object_or_404(Product, pk=item_id)
        size = None
        if 'product_size' in request.POST:
            size = request.POST['product_size']
        bag = request.session.get('bag', {})

        if size:
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
            messages.success(request, f'Removed Size {size.upper()} {product.name} from your bag')
        else:
            bag.pop(item_id)
            messages.success(request, f'Removed {product.name} from your bag')

        # overwrite the bag variable in the session with the updated version
        request.session['bag'] = bag
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)
