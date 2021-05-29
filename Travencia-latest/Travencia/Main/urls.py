from django.urls import path
from .views import (home, about, ItemDetailView, OrderSummaryView,
                    add_to_cart,
                    remove_from_cart,
                    remove_single_item_from_cart,
                    PaymentView,
                    AddCouponView,
                    RequestRefundView,
                    remove_single_customer_from_cart,
                    add_guest_to_cart,BookList,BookDetail, email,csv_upload_file,                
                    form_email,
                    HomeView, BookList2,
                   ContactView,  index, Mission,ThankYou,PaymentSuccess,
                    FAQ,
                    pay)
app_name = 'Main'

urlpatterns =[
    path('', home, name='home'), 
    path('book/', BookList2.as_view(), name='book'),
    #path('book2/', BookList2.as_view(), name='book2'),
    path('about/', about, name='about'), 
    path('Contact/', ContactView, name='Contact'), 
    #path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('Booking-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('add-coupon/', AddCouponView.as_view(), name='add-coupon'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart,
         name='remove-single-item-from-cart'),
    path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),
    path('request-refund/', RequestRefundView.as_view(), name='request-refund'),
    path('NewsLetter/', index, name='NewsLetter'),
    path('Mission/', Mission, name='Mission'),
    path('Terms&Conditions/', FAQ, name='Terms&Conditions'),
    path('add_guest_to_cart/<slug>/', add_guest_to_cart, name='add-guest-to-cart'),
    path('remove_single_customer_from_cart/<slug>/', remove_single_customer_from_cart,
         name='remove-single-customer-from-cart'),
    #path('ThankYou', ThankYou.as_view(), name='ThankYou') 
    path('ThankYou', ThankYou, name='ThankYou'),
    path('BookList/', BookList.as_view(), name='BookList'),   
    path('BookDetail/<slug>/', BookDetail, name='BookDetail'),   
    path('Payment_success/', PaymentSuccess.as_view(), name='PaymentSuccess'),   
    path('email/',email, name='email'),   
    path('email2/',form_email, name='email2'),   


    path('pay/',pay, name='pay'), 
    path('csv/',csv_upload_file, name='csv'), 
    


    

    
]