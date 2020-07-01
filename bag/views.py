from django.shortcuts import render, redirect, reverse, HttpResponse

# Create your views here.


def view_bag(request):
    """ View to return shopping bag page"""
    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """
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
            else:
                # otherwise just set it equal to the quantity.
                bag[item_id]['items_by_size'][size] = quantity
        else:
            bag[item_id] = {'items_by_size': {size: quantity}}
    # if the products has no size parameter
    else:
        # Within the bag dictionary, create a key of the items id and
        # set it equal to the quantity. If the item is already in the bag in
        # other words if there's already a key in the bag dictionary matching
        # this product id, increment its quantity accordingly.
        if item_id in list(bag.keys()):
            bag[item_id] += quantity
        else:
            bag[item_id] = quantity

    # overwrite the bag variable in the session with the updated version
    request.session['bag'] = bag
    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """ Adjust the quantity of the specified product to the requisite amount """

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
        else:
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
    else:
        if quantity > 0:
            bag[item_id] = quantity
        else:
            bag.pop(item_id)

    # overwrite the bag variable in the session with the updated version
    request.session['bag'] = bag
    return redirect(reverse('view_bag'))


def remove_from_bag(request, item_id):
    """ Remove an item from the shopping bag """

    try:
        size = None
        if 'product_size' in request.POST:
            size = request.POST['product_size']
        bag = request.session.get('bag', {})

        if size:
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
        else:
            bag.pop(item_id)

        # overwrite the bag variable in the session with the updated version
        request.session['bag'] = bag
        return HttpResponse(status=200)
    except Exception as e:
        return HttpResponse(status=500)
