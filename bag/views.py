from django.shortcuts import render, redirect, reverse, HttpResponse

# Create your views here.

def view_bag(request):
    """ A view that renders the baf contents page
    """
    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """
    Add a quantity of the specified product to the shopping bag.
    """

    # Get the quantity of the product from the POST request and convert it to an integer
    quantity = int(request.POST.get('quantity'))
    
    # Get the URL to redirect to after adding the product to the bag
    redirect_url = request.POST.get('redirect_url')
    
    # Retrieve the current shopping bag from the session, or initialize an empty bag if none exists
    bag = request.session.get('bag', {})
    
    # Initialize size as None; this will hold the product size if provided
    size = None
    
    # Check if a product size is included in the POST data; if so, set the size variable
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    
    # Check if the product has a size
    if size:
        # If the product is already in the bag
        if item_id in list(bag.keys()):
            # Check if the specific size of the product is already in the bag
            if size in bag[item_id]['items_by_size'].keys():
                # Increase the quantity of the product for that size
                bag[item_id]['items_by_size'][size] += quantity
            else:
                # Add the size to the product's size dictionary with the given quantity
                bag[item_id]['items_by_size'][size] = quantity
        else:
            # If the product is not in the bag, add it with its size and quantity
            bag[item_id] = {'items_by_size': {size: quantity}}
    else:
        # If the product does not have a size
        if item_id in list(bag.keys()):
            # Increase the quantity of the product
            bag[item_id] += quantity
        else:
            # Add the product to the bag with the given quantity
            bag[item_id] = quantity

    # Update the session with the modified shopping bag
    request.session['bag'] = bag
    
    # Redirect the user to the URL provided in the POST request
    return redirect(redirect_url)

def adjust_bag(request, item_id):
    """
    Adjust the quantity of products in the shopping bag.
    """

    # Get the new quantity of the product from the POST request and convert it to an integer
    quantity = int(request.POST.get('quantity'))
    
    # Initialize size as None; this will hold the product size if provided
    size = None
    
    # Check if a product size is included in the POST data; if so, set the size variable
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    # Retrieve the current shopping bag from the session, or initialize an empty bag if none exists
    bag = request.session.get('bag', {})
    # Check if the product has a size
    if size:
        # If the quantity is greater than zero, update the quantity for the specific size
        if quantity > 0:
            bag[item_id]['items_by_size'][size] = quantity
        else:
            # If the quantity is zero or less, remove the size from the product's size dictionary
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
    else:
        # If the product does not have a size
        if quantity > 0:
            # Update the quantity of the product in the bag
            bag[item_id] = quantity
        else:
            # If the quantity is zero or less, remove the product from the bag
            bag.pop(item_id)

    # Update the session with the modified shopping bag
    request.session['bag'] = bag
    # Redirect the user to the 'view_bag' page
    return redirect(reverse('view_bag'))

def remove_from_bag(request, item_id):
    """
    Adjust the quantity of products in the shopping bag.
    """
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


        request.session['bag'] = bag
        return HttpResponse(status=200)
    except Exception as e:
        return HttpResponse(status=500)

