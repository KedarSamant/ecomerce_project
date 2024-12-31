"""
URL configuration for ecomerce_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .import views as v

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('',v.home),
    path('signup',v.sign_up,name='sign'),
    path('login',v.login_view,name='login'),
    path('logout',v.logout_view,name='logout'),
    path('plist',v.product_list,name='product'),
    path('<int:id>',v.cato_wise_pro,name='cato'),
    path('addtocart/<int:pid>',v.add_to_cart,name='add'),
    path('clist',v.cart_list,name='clist'),
    path('p_search',v.product_search,name='p_search'),
    path('delete2/<int:cart_id>', v.delete_cart_item, name='delete1'),
    path('create_order/', v.create_order, name='create_order'),
    path('payment_success/', v.payment_success, name='payment_success'),
    path('place',v.place_data),
    path('product/<int:id>', v.product_detail, name='product_detail'),
    path('your-orders/', v.user_orders, name='user_orders'),
   
]
