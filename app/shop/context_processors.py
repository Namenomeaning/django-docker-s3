from .models import Cart


def cart_context(request):
    """
    Context processor to make cart data available in all templates
    """
    cart = None
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            pass
    else:
        if request.session.session_key:
            try:
                cart = Cart.objects.get(session_key=request.session.session_key)
            except Cart.DoesNotExist:
                pass
    
    return {'cart': cart}
