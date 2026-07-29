from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.urls import reverse
from .models import Order, ContactMessage, Product
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
import json

def product_detail_view(model_request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(model_request, 'cart/product_detail.html', {'product': product})

def cart_view(request):
    cart_key = f'cart_{request.user.id}' if request.user.is_authenticated else 'cart_guest'
    
    if 'new_items_count' in request.session:
        request.session['new_items_count'] = 0
        
    cart = request.session.get(cart_key, {})
    items = []
    total = 0
    for pid, qty in cart.items():
        try:
            prod = Product.objects.get(id=int(pid))
            subtotal = prod.price * qty
            items.append({
    'id': prod.id,
    'name': prod.name,
    'price': prod.price,
    'image': prod.image.url if prod.image else '',  # <--- تعديل هنا بإضافة .url
    'quantity': qty,
    'subtotal': subtotal,
})
            total += subtotal
        except Product.DoesNotExist:
            continue
            
    return render(request, 'cart/cart.html', {'items': items, 'total': total})

def add_to_cart(request, product_id):
    if not request.user.is_authenticated:
        return JsonResponse({'redirect': reverse('login')}, status=403)
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        cart_key = f'cart_{request.user.id}'
        cart = request.session.get(cart_key, {})
        pid = str(product_id)
        cart[pid] = cart.get(pid, 0) + 1
        request.session[cart_key] = cart
        
        new_items = request.session.get('new_items_count', 0) + 1
        request.session['new_items_count'] = new_items
        return JsonResponse({'success': True, 'cart_count': new_items})
    return JsonResponse({'success': False}, status=400)

def remove_from_cart(request, product_id):
    cart_key = f'cart_{request.user.id}' if request.user.is_authenticated else 'cart_guest'
    cart = request.session.get(cart_key, {})
    pid = str(product_id)
    if pid in cart:
        if cart[pid] > 1:
            cart[pid] -= 1
        else:
            del cart[pid]
    request.session[cart_key] = cart
    return redirect('cart')

def wishlist_view(request):
    wishlist_key = f'wishlist_{request.user.id}' if request.user.is_authenticated else 'wishlist_guest'
    wishlist = request.session.get(wishlist_key, [])
    items = Product.objects.filter(id__in=wishlist)
    return render(request, 'cart/wishlist.html', {'items': items})

def toggle_wishlist(request, product_id):
    if not request.user.is_authenticated:
        return JsonResponse({'redirect': reverse('login')}, status=403)
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        wishlist_key = f'wishlist_{request.user.id}'
        wishlist = request.session.get(wishlist_key, [])
        pid = int(product_id)
        if pid in wishlist:
            wishlist.remove(pid)
            liked = False
        else:
            wishlist.append(pid)
            liked = True
        request.session[wishlist_key] = wishlist
        return JsonResponse({'success': True, 'liked': liked, 'wishlist_count': len(wishlist)})
    return JsonResponse({'success': False}, status=400)

def checkout_view(request):
    if request.GET.get('placed') == '1':
        return render(request, 'cart/checkout.html')  
    cart_key = f'cart_{request.user.id}' if request.user.is_authenticated else 'cart_guest'
    cart = request.session.get(cart_key, {})
    if not cart:
        messages.warning(request, "Your cart is empty.")
        return redirect('cart')
    return render(request, 'cart/checkout.html')

def place_order(request):
    if request.method == 'POST':
        cart_key = f'cart_{request.user.id}' if request.user.is_authenticated else 'cart_guest'
        cart = request.session.get(cart_key, {})
        if not cart:
            messages.error(request, "Cart is empty.")
            return redirect('cart')

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        city = request.POST.get('city')
        phone = request.POST.get('phone')
        email = request.POST.get('email', '')

        items = []
        total = 0
        for pid, qty in cart.items():
            try:
                prod = Product.objects.get(id=int(pid))
                subtotal = prod.price * qty
                items.append({
                    'name': prod.name,
                    'price': str(prod.price),
                    'quantity': qty,
                    'subtotal': str(subtotal),
                })
                total += subtotal
            except Product.DoesNotExist:
                continue

        Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            first_name=first_name,
            last_name=last_name,
            address=address,
            city=city,
            phone=phone,
            email=email,
            items_data=json.dumps(items),  
            total=total,
        )

        request.session[cart_key] = {}
        messages.success(request, "Order placed successfully! Payment on delivery.")
        return redirect(reverse('checkout') + '?placed=1')
    else:
        return redirect('checkout')

def orders_view(request):
    orders = Order.objects.all().order_by('-created_at')
    for order in orders:
        order.items_data = json.loads(order.items_data)
    return render(request, 'cart/orders.html', {'orders': orders})

def all_products_view(request):
    products = Product.objects.all()  
    return render(request, 'cart/all_products.html', {'products': products})

def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        if name and email and phone and message:
            ContactMessage.objects.create(
                name=name,
                email=email,
                phone=phone,
                message=message,
            )
            request.session['contact_success'] = True
            return redirect(reverse('home') + '#contact')
        else:
            messages.error(request, 'Please fill all required fields.')
            return redirect(reverse('home') + '#contact')
    return redirect('home')

@staff_member_required(login_url='login')
def contact_messages_view(request):
    msgs = ContactMessage.objects.all().order_by('-created_at')
    return render(request, 'cart/contact_messages.html', {'messages': msgs})

@login_required
def my_orders_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    for order in orders:
        order.items_data = json.loads(order.items_data)
    return render(request, 'cart/my_orders.html', {'orders': orders})

@login_required
def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if request.method == 'POST':
        order.delete()
        messages.success(request, 'Order deleted successfully.')
    return redirect('my_orders')