from django.shortcuts import render
from cart.models import Product  # استيراد جدول المنتجات من قاعدة البيانات

def home_view(request):
    if 'reset' in request.GET:
        request.session.pop('contact_success', None)
        contact_success = False
    else:
        contact_success = request.session.pop('contact_success', False)
    
    return render(request, 'home.html', {
        'products': Product.objects.all(),  
        'liked_product_ids': request.session.get('wishlist', []),
        'contact_success': contact_success,
    })