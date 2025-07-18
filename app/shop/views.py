from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.sessions.models import Session
from django.core.cache import cache
from .models import Category, Product, Cart, CartItem, Order, OrderItem
from .forms import OrderCreateForm


def product_list(request, category_slug=None):
    # Create cache key
    cache_key = f'product_list_{category_slug or "all"}'
    
    # Try to get from cache
    cached_data = cache.get(cache_key)
    if cached_data:
        print(f"✅ CACHE HIT: Retrieved product list from cache for key: {cache_key}")
        return render(request, 'shop/product_list.html', cached_data)
    
    print(f"❌ CACHE MISS: Fetching product list from database for key: {cache_key}")
    
    # If not in cache, fetch from database
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    # Prepare data for template
    context_data = {
        'category': category,
        'categories': categories,
        'products': products
    }
    
    # Store in cache for 5 minutes (300 seconds)
    cache.set(cache_key, context_data, 300)
    print(f"💾 CACHED: Stored product list in cache for key: {cache_key}")
    
    return render(request, 'shop/product_list.html', context_data)


def product_detail(request, id, slug):
    # Create cache key
    cache_key = f'product_detail_{id}_{slug}'
    
    # Try to get from cache
    cached_product = cache.get(cache_key)
    if cached_product:
        print(f"✅ CACHE HIT: Retrieved product detail from cache for key: {cache_key}")
        return render(request, 'shop/product_detail.html', {'product': cached_product})
    
    print(f"❌ CACHE MISS: Fetching product detail from database for key: {cache_key}")
    
    # If not in cache, fetch from database
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    
    # Store in cache for 10 minutes (600 seconds)
    cache.set(cache_key, product, 600)
    print(f"💾 CACHED: Stored product detail in cache for key: {cache_key}")
    
    return render(request, 'shop/product_detail.html', {'product': product})


def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        cart, created = Cart.objects.get_or_create(session_key=request.session.session_key)
    return cart


@require_POST
def cart_add(request, product_id):
    cart = get_or_create_cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': quantity}
    )
    
    if not created:
        cart_item.quantity += quantity
        cart_item.save()
    
    messages.success(request, f'{product.name} added to cart!')
    return redirect('shop:cart_detail')


def cart_detail(request):
    cart = get_or_create_cart(request)
    return render(request, 'shop/cart_detail.html', {'cart': cart})


@require_POST
def cart_remove(request, product_id):
    cart = get_or_create_cart(request)
    product = get_object_or_404(Product, id=product_id)
    
    try:
        cart_item = CartItem.objects.get(cart=cart, product=product)
        cart_item.delete()
        messages.success(request, f'{product.name} removed from cart!')
    except CartItem.DoesNotExist:
        pass
    
    return redirect('shop:cart_detail')


def order_create(request):
    cart = get_or_create_cart(request)
    
    if cart.items.count() == 0:
        messages.error(request, 'Your cart is empty!')
        return redirect('shop:cart_detail')
    
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.save()
            
            # Create order items from cart
            for cart_item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    price=cart_item.product.price,
                    quantity=cart_item.quantity
                )
            
            # Clear the cart
            cart.items.all().delete()
            
            messages.success(request, f'Order #{order.id} created successfully!')
            return render(request, 'shop/order_created.html', {'order': order})
    else:
        form = OrderCreateForm()
    
    return render(request, 'shop/order_create.html', {
        'cart': cart,
        'form': form
    })


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'shop/order_history.html', {'orders': orders})
