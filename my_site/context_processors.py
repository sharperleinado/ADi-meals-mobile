from cart.models import Cart




def context_render(request):
    cart = ""
    fname = ""
    cart_quantity = ""
    try:
        if request.user.is_authenticated:
            cart = Cart.objects.get(user=request.user)
            cart_quantity = cart.total_quantity()
            fname = request.user.first_name
        else:
            cart = Cart.objects.get(session_id=request.session['cart_users'],is_paid=False)
            cart_quantity = cart.total_quantity()
            fname = "Anonymous"
    except:
        cart_quantity = 0
    
    return {'cart':cart,'cart_quantity':cart_quantity,'fname':fname}
        

