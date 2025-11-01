# shop/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Cart, CartItem, Order, OrderItem, UserFeedback # MODIFIED IMPORT
from django.db.models import Case, When, Sum
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User # Make sure User is imported

# Import our new super-fast Cython function!
from .recommender_cy import get_recommendations_cy

# --- Product List View ---
def product_list(request):
    products = Product.objects.all()
    return render(request, 'shop/product_list.html', {'products': products})

# --- Product Detail View (MODIFIED) ---
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    # --- START OF NEW/MODIFIED CODE ---
    
    # Get the user's feedback, but only if they are logged in
    liked_ids = set()
    disliked_ids = set()
    if request.user.is_authenticated:
        liked_ids = set(UserFeedback.objects.filter(
            user=request.user, feedback=UserFeedback.LIKE
        ).values_list('product_id', flat=True))
        
        disliked_ids = set(UserFeedback.objects.filter(
            user=request.user, feedback=UserFeedback.DISLIKE
        ).values_list('product_id', flat=True))

    # --- END OF NEW/MODIFIED CODE ---

    # Get data for the Cython function
    all_products_data = [
        (p.id, p.get_tags_list()) 
        for p in Product.objects.exclude(pk=product.pk)
    ]
    
    # Call the *fast* Cython function with the new feedback data
    recommended_ids = get_recommendations_cy(
        product.get_tags_list(), 
        all_products_data,
        liked_ids,           # Pass liked IDs
        disliked_ids         # Pass disliked IDs
    )
    
    # Get the full Product objects from the recommended IDs
    preserved_order = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(recommended_ids)])
    recommended_products = Product.objects.filter(pk__in=recommended_ids).order_by(preserved_order)

    context = {
        'product': product,
        'recommended_products': recommended_products
    }
    return render(request, 'shop/product_detail.html', context)

# --- Cart and Checkout Views (Existing) ---

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, item_created = CartItem.objects.get_or_create(
        cart=cart, 
        product=product
    )
    
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()
        
    return redirect('view_cart')

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
        
    return redirect('view_cart')

@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    total_price = sum(item.get_total_price() for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'total_price': total_price
    }
    return render(request, 'shop/view_cart.html', context)

@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = cart.items.all()

    if not cart_items:
        return redirect('view_cart')

    total_amount = sum(item.get_total_price() for item in cart_items)
    order = Order.objects.create(
        user=request.user,
        total_amount=total_amount
    )

    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )
    
    cart_items.delete()
    return render(request, 'shop/order_complete.html', {'order': order})

# --- Feedback View (NEW) ---

@login_required
def submit_feedback(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    feedback_type = int(request.POST.get('feedback_type')) # Get 1 for Like, -1 for Dislike

    if feedback_type in [UserFeedback.LIKE, UserFeedback.DISLIKE]:
        # Update or create the feedback
        UserFeedback.objects.update_or_create(
            user=request.user,
            product=product,
            defaults={'feedback': feedback_type}
        )
    
    # Send the user back to the product page they were just on
    return redirect('product_detail', pk=product_id)