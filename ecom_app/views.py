from django.shortcuts import render,redirect
from django.core.paginator import Paginator
from .models import Category,Product,Cart,UserRegister,Order
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
import razorpay
from django.conf import settings
from django.http import HttpResponseRedirect
# from django.views.decorators.csrf import csrf_exempt
# Create your views here.
#render: This function is used to generate an HTML response from a given template and context.
from django.contrib import messages

def home(request):
    pl=Product.objects.all()
    duplicate_cate=set()
    for i in pl:
        duplicate_cate.add(i.category)
    #paginator code
    paginator=Paginator(pl,4)#it displays 4 products on sigle page
    page=request.GET.get('page') #here request.GET is a dictonary eg page=1, ,'page' is a key and we store its value in page variable
    pl=paginator.get_page(page)#it will fetches the product of respected page number from paginator
    context={'pl':pl,'duplicate_cate':duplicate_cate,'messages': messages.get_messages(request)}
    return render(request, 'home.html',context)
    #return render(request, 'home.html', {'messages': messages.get_messages(request)})


# getting product

# def product_list(request):
#     pl=Product.objects.all()
#     context={'pl':pl}

#     return render(request,'plist.html',context)

# remove duplicate data in category
def product_list(request):
    # uid=request.session.get('uid')
    pl=Product.objects.all()
    #This line retrieves all products from the database and stores them in the all_products variable.
    duplicate_cate=set()
    for i in pl:
        duplicate_cate.add(i.category)
    context={'pl':pl,'duplicate_cate':duplicate_cate}

    return render(request,'plist.html',context)

def cato_wise_pro(request,id):
    # retrive all product
    pl=Product.objects.all()
    # collect unique categories
    #This line retrieves all products from the database and stores them in the all_products variable.
    duplicate_cate=set()
    #create a set of unique categories from all the products. Using a set automatically handles duplicates, ensuring that each category is only listed once.
    for i in pl:
        duplicate_cate.add(i.category)
        # Filter product by category
        #This line filters the Product queryset to only include products that belong to the category identified by the (id) parameter. The filtered results are stored in pl.
        pl=Product.objects.filter(category=id)
    context={'duplicate_cate':duplicate_cate,'pl':pl}
    return render(request,'plist.html',context)


from django.contrib.auth.decorators import login_required

@login_required(login_url='/signup') #befor the add)to_cart runs django checks that user is logged in or authenticated

def add_to_cart(request,pid):
    product_id=Product.objects.get(id=pid)
    # user_id=request.session.get('uid')
    user=request.user
    # user=User.objects.get(id=user_id)
    # Check if the product is already in the user's cart
    #Check/Create Cart Item: This line attempts to fetch an existing Cart entry for the specified product and user.
    # The get_or_create method does two things:
    #It tries to get an existing Cart object with the given product and user.
    #If it finds one, it assigns it to cart_item and sets created to False.
    #If it doesn't find one, it creates a new Cart object with those parameters and sets created to True.
    cart_item, created = Cart.objects.get_or_create(product=product_id, user=user)
    # Cart.objects.get_or_create:
    # Searches for an existing cart entry (Cart) for the specified product and user.
    # If found, assigns it to cart_item and sets created = False.
    # If not found, creates a new Cart entry and sets created = True.
    if not created:
        # If the cart item already existed, increase the quantity
        cart_item.quantity += 1
        cart_item.save()
    else:
        # If it was newly created, set the initial quantity
        cart_item.quantity = 1
        cart_item.save()
    # Redirect to the referring page (the current page the user was on)
    referer = request.META.get('HTTP_REFERER')  # Get the previous page URL
    if referer:
        return HttpResponseRedirect(referer)  # Redirect back to the referring page

    return redirect('/plist')


@login_required(login_url='/signup')
def cart_list(request):
    user=request.user
    # user_id = request.session.get('uid')
    # cart_items = Cart.objects.filter(user_id=user_id)
    cart_items = Cart.objects.filter(user=user)
    print(cart_items)
    
    if request.method == 'POST':
        for item in cart_items:
            new_quantity = request.POST.get(f'quantity-{item.product.id}')
            
            if new_quantity:
                item.quantity = int(new_quantity)
                item.save()
        return redirect('/clist')  # Redirect to refresh the cart after updating

    cart_with_subtotals = [
        {
            'item': item,
            'subtotal': round(item.product.price * item.quantity, 2)  # Ensure subtotal is rounded to two decimal places
        } for item in cart_items
    ]
    
    total_price = sum(item['subtotal'] for item in cart_with_subtotals)
    
    context = {
        'cl': cart_with_subtotals,
        'total_price': round(total_price, 2)  # Ensure total price is rounded to two decimal places
    }
    return render(request, 'clist.html', context)



def product_search(request):
    srch = request.POST.get('srch')
    if srch:
        # Filter products by name or description containing the search term
        pl = Product.objects.filter(name__icontains=srch) | Product.objects.filter(description__icontains=srch)
    else:
        pl = Product.objects.none()  # Return an empty queryset if no search term is provided

    context = {'pl': pl}
    return render(request, 'plist.html', context)



from django.shortcuts import get_object_or_404

def delete_cart_item(request, cart_id):
    user = request.user  # Get the currently logged-in user
    # Attempt to get the cart item for the user
    cart_item = get_object_or_404(Cart, id=cart_id, user=user)  # This will raise a 404 if not found
    cart_item.delete()  # Delete the cart item
    return redirect('/clist')  # Redirect back to the cart list after deletion





def sign_up(request):
    if request.method=='POST':
        f=UserRegister(request.POST)#this is html code with value attribite which stores the value entered by user
        if f.is_valid():#this is_valid function return true or false
            f.save()
            return redirect('/')
        else:
            return render(request, 'signup.html', {'form': f})  # Pass form with errors
    else:
        f=UserRegister()#this object is creating only empty form without value atribute
        print(f)
        context={ 'form':f }
        return render(request,'signup.html',context)



from django.contrib import messages  # Import messages

def login_view(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        passw = request.POST.get('password')
        user = authenticate(request, username=uname, password=passw)# this function returns username
        
        if user is not None:
            login(request, user)#this function creates a session and stores id of logged in user
            messages.success(request, 'Login successful!')  
            return redirect('/') 
        else:
            messages.error(request, 'Invalid username or password.')  
            return render(request, 'login.html')
    
    return render(request, 'login.html')








def logout_view(request):
    logout(request)#this function will distroy the session ie it will deletes the data from the session
    return redirect('/')


import razorpay
from django.conf import settings
from django.shortcuts import render, redirect
from .models import Cart,Order

import razorpay
from django.conf import settings
from django.http import JsonResponse




def payment_success(request):
    user = request.user
    # Clear the cart (if needed)
    Cart.objects.filter(user=user).delete()
    messages.success(request, "Your payment was successful! Your order has been placed.")
    return redirect('payment_success.html')  # Redirect to 'Your Orders' page

import logging

def create_order(request):
    if request.method == 'POST':
        logging.info(f"Received data: {request.body.decode('utf-8')}")  # Log incoming data
        user_id = request.user.id
        cart_items = Cart.objects.filter(user_id=user_id)

        total_amount = sum(item.product.price * item.quantity for item in cart_items)

        if total_amount <= 0:
            return JsonResponse({'error': 'Total amount must be greater than 0.'}, status=400)

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        try:
            razorpay_order = client.order.create({
                'amount': total_amount * 100,
                'currency': 'INR',
                'payment_capture': '1'
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

        order = Order(total_price=total_amount, order_id=razorpay_order['id'], user_id=user_id)
        order.save()
        order.cart_items.set(cart_items)
        cart_items.delete()
        
        request.session['razorpay_order_id'] = razorpay_order['id']
        return JsonResponse(razorpay_order)

    return JsonResponse({'error': 'Invalid request'}, status=400)






def place_data(request):
    user=request.user
    cart_items = Cart.objects.filter(user=user)
    if not cart_items.exists():
        messages.error(request, "Your cart is empty! Add products to proceed with the order.")
        return redirect('/clist')
    return render(request,'checkout.html')
   

from django.shortcuts import render
from .models import Product

def product_detail(request, id):
    
    product=Product.objects.get(id=id)
    context = {
        'product': product
    }
    return render(request, 'product_detail.html', context)

@login_required(login_url='/login')  # Ensure the user is logged in to view their orders
def user_orders(request):
    user = request.user  # Get the logged-in user
    orders = Order.objects.filter(user=user).order_by('-created_at')  # Get all orders of the user sorted by date
    context = {
        'orders': orders
    }
    order=Order.objects.first()
    p=order.cart_items.all()
    for cart in p:
        print(cart.product.name)
    else:
        print('nothing is there')
    return render(request, 'user_orders.html', context)





