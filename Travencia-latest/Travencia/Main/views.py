import datetime

import stripe

#from .pdf_test import render_to_pdf

from django.conf import settings

from django.contrib import messages

from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth.decorators import login_required

from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import render, get_object_or_404

from django.views.generic import ListView, DetailView, View

from django.shortcuts import redirect

from django.utils import timezone

from django.db.models import Q

from .forms import CheckoutForm,payform, CouponForm, RefundForm, PaymentForm,  EmailSignupForm, HomeContatct, AddressTow, ContactHome,Csv_form

from .models import Item, OrderItem, Order, Details, Payment, Coupon, Refund, UserProfile,  Signupmodel, HomeContatcModel, Csv

from django.views.generic.edit import FormView

import random

import string

import requests 

import json

from django.utils import timezone

from django.utils import timezone    

from datetime import date 

import pandas as pd

date_time_var = date.day

import csv

from django.core.mail import EmailMultiAlternatives

from django.utils.crypto import get_random_string

from django.core.mail import send_mail, EmailMessage

from django.template.loader import render_to_string

from django.http import HttpResponseRedirect, Http404

from .filters import ItemFilter

stripe.api_key = settings.STRIPE_SECRET_KEY


from django.core.mail import send_mail

from post_office import mail

from lazysignup.decorators import allow_lazy_user


MAILCHIMP_API_KEY = settings.MAILCHIMP_API_KEY

MAILCHIMP_DATA_CENTER = settings.MAILCHIMP_DATA_CENTER

MAILCHIMP_EMAIL_LIST_ID = settings.MAILCHIMP_EMAIL_LIST_ID


api_url = 'https://{dc}.api.mailchimp.com/3.0'.format(dc=MAILCHIMP_DATA_CENTER)

members_endpoint = '{api_url}/lists/{list_id}/members'.format(

    api_url=api_url,

    list_id=MAILCHIMP_EMAIL_LIST_ID

)


def subscribe(email):

    data = {

        "email_address": email,

        "status": "subscribed"

    }

    r = requests.post(

        members_endpoint,

        auth=("", MAILCHIMP_API_KEY),

        data=json.dumps(data)

    )

    return r.status_code, r.json()



def index(request):


    return render(request, 'Main/join.html')





#@login_required
def jls_extract_def():
    
    return 


def csv_upload_file(request):

    form = Csv_form(request.POST or None, request.FILES or None)

    if form.is_valid():
        

        form.save()

        obj = Csv.objects.get(activated=False)
        prom_cons_place = ""

        with open(obj.file_name.path, 'r') as f:

            reader = csv.reader(f)

            for i, row in enumerate(reader):

                if i ==0:

                    pass

                else:



                    try:

           

                        obj_re = Item.objects.get(title=row[0], convention=row[1],  address=row[3],)

                        if obj_re:

                            print(obj_re.title, 'Mohammed')


                            obj_re.price=float(row[2])
                            obj_re.start_date=row[4]
                            obj_re.end_date=row[5]
                            obj_re.convention_address=row[6]
                            obj_re.promo_code=row[7]

                            obj_re.image= obj_re.image
                            print(obj_re.image.url)

                            obj_re.save()     

                        

                    except ObjectDoesNotExist:


                        new_item = Item(title=row[0], convention=row[1], price=float(row[2]), address=row[3], start_date=row[4], end_date=row[5], promo_code=row[7], convention_address=row[6] )   

                        new_item.save()  
                   

        obj.activated = True

        obj.save()

        messages.info(request, "Done!")

        form = Csv_form()


    context = {

        'form':form,

    }
  
      

    return render(request, "Main/csv.html", context)



def create_ref_code():

    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))



def products(request):
  

    context = {

        'items': Item.objects.all(),
    

    }

    return render(request, "products.html", context)



def is_valid_form(values):

    valid = True

    for field in values:

        if field == '':

            valid = False

    return valid




def randGen():

    return ''.join(random.choices(string.ascii_lowercase + string.digits , k=10)).upper() 



order_num= randGen().upper()










class PaymentView(View):

    def get(self, *args, **kwargs):

        order = Order.objects.get(user=self.request.user, ordered=False)

        if order.billing_address:

            context = {

                'order': order,

                'DISPLAY_COUPON_FORM': False

            }

            userprofile = self.request.user.userprofile

            if userprofile.one_click_purchasing:

                # fetch the users card list

                cards = stripe.Customer.list_sources(

                    userprofile.stripe_customer_id,

                    limit=3,

                    object='card'

                )

                card_list = cards['data']

                if len(card_list) > 0:

                    # update the context with the default card

                    context.update({

                        'card': card_list[0]

                    })

            return render(self.request, "Main/payment.html", context)

        else:

            messages.warning(

                self.request, "You have not added a billing address")

            return redirect("Main:checkout")


    def post(self, *args, **kwargs):

        order = Order.objects.get(user=self.request.user, ordered=False)

        form = PaymentForm(self.request.POST)

        userprofile = UserProfile.objects.get(user=self.request.user)

        if form.is_valid():

            token = form.cleaned_data.get('stripeToken')

            save = form.cleaned_data.get('save')

            use_default = form.cleaned_data.get('use_default')


            if save:

                if userprofile.stripe_customer_id != '' and userprofile.stripe_customer_id is not None:

                    customer = stripe.Customer.retrieve(

                        userprofile.stripe_customer_id)

                    customer.sources.create(source=token)


                else:

                    customer = stripe.Customer.create(

                        email=self.request.user.email,

                    )

                    customer.sources.create(source=token)

                    userprofile.stripe_customer_id = customer['id']

                    userprofile.one_click_purchasing = True

                    userprofile.save()


            amount = int(order.get_total() * 100)


            try:


                if use_default or save:

                    # charge the customer because we cannot charge the token more than once

                    charge = stripe.Charge.create(

                        amount=amount,  # cents

                        currency="usd",

                        customer=userprofile.stripe_customer_id

                    )

                else:

                    # charge once off on the token

                    charge = stripe.Charge.create(

                        amount=amount,  # cents

                        currency="usd",

                        source=token

                    )


                # create the payment

                payment = Payment()

                payment.stripe_charge_id = charge['id']

                payment.user = self.request.user

                payment.amount = order.get_total()

                payment.save()


                # assign the payment to the order


                order_items = order.items.all()

                order_items.update(ordered=True)

                for item in order_items:

                    item.save()


                order.ordered = True

                order.payment = payment

                order.ref_code = create_ref_code()

                order.save()


                messages.success(self.request, "Your order was successful!")

                return redirect("/")


            except stripe.error.CardError as e:

                body = e.json_body

                err = body.get('error', {})

                messages.warning(self.request, f"{err.get('message')}")

                return redirect("/")


            except stripe.error.RateLimitError as e:

                # Too many requests made to the API too quickly

                messages.warning(self.request, "Rate limit error")

                return redirect("/")


            except stripe.error.InvalidRequestError as e:

                # Invalid parameters were supplied to Stripe's API

                print(e)

                messages.warning(self.request, "Invalid parameters")

                return redirect("/")


            except stripe.error.AuthenticationError as e:

                # Authentication with Stripe's API failed

                # (maybe you changed API keys recently)

                messages.warning(self.request, "Not authenticated")

                return redirect("/")


            except stripe.error.APIConnectionError as e:

                # Network communication with Stripe failed

                messages.warning(self.request, "Network error")

                return redirect("/")


            except stripe.error.StripeError as e:

                # Display a very generic error to the user, and maybe send

                # yourself an email

                messages.warning(

                    self.request, "Something went wrong. You were not charged. Please try again.")

                return redirect("/")


            except Exception as e:

                # send an email to ourselves

                messages.warning(

                    self.request, "A serious error occurred. We have been notifed.")

                return redirect("/")


        messages.warning(self.request, "Invalid data received")

        return redirect("/payment/stripe/")



class HomeView(ListView):


    model = Item

    paginate_by = 10

    template_name = "Main/Book.html"
   

    def get_queryset(self):

        query = self.request.GET.get('q')

        if query:

            object_list = Item.objects.filter(

            Q(title__icontains=query)|

            Q(description__icontains=query)|

            Q(price__icontains=query)|

            Q(convention__icontains=query)|

            Q(discount_price__icontains=query)


        )

            return object_list                 

        else:

            object_list = Item.objects.all()

        return object_list



class OrderSummaryView(LoginRequiredMixin, View):

    def get(self, *args, **kwargs):



        try:

            order = Order.objects.get(user=self.request.user, ordered=False)

            context = {

                'object': order,
               

            }

            return render(self.request, 'Main/order_summary.html', context)

        except ObjectDoesNotExist:

            messages.warning(self.request, "You do not have an active order")

            return redirect("/")








def get_coupon(request, code):

    try:

        coupon = Coupon.objects.get(code=code)

        return coupon

    except ObjectDoesNotExist:

        messages.info(request, "This coupon does not exist")

        return redirect("Main:checkout")



class AddCouponView(View):

    def post(self, *args, **kwargs):

        form = CouponForm(self.request.POST or None)

        if form.is_valid():

            try:

                code = form.cleaned_data.get('code')

                order = Order.objects.get(

                    user=self.request.user, ordered=False)

                order.coupon = get_coupon(self.request, code)

                order.save()

                messages.success(self.request, "Successfully added coupon")

                return redirect("Main:checkout")

            except ObjectDoesNotExist:

                messages.info(self.request, "You do not have an active order")

                return redirect("Main:checkout")



class RequestRefundView(View):

    def get(self, *args, **kwargs):

        form = RefundForm()

        context = {

            'form': form

        }

        return render(self.request, "request_refund.html", context)


    def post(self, *args, **kwargs):

        form = RefundForm(self.request.POST)

        if form.is_valid():

            ref_code = form.cleaned_data.get('ref_code')

            message = form.cleaned_data.get('message')

            email = form.cleaned_data.get('email')

            # edit the order

            try:

                order = Order.objects.get(ref_code=ref_code)

                order.refund_requested = True

                order.save()


                # store the refund

                refund = Refund()
                refund.order = order
                refund.reason = message
                refund.email = email

                refund.save()


                messages.info(self.request, "Your request was received.")

                return redirect("Main:request-refund")


            except ObjectDoesNotExist:

                messages.info(self.request, "This order does not exist.")

                return redirect("Main:request-refund")



def home(request):

    form = HomeContatct(request.POST or None)

    if form.is_valid():

        name = form.cleaned_data.get('name')

        email = form.cleaned_data.get('email')

        message = form.cleaned_data.get('message')
        

        Mat = HomeContatcModel(

            name = name,

            email=email,
            message=message

            )
  

        Mat.save()
        


    form = HomeContatct()


    form2 = EmailSignupForm(request.POST or None)

    if request.method == "POST":

        if form2.is_valid():

            email_signup_qs = Signupmodel.objects.filter(email=form2.instance.email)

            if email_signup_qs.exists():

                messages.info(request, "You are already subscribed")

            else:

                subscribe(form2.instance.email)

                form2.save()

            form2 = EmailSignupForm()



       


    return render(request, 'Main/Home.html', context={'form':form,'form2':form2})


def about(request):

    return render(request, 'Main/about.html', context={})




 



class ItemDetailView(DetailView):
    

    model = Item

    template_name = "Main/product.html"




    def get_context_data(self, **kwargs):

        context = super(ItemDetailView, self).get_context_data(**kwargs)

        context['form'] = CheckoutForm

        return context


''' 

    def get_context_data(self, **kwargs):

        context = super(ItemDetailView, self).get_context_data(**kwargs)

        context['form'] = self.get_form()

        return context


    def post(self, request, *args, **kwargs):

        return FormView.post(self, request, *args, **kwargs)

'''



def ContactView(request):

    form = ContactHome(request.POST or None)

    if form.is_valid():

        form.save()

    form = ContactHome()

    context ={

        'form':form

    }    


    return render(request,'Main/Contact.html', context)



def Mission(request):

    return render(request, 'Main/Mission.html')    

def FAQ(request):

    return render(request, 'Main/FAQ.html')    






@allow_lazy_user

def add_to_cart(request, slug):

    item = get_object_or_404(Item, slug=slug)

    order_item, created = OrderItem.objects.get_or_create(

        item=item,

        user=request.user,

        ordered=False

    )

    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():

        order = order_qs[0]

        # check if the order item is in the order

        if order.items.filter(item__slug=item.slug).exists():

            order_item.quantity += 1

            order_item.save()

            messages.info(request, "This item quantity was updated.")

            return redirect("Main:order-summary")

        else:

            order.items.add(order_item)

            messages.info(request, "This item was added to your cart.")

            return redirect("Main:order-summary")

    else:

        ordered_date = timezone.now()

        order = Order.objects.create(

            user=request.user, ordered_date=ordered_date)

        order.items.add(order_item)

        messages.info(request, "This item was added to your cart.")

        return redirect("Main:order-summary")



@allow_lazy_user

def remove_from_cart(request, slug):

    item = get_object_or_404(Item, slug=slug)

    order_qs = Order.objects.filter(

        user=request.user,

        ordered=False

    )

    if order_qs.exists():

        order = order_qs[0]

        # check if the order item is in the order

        if order.items.filter(item__slug=item.slug).exists():

            order_item = OrderItem.objects.filter(

                item=item,

                user=request.user,

                ordered=False

            )[0]

            order.items.remove(order_item)

            messages.info(request, "This item was removed from your cart.")

            return redirect("Main:order-summary")

        else:

            messages.info(request, "This item was not in your cart")

            return redirect("Main:product", slug=slug)

    else:

        messages.info(request, "You do not have an active order")

        return redirect("Main:product", slug=slug)


@allow_lazy_user

def remove_single_item_from_cart(request, slug):

    item = get_object_or_404(Item, slug=slug)

    order_qs = Order.objects.filter(

        user=request.user,

        ordered=False

    )

    if order_qs.exists():

        order = order_qs[0]

        # check if the order item is in the order

        if order.items.filter(item__slug=item.slug).exists():

            order_item = OrderItem.objects.filter(

                item=item,

                user=request.user,

                ordered=False

            )[0]

            if order_item.quantity > 1:

                order_item.quantity -= 1

                order_item.save()

            else:

                order.items.remove(order_item)

            messages.info(request, "This item quantity was updated.")

            return redirect("Main:order-summary")

        else:

            messages.info(request, "This item was not in your cart")

            return redirect("Main:product", slug=slug)

    else:

        messages.info(request, "You do not have an active order")

        return redirect("Main:product", slug=slug)





@allow_lazy_user

def remove_single_customer_from_cart(request, slug):

    item = get_object_or_404(Item, slug=slug)

    order_qs = Order.objects.filter(

        user=request.user,

        ordered=False

    )

    if order_qs.exists():

        order = order_qs[0]

        # check if the order item is in the order

        if order.items.filter(item__slug=item.slug).exists():

            order_item = OrderItem.objects.filter(

                item=item,

                user=request.user,

                ordered=False

            )[0]

            if order_item.guest > 1:

                order_item.guest -= 1

                order_item.save()

            else:

                order.items.remove(order_item)

            messages.info(request, "This item quantity was updated.")

            return redirect("Main:order-summary")

        else:

            messages.info(request, "This item was not in your cart")

            return redirect("Main:product", slug=slug)

    else:

        messages.info(request, "You do not have an active order")

        return redirect("Main:product", slug=slug)




@allow_lazy_user

def add_guest_to_cart(request, slug):

    item = get_object_or_404(Item, slug=slug)

    order_item, created = OrderItem.objects.get_or_create(

        item=item,

        user=request.user,

        ordered=False

    )

    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():

        order = order_qs[0]

        # check if the order item is in the order

        if order.items.filter(item__slug=item.slug).exists():

            order_item.guest += 1

            order_item.save()

            messages.info(request, "This item quantity was updated.")

            return redirect("Main:order-summary")

        else:

            order.items.add(order_item)

            messages.info(request, "This item was added to your cart.")

            return redirect("Main:order-summary")

    else:

        ordered_date = timezone.now()

        order = Order.objects.create(

            user=request.user, ordered_date=ordered_date)

        order.items.add(order_item)

        messages.info(request, "This item was added to your cart.")

        return redirect("Main:order-summary")








'''

def BookList(request):

    ItmeList = Item.objects.all().order_by("-id")

   


    context = {

        'ItmeList':ItmeList,
       

    }

    return render(request, "Main/homelist.html", context)

'''

'''

def BookList(request):

    ItmeList = Item.objects.all().order_by("-id")


            


    context = {

        'ItmeList':ItmeList,
   
       

    }

    return render(request, "Main/homelist.html", context)

'''




class BookList2(ListView):


    model = Item

    paginate_by = 10

    template_name = "Main/homelist.html"
    


 



    def get_context_data(self, **kwargs):          

        context = super().get_context_data(**kwargs)                     

        stuff = Item.objects.all().first()

        context["stuff"] = stuff

        #messages.add_message(self.request, messages.INFO, f'{self.request.user.username} You have access to this page')

        return context
   

    def get_queryset(self):

        query = self.request.GET.get('q')

        if query:

            object_list = Item.objects.filter(

            Q(title__iexact=query)|

            Q(description__iexact=query)|

            Q(price__iexact=query)|

            Q(convention__iexact=query)|

            Q(discount_price__iexact=query)


        )

            return object_list                 

        else:

            object_list = Item.objects.all()

        return object_list

       























class BookList(ListView):


    model = Item

    paginate_by = 10

    template_name = "Main/homelist_2.html"
    


 



    def get_context_data(self, **kwargs):          

        context = super().get_context_data(**kwargs)                     

        stuff = Item.objects.all().first()

        context["stuff"] = stuff

        #messages.add_message(self.request, messages.INFO, f'{self.request.user.username} You have access to this page')

        return context
   

    def get_queryset(self):

        query = self.request.GET.get('q')

        if query:

            object_list = Item.objects.filter(

            Q(title__iexact=query)|

            Q(description__iexact=query)|

            Q(price__iexact=query)|

            Q(convention__iexact=query)|

            Q(discount_price__iexact=query)


        )

            return object_list                 

        else:

            object_list = Item.objects.all()

        return object_list

       




@allow_lazy_user

def BookDetail(request, slug):

    try:


        ItmeDetail = Item.objects.get(slug=slug)

        Hotel_name = ItmeDetail.title

        Hotel_price = ItmeDetail.price * 1.20

    except ObjectDoesNotExist:

        raise Http404("This Offer is not avaiable now our dear customer! contact us if you have any concerns.")
       

    order_qs = Order.objects.filter(user=request.user, ordered=False)

    form = CheckoutForm(request.POST or None)

    if form.is_valid():

        First_Name                    =     form.cleaned_data.get('First_Name')

        Last_Name                     =     form.cleaned_data.get('Last_Name')

        EMail                         =     form.cleaned_data.get('EMail')

        Company_Name                  =     form.cleaned_data.get('Company_Name')

        zip                           =     form.cleaned_data.get('zip')

        Phone_Number                  =     form.cleaned_data.get('Phone_Number')
      

        Number_OF_Guests              =     form.cleaned_data.get('Number_OF_Guests')


        #11111 

        Room_1                        =     form.cleaned_data.get('Room_1')

        first_name_of_guest_NO_1_R1   =     form.cleaned_data.get('first_name_of_guest_NO_1_R1')

        last_name_of_guest_NO_1_R1    =     form.cleaned_data.get('last_name_of_guest_NO_1_R1')

        first_name_of_guest_NO_2_R1   =     form.cleaned_data.get('first_name_of_guest_NO_2_R1')

        last_name_of_guest_NO_2_R1    =     form.cleaned_data.get('last_name_of_guest_NO_2_R1')

        guest_NO_1_check_in_R1        =     form.cleaned_data.get('guest_NO_1_check_in_R1')

        guest_NO_1_check_out_R1       =     form.cleaned_data.get('guest_NO_1_check_out_R1')

        guest_NO_2_check_in_R1        =     form.cleaned_data.get('guest_NO_2_check_in_R1')

        guest_NO_2_check_out_R1       =     form.cleaned_data.get('guest_NO_2_check_out_R1')

        #22222



        Room_2                        =     form.cleaned_data.get('Room_2')

        first_name_of_guest_NO_1_R2   =     form.cleaned_data.get('first_name_of_guest_NO_1_R2')

        last_name_of_guest_NO_1_R2    =     form.cleaned_data.get('last_name_of_guest_NO_1_R2')

        first_name_of_guest_NO_2_R2   =     form.cleaned_data.get('first_name_of_guest_NO_2_R2')

        last_name_of_guest_NO_2_R2    =     form.cleaned_data.get('last_name_of_guest_NO_2_R2')

        guest_NO_1_check_in_R2        =     form.cleaned_data.get('guest_NO_1_check_in_R2')

        guest_NO_1_check_out_R2       =     form.cleaned_data.get('guest_NO_1_check_out_R2')

        guest_NO_2_check_in_R2        =     form.cleaned_data.get('guest_NO_2_check_in_R2')

        guest_NO_2_check_out_R2       =     form.cleaned_data.get('guest_NO_2_check_out_R2')




        #333333



        Room_3                        =     form.cleaned_data.get('Room_3')

        first_name_of_guest_NO_1_R3   =     form.cleaned_data.get('first_name_of_guest_NO_1_R3')

        last_name_of_guest_NO_1_R3    =     form.cleaned_data.get('last_name_of_guest_NO_1_R3')

        first_name_of_guest_NO_2_R3   =     form.cleaned_data.get('first_name_of_guest_NO_2_R3')

        last_name_of_guest_NO_2_R3    =     form.cleaned_data.get('last_name_of_guest_NO_2_R3')

        guest_NO_1_check_in_R3        =     form.cleaned_data.get('guest_NO_1_check_in_R3')

        guest_NO_1_check_out_R3       =     form.cleaned_data.get('guest_NO_1_check_out_R3')

        guest_NO_2_check_in_R3        =     form.cleaned_data.get('guest_NO_2_check_in_R3')

        guest_NO_2_check_out_R3       =     form.cleaned_data.get('guest_NO_2_check_out_R3')



        #44444





        Room_4                        = form.cleaned_data.get('Room_4')

        first_name_of_guest_NO_1_R4   = form.cleaned_data.get('first_name_of_guest_NO_1_R4')

        last_name_of_guest_NO_1_R4    = form.cleaned_data.get('last_name_of_guest_NO_1_R4')

        guest_NO_1_check_in_R4        = form.cleaned_data.get('guest_NO_1_check_in_R4')

        guest_NO_1_check_out_R4       = form.cleaned_data.get('guest_NO_1_check_out_R4')

        first_name_of_guest_NO_2_R4   = form.cleaned_data.get('first_name_of_guest_NO_2_R4')

        last_name_of_guest_NO_2_R4    = form.cleaned_data.get('last_name_of_guest_NO_2_R4')

        guest_NO_2_check_in_R4        = form.cleaned_data.get('guest_NO_2_check_in_R4')

        guest_NO_2_check_out_R4       = form.cleaned_data.get('guest_NO_2_check_out_R4')






        #55555555




        Room_5                         =    form.cleaned_data.get('Room_5')

        first_name_of_guest_NO_1_R5    =    form.cleaned_data.get('first_name_of_guest_NO_1_R5')

        last_name_of_guest_NO_1_R5     =    form.cleaned_data.get('last_name_of_guest_NO_1_R5')

        guest_NO_1_check_in_R5         =    form.cleaned_data.get('guest_NO_1_check_in_R5')

        guest_NO_1_check_out_R5        =    form.cleaned_data.get('guest_NO_1_check_out_R5')

        first_name_of_guest_NO_2_R5    =    form.cleaned_data.get('first_name_of_guest_NO_2_R5')

        last_name_of_guest_NO_2_R5     =    form.cleaned_data.get('last_name_of_guest_NO_2_R5')

        guest_NO_2_check_in_R5         =    form.cleaned_data.get('guest_NO_2_check_in_R5')

        guest_NO_2_check_out_R5        =    form.cleaned_data.get('guest_NO_2_check_out_R5')



        #666666666



        Room_6                         =    form.cleaned_data.get('Room_6')

        first_name_of_guest_NO_1_R6    =    form.cleaned_data.get('first_name_of_guest_NO_1_R6')

        last_name_of_guest_NO_1_R6     =    form.cleaned_data.get('last_name_of_guest_NO_1_R6')

        guest_NO_1_check_in_R6         =    form.cleaned_data.get('guest_NO_1_check_in_R6')

        guest_NO_1_check_out_R6        =    form.cleaned_data.get('guest_NO_1_check_out_R6')

        first_name_of_guest_NO_2_R6    =    form.cleaned_data.get('first_name_of_guest_NO_2_R6')

        last_name_of_guest_NO_2_R6     =    form.cleaned_data.get('last_name_of_guest_NO_2_R6')

        guest_NO_2_check_in_R6         =    form.cleaned_data.get('guest_NO_2_check_in_R6')

        guest_NO_2_check_out_R6        =    form.cleaned_data.get('guest_NO_2_check_out_R6')





        #777777777



        Room_7                         =    form.cleaned_data.get('Room_7')

        first_name_of_guest_NO_1_R7    =    form.cleaned_data.get('first_name_of_guest_NO_1_R7')

        last_name_of_guest_NO_1_R7     =    form.cleaned_data.get('last_name_of_guest_NO_1_R7')

        guest_NO_1_check_in_R7         =    form.cleaned_data.get('guest_NO_1_check_in_R7')

        guest_NO_1_check_out_R7        =    form.cleaned_data.get('guest_NO_1_check_out_R7')

        first_name_of_guest_NO_2_R7    =    form.cleaned_data.get('first_name_of_guest_NO_2_R7')

        last_name_of_guest_NO_2_R7     =    form.cleaned_data.get('last_name_of_guest_NO_2_R7')

        guest_NO_2_check_in_R7         =    form.cleaned_data.get('guest_NO_2_check_in_R7')

        guest_NO_2_check_out_R7        =    form.cleaned_data.get('guest_NO_2_check_out_R7')




        #888888888



        Room_8                         =    form.cleaned_data.get('Room_8')

        first_name_of_guest_NO_1_R8    =    form.cleaned_data.get('first_name_of_guest_NO_1_R8')

        last_name_of_guest_NO_1_R8     =    form.cleaned_data.get('last_name_of_guest_NO_1_R8')

        guest_NO_1_check_in_R8         =    form.cleaned_data.get('guest_NO_1_check_in_R8')

        guest_NO_1_check_out_R8        =    form.cleaned_data.get('guest_NO_1_check_out_R8')

        first_name_of_guest_NO_2_R8    =    form.cleaned_data.get('first_name_of_guest_NO_2_R8')

        last_name_of_guest_NO_2_R8     =    form.cleaned_data.get('last_name_of_guest_NO_2_R8')

        guest_NO_2_check_in_R8         =    form.cleaned_data.get('guest_NO_2_check_in_R8')

        guest_NO_2_check_out_R8        =    form.cleaned_data.get('guest_NO_2_check_out_R8')





        #9999999999999



        Room_9                         =    form.cleaned_data.get('Room_9')

        first_name_of_guest_NO_1_R9    =    form.cleaned_data.get('first_name_of_guest_NO_1_R9')

        last_name_of_guest_NO_1_R9     =    form.cleaned_data.get('last_name_of_guest_NO_1_R9')

        guest_NO_1_check_in_R9         =    form.cleaned_data.get('guest_NO_1_check_in_R9')

        guest_NO_1_check_out_R9        =    form.cleaned_data.get('guest_NO_1_check_out_R9')

        first_name_of_guest_NO_2_R9    =    form.cleaned_data.get('first_name_of_guest_NO_2_R9')

        last_name_of_guest_NO_2_R9     =    form.cleaned_data.get('last_name_of_guest_NO_2_R9')

        guest_NO_2_check_in_R9         =    form.cleaned_data.get('guest_NO_2_check_in_R9')

        guest_NO_2_check_out_R9        =    form.cleaned_data.get('guest_NO_2_check_out_R9')








        #1010101010101010101






        Room_10                         =    form.cleaned_data.get('Room_10')

        first_name_of_guest_NO_1_R10    =    form.cleaned_data.get('first_name_of_guest_NO_1_R10')

        last_name_of_guest_NO_1_R10     =    form.cleaned_data.get('last_name_of_guest_NO_1_R10')

        guest_NO_1_check_in_R10         =    form.cleaned_data.get('guest_NO_1_check_in_R10')

        guest_NO_1_check_out_R10        =    form.cleaned_data.get('guest_NO_1_check_out_R10')

        first_name_of_guest_NO_2_R10    =    form.cleaned_data.get('first_name_of_guest_NO_2_R10')

        last_name_of_guest_NO_2_R10     =    form.cleaned_data.get('last_name_of_guest_NO_2_R10')

        guest_NO_2_check_in_R10         =    form.cleaned_data.get('guest_NO_2_check_in_R10')

        guest_NO_2_check_out_R10        =    form.cleaned_data.get('guest_NO_2_check_out_R10')






        #1111111111111111111111





        Room_11                         =    form.cleaned_data.get('Room_11')

        first_name_of_guest_NO_1_R11    =    form.cleaned_data.get('first_name_of_guest_NO_1_R11')

        last_name_of_guest_NO_1_R11     =    form.cleaned_data.get('last_name_of_guest_NO_1_R11')

        guest_NO_1_check_in_R11         =    form.cleaned_data.get('guest_NO_1_check_in_R11')

        guest_NO_1_check_out_R11        =    form.cleaned_data.get('guest_NO_1_check_out_R11')

        first_name_of_guest_NO_2_R11    =    form.cleaned_data.get('first_name_of_guest_NO_2_R11')

        last_name_of_guest_NO_2_R11     =    form.cleaned_data.get('last_name_of_guest_NO_2_R11')

        guest_NO_2_check_in_R11         =    form.cleaned_data.get('guest_NO_2_check_in_R11')

        guest_NO_2_check_out_R11        =    form.cleaned_data.get('guest_NO_2_check_out_R11')



        #1212121212222121212





        Room_12                         =    form.cleaned_data.get('Room_12')

        first_name_of_guest_NO_1_R12    =    form.cleaned_data.get('first_name_of_guest_NO_1_R12')

        last_name_of_guest_NO_1_R12     =    form.cleaned_data.get('last_name_of_guest_NO_1_R12')

        guest_NO_1_check_in_R12         =    form.cleaned_data.get('guest_NO_1_check_in_R12')

        guest_NO_1_check_out_R12        =    form.cleaned_data.get('guest_NO_1_check_out_R12')

        first_name_of_guest_NO_2_R12    =    form.cleaned_data.get('first_name_of_guest_NO_2_R12')

        last_name_of_guest_NO_2_R12     =    form.cleaned_data.get('last_name_of_guest_NO_2_R12')

        guest_NO_2_check_in_R12         =    form.cleaned_data.get('guest_NO_2_check_in_R12')

        guest_NO_2_check_out_R12        =    form.cleaned_data.get('guest_NO_2_check_out_R12')





        #131313131313313131313313




        Room_13                         =    form.cleaned_data.get('Room_13')

        first_name_of_guest_NO_1_R13    =    form.cleaned_data.get('first_name_of_guest_NO_1_R13')

        last_name_of_guest_NO_1_R13     =    form.cleaned_data.get('last_name_of_guest_NO_1_R13')

        guest_NO_1_check_in_R13         =    form.cleaned_data.get('guest_NO_1_check_in_R13')

        guest_NO_1_check_out_R13        =    form.cleaned_data.get('guest_NO_1_check_out_R13')

        first_name_of_guest_NO_2_R13    =    form.cleaned_data.get('first_name_of_guest_NO_2_R13')

        last_name_of_guest_NO_2_R13     =    form.cleaned_data.get('last_name_of_guest_NO_2_R13')

        guest_NO_2_check_in_R13         =    form.cleaned_data.get('guest_NO_2_check_in_R13')

        guest_NO_2_check_out_R13        =    form.cleaned_data.get('guest_NO_2_check_out_R13')




        #14141414141414141414141







        Room_14                         =    form.cleaned_data.get('Room_14')

        first_name_of_guest_NO_1_R14    =    form.cleaned_data.get('first_name_of_guest_NO_1_R14')

        last_name_of_guest_NO_1_R14     =    form.cleaned_data.get('last_name_of_guest_NO_1_R14')

        guest_NO_1_check_in_R14         =    form.cleaned_data.get('guest_NO_1_check_in_R14')

        guest_NO_1_check_out_R14        =    form.cleaned_data.get('guest_NO_1_check_out_R14')

        first_name_of_guest_NO_2_R14    =    form.cleaned_data.get('first_name_of_guest_NO_2_R14')

        last_name_of_guest_NO_2_R14     =    form.cleaned_data.get('last_name_of_guest_NO_2_R14')

        guest_NO_2_check_in_R14         =    form.cleaned_data.get('guest_NO_2_check_in_R14')

        guest_NO_2_check_out_R14        =    form.cleaned_data.get('guest_NO_2_check_out_R14')





        #1515151515151515155





        Room_15                         =    form.cleaned_data.get('Room_15')

        first_name_of_guest_NO_1_R15    =    form.cleaned_data.get('first_name_of_guest_NO_1_R15')

        last_name_of_guest_NO_1_R15     =    form.cleaned_data.get('last_name_of_guest_NO_1_R15')

        guest_NO_1_check_in_R15         =    form.cleaned_data.get('guest_NO_1_check_in_R15')

        guest_NO_1_check_out_R15        =    form.cleaned_data.get('guest_NO_1_check_out_R15')

        first_name_of_guest_NO_2_R15    =    form.cleaned_data.get('first_name_of_guest_NO_2_R15')

        last_name_of_guest_NO_2_R15     =    form.cleaned_data.get('last_name_of_guest_NO_2_R15')

        guest_NO_2_check_in_R15         =    form.cleaned_data.get('guest_NO_2_check_in_R15')

        guest_NO_2_check_out_R15        =    form.cleaned_data.get('guest_NO_2_check_out_R15')








    
      



        total          = 0

        Detail_Deposit = 0

        Detail_Rest    = 0

        Detail_Tax     = 0


        # Room 1

        if guest_NO_1_check_in_R1 is not None:

            Gu1 =guest_NO_1_check_out_R1  -  guest_NO_1_check_in_R1

            Gu1Diff = Gu1.days


            total+=  Gu1Diff


        # Room 2

        if guest_NO_1_check_in_R2 is not None:

            Gu2 =guest_NO_1_check_out_R2  -  guest_NO_1_check_in_R2

            Gu1Diff2 = Gu2.days


            total+=  Gu1Diff2     



        # Room 3

        if guest_NO_1_check_in_R3 is not None:

            Gu3 =guest_NO_1_check_out_R3  -  guest_NO_1_check_in_R3

            Gu1Diff3 = Gu3.days


            total+=  Gu1Diff3 


        #4

        if guest_NO_1_check_in_R4 is not None:

            Gu4 =guest_NO_1_check_out_R4  -  guest_NO_1_check_in_R4

            Gu1Diff4 = Gu4.days


            total+=  Gu1Diff4 

        #5


        if guest_NO_1_check_in_R5 is not None:

            Gu5 =guest_NO_1_check_out_R5  -  guest_NO_1_check_in_R5

            Gu1Diff5 = Gu5.days


            total+=  Gu1Diff5 



        #6


        if guest_NO_1_check_in_R6 is not None:

            Gu6 =guest_NO_1_check_out_R6  -  guest_NO_1_check_in_R6

            Gu1Diff6 = Gu6.days


            total+=  Gu1Diff6 


        #7


        if guest_NO_1_check_in_R7 is not None:

            Gu7 =guest_NO_1_check_out_R7  -  guest_NO_1_check_in_R7

            Gu1Diff7 = Gu7.days


            total+=  Gu1Diff7


        #8


        if guest_NO_1_check_in_R8 is not None:

            Gu8 =guest_NO_1_check_out_R8  -  guest_NO_1_check_in_R8

            Gu1Diff8 = Gu8.days


            total+=  Gu1Diff8 


        #9


        if guest_NO_1_check_in_R9 is not None:

            Gu9 =guest_NO_1_check_out_R9  -  guest_NO_1_check_in_R9

            Gu1Diff9 = Gu9.days


            total+=  Gu1Diff9 


        #10



        if guest_NO_1_check_in_R10 is not None:

            Gu10 =guest_NO_1_check_out_R10  -  guest_NO_1_check_in_R10

            Gu1Diff10 = Gu10.days


            total+=  Gu1Diff10 


        #11


        if guest_NO_1_check_in_R11 is not None:

            Gu11 =guest_NO_1_check_out_R11  -  guest_NO_1_check_in_R11

            Gu1Diff11 = Gu11.days


            total+=  Gu1Diff11  


        #12


        if guest_NO_1_check_in_R12 is not None:

            Gu12 =guest_NO_1_check_out_R12  -  guest_NO_1_check_in_R12

            Gu1Diff12 = Gu12.days


            total+=  Gu1Diff12 


        #13


        if guest_NO_1_check_in_R13 is not None:

            Gu13 =guest_NO_1_check_out_R13  -  guest_NO_1_check_in_R13

            Gu1Diff13 = Gu13.days


            total+=  Gu1Diff13 



        #14



        if guest_NO_1_check_in_R14 is not None:

            Gu14 =guest_NO_1_check_out_R14  -  guest_NO_1_check_in_R14

            Gu1Diff14 = Gu14.days


            total+=  Gu1Diff14 


        #15


        if guest_NO_1_check_in_R15 is not None:

            Gu15 =guest_NO_1_check_out_R15  -  guest_NO_1_check_in_R15

            Gu1Diff15 = Gu15.days


            total+=  Gu1Diff15 


        #16


        if guest_NO_1_check_in_R16 is not None:

            Gu16 =guest_NO_1_check_out_R16  -  guest_NO_1_check_in_R16

            Gu1Diff16 = Gu16.days


            total+=  Gu1Diff16 


        #17 


        if guest_NO_1_check_in_R17 is not None:

            Gu17 =guest_NO_1_check_out_R17  -  guest_NO_1_check_in_R17

            Gu1Diff17 = Gu17.days


            total+=  Gu1Diff17    


        #18


        if guest_NO_1_check_in_R18 is not None:

            Gu18 =guest_NO_1_check_out_R18  -  guest_NO_1_check_in_R18

            Gu1Diff18 = Gu18.days


            total+=  Gu1Diff18 


        #19


        if guest_NO_1_check_in_R19 is not None:

            Gu19 =guest_NO_1_check_out_R19  -  guest_NO_1_check_in_R19

            Gu1Diff19 = Gu19.days


            total+=  Gu1Diff19 



        #20


        if guest_NO_1_check_in_R20 is not None:

            Gu20 =guest_NO_1_check_out_R20  -  guest_NO_1_check_in_R20

            Gu1Diff20 = Gu20.days


            total+=  Gu1Diff20
                    



        # Room 1

        if guest_NO_2_check_in_R1 is not None:

            Gu2_1 =guest_NO_2_check_out_R1  -  guest_NO_2_check_in_R1

            Gu2_1Diff = Gu2_1.days


            total+=  Gu2_1Diff


        # Room 2

        if guest_NO_2_check_in_R2 is not None:

            Gu2_2 =guest_NO_2_check_out_R2  -  guest_NO_2_check_in_R2

            Gu2Diff2 = Gu2_2.days


            total+=  Gu2Diff2     



        # Room 3

        if guest_NO_2_check_in_R3 is not None:

            Gu2_3 =guest_NO_2_check_out_R3  -  guest_NO_2_check_in_R3

            Gu2Diff3 = Gu2_3.days


            total+=  Gu2Diff3 


        #4

        if guest_NO_2_check_in_R4 is not None:

            Gu2_4 =guest_NO_2_check_out_R4  -  guest_NO_2_check_in_R4

            Gu2Diff4 = Gu2_4.days


            total+=  Gu2Diff4 

        #5


        if guest_NO_2_check_in_R5 is not None:

            Gu2_5 =guest_NO_2_check_out_R5  -  guest_NO_2_check_in_R5

            Gu2Diff5 = Gu2_5.days


            total+=  Gu2Diff5 



        #6


        if guest_NO_2_check_in_R6 is not None:

            Gu2_6 =guest_NO_2_check_out_R6  -  guest_NO_2_check_in_R6

            Gu2Diff6 = Gu2_6.days


            total+=  Gu2Diff6 


        #7


        if guest_NO_2_check_in_R7 is not None:

            Gu2_7 =guest_NO_2_check_out_R7  -  guest_NO_2_check_in_R7

            Gu2Diff7 = Gu2_7.days


            total+=  Gu2Diff7


        #8


        if guest_NO_2_check_in_R8 is not None:

            Gu2_8 =guest_NO_2_check_out_R8  -  guest_NO_2_check_in_R8

            Gu2Diff8 = Gu2_8.days


            total+=  Gu2Diff8 


        #9


        if guest_NO_2_check_in_R9 is not None:

            Gu2_9 =guest_NO_2_check_out_R9  -  guest_NO_2_check_in_R9

            Gu2Diff9 = Gu2_9.days


            total+=  Gu2Diff9 


        #10



        if guest_NO_2_check_in_R10 is not None:

            Gu2_10 =guest_NO_2_check_out_R10  -  guest_NO_2_check_in_R10

            Gu2Diff10 = Gu2_10.days


            total+=  Gu2Diff10 


        #11


        if guest_NO_2_check_in_R11 is not None:

            Gu2_11 =guest_NO_2_check_out_R11  -  guest_NO_2_check_in_R11

            Gu2Diff11 = Gu2_11.days


            total+=  Gu2Diff11  


        #12


        if guest_NO_2_check_in_R12 is not None:

            Gu2_12 =guest_NO_2_check_out_R12  -  guest_NO_2_check_in_R12

            Gu2Diff12 = Gu2_12.days


            total+=  Gu2Diff12 


        #13


        if guest_NO_2_check_in_R13 is not None:

            Gu2_13 =guest_NO_2_check_out_R13  -  guest_NO_2_check_in_R13

            Gu2Diff13 = Gu2_13.days


            total+=  Gu2Diff13 



        #14



        if guest_NO_2_check_in_R14 is not None:

            Gu2_14 =guest_NO_2_check_out_R14  -  guest_NO_2_check_in_R14

            Gu2Diff14 = Gu2_14.days


            total+=  Gu2Diff14 


        #15


        if guest_NO_2_check_in_R15 is not None:

            Gu2_15 =guest_NO_2_check_out_R15  -  guest_NO_2_check_in_R15

            Gu2Diff15 = Gu2_15.days


            total+=  Gu2Diff15 


        #16


        if guest_NO_2_check_in_R16 is not None:

            Gu2_16 =guest_NO_2_check_out_R16  -  guest_NO_2_check_in_R16

            Gu2Diff16 = Gu2_16.days


            total+=  Gu2Diff16 


        #17 


        if guest_NO_2_check_in_R17 is not None:

            Gu2_17 =guest_NO_2_check_out_R17  -  guest_NO_2_check_in_R17

            Gu2Diff17 = Gu2_17.days


            total+=  Gu2Diff17    


        #18


        if guest_NO_2_check_in_R18 is not None:

            Gu2_18 =guest_NO_2_check_out_R18  -  guest_NO_2_check_in_R18

            Gu2Diff18 = Gu2_18.days


            total+=  Gu2Diff18 


        #19


        if guest_NO_2_check_in_R19 is not None:

            Gu2_19 =guest_NO_2_check_out_R19  -  guest_NO_2_check_in_R19

            Gu2Diff19 = Gu2_19.days


            total+=  Gu2Diff19 



        #20


        if guest_NO_2_check_in_R20 is not None:

            Gu2_20 =guest_NO_2_check_out_R20  -  guest_NO_2_check_in_R20

            Gu2Diff20 = Gu2_20.days


            total+=  Gu2Diff20
                    


    

                                          


        Detail_instance = Details(

        item                                    = ItmeDetail,

        user                                    = request.user,

        Guests                                  = Number_OF_Guests,  
  

        Nights                                  = total,

        First_Name                              =First_Name,

        Last_Name                               =Last_Name,

        EMail                                   =EMail,

        Company_Name                            =Company_Name,

        zip                                     =zip,
     

        Phone_Number                            =Phone_Number,

        Number_OF_Guests =                      Number_OF_Guests,

        Room_1                                  =Room_1,

        first_name_of_guest_NO_1_R1             =first_name_of_guest_NO_1_R1,

        last_name_of_guest_NO_1_R1              =last_name_of_guest_NO_1_R1,

        first_name_of_guest_NO_2_R1             =first_name_of_guest_NO_2_R1,

        last_name_of_guest_NO_2_R1              =last_name_of_guest_NO_2_R1,

        guest_NO_1_check_in_R1                  =guest_NO_1_check_in_R1,

        guest_NO_1_check_out_R1                 =guest_NO_1_check_out_R1,

        guest_NO_2_check_in_R1                  =guest_NO_2_check_in_R1,

        guest_NO_2_check_out_R1                 =guest_NO_2_check_out_R1,

        ##22222          

        Room_2                                  =Room_2,

        first_name_of_guest_NO_1_R2             =first_name_of_guest_NO_1_R2,

        last_name_of_guest_NO_1_R2              =last_name_of_guest_NO_1_R2,

        first_name_of_guest_NO_2_R2             =first_name_of_guest_NO_2_R2,

        last_name_of_guest_NO_2_R2              =last_name_of_guest_NO_2_R2,

        guest_NO_1_check_in_R2                  =guest_NO_1_check_in_R2,

        guest_NO_1_check_out_R2                 =guest_NO_1_check_out_R2,

        guest_NO_2_check_in_R2                  =guest_NO_2_check_in_R2,

        guest_NO_2_check_out_R2                 =guest_NO_2_check_out_R2,



        Room_3                                  =   Room_3,

        first_name_of_guest_NO_1_R3             =   first_name_of_guest_NO_1_R3,

        last_name_of_guest_NO_1_R3              =   last_name_of_guest_NO_1_R3,

        guest_NO_1_check_in_R3                  =   guest_NO_1_check_in_R3,

        guest_NO_1_check_out_R3                 =   guest_NO_1_check_out_R3,

        first_name_of_guest_NO_2_R3             =   first_name_of_guest_NO_2_R3,

        last_name_of_guest_NO_2_R3              =   last_name_of_guest_NO_2_R3,

        guest_NO_2_check_in_R3                  =   guest_NO_2_check_in_R3,

        guest_NO_2_check_out_R3                 =   guest_NO_2_check_out_R3,



        Room_4                                   =  Room_4,  

        first_name_of_guest_NO_1_R4              =  first_name_of_guest_NO_1_R4,

        last_name_of_guest_NO_1_R4               =  last_name_of_guest_NO_1_R4,

        guest_NO_1_check_in_R4                   =  guest_NO_1_check_in_R4,

        guest_NO_1_check_out_R4                  =  guest_NO_1_check_out_R4,

        first_name_of_guest_NO_2_R4              =  first_name_of_guest_NO_2_R4,

        last_name_of_guest_NO_2_R4               =  last_name_of_guest_NO_2_R4,

        guest_NO_2_check_in_R4                   =  guest_NO_2_check_in_R4,

        guest_NO_2_check_out_R4                  =  guest_NO_2_check_out_R4,


        Room_5                                   =  Room_5,

        first_name_of_guest_NO_1_R5              =  first_name_of_guest_NO_1_R5,

        last_name_of_guest_NO_1_R5               =  last_name_of_guest_NO_1_R5,

        guest_NO_1_check_in_R5                   =  guest_NO_1_check_in_R5,

        guest_NO_1_check_out_R5                  =  guest_NO_1_check_out_R5,

        first_name_of_guest_NO_2_R5              =  first_name_of_guest_NO_2_R5,

        last_name_of_guest_NO_2_R5               =  last_name_of_guest_NO_2_R5,

        guest_NO_2_check_in_R5                   =  guest_NO_2_check_in_R5,

        guest_NO_2_check_out_R5                  =  guest_NO_2_check_out_R5,


        Room_6                                   =  Room_6,

        first_name_of_guest_NO_1_R6              =  first_name_of_guest_NO_1_R6,

        last_name_of_guest_NO_1_R6               =  last_name_of_guest_NO_1_R6,

        guest_NO_1_check_in_R6                   =  guest_NO_1_check_in_R6,

        guest_NO_1_check_out_R6                  =  guest_NO_1_check_out_R6,

        first_name_of_guest_NO_2_R6              =  first_name_of_guest_NO_2_R6,

        last_name_of_guest_NO_2_R6               =  last_name_of_guest_NO_2_R6,

        guest_NO_2_check_in_R6                   =  guest_NO_2_check_in_R6,

        guest_NO_2_check_out_R6                  =  guest_NO_2_check_out_R6,


        Room_7                                   =  Room_7,

        first_name_of_guest_NO_1_R7              =  first_name_of_guest_NO_1_R7,

        last_name_of_guest_NO_1_R7               =  last_name_of_guest_NO_1_R7,

        guest_NO_1_check_in_R7                   =  guest_NO_1_check_in_R7,

        guest_NO_1_check_out_R7                  =  guest_NO_1_check_out_R7,

        first_name_of_guest_NO_2_R7              =  first_name_of_guest_NO_2_R7,

        last_name_of_guest_NO_2_R7               =  last_name_of_guest_NO_2_R7,

        guest_NO_2_check_in_R7                   =  guest_NO_2_check_in_R7,

        guest_NO_2_check_out_R7                  =  guest_NO_2_check_out_R7,


        Room_8                                   =  Room_8,

        first_name_of_guest_NO_1_R8              =  first_name_of_guest_NO_1_R8,

        last_name_of_guest_NO_1_R8               =  last_name_of_guest_NO_1_R8,

        guest_NO_1_check_in_R8                   =  guest_NO_1_check_in_R8,

        guest_NO_1_check_out_R8                  =  guest_NO_1_check_out_R8,

        first_name_of_guest_NO_2_R8              =  first_name_of_guest_NO_2_R8,

        last_name_of_guest_NO_2_R8               =  last_name_of_guest_NO_2_R8,

        guest_NO_2_check_in_R8                   =  guest_NO_2_check_in_R8,

        guest_NO_2_check_out_R8                  =  guest_NO_2_check_out_R8,


        Room_9                                   =  Room_9,

        first_name_of_guest_NO_1_R9              =  first_name_of_guest_NO_1_R9,

        last_name_of_guest_NO_1_R9               =  last_name_of_guest_NO_1_R9,

        guest_NO_1_check_in_R9                   =  guest_NO_1_check_in_R9,

        guest_NO_1_check_out_R9                  =  guest_NO_1_check_out_R9,

        first_name_of_guest_NO_2_R9              =  first_name_of_guest_NO_2_R9,

        last_name_of_guest_NO_2_R9               =  last_name_of_guest_NO_2_R9,

        guest_NO_2_check_in_R9                   =  guest_NO_2_check_in_R9,

        guest_NO_2_check_out_R9                  =  guest_NO_2_check_out_R9,







        Room_10                                   =  Room_10,

        first_name_of_guest_NO_1_R10              =  first_name_of_guest_NO_1_R10,

        last_name_of_guest_NO_1_R10               =  last_name_of_guest_NO_1_R10,

        guest_NO_1_check_in_R10                   =  guest_NO_1_check_in_R10,

        guest_NO_1_check_out_R10                  =  guest_NO_1_check_out_R10,

        first_name_of_guest_NO_2_R10              =  first_name_of_guest_NO_2_R10,

        last_name_of_guest_NO_2_R10               =  last_name_of_guest_NO_2_R10,

        guest_NO_2_check_in_R10                   =  guest_NO_2_check_in_R10,

        guest_NO_2_check_out_R10                  =  guest_NO_2_check_out_R10,




        Room_11                                   =  Room_11,

        first_name_of_guest_NO_1_R11              =  first_name_of_guest_NO_1_R11,

        last_name_of_guest_NO_1_R11               =  last_name_of_guest_NO_1_R11,

        guest_NO_1_check_in_R11                   =  guest_NO_1_check_in_R11,

        guest_NO_1_check_out_R11                  =  guest_NO_1_check_out_R11,

        first_name_of_guest_NO_2_R11              =  first_name_of_guest_NO_2_R11,

        last_name_of_guest_NO_2_R11               =  last_name_of_guest_NO_2_R11,

        guest_NO_2_check_in_R11                   =  guest_NO_2_check_in_R11,

        guest_NO_2_check_out_R11                  =  guest_NO_2_check_out_R11,



        Room_12                                   =  Room_12,

        first_name_of_guest_NO_1_R12              =  first_name_of_guest_NO_1_R12,

        last_name_of_guest_NO_1_R12               =  last_name_of_guest_NO_1_R12,

        guest_NO_1_check_in_R12                   =  guest_NO_1_check_in_R12,

        guest_NO_1_check_out_R12                  =  guest_NO_1_check_out_R12,

        first_name_of_guest_NO_2_R12              =  first_name_of_guest_NO_2_R12,

        last_name_of_guest_NO_2_R12               =  last_name_of_guest_NO_2_R12,

        guest_NO_2_check_in_R12                   =  guest_NO_2_check_in_R12,

        guest_NO_2_check_out_R12                  =  guest_NO_2_check_out_R12,





        Room_13                                   =  Room_13,

        first_name_of_guest_NO_1_R13              =  first_name_of_guest_NO_1_R13,

        last_name_of_guest_NO_1_R13               =  last_name_of_guest_NO_1_R13,

        guest_NO_1_check_in_R13                   =  guest_NO_1_check_in_R13,

        guest_NO_1_check_out_R13                  =  guest_NO_1_check_out_R13,

        first_name_of_guest_NO_2_R13              =  first_name_of_guest_NO_2_R13,

        last_name_of_guest_NO_2_R13               =  last_name_of_guest_NO_2_R13,

        guest_NO_2_check_in_R13                   =  guest_NO_2_check_in_R13,

        guest_NO_2_check_out_R13                  =  guest_NO_2_check_out_R13,




        Room_14                                   =  Room_14,

        first_name_of_guest_NO_1_R14              =  first_name_of_guest_NO_1_R14,

        last_name_of_guest_NO_1_R14               =  last_name_of_guest_NO_1_R14,

        guest_NO_1_check_in_R14                   =  guest_NO_1_check_in_R14,

        guest_NO_1_check_out_R14                  =  guest_NO_1_check_out_R14,

        first_name_of_guest_NO_2_R14              =  first_name_of_guest_NO_2_R14,

        last_name_of_guest_NO_2_R14               =  last_name_of_guest_NO_2_R14,

        guest_NO_2_check_in_R14                   =  guest_NO_2_check_in_R14,

        guest_NO_2_check_out_R14                  =  guest_NO_2_check_out_R14,



        Room_15                                   =  Room_15,

        first_name_of_guest_NO_1_R15              =  first_name_of_guest_NO_1_R15,

        last_name_of_guest_NO_1_R15               =  last_name_of_guest_NO_1_R15,

        guest_NO_1_check_in_R15                   =  guest_NO_1_check_in_R15,

        guest_NO_1_check_out_R15                  =  guest_NO_1_check_out_R15,

        first_name_of_guest_NO_2_R15              =  first_name_of_guest_NO_2_R15,

        last_name_of_guest_NO_2_R15               =  last_name_of_guest_NO_2_R15,

        guest_NO_2_check_in_R15                   =  guest_NO_2_check_in_R15,

        guest_NO_2_check_out_R15                  =  guest_NO_2_check_out_R15,





        )


         
      



        Detail_instance.save()

        Detail_total = Detail_instance.get_total_item_price()


        Detail_Tax   = Detail_instance.get_Tax()

        Detail_Deposit = Detail_instance.get_partial()


        Detail_Rest = float(Detail_total) - float(Detail_Deposit)

        Detail_Full_Name = First_Name +' '+ Last_Name

        Hotel_name = Hotel_name


        print(Detail_total, "This Is Detail total ")

        print(Detail_Full_Name, "This is Full Name")

        print(Detail_Deposit, "This it Detail Deposit")

        print(Hotel_name, "This it Hotel Name")

        print(Hotel_price, )

    



        order_qs = Order.objects.filter(user=request.user, ordered=False)


        # here i should use lasturl = request.META.get('HTTP_REFERER)

        # if lasturl == 'www.Travencia.com/PaymentSuccess':

            # 

        if order_qs.exists():
         

            order_qs.delete()


          
      


        # check if the order item is in the order

        ordered_date = timezone.now()

        order = Order.objects.create(

        user=request.user, ordered_date=ordered_date)

        order.details.add(Detail_instance)

        messages.info(request, "")

        return redirect("Main:PaymentSuccess")
 





    context = {

        'ItmeDetail':ItmeDetail,

        'form':form,

    }
    


    return render(request, "Main/homedetail.html", context)





def ThankYou(request):

    Full_Name = ''

    if request.session.get('name'):

        Full_Name = request.session.get('name')

    context = {

        'FullName':Full_Name,

    }    

    print(Full_Name, 'You')

    return render(request, "Main/thankyou.html",context)


from django.utils import timezone    
import math


class PaymentSuccess(View):

    def get(self, *args, **kwargs):



        try:

            form = payform()

            order = Order.objects.get(user=self.request.user, ordered=False)

            context = {

                'object': order,

                'form':form
               

            }

            return render(self.request, 'Main/PaymentDetails.html', context)

        except ObjectDoesNotExist:

            messages.warning(self.request, "You do not have an active order")

            return redirect("/")
            



    def post(self, *args, **kwargs):



        try:

            form = payform(self.request.POST)

            
            order = Order.objects.get(user=self.request.user, ordered=False)
         
            

            if form.is_valid():

                Card_Number = form.cleaned_data.get('Card_Number')

                Card_Holder = form.cleaned_data.get('Card_Holder')

                Terms       = form.cleaned_data.get('Terms')

                Expires     = form.cleaned_data.get('Expires')

                CVC         = form.cleaned_data.get('CVC')

                Card_Number_Str = Card_Number
                Card_Number_Flo = float(Card_Number_Str)
                print(Card_Number_Flo, 'Card_Number_Flo')
                print(type(Card_Number_Flo))
                Card_Number_Int = int(Card_Number_Flo)
                print(Card_Number_Int)
                print(type(Card_Number_Int))
                number_depo = float()
                for item in order.details.all():
                    depo_ini = item.get_partial()
                    depo_ini2 = float(depo_ini)
                    print(depo_ini)
                    number_depo += depo_ini2
                    print(number_depo, 'this is int stack holder')
                if 9 > 5:
                    messages.info(self.request, "")
                else:
                    messages.warning(self.request, "Sorry, Your Payment Must Be Equal To The Down Payment.")
                    return redirect("Main:PaymentSuccess") 
                


                payment = Payment()

                order_items = order.details.all()

                order_items.update(ordered=True)

                for item in order_items:

                    item.save()

                amount = number_depo

                payment.amount =amount

                payment.user =self.request.user

                payment.Card_Number = Card_Number

                payment.Card_Holder = Card_Holder

                payment.Terms = Terms

                payment.Expires = Expires

                payment.CVC = CVC


                payment.save()

                order.payment = payment

                for item in order.details.all():

                    order_num          = randGen().upper()

                    Hotel_name         = item.item.title

                    Hotel_price        = item.item.price * 1.20

                    Hotel_price_No_Tax = item.item.price 

                    Detail_Full_Name   = item.First_Name + ' ' +  item.Last_Name

                    The_Email          = item.EMail

                    Company_Name       = item.Company_Name

                    The_Nights         = item.Nights 

                    Detail_Tax         = item.get_Tax()

                    Detail_Deposit     = item.get_partial()

                    Detail_total       = item.get_final_price()

                    Number_OF_Guests   = item.Number_OF_Guests 

                    zip                = "zip code" 

                    Phone_Number       = item.Phone_Number

                    Detail_Rest        = float(Detail_total) - float(Detail_Deposit)


                    Room_1                          =   item.Room_1
                    first_name_of_guest_NO_1_R1     =   item.first_name_of_guest_NO_1_R1
                    last_name_of_guest_NO_1_R1      =   item.last_name_of_guest_NO_1_R1
                    guest_NO_1_check_in_R1          =   item.guest_NO_1_check_in_R1
                    guest_NO_1_check_out_R1         =   item.guest_NO_1_check_out_R1
                    duration_guest_NO_1_R1          =   item.duration_guest_NO_1_R1
                    first_name_of_guest_NO_2_R1     =   item.first_name_of_guest_NO_2_R1
                    last_name_of_guest_NO_2_R1      =   item.last_name_of_guest_NO_2_R1
                    guest_NO_2_check_in_R1          =   item.guest_NO_2_check_in_R1
                    guest_NO_2_check_out_R1         =   item.guest_NO_2_check_out_R1

                    Room_2                          =   item.Room_2
                    first_name_of_guest_NO_1_R2     =   item.first_name_of_guest_NO_1_R2
                    last_name_of_guest_NO_1_R2      =   item.last_name_of_guest_NO_1_R2
                    guest_NO_1_check_in_R2          =   item.guest_NO_1_check_in_R2
                    guest_NO_1_check_out_R2         =   item.guest_NO_1_check_out_R2
                    first_name_of_guest_NO_2_R2     =   item.first_name_of_guest_NO_2_R2
                    last_name_of_guest_NO_2_R2      =   item.last_name_of_guest_NO_2_R2
                    guest_NO_2_check_in_R2          =   item.guest_NO_2_check_in_R2
                    guest_NO_2_check_out_R2         =   item.guest_NO_2_check_out_R2


                    Room_3                          =   item.Room_3
                    first_name_of_guest_NO_1_R3     =   item.first_name_of_guest_NO_1_R3
                    last_name_of_guest_NO_1_R3      =   item.last_name_of_guest_NO_1_R3
                    guest_NO_1_check_in_R3          =   item.guest_NO_1_check_in_R3
                    guest_NO_1_check_out_R3         =   item.guest_NO_1_check_out_R3
                    first_name_of_guest_NO_2_R3     =   item.first_name_of_guest_NO_2_R3
                    last_name_of_guest_NO_2_R3      =   item.last_name_of_guest_NO_2_R3
                    guest_NO_2_check_in_R3          =   item.guest_NO_2_check_in_R3
                    guest_NO_2_check_out_R3         =   item.guest_NO_2_check_out_R3



                    Room_4                          =  item.Room_4
                    first_name_of_guest_NO_1_R4     =  item.first_name_of_guest_NO_1_R4
                    last_name_of_guest_NO_1_R4      =  item.last_name_of_guest_NO_1_R4
                    guest_NO_1_check_in_R4          =  item.guest_NO_1_check_in_R4
                    guest_NO_1_check_out_R4         =  item.guest_NO_1_check_out_R4
                    first_name_of_guest_NO_2_R4     =  item.first_name_of_guest_NO_2_R4
                    last_name_of_guest_NO_2_R4      =  item.last_name_of_guest_NO_2_R4
                    guest_NO_2_check_in_R4          =  item.guest_NO_2_check_in_R4
                    guest_NO_2_check_out_R4         =  item.guest_NO_2_check_out_R4



                    Room_5                          = item.Room_5
                    first_name_of_guest_NO_1_R5     = item.first_name_of_guest_NO_1_R5
                    last_name_of_guest_NO_1_R5      = item.last_name_of_guest_NO_1_R5
                    guest_NO_1_check_in_R5          = item.guest_NO_1_check_in_R5
                    guest_NO_1_check_out_R5         = item.guest_NO_1_check_out_R5
                    first_name_of_guest_NO_2_R5     = item.first_name_of_guest_NO_2_R5
                    last_name_of_guest_NO_2_R5      = item.last_name_of_guest_NO_2_R5
                    guest_NO_2_check_in_R5          = item.guest_NO_2_check_in_R5
                    guest_NO_2_check_out_R5         = item.guest_NO_2_check_out_R5



                    Room_6                          =   item.Room_6
                    first_name_of_guest_NO_1_R6     =   item.first_name_of_guest_NO_1_R6
                    last_name_of_guest_NO_1_R6      =   item.last_name_of_guest_NO_1_R6
                    guest_NO_1_check_in_R6          =   item.guest_NO_1_check_in_R6
                    guest_NO_1_check_out_R6         =   item.guest_NO_1_check_out_R6
                    first_name_of_guest_NO_2_R6     =   item.first_name_of_guest_NO_2_R6
                    last_name_of_guest_NO_2_R6      =   item.last_name_of_guest_NO_2_R6
                    guest_NO_2_check_in_R6          =   item.guest_NO_2_check_in_R6
                    guest_NO_2_check_out_R6         =   item.guest_NO_2_check_out_R6


                    Room_7                          =   item.Room_7
                    first_name_of_guest_NO_1_R7     =   item.first_name_of_guest_NO_1_R7
                    last_name_of_guest_NO_1_R7      =   item.last_name_of_guest_NO_1_R7
                    guest_NO_1_check_in_R7          =   item.guest_NO_1_check_in_R7
                    guest_NO_1_check_out_R7         =   item.guest_NO_1_check_out_R7
                    first_name_of_guest_NO_2_R7     =   item.first_name_of_guest_NO_2_R7
                    last_name_of_guest_NO_2_R7      =   item.last_name_of_guest_NO_2_R7
                    guest_NO_2_check_in_R7          =   item.guest_NO_2_check_in_R7
                    guest_NO_2_check_out_R7         =   item.guest_NO_2_check_out_R7

                    Room_8                          =   item.Room_8
                    first_name_of_guest_NO_1_R8     =   item.first_name_of_guest_NO_1_R8
                    last_name_of_guest_NO_1_R8      =   item.last_name_of_guest_NO_1_R8
                    guest_NO_1_check_in_R8          =   item.guest_NO_1_check_in_R8
                    guest_NO_1_check_out_R8         =   item.guest_NO_1_check_out_R8
                    first_name_of_guest_NO_2_R8     =   item.first_name_of_guest_NO_2_R8
                    last_name_of_guest_NO_2_R8      =   item.last_name_of_guest_NO_2_R8
                    guest_NO_2_check_in_R8          =   item.guest_NO_2_check_in_R8
                    guest_NO_2_check_out_R8         =   item.guest_NO_2_check_out_R8
                    
                    Room_9                          =   item.Room_9
                    first_name_of_guest_NO_1_R9     =   item.first_name_of_guest_NO_1_R9
                    last_name_of_guest_NO_1_R9      =   item.last_name_of_guest_NO_1_R9
                    guest_NO_1_check_in_R9          =   item.guest_NO_1_check_in_R9
                    guest_NO_1_check_out_R9         =   item.guest_NO_1_check_out_R9
                    first_name_of_guest_NO_2_R9     =   item.first_name_of_guest_NO_2_R9
                    last_name_of_guest_NO_2_R9      =   item.last_name_of_guest_NO_2_R9
                    guest_NO_2_check_in_R9          =   item.guest_NO_2_check_in_R9
                    guest_NO_2_check_out_R9         =   item.guest_NO_2_check_out_R9


                    Room_10                         =   item.Room_10                         
                    first_name_of_guest_NO_1_R10    =   item.first_name_of_guest_NO_1_R10
                    last_name_of_guest_NO_1_R10     =   item.last_name_of_guest_NO_1_R10
                    guest_NO_1_check_in_R10         =   item.guest_NO_1_check_in_R10
                    guest_NO_1_check_out_R10        =   item.guest_NO_1_check_out_R10
                    first_name_of_guest_NO_2_R10    =   item.first_name_of_guest_NO_2_R10
                    last_name_of_guest_NO_2_R10     =   item.last_name_of_guest_NO_2_R10
                    guest_NO_2_check_in_R10         =   item.guest_NO_2_check_in_R10
                    guest_NO_2_check_out_R10        =   item.guest_NO_2_check_out_R10

                    Room_11                         =   item.Room_11
                    first_name_of_guest_NO_1_R11    =   item.first_name_of_guest_NO_1_R11
                    last_name_of_guest_NO_1_R11     =   item.last_name_of_guest_NO_1_R11
                    guest_NO_1_check_in_R11         =   item.guest_NO_1_check_in_R11
                    guest_NO_1_check_out_R11        =   item.guest_NO_1_check_out_R11
                    first_name_of_guest_NO_2_R11    =   item.first_name_of_guest_NO_2_R11
                    last_name_of_guest_NO_2_R11     =   item.last_name_of_guest_NO_2_R11
                    guest_NO_2_check_in_R11         =   item.guest_NO_2_check_in_R11
                    guest_NO_2_check_out_R11        =   item.guest_NO_2_check_out_R11




                    Room_12                         =   item.Room_12
                    first_name_of_guest_NO_1_R12    =   item.first_name_of_guest_NO_1_R12
                    last_name_of_guest_NO_1_R12     =   item.last_name_of_guest_NO_1_R12
                    guest_NO_1_check_in_R12         =   item.guest_NO_1_check_in_R12
                    guest_NO_1_check_out_R12        =   item.guest_NO_1_check_out_R12
                    first_name_of_guest_NO_2_R12    =   item.first_name_of_guest_NO_2_R12
                    last_name_of_guest_NO_2_R12     =   item.last_name_of_guest_NO_2_R12
                    guest_NO_2_check_in_R12         =   item.guest_NO_2_check_in_R12
                    guest_NO_2_check_out_R12        =   item.guest_NO_2_check_out_R12

                    Room_13                         =   item.Room_13
                    first_name_of_guest_NO_1_R13    =   item.first_name_of_guest_NO_1_R13
                    last_name_of_guest_NO_1_R13     =   item.last_name_of_guest_NO_1_R13
                    guest_NO_1_check_in_R13         =   item.guest_NO_1_check_in_R13
                    guest_NO_1_check_out_R13        =   item.guest_NO_1_check_out_R13
                    first_name_of_guest_NO_2_R13    =   item.first_name_of_guest_NO_2_R13
                    last_name_of_guest_NO_2_R13     =   item.last_name_of_guest_NO_2_R13
                    guest_NO_2_check_in_R13         =   item.guest_NO_2_check_in_R13
                    guest_NO_2_check_out_R13        =   item.guest_NO_2_check_out_R13

                    Room_14                         =   item.Room_14
                    first_name_of_guest_NO_1_R14    =   item.first_name_of_guest_NO_1_R14
                    last_name_of_guest_NO_1_R14     =   item.last_name_of_guest_NO_1_R14
                    guest_NO_1_check_in_R14         =   item.guest_NO_1_check_in_R14
                    guest_NO_1_check_out_R14        =   item.guest_NO_1_check_out_R14
                    first_name_of_guest_NO_2_R14    =   item.first_name_of_guest_NO_2_R14
                    last_name_of_guest_NO_2_R14     =   item.last_name_of_guest_NO_2_R14
                    guest_NO_2_check_in_R14         =   item.guest_NO_2_check_in_R14
                    guest_NO_2_check_out_R14        =   item.guest_NO_2_check_out_R14

                    Room_15                         =   item.Room_15
                    first_name_of_guest_NO_1_R15    =   item.first_name_of_guest_NO_1_R15
                    last_name_of_guest_NO_1_R15     =   item.last_name_of_guest_NO_1_R15
                    guest_NO_1_check_in_R15         =   item.guest_NO_1_check_in_R15
                    guest_NO_1_check_out_R15        =   item.guest_NO_1_check_out_R15
                    first_name_of_guest_NO_2_R15    =   item.first_name_of_guest_NO_2_R15
                    last_name_of_guest_NO_2_R15     =   item.last_name_of_guest_NO_2_R15
                    guest_NO_2_check_in_R15         =   item.guest_NO_2_check_in_R15
                    guest_NO_2_check_out_R15        =   item.guest_NO_2_check_out_R15                  




                    self.request.session['name'] = Detail_Full_Name

                    print(self.request.session['name'])

                    if item.EMail:
                        template_email = render_to_string('Main/form_template_english.html', {           
                            
                        'Detail_Full_Name':Detail_Full_Name, 'order_num':order_num, 'Detail_Tax':Detail_Tax,'Total':Detail_total,'Detail_Rest':Detail_Rest, 'Detail_Deposit':Detail_Deposit,'Hotel':Hotel_name, 


                        'date_time_var':timezone.localdate(), 'Company_Name':Company_Name, 'customer_tel':Phone_Number,'Hotel_price':Hotel_price_No_Tax,  'zip':zip,  'Number_OF_Guests':Number_OF_Guests, 'Nights':int(The_Nights),
                        'The_Email': The_Email,
                        'Phone_Number': Phone_Number,
                        'Room_1':Room_1,
                        'first_name_of_guest_NO_1_R1':first_name_of_guest_NO_1_R1,
                        'last_name_of_guest_NO_1_R1':last_name_of_guest_NO_1_R1,
                        'guest_NO_1_check_in_R1':guest_NO_1_check_in_R1,
                        'guest_NO_1_check_out_R1':guest_NO_1_check_out_R1,
                        'duration_guest_NO_1_R1':duration_guest_NO_1_R1,
                        'first_name_of_guest_NO_2_R1':first_name_of_guest_NO_2_R1,
                        'last_name_of_guest_NO_2_R1':last_name_of_guest_NO_2_R1,
                        'guest_NO_2_check_in_R1':guest_NO_2_check_in_R1,
                        'guest_NO_2_check_out_R1':guest_NO_2_check_out_R1,


                        'Room_2' :Room_2,
                        'first_name_of_guest_NO_1_R2' :first_name_of_guest_NO_1_R2,
                        'last_name_of_guest_NO_1_R2' :last_name_of_guest_NO_1_R2,
                        'guest_NO_1_check_in_R2' :guest_NO_1_check_in_R2,
                        'guest_NO_1_check_out_R2' :guest_NO_1_check_out_R2,
                        'first_name_of_guest_NO_2_R2' :first_name_of_guest_NO_2_R2,
                        'last_name_of_guest_NO_2_R2' :last_name_of_guest_NO_2_R2,
                        'guest_NO_2_check_in_R2' :guest_NO_2_check_in_R2,
                        'guest_NO_2_check_out_R2' :guest_NO_2_check_out_R2,
                        'Room_3' :Room_3,
                        'first_name_of_guest_NO_1_R3' :first_name_of_guest_NO_1_R3,
                        'last_name_of_guest_NO_1_R3' :last_name_of_guest_NO_1_R3,
                        'guest_NO_1_check_in_R3' :guest_NO_1_check_in_R3,
                        'guest_NO_1_check_out_R3' :guest_NO_1_check_out_R3,
                        'first_name_of_guest_NO_2_R3' :first_name_of_guest_NO_2_R3,
                        'last_name_of_guest_NO_2_R3' :last_name_of_guest_NO_2_R3,
                        'guest_NO_2_check_in_R3' :guest_NO_2_check_in_R3,
                        'guest_NO_2_check_out_R3' :guest_NO_2_check_out_R3,
                        'Room_4' :Room_4,
                        'first_name_of_guest_NO_1_R4' :first_name_of_guest_NO_1_R4,
                        'last_name_of_guest_NO_1_R4' :last_name_of_guest_NO_1_R4,
                        'guest_NO_1_check_in_R4' :guest_NO_1_check_in_R4,
                        'guest_NO_1_check_out_R4' :guest_NO_1_check_out_R4,
                        'first_name_of_guest_NO_2_R4' :first_name_of_guest_NO_2_R4,
                        'last_name_of_guest_NO_2_R4' :last_name_of_guest_NO_2_R4,
                        'guest_NO_2_check_in_R4' :guest_NO_2_check_in_R4,
                        'guest_NO_2_check_out_R4' :guest_NO_2_check_out_R4,
                        'Room_5' :Room_5,
                        'first_name_of_guest_NO_1_R5' :first_name_of_guest_NO_1_R5,
                        'last_name_of_guest_NO_1_R5' :last_name_of_guest_NO_1_R5,
                        'guest_NO_1_check_in_R5' :guest_NO_1_check_in_R5,
                        'guest_NO_1_check_out_R5' :guest_NO_1_check_out_R5,
                        'first_name_of_guest_NO_2_R5' :first_name_of_guest_NO_2_R5,
                        'last_name_of_guest_NO_2_R5' :last_name_of_guest_NO_2_R5,
                        'guest_NO_2_check_in_R5' :guest_NO_2_check_in_R5,
                        'guest_NO_2_check_out_R5' :guest_NO_2_check_out_R5,
                        'Room_6' :Room_6,
                        'first_name_of_guest_NO_1_R6' :first_name_of_guest_NO_1_R6,
                        'last_name_of_guest_NO_1_R6' :last_name_of_guest_NO_1_R6,
                        'guest_NO_1_check_in_R6' :guest_NO_1_check_in_R6,
                        'guest_NO_1_check_out_R6' :guest_NO_1_check_out_R6,
                        'first_name_of_guest_NO_2_R6' :first_name_of_guest_NO_2_R6,
                        'last_name_of_guest_NO_2_R6' :last_name_of_guest_NO_2_R6,
                        'guest_NO_2_check_in_R6' :guest_NO_2_check_in_R6,
                        'guest_NO_2_check_out_R6' :guest_NO_2_check_out_R6,
                        'Room_7' :Room_7,
                        'first_name_of_guest_NO_1_R7' :first_name_of_guest_NO_1_R7,
                        'last_name_of_guest_NO_1_R7' :last_name_of_guest_NO_1_R7,
                        'guest_NO_1_check_in_R7' :guest_NO_1_check_in_R7,
                        'guest_NO_1_check_out_R7' :guest_NO_1_check_out_R7,
                        'first_name_of_guest_NO_2_R7' :first_name_of_guest_NO_2_R7,
                        'last_name_of_guest_NO_2_R7' :last_name_of_guest_NO_2_R7,
                        'guest_NO_2_check_in_R7' :guest_NO_2_check_in_R7,
                        'guest_NO_2_check_out_R7' :guest_NO_2_check_out_R7,
                        'Room_8':Room_8,
                        'first_name_of_guest_NO_1_R8':first_name_of_guest_NO_1_R8,
                        'last_name_of_guest_NO_1_R8':last_name_of_guest_NO_1_R8,
                        'guest_NO_1_check_in_R8':guest_NO_1_check_in_R8,
                        'guest_NO_1_check_out_R8':guest_NO_1_check_out_R8,
                        'first_name_of_guest_NO_2_R8':first_name_of_guest_NO_2_R8,
                        'last_name_of_guest_NO_2_R8':last_name_of_guest_NO_2_R8,
                        'guest_NO_2_check_in_R8':guest_NO_2_check_in_R8,
                        'guest_NO_2_check_out_R8':guest_NO_2_check_out_R8,
                        'Room_9':Room_9,
                        'first_name_of_guest_NO_1_R9':first_name_of_guest_NO_1_R9,
                        'last_name_of_guest_NO_1_R9':last_name_of_guest_NO_1_R9,
                        'guest_NO_1_check_in_R9':guest_NO_1_check_in_R9,
                        'guest_NO_1_check_out_R9':guest_NO_1_check_out_R9,
                        'first_name_of_guest_NO_2_R9':first_name_of_guest_NO_2_R9,
                        'last_name_of_guest_NO_2_R9':last_name_of_guest_NO_2_R9,
                        'guest_NO_2_check_in_R9':guest_NO_2_check_in_R9,
                        'guest_NO_2_check_out_R9':guest_NO_2_check_out_R9,
                        'Room_10':Room_10,
                        'first_name_of_guest_NO_1_R10':first_name_of_guest_NO_1_R10,
                        'last_name_of_guest_NO_1_R10':last_name_of_guest_NO_1_R10,
                        'guest_NO_1_check_in_R10':guest_NO_1_check_in_R10,
                        'guest_NO_1_check_out_R10':guest_NO_1_check_out_R10,
                        'first_name_of_guest_NO_2_R10':first_name_of_guest_NO_2_R10,
                        'last_name_of_guest_NO_2_R10':last_name_of_guest_NO_2_R10,
                        'guest_NO_2_check_in_R10':guest_NO_2_check_in_R10,
                        'guest_NO_2_check_out_R10':guest_NO_2_check_out_R10,
                        'Room_11':Room_11,
                        'first_name_of_guest_NO_1_R11':first_name_of_guest_NO_1_R11,
                        'last_name_of_guest_NO_1_R11':last_name_of_guest_NO_1_R11,
                        'guest_NO_1_check_in_R11':guest_NO_1_check_in_R11,
                        'guest_NO_1_check_out_R11':guest_NO_1_check_out_R11,
                        'first_name_of_guest_NO_2_R11':first_name_of_guest_NO_2_R11,
                        'last_name_of_guest_NO_2_R11':last_name_of_guest_NO_2_R11,
                        'guest_NO_2_check_in_R11':guest_NO_2_check_in_R11,
                        'guest_NO_2_check_out_R11':guest_NO_2_check_out_R11,
                        'Room_12':Room_12,
                        'first_name_of_guest_NO_1_R12':first_name_of_guest_NO_1_R12,
                        'last_name_of_guest_NO_1_R12':last_name_of_guest_NO_1_R12,
                        'guest_NO_1_check_in_R12':guest_NO_1_check_in_R12,
                        'guest_NO_1_check_out_R12':guest_NO_1_check_out_R12,
                        'first_name_of_guest_NO_2_R12':first_name_of_guest_NO_2_R12,
                        'last_name_of_guest_NO_2_R12':last_name_of_guest_NO_2_R12,
                        'guest_NO_2_check_in_R12':guest_NO_2_check_in_R12,
                        'guest_NO_2_check_out_R12':guest_NO_2_check_out_R12,
                        'Room_13':Room_13,
                        'first_name_of_guest_NO_1_R13':first_name_of_guest_NO_1_R13,
                        'last_name_of_guest_NO_1_R13':last_name_of_guest_NO_1_R13,
                        'guest_NO_1_check_in_R13':guest_NO_1_check_in_R13,
                        'guest_NO_1_check_out_R13':guest_NO_1_check_out_R13,
                        'first_name_of_guest_NO_2_R13':first_name_of_guest_NO_2_R13,
                        'last_name_of_guest_NO_2_R13':last_name_of_guest_NO_2_R13,
                        'guest_NO_2_check_in_R13':guest_NO_2_check_in_R13,
                        'guest_NO_2_check_out_R13':guest_NO_2_check_out_R13,
                        'Room_14':Room_14,
                        'first_name_of_guest_NO_1_R14':first_name_of_guest_NO_1_R14,
                        'last_name_of_guest_NO_1_R14':last_name_of_guest_NO_1_R14,
                        'guest_NO_1_check_in_R14':guest_NO_1_check_in_R14,
                        'guest_NO_1_check_out_R14':guest_NO_1_check_out_R14,
                        'first_name_of_guest_NO_2_R14':first_name_of_guest_NO_2_R14,
                        'last_name_of_guest_NO_2_R14':last_name_of_guest_NO_2_R14,
                        'guest_NO_2_check_in_R14':guest_NO_2_check_in_R14,
                        'guest_NO_2_check_out_R14':guest_NO_2_check_out_R14,
                        'Room_15':Room_15,
                        'first_name_of_guest_NO_1_R15':first_name_of_guest_NO_1_R15,
                        'last_name_of_guest_NO_1_R15':last_name_of_guest_NO_1_R15,
                        'guest_NO_1_check_in_R15':guest_NO_1_check_in_R15,
                        'guest_NO_1_check_out_R15':guest_NO_1_check_out_R15,
                        'first_name_of_guest_NO_2_R15':first_name_of_guest_NO_2_R15,
                        'last_name_of_guest_NO_2_R15':last_name_of_guest_NO_2_R15,
                        'guest_NO_2_check_in_R15':guest_NO_2_check_in_R15,
                        'guest_NO_2_check_out_R15':guest_NO_2_check_out_R15,



                        } )



                        me = EmailMessage(

                            'Travencia | Hotel Form',template_email , settings.EMAIL_HOST_USER, [The_Email,'mohamedsaleh902@yahoo.com', 'mojaba808@gmail.com'], 

                        )

                        me.content_subtype = "html"

                        me.fail_silently = False

                        me.send()  
                    








                    if item.EMail:


                        template_email = render_to_string('Main/email_template_english.html', {'Detail_Full_Name':Detail_Full_Name, 'order_num':order_num, 'Detail_Tax':Detail_Tax,'Total':Detail_total,'Detail_Rest':Detail_Rest, 'Detail_Deposit':Detail_Deposit,'Hotel':Hotel_name, 


                        'date_time_var':timezone.localdate(), 'Company_Name':Company_Name, 'customer_tel':Phone_Number,'Hotel_price':Hotel_price,  'zip':zip,  'Number_OF_Guests':Number_OF_Guests, 'Nights':int(The_Nights) } )


                        me = EmailMessage(

                            'Travencia | Invoice',template_email , settings.EMAIL_HOST_USER, [The_Email,'mohamedsaleh902@yahoo.com', 'mojaba808@gmail.com'], 

                        )

                        me.content_subtype = "html"

                        me.fail_silently = False

                        me.send()  
       

                    
                  


                    order.ordered       = True

                    order.Deposit       = Detail_Deposit

                    order.Company_Name  = Company_Name

                    order.Hotel_Name    = Hotel_name

                    order.Hotel_Rate    = Hotel_price

                    order.Tax           = Detail_Tax 

                    order.Total         = Detail_total

                    order.Rest          = Detail_Rest

                    order.Email         = The_Email

                    order.Tel           = Phone_Number

                    order.Nights        = The_Nights

                    order.Guests_Number = Number_OF_Guests

                    order.Customer_Name = Detail_Full_Name
                    order.ref_code      = order_num

                    order.save()


       

                return redirect("Main:ThankYou")

            context = {

                'object': order,

                'form':form
               

            }

            return render(self.request, 'Main/PaymentDetails.html', context)

        except ObjectDoesNotExist:

            messages.warning(self.request, "You do not have an active order")

            return redirect("/")



def email(request):

    context = {

        'order_num':order_num,

        'date_time_var':timezone.localdate(),

    }

    return render(request, "Main/email_template_english.html", context)




def form_email(request):

    context = {

        'order_num':order_num,

        'date_time_var':timezone.localdate(),

    }

    return render(request, "Main/form_template_english.html", context)


def pay(request):

    return render(request, "Main/Spare payment details.html")