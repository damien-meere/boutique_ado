from django.shortcuts import render, redirect

# Create your views here.


def view_bag(request):
    """ View to return shopping bag page"""
    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """
    quantity = request.POST.get('quantity')
    redirect_url = request.POST.get('redirect_url')
    # the contents of the shopping 'bag' will persist within the HTTP session
    # maintained between the cliet browser and the django server itself
    bag = request.session.get('bag', {})

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
    print(request.session['bag'])
    return redirect(redirect_url)
