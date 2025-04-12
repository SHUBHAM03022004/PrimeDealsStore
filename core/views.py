from django.shortcuts import render, redirect
from core.forms import *
from django.contrib import messages
from core.models import *
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse



# Create your views here.
def index(request):
    products = Product.objects.all()
    return render(request, 'core/index.html', {'products': products})

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            print('True')
            form.save()
            print('Saved')
            messages.success(request, 'Product added successfully')
            return redirect('add_product')
        else:
            print('False')
            print(form.errors)
            messages.info(request, 'Error in form submission')

    else:
        form = ProductForm()
    return render(request, 'core/add_product.html', {'form': form})

def product_desc(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'core/product_desc.html', {'product': product})

def add_to_cart(request, pk):
    product = Product.objects.get(id=pk)
    order_item, created = OrderItem.objects.get_or_create(
        product=product,
        user=request.user,
        ordered=False,
    )

    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(product__id=pk).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, 'Added Quantity Item')
            return redirect('product_desc', pk=pk)
        else:
            order.items.add(order_item)
            messages.info(request, 'Item Added to cart')
            return redirect('product_desc', pk=pk)
        
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user,
            ordered_date=ordered_date,
        )
        order.items.add(order_item)
        messages.info(request, 'Item Added to cart')
        return redirect('product_desc', pk=pk)
    


def orderlist(request):
    if Order.objects.filter(user=request.user, ordered=False).exists():
        order = Order.objects.get(user=request.user, ordered=False)
        return render(request, 'core/orderlist.html', {'order': order})
    else:
        return render(request, 'core/orderlist.html', {'message': 'No items in cart'})
    

def add_item(request, pk):
    product = Product.objects.get(id=pk)
    order_item, created = OrderItem.objects.get_or_create(
        product=product,
        user=request.user,
        ordered=False,
    )

    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(product__id=pk).exists():
            if order_item.quantity < product.product_available_count:
                order_item.quantity += 1
                order_item.save()
                messages.info(request, 'Added Quantity Item')
                return redirect('orderlist')
            else:
                messages.info(request, 'Sorry! Item not in cart')
                return redirect('orderlist')
        else:
            order.items.add(order_item)
            messages.info(request, 'Item Added to cart')
            return redirect('product_desc', pk=pk)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user,
            ordered_date=ordered_date,
        )
        order.items.add(order_item)
        messages.info(request, 'Item Added to cart')
        return redirect('product_desc', pk=pk)


def remove_item(request, pk):
    item = get_object_or_404(Product, id=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(product__id=pk).exists():
            order_item = OrderItem.objects.filter(product=item, user=request.user, ordered=False).first()
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                # Remove the OrderItem from the Order and delete it
                order.items.remove(order_item)
                order_item.delete()
            messages.info(request, 'Removed quantity/item from your cart.')
            return redirect('orderlist')
        else:
            messages.info(request, 'Item not in your cart.')
            return redirect('orderlist')
    else:
        messages.info(request, "You don't have an active order.")
        return redirect('orderlist')
    
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CheckoutForm
from .models import CheckoutAddress
from django.core.exceptions import ObjectDoesNotExist

def checkout(request):
    if CheckoutAddress.objects.filter(user=request.user).exists():
        return render(request, 'core/checkout.html', {'payment_allow': "allow"})
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            street_address = form.cleaned_data.get('street_address')
            apartment_address = form.cleaned_data.get('apartment_address')
            country = form.cleaned_data.get('country')
            zip_code = form.cleaned_data.get('zip')

            try:
                checkout_address = CheckoutAddress(
                    user=request.user,
                    street_address=street_address,
                    apartment_address=apartment_address,
                    country=country,
                    zipcode=zip_code
                )
                checkout_address.save()
                messages.success(request, 'Checkout address saved successfully.')
                return render(request, 'core/checkout.html', {'payment_allow': "allow", 'form': form})
            except Exception as e:
                messages.warning(request, f'Error saving address: {e}')
                return redirect('checkout_page')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CheckoutForm()

    return render(request, 'core/checkout.html', {'form': form})




def simulate_payment(request):
    try:
        order = Order.objects.get(user=request.user, ordered=False)
        order.ordered = True
        order.ordered_date = timezone.now()
        order.payment_status = 'Paid'
        order.save()
        return redirect('order_confirmation')
    except Order.DoesNotExist:
        messages.warning(request, "No active order found.")
        return redirect('orderlist')

def order_confirmation(request):
    order = Order.objects.filter(user=request.user, ordered=True).last()
    
    # Get the user's checkout address
    try:
        checkout_address = CheckoutAddress.objects.get(user=request.user)
    except CheckoutAddress.DoesNotExist:
        checkout_address = None

    return render(request, 'core/order_confirmation.html', {
        'order': order,
        'checkout_address': checkout_address
    })


def invoice_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    items = order.items.all()
    return render(request, 'invoice_detail.html', {
        'order': order,
        'items': items
    })