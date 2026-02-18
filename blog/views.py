import random
from django.http import HttpResponse
from .forms import *
from .models import *
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from .utils import render_to_pdf 
from django.db.models import Avg
from django.http import JsonResponse
from django.utils import timezone  
from datetime import timedelta
from django.urls import reverse


from .forms import CustomRegisterForm
from .models import * 





def home(request):
    mobile_row = Product.objects.filter(category__name__icontains="Mobiles", available=True).order_by('-id')[:10]
    furniture_row = Product.objects.filter(category__name='Home Furniture', available=True).order_by('-id')[:10]
    tv_row = Product.objects.filter(category__name__icontains="Television", available=True).order_by('-id')[:10]
    grocery_row = Product.objects.filter(category__name__icontains="Grocery", available=True).order_by('-id')[:10]
    fashion_row = FashionItem.objects.filter(available=True).order_by('-created')[:10]

    context = {
        'mobile_row': mobile_row,
        'furniture_row': furniture_row,
        'tv_row': tv_row,
        'grocery_row': grocery_row,
        'fashion_row': fashion_row,
    }
    return render(request, 'category.html', context)




def load_more_products(request):
    all_titles = [
        "Season Specials", "Best Sellers", "Top Rated", "Trending Now", 
        "Budget Buys", "New Arrivals", "Editors Pick", "Limited Offer",
        "Flash Sale", "Weekend Deals", "Members Only", "Clearance"
    ]
    
    
    selected_titles = random.sample(all_titles, 3)

    response_data = []

    for title in selected_titles:
        items = []
        is_fashion = random.choice([True, False])

        if is_fashion:
            all_ids = list(FashionItem.objects.filter(available=True).values_list('id', flat=True))
            if all_ids:
                random_ids = random.sample(all_ids, min(len(all_ids), 4))
                products = FashionItem.objects.filter(id__in=random_ids)
                for p in products:
                    items.append({
                        'name': p.name,
                        'price': p.base_price,
                        'image': p.image.url if p.image else "",
                        'url': reverse('fashion_detail', args=[p.id])
                    })
        else:
            all_ids = list(Product.objects.filter(available=True).values_list('id', flat=True))
            if all_ids:
                random_ids = random.sample(all_ids, min(len(all_ids), 4))
                products = Product.objects.filter(id__in=random_ids)
                for p in products:
                    items.append({
                        'name': p.name,
                        'price': p.price,
                        'image': p.image.url if p.image else "",
                        'url': reverse('product_detail', args=[p.id])
                    })
        
        if items:
            response_data.append({'title': title, 'products': items})

    return JsonResponse({'sections': response_data})



def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    return render(request, 'category_products.html', {'category': category, 'products': products})

def search_products(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        sort_by = request.GET.get('sort')
        
        if query:
            products = Product.objects.filter(
                Q(name__icontains=query) | 
                Q(description__icontains=query) |
                Q(category__name__icontains=query)
            )

            fashion_items = FashionItem.objects.filter(
                Q(name__icontains=query) |
                Q(brand__icontains=query) |
                Q(description__icontains=query)
            )

            if sort_by == 'l2h':
                products = products.order_by('price')
                fashion_items = fashion_items.order_by('base_price')
            elif sort_by == 'h2l':
                products = products.order_by('-price')
                fashion_items = fashion_items.order_by('-base_price')

            context = {
                'products': products, 
                'fashion_items': fashion_items,
                'query': query, 
                'sort_by': sort_by
            }
            return render(request, 'search_results.html', context)
            
    return redirect('home')

def search_suggestions(request):
    query = request.GET.get('term', '')
    results = []

    if len(query) > 1: 
        
        products = Product.objects.filter(name__icontains=query)[:5]
        for p in products:
            results.append({
                'label': p.name, 
                'image': p.image.url if p.image else '',
                'url': reverse('product_detail', args=[p.id]) 
            })

        
        fashions = FashionItem.objects.filter(name__icontains=query)[:5]
        for f in fashions:
            results.append({
                'label': f.name,
                'image': f.image.url if f.image else '',
                'url': reverse('fashion_detail', args=[f.id])
            })

    return JsonResponse(results, safe=False)





def fashion(request):
    
    all_fashion = FashionItem.objects.filter(available=True) 
    
    
    fashion_row_1 = all_fashion[0:10]   
    fashion_row_2 = all_fashion[10:20]  
    fashion_row_3 = all_fashion[20:30]  

    context = {
        'fashion_row_1': fashion_row_1,
        'fashion_row_2': fashion_row_2,
        'fashion_row_3': fashion_row_3,
    }
    return render(request, 'fashion_list.html', context)

def fashion_detail(request, product_id):
    product = get_object_or_404(FashionItem, id=product_id)
    related_products = FashionItem.objects.filter(category=product.category).exclude(id=product_id)[:5]
    reviews = ReviewRating.objects.filter(fashion_item_id=product.id, status=True)

    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    if avg_rating is None:
        avg_rating = 0
    else:
        avg_rating = round(avg_rating, 1)

    review_count = reviews.count()

    rating_counts = {
        '5': reviews.filter(rating=5).count(),
        '4': reviews.filter(rating__gte=4, rating__lt=5).count(),
        '3': reviews.filter(rating__gte=3, rating__lt=4).count(),
        '2': reviews.filter(rating__gte=2, rating__lt=3).count(),
        '1': reviews.filter(rating__gte=1, rating__lt=2).count(),
    }

    context = {
        'product': product,
        'related_products': related_products,
        'reviews': reviews,
        'submit_url': 'submit_fashion_review', 
        'avg_rating': avg_rating,
        'review_count': review_count,
        'rating_counts': rating_counts,
    }
    return render(request, 'fashion_detail.html', context)

def electronics_catalog(request):
    category = get_object_or_404(Category, name="Electronics")
    products = Product.objects.filter(category=category)
    return render(request, 'electronics_list.html', {'category': category, 'products': products})

def furniture_catalog(request):
    furniture_data = Product.objects.filter(category__name='Home Furniture')
    return render(request, 'furniture_list.html', {'items': furniture_data})

def tv_appliances_catalog(request):
    items = Product.objects.filter(category__name__icontains="Television")
    return render(request, 'tv_appliances_list.html', {'items': items})

def grocery_catalog(request):
    items = Product.objects.filter(category__name__icontains="Grocery")
    return render(request, 'grocery_list.html', {'items': items})

def product_detail(request, product_id):
    reviews = None
    submit_url = 'submit_review'

    try:
        product = Product.objects.get(id=product_id)
        related_products = Product.objects.filter(category=product.category).exclude(id=product_id)[:5]
        reviews = ReviewRating.objects.filter(product_id=product.id, status=True)
        submit_url = 'submit_review'

    except Product.DoesNotExist:
        product = get_object_or_404(FashionItem, id=product_id)
        related_products = FashionItem.objects.filter(category=product.category).exclude(id=product_id)[:5]
        reviews = ReviewRating.objects.filter(fashion_item_id=product.id, status=True)
        submit_url = 'submit_fashion_review'

    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    if avg_rating is None:
        avg_rating = 0
    else:
        avg_rating = round(avg_rating, 1)

    review_count = reviews.count()

    rating_counts = {
        '5': reviews.filter(rating=5).count(),
        '4': reviews.filter(rating__gte=4, rating__lt=5).count(),
        '3': reviews.filter(rating__gte=3, rating__lt=4).count(),
        '2': reviews.filter(rating__gte=2, rating__lt=3).count(),
        '1': reviews.filter(rating__gte=1, rating__lt=2).count(),
    }

    context = {
        'product': product,
        'related_products': related_products,
        'reviews': reviews,
        'submit_url': submit_url,
        'avg_rating': avg_rating,
        'review_count': review_count,
        'rating_counts': rating_counts,
    }
    return render(request, 'product_detail.html', context)


def submit_fashion_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            
            reviews = ReviewRating.objects.get(user__id=request.user.id, fashion_item__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you! Your review has been updated.')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                
                data.fashion_item_id = product_id 
                data.user_id = request.user.id
                
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted.')
                return redirect(url)







@login_required(login_url='login')
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
        messages.info(request, "Item quantity updated!")
    else:
        messages.success(request, "Item added to cart successfully!")
    return redirect('view_cart')

@login_required(login_url='login')
def add_fashion_to_cart(request, item_id):
    fashion_item = get_object_or_404(FashionItem, id=item_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, fashion_item=fashion_item)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
        messages.info(request, "Quantity updated!")
    else:
        messages.success(request, "Fashion item added to cart!")
    return redirect('view_cart')


@login_required(login_url='login') 
def add_to_cart_ajax(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        item_type = request.GET.get('type')
        
        cart_count = 0
        
        if item_type == 'normal':
            product = get_object_or_404(Product, id=prod_id)
            item, created = Cart.objects.get_or_create(user=request.user, product=product)
            if not created:
                item.quantity += 1
                item.save()
        
        elif item_type == 'fashion':
            fashion_item = get_object_or_404(FashionItem, id=prod_id)
            item, created = Cart.objects.get_or_create(user=request.user, fashion_item=fashion_item)
            if not created:
                item.quantity += 1
                item.save()

        
        cart_count = Cart.objects.filter(user=request.user).count()
        
        return JsonResponse({'status': 'Added', 'cart_count': cart_count})


@login_required(login_url='login')
def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.total_cost for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})

def plus_cart(request, cart_id):
    item = get_object_or_404(Cart, id=cart_id)
    item.quantity += 1
    item.save()
    return redirect(request.META.get('HTTP_REFERER', 'view_cart'))

def minus_cart(request, cart_id):
    item = get_object_or_404(Cart, id=cart_id)
    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    return redirect(request.META.get('HTTP_REFERER', 'view_cart'))

def remove_cart(request, cart_id):
    item = get_object_or_404(Cart, id=cart_id)
    item.delete()
    if 'checkout' in request.META.get('HTTP_REFERER', ''):
         return redirect('home')
    return redirect('view_cart')





@login_required(login_url='login')
def cart_checkout_summary(request):
    cart_items = Cart.objects.filter(user=request.user)
    if not cart_items:
        return redirect('home')
    total_price = sum(item.total_cost for item in cart_items)
    return render(request, 'order_summary.html', {'cart_items': cart_items, 'total_price': total_price, 'type': 'cart'})

@login_required(login_url='login')
def checkout_summary(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    return render(request, 'order_summary.html', {'item': cart_item, 'total_price': cart_item.total_cost, 'type': 'normal'})

@login_required(login_url='login')
def fashion_checkout_summary(request, product_id):
    product = get_object_or_404(FashionItem, id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, fashion_item=product)
    return render(request, 'order_summary.html', {'item': cart_item, 'total_price': cart_item.total_cost, 'type': 'fashion'})

from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages


@login_required(login_url='login')
def payment_page(request, item_type, item_id):
    discount = 0
    item = None
    actual_price = 0
    
    if item_type == 'cart':
        cart_items = Cart.objects.filter(user=request.user)
        if not cart_items.exists():
            return redirect('home')
        actual_price = sum(item.total_cost for item in cart_items)
    
    elif item_type == 'buy_now':
        product = get_object_or_404(Product, id=item_id)
        cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
        actual_price = cart_item.total_cost
        item = cart_item
        
    elif item_type == 'fashion':
        fashion_item = get_object_or_404(FashionItem, id=item_id)
        cart_item, created = Cart.objects.get_or_create(user=request.user, fashion_item=fashion_item)
        actual_price = cart_item.total_cost
        item = cart_item

    else:
        return redirect('home')

    final_price = actual_price - discount
    if request.method == 'POST':
        address = "No Address Provided"
        if hasattr(request.user, 'profile'):
            address = request.user.profile.address
        new_order = Order.objects.create(
            user=request.user,
            total_price=final_price,
            address=address,
            status='Order Placed',
            is_paid=True,
            payment_method='Card'
        )

        if item_type == 'cart':
            cart_items = Cart.objects.filter(user=request.user)
            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=new_order,
                    product=cart_item.product,
                    fashion_item=cart_item.fashion_item,
                    quantity=cart_item.quantity,
                    price=cart_item.total_cost
                )
            cart_items.delete()

        elif item:
            OrderItem.objects.create(
                order=new_order,
                product=item.product,
                fashion_item=item.fashion_item,
                quantity=item.quantity,
                price=item.total_cost
            )
            item.delete()

        subject = f"Order Confirmed! - Order #{new_order.id}"
        message = f"Hi {request.user.username},\n\nThank you for shopping with ShopKart! 🎉\n\nYour Order #{new_order.id} has been placed successfully.\nTotal Amount Paid: ₹{final_price}\n\nWe will update you once it is shipped.\n\nBest Regards,\nTeam ShopKart"
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [request.user.email, ]
        
        
        try:
            send_mail(subject, message, email_from, recipient_list)
            print("✅ Email sent successfully!") 
        except Exception as e:
            print(f"❌ Email Error: {e}") 
        messages.success(request, f"Order Placed Successfully! Confirmation email sent to {request.user.email}")
        return redirect('my_orders')

    context = {
        'total_price': actual_price,
        'discount': discount,
        'final_price': final_price,
        'item': item,
        'item_type': item_type,  
        'item_id': item_id
    }

    return render(request, 'payment.html', context)





def generate_otp():
    return random.randint(100000, 999999)

def send_otp_email(email, otp):
    send_mail(
        'Your Verification OTP for ShopKart',
        f'Your One-Time Password (OTP) is: {otp}',
        settings.EMAIL_HOST_USER,
        [email]
    )

def register_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            request.session['register_data'] = form.cleaned_data
            otp = generate_otp()
            send_otp_email(form.cleaned_data['email'], otp)
            
            request.session['otp'] = otp
            request.session['otp_email'] = form.cleaned_data['email']
            request.session['verification_type'] = 'register'
            
            messages.info(request, "OTP sent to your email!")
            return redirect('verify_otp')
    else:
        form = CustomRegisterForm()
    return render(request, 'register.html', {'form': form})

def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        user_input = request.POST.get('username') 
        password = request.POST.get('password')
        
        user = authenticate(request, username=user_input, password=password)
        if user is None:
            try:
                user_obj = User.objects.get(email=user_input)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                pass

        if user is not None:
            otp = generate_otp()
            send_otp_email(user.email, otp)
            
            request.session['otp'] = otp
            request.session['login_user_id'] = user.id
            request.session['verification_type'] = 'login'
            
            messages.info(request, "OTP sent to your email!")
            return redirect('verify_otp')
        else:
            messages.error(request, "Invalid Username/Email or Password.")
    return render(request, 'login.html')

def forgot_password_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if User.objects.filter(email=email).exists():
            otp = generate_otp()
            send_otp_email(email, otp)
            
            request.session['otp'] = otp
            request.session['otp_email'] = email
            request.session['verification_type'] = 'reset'
            
            messages.success(request, "OTP sent to your email.")
            return redirect('verify_otp')
        else:
            messages.error(request, "This email is not registered with us.")
    return render(request, 'forgot_password.html')

def verify_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        saved_otp = request.session.get('otp')
        verification_type = request.session.get('verification_type')
        
        if str(saved_otp) == str(entered_otp):
            if verification_type == 'register':
                data = request.session.get('register_data')
                user = User.objects.create_user(username=data['username'], email=data['email'], password=data['password1'])
                login(request, user)
                del request.session['otp'], request.session['register_data']
                messages.success(request, "Registration Successful!")

            elif verification_type == 'login':
                user = User.objects.get(id=request.session.get('login_user_id'))
                login(request, user)
                del request.session['otp'], request.session['login_user_id']
                messages.success(request, "Logged in Successfully!")

            elif verification_type == 'reset':
                del request.session['otp']
                return redirect('reset_password')

            return redirect('home')
        else:
            messages.error(request, "Invalid OTP! Please try again.")
    return render(request, 'otp_verify.html')

def reset_password_page(request):
    email = request.session.get('otp_email')
    if not email: return redirect('login')

    if request.method == 'POST':
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        
        if pass1 != pass2:
            messages.error(request, "Passwords do not match!")
            return redirect('reset_password')

        user = User.objects.get(email=email)
        if user.check_password(pass1):
            messages.error(request, "You used your Old Password! Please enter a New Password.")
            return redirect('reset_password')

        user.set_password(pass1)
        user.save()
        
        if 'otp_email' in request.session: del request.session['otp_email']
        if 'verification_type' in request.session: del request.session['verification_type']
        
        messages.success(request, "Password changed successfully! Please Login.")
        return redirect('login')
    return render(request, 'reset_password.html')

def resend_otp(request):
    verification_type = request.session.get('verification_type')
    email = None

    if verification_type == 'register':
        email = request.session.get('otp_email')
    elif verification_type == 'login':
        user_id = request.session.get('login_user_id')
        if user_id: email = User.objects.get(id=user_id).email
    elif verification_type == 'reset':
        email = request.session.get('otp_email')

    if email:
        otp = generate_otp()
        send_otp_email(email, otp)
        request.session['otp'] = otp
        messages.success(request, "New OTP has been sent to your email!")
    else:
        messages.error(request, "Something went wrong, please try again.")
        return redirect('login')
        
    return redirect('verify_otp')

def logout_user(request):
    logout(request)
    return redirect('login')





def flight_home(request):
    return render(request, 'flight_home.html')

def flight_search(request):
    if request.method == 'GET':
        flights = Flight.objects.filter(
            source__icontains=request.GET.get('from', ''), 
            destination__icontains=request.GET.get('to', '')
        )
        return render(request, 'flight_results.html', {'flights': flights})
    return redirect('flight_home')


@login_required(login_url='login')
def profile_page(request):
    
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, instance=profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile') 

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'profile.html', context)


@login_required(login_url='login')
def place_order(request):
    cart_items = Cart.objects.filter(user=request.user)
    
    if not cart_items:
        return redirect('home')

    total_price = sum(item.total_cost for item in cart_items)
    
    
    address = "No Address Provided" 
    if hasattr(request.user, 'profile'):
        address = request.user.profile.address

    
    new_order = Order.objects.create(
        user=request.user,
        total_price=total_price,
        address=address
    )

    
    for item in cart_items:
        OrderItem.objects.create(
            order=new_order,
            product=item.product,          
            fashion_item=item.fashion_item, 
            quantity=item.quantity,
            price=item.total_cost
        )

    
    cart_items.delete()
    
    messages.success(request, "Order Placed Successfully!")
    return redirect('my_orders')



@login_required(login_url='login')
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    current_time = timezone.now()

    for order in orders:
        if order.status != 'Cancelled' and order.status != 'Delivered':
            
            time_diff = current_time - order.created_at

            if time_diff > timedelta(days=3):
                order.status = 'Delivered'
                order.save()
            
            elif time_diff > timedelta(days=2):
                order.status = 'Out for Delivery'
                order.save()

            elif time_diff > timedelta(days=1):
                order.status = 'Shipped'
                order.save()

    context = {
        'orders': orders
    }
    return render(request, 'orders.html', context)



@login_required(login_url='login')
def download_invoice(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    context = {
        'order': order,
        'items': order.items.all(),
        'customer': request.user
    }
    
    
    pdf = render_to_pdf('invoice.html', context)
    
    if pdf:
        
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = f"Invoice_{order.id}.pdf"
        content = f"inline; filename={filename}"
        response['Content-Disposition'] = content
        return response
        
    return HttpResponse("Not Found")


def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER') 
    if request.method == 'POST':
        try:
            
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you! Your review has been updated.')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted.')
                return redirect(url)
            
@login_required(login_url='login')
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if order.status == 'Shipped' or order.status == 'Delivered' or order.status == 'Cancelled':
        messages.error(request, "You cannot cancel this order now.")
    else:
        order.status = 'Cancelled'
        order.save()
        messages.success(request, "Order cancelled successfully!")

    return redirect('my_orders')



@login_required(login_url='login')
def wishlist_page(request):
    
    wishlist_items = Wishlist.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})

@login_required(login_url='login')
def add_to_wishlist(request, item_type, item_id):
    if item_type == 'normal':
        product = get_object_or_404(Product, id=item_id)
        
        Wishlist.objects.get_or_create(user=request.user, product=product)
        messages.success(request, f"{product.name} added to Wishlist ❤️")
        
    elif item_type == 'fashion':
        fashion = get_object_or_404(FashionItem, id=item_id)
        Wishlist.objects.get_or_create(user=request.user, fashion_item=fashion)
        messages.success(request, f"{fashion.name} added to Wishlist ❤️")
        
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required(login_url='login')
def remove_wishlist(request, wishlist_id):
    item = get_object_or_404(Wishlist, id=wishlist_id)
    item.delete()
    messages.warning(request, "Item removed from Wishlist 💔")
    return redirect('wishlist_page')


def chatbot_response(request):
    user_message = request.GET.get('msg', '').lower()
    response_text = "I'm sorry, I didn't understand that. You can ask about 'Order Status', 'Return Policy', or 'Payment'."

    
    if 'hi' in user_message or 'hello' in user_message:
        response_text = "Hello! Welcome to Flipkart Clone Support. How can I help you today?"

    
    elif 'order' in user_message or 'status' in user_message:
        if request.user.is_authenticated:
            
            last_order = Order.objects.filter(user=request.user).last()
            if last_order:
                response_text = f"Your last order (ID: #{last_order.id}) is currently: **{last_order.status}**."
            else:
                response_text = "You haven't placed any orders yet."
        else:
            response_text = "Please login to check your order status."

    
    elif 'return' in user_message or 'refund' in user_message:
        response_text = "We have a 7-day return policy. If the product is damaged, you can request a full refund."

    
    elif 'pay' in user_message:
        response_text = "We accept Credit/Debit Cards, UPI, and Cash on Delivery (COD)."

    
    elif 'thank' in user_message:
        response_text = "You're welcome! Happy Shopping! 🛍️"

    return JsonResponse({'response': response_text})