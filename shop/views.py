from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Order, OrderItem
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# ================= HOME =================
def home(request):

    query = request.GET.get('q')
    category = request.GET.get('category')

    products = Product.objects.all()

    if query:
        products = products.filter(name__icontains=query)

    if category:
        products = products.filter(category=category)

    cart_count = 0

    if request.user.is_authenticated:

        order, created = Order.objects.get_or_create(
            customer=request.user,
            complete=False
        )

        cart_count = order.orderitem_set.count()

    return render(request, 'shop/home.html', {
        'products': products,
        'cart_count': cart_count
    })


# ================= REGISTER =================
def register(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:

            User.objects.create_user(
                username=username,
                password=password
            )

            messages.success(request, "Registration Successful")

            return redirect('login')

    return render(request, 'shop/register.html')


# ================= LOGIN =================
def user_login(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:

            user = authenticate(
                request,
                username=username,
                password=password
            )

            if user:

                login(request, user)

                messages.success(request, "Login Successful")

                return redirect(request.GET.get('next', 'home'))

    return render(request, 'shop/login.html')


# ================= LOGOUT =================
def user_logout(request):

    logout(request)

    messages.success(request, "Logged Out Successfully")

    return redirect('home')


# ================= PRODUCT DETAILS =================
def product_detail(request, product_id):

    product = get_object_or_404(Product, id=product_id)

    return render(request, 'shop/product_detail.html', {
        'product': product
    })


# ================= ADD TO CART =================
@login_required
def add_to_cart(request, product_id):

    product = get_object_or_404(Product, id=product_id)

    order, created = Order.objects.get_or_create(
        customer=request.user,
        complete=False
    )

    order_item, created = OrderItem.objects.get_or_create(
        order=order,
        product=product
    )

    if not created:
        order_item.quantity += 1

    order_item.save()

    messages.success(request, "Product Added To Cart")

    return redirect('cart')


# ================= REMOVE FROM CART =================
@login_required
def remove_from_cart(request, item_id):

    item = get_object_or_404(OrderItem, id=item_id)

    item.delete()

    messages.success(request, "Product Removed From Cart")

    return redirect('cart')


# ================= BUY NOW =================
@login_required
def buy_now(request, product_id):

    product = get_object_or_404(Product, id=product_id)

    order, created = Order.objects.get_or_create(
        customer=request.user,
        complete=False
    )

    order_item, created = OrderItem.objects.get_or_create(
        order=order,
        product=product
    )

    if not created:
        order_item.quantity += 1

    order_item.save()

    return redirect('checkout')


# ================= CART =================
@login_required
def cart(request):

    order, created = Order.objects.get_or_create(
        customer=request.user,
        complete=False
    )

    items = order.orderitem_set.all()

    total = sum([
        item.product.price * item.quantity
        for item in items
    ])

    return render(request, 'shop/cart.html', {
        'items': items,
        'total': total
    })


# ================= UPDATE QUANTITY =================
@login_required
def update_quantity(request, item_id, action):

    item = get_object_or_404(OrderItem, id=item_id)

    if action == 'increase':
        item.quantity += 1

    elif action == 'decrease':
        item.quantity -= 1

    if item.quantity <= 0:
        item.delete()

    else:
        item.save()

    return redirect('cart')


# ================= CHECKOUT =================
@login_required
def checkout(request):

    order, created = Order.objects.get_or_create(
        customer=request.user,
        complete=False
    )

    items = order.orderitem_set.all()

    total = sum([
        item.product.price * item.quantity
        for item in items
    ])

    if request.method == 'POST':

        order.complete = True
        order.save()

        messages.success(request, "Order Placed Successfully")

        return redirect('checkout_success')

    return render(request, 'shop/checkout.html', {
        'items': items,
        'total': total
    })


# ================= CHECKOUT SUCCESS =================
@login_required
def checkout_success(request):

    return render(request, 'shop/checkout_success.html')


# ================= ORDER HISTORY =================
@login_required
def order_history(request):

    orders = Order.objects.filter(
        customer=request.user,
        complete=True
    )

    total_spent = sum([
        order.get_total()
        for order in orders
    ])

    return render(request, 'shop/order_history.html', {
        'orders': orders,
        'total_spent': total_spent
    })


# ================= ABOUT PAGE =================
def about(request):

    return render(request, 'shop/about.html')


# ================= CONTACT PAGE =================
def contact(request):

    return render(request, 'shop/contact.html')