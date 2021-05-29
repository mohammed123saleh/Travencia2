from django.db.models.signals import post_save
from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.shortcuts import reverse
from django_countries.fields import CountryField
import pendulum
import datetime
from autoslug import AutoSlugField
from PIL import Image


from django.utils.crypto import get_random_string


from datetime import date, timedelta
from django.template.defaultfilters import slugify
from math import ceil
from django.utils import timezone

import random 
import string

slugRand = random.choices(string.ascii_lowercase + string.digits, k=20)
me = random.randrange(0, 100000, 2)
mar = str(me * 1) 


one     = 1
two     = 2
three   = 3
four    = 4
five    = 5
six     = 6
seven   = 7
eight   = 8
nine    = 9
ten     = 10

eleven      = 11
tweleve     = 12
thirteen    = 13
fourteen    = 14
fifteen     = 15
sixteen     = 16
seventeen   = 17
eighteen    = 18
nineteen    = 19
twenty      = 20

'''
Number_OF_Guests = (
    ('one', 1), ('two', 2), ('three', 3), ('four', 4), ('five', 5), ('six', 6), ('seven', 7), ('eight', 8), ('nine', 9), ('ten', 10), ('eleven', 11), ('tweleve', 12), ('thirteen', 13), ('fourteen', 14), ('fifteen', 15), ('sixteen', 16), ('seventeen', 17), ('eighteen', 18), ('nineteen', 19), ('twenty', 20)
)
'''


Number_OF_Guests = (
    (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15),
)


ROOM_TYPE = (
    ('S', 'single'),
    ('D', 'Double')
)



CATEGORY_CHOICES = (
    ('OB', 'One Bed'),
    ('DB', 'Double Bed'),
    ('S', 'Suite')
)

LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger')
)

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)
 

class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)
    one_click_purchasing = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Item(models.Model):
    
    show = models.BooleanField(default=True)
    title = models.CharField(max_length=250, unique=False, verbose_name="Hotel Name")
    convention = models.CharField(max_length=260, unique=False)
    address = models.CharField(max_length=200)
    price = models.FloatField(unique=False)
    discount_price = models.FloatField(blank=True, null=True, editable=False)
    promo_code = models.CharField(max_length=15, null=True, blank=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2, editable=False)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1, editable=False)
    description = models.TextField(null=True, blank=True, editable=False)
    #slug = models.SlugField(max_length=500, unique=False,help_text='random #input')
    slug = AutoSlugField(populate_from='title',)
    convention_address = models.CharField(max_length=255, blank=True, null=True)
    start_date = models.CharField(max_length=255, null=True, blank=True)
    end_date = models.CharField(max_length=255, null=True, blank=True)
    convention_image = models.ImageField(upload_to='Hotel',  null=True, blank=True)
    image = models.ImageField(upload_to='Hotel', default='Hotel/moha.jpeg', null=True, blank=True)
    class Meta:
        ordering = ['id']
    


    def __str__(self):
        return self.title  
    def save(self, *args, **kwargs, ):

        self.slug = slugify(self.title + '-' + self.convention + '-' + 'Date: '+ '-' + self.start_date + str(get_random_string(12)) + str(self.price))
        super(Item, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("Main:BookDetail", kwargs={
        'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("Main:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("Main:remove-from-cart", kwargs={
            'slug': self.slug
        })

    def add_guest_to_cart_url(self):
        return reverse("Main:add-guest-to-cart", kwargs={
        'slug': self.slug
    })

    def remove_single_customer_from_cart_url(self):
        return reverse("Main:remove-single-customer-from-cart", kwargs={
        'slug': self.slug
        })





    




class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
  
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(default=1)
    guest = models.IntegerField(default=1)
   

   

    def __str__(self):
        return f"{self.quantity} {self.item.title} "
    


  
    def get_total_item_price(self):
        return self.quantity * self.guest * self.item.price  
#        self.item.stay_duration = self.item.check_out_date - self.item.check_in_date
#        calculated_duration = timezone.timedelta(days=ceil(self.item.stay_duration.total_seconds() / 3600 / 24))
#        duration = calculated_duration.days

          # here i should to insert the duration  which will come from the form  datepicker which comes from django-bootstrap-datepicker

    def get_total_discount_item_price(self):
#        self.item.stay_duration = self.item.check_out_date - self.item.check_in_date
#        calculated_duration = timezone.timedelta(days=ceil(self.item.stay_duration.total_seconds() / 3600 / 24))
#        duration = calculated_duration.days
        return self.quantity * self.guest * self.item.discount_price   # here i should to insert the duration  which will come from the form  datepicker which comes from django-bootstrap-datepicker

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()




class Order(models.Model):

    Customer_Name = models.CharField(max_length=250)
    Email         = models.CharField(max_length=250) 
    Tel           = models.CharField(max_length=250)
    Company_Name  = models.CharField(max_length=250)
    Nights        = models.CharField(max_length=250)
    Guests_Number = models.CharField(max_length=250)
    Hotel_Name    = models.CharField(max_length=250)
    Hotel_Rate    = models.CharField(max_length=250) 
    Deposit       = models.CharField(max_length=250)  
    Tax           = models.CharField(max_length=250)
    Total         = models.CharField(max_length=250)
    Rest          = models.CharField(max_length=250)  
   


    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, editable=False)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    details = models.ManyToManyField('Details', editable=False)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
   
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)
        
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    '''
    1. Item added to cart
    2. Adding a billing address
    (Failed checkout)
    3. Payment
    (Preprocessing, processing, packaging etc.)
    4. Being delivered
    5. Received
    6. Refunds
    '''

    def __str__(self):
        return f"Order ID : {self.id} User Name: {self.user.username} "  

    def get_total(self):
        total = 0
        for order_item in self.details.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total 



    def get_partial(self):
        total = 0
        for order_item in self.details.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total / 5

    def get_Tax(self):
        total = 0
        for order_item in self.details.all():
            total += order_item.get_total_without_tax()
        if self.coupon:
            total -= self.coupon.amount
        return total / 5



 

class Details(models.Model):
    user                = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="User_id",
                             on_delete=models.CASCADE, null=True, blank=True, editable=False)

    item                = models.ForeignKey(Item, on_delete=models.CASCADE, null=True, blank=True, editable=False)
    Nights              = models.IntegerField(default=1)
    Guests              = models.IntegerField(default=1)
    ordered             = models.BooleanField(default=False)
    First_Name          = models.CharField(max_length=260)
    Last_Name           = models.CharField(max_length=260)
    EMail               = models.EmailField()
    Company_Name        = models.CharField(max_length=260, null=True, blank=True)
    zip                 = models.CharField(max_length=6, null=True, blank=True)
    Phone_Number        = models.CharField(max_length=16)
    Number_OF_Guests    = models.CharField(max_length=10, choices=Number_OF_Guests, default=1)





    Room_1 = models.CharField(choices=ROOM_TYPE, max_length=1)
    first_name_of_guest_NO_1_R1 = models.CharField(max_length=260)
    last_name_of_guest_NO_1_R1 = models.CharField(max_length=260)
    guest_NO_1_check_in_R1 = models.DateField(null=True, blank=True)
    guest_NO_1_check_out_R1 = models.DateField(null=True, blank=True)
    duration_guest_NO_1_R1 = models.DurationField(null=True, blank=True,editable=False)
    first_name_of_guest_NO_2_R1 = models.CharField(max_length=260, null=True, blank=True)
    last_name_of_guest_NO_2_R1 = models.CharField(max_length=260, null=True, blank=True)
    guest_NO_2_check_in_R1 = models.DateField(null=True, blank=True)
    guest_NO_2_check_out_R1 = models.DateField(null=True, blank=True)

#222222222222222222222222

    Room_2 = models.CharField(choices=ROOM_TYPE, max_length=1,null=True, blank=True )
    first_name_of_guest_NO_1_R2 = models.CharField(max_length=260, null=True, blank=True)
    last_name_of_guest_NO_1_R2 = models.CharField(max_length=260, null=True, blank=True)
    guest_NO_1_check_in_R2 = models.DateField( null=True, blank=True)
    guest_NO_1_check_out_R2 = models.DateField( null=True, blank=True)
    first_name_of_guest_NO_2_R2 = models.CharField(max_length=260, null=True, blank=True)
    last_name_of_guest_NO_2_R2 = models.CharField(max_length=260, null=True, blank=True)
    guest_NO_2_check_in_R2 = models.DateField(null=True, blank=True)
    guest_NO_2_check_out_R2= models.DateField(null=True, blank=True)



#33333333333333333333333333



    Room_3 = models.CharField(choices=ROOM_TYPE, max_length=1,null=True, blank=True )
    first_name_of_guest_NO_1_R3 = models.CharField(max_length=260, null=True, blank=True)
    last_name_of_guest_NO_1_R3 = models.CharField(max_length=260, null=True, blank=True)
    guest_NO_1_check_in_R3 = models.DateField( null=True, blank=True)
    guest_NO_1_check_out_R3 = models.DateField( null=True, blank=True)
    first_name_of_guest_NO_2_R3 = models.CharField(max_length=260, null=True, blank=True)
    last_name_of_guest_NO_2_R3 = models.CharField(max_length=260, null=True, blank=True)
    guest_NO_2_check_in_R3 = models.DateField(null=True, blank=True)
    guest_NO_2_check_out_R3= models.DateField(null=True, blank=True)




#44444444444444444444



    Room_4                       = models.CharField(choices=ROOM_TYPE, max_length=1,null=True, blank=True )


    first_name_of_guest_NO_1_R4  = models.CharField(max_length=260, null=True, blank=True)
    last_name_of_guest_NO_1_R4   = models.CharField(max_length=260, null=True, blank=True)
    guest_NO_1_check_in_R4       = models.DateField( null=True, blank=True)
    guest_NO_1_check_out_R4      = models.DateField( null=True, blank=True)


    first_name_of_guest_NO_2_R4  = models.CharField(max_length=260, null=True, blank=True)
    last_name_of_guest_NO_2_R4   = models.CharField(max_length=260, null=True, blank=True)
    guest_NO_2_check_in_R4       = models.DateField(null=True, blank=True)
    guest_NO_2_check_out_R4      = models.DateField(null=True, blank=True)





#555555555555555555





    Room_5                       = models.CharField(choices=ROOM_TYPE, max_length=1,null=True, blank=True )


    first_name_of_guest_NO_1_R5  = models.CharField(max_length=260, null=True, blank=True)
    last_name_of_guest_NO_1_R5   = models.CharField(max_length=260, null=True, blank=True)
    guest_NO_1_check_in_R5       = models.DateField( null=True, blank=True)
    guest_NO_1_check_out_R5      = models.DateField( null=True, blank=True)


    first_name_of_guest_NO_2_R5  = models.CharField(max_length=260, null=True, blank=True)
    last_name_of_guest_NO_2_R5   = models.CharField(max_length=260, null=True, blank=True)
    guest_NO_2_check_in_R5       = models.DateField(null=True, blank=True)
    guest_NO_2_check_out_R5      = models.DateField(null=True, blank=True)






#666666666666666666


    Room_6                       = models.CharField(choices=ROOM_TYPE, max_length=1,null=True, blank=True )


    first_name_of_guest_NO_1_R6  = models.CharField(max_length=260, null=True, blank=True)
    last_name_of_guest_NO_1_R6  = models.CharField(max_length=260, null=True, blank=True)
    guest_NO_1_check_in_R6       = models.DateField( null=True, blank=True)
    guest_NO_1_check_out_R6      = models.DateField( null=True, blank=True)


    first_name_of_guest_NO_2_R6  = models.CharField(max_length=260, null=True, blank=True)
    last_name_of_guest_NO_2_R6   = models.CharField(max_length=260, null=True, blank=True)
    guest_NO_2_check_in_R6       = models.DateField(null=True, blank=True)
    guest_NO_2_check_out_R6      = models.DateField(null=True, blank=True)






#77777777777777777777



    Room_7                       = models.CharField(choices=ROOM_TYPE, max_length=1,null=True, blank=True )


    first_name_of_guest_NO_1_R7  = models.CharField(max_length=260, null=True, blank=True)
    last_name_of_guest_NO_1_R7  = models.CharField(max_length=260, null=True, blank=True)
    guest_NO_1_check_in_R7       = models.DateField( null=True, blank=True)
    guest_NO_1_check_out_R7      = models.DateField( null=True, blank=True)


    first_name_of_guest_NO_2_R7  = models.CharField(max_length=260, null=True, blank=True)
    last_name_of_guest_NO_2_R7   = models.CharField(max_length=260, null=True, blank=True)
    guest_NO_2_check_in_R7       = models.DateField(null=True, blank=True)
    guest_NO_2_check_out_R7      = models.DateField(null=True, blank=True)




#888888888888888888888



    Room_8                       = models.CharField(choices=ROOM_TYPE, max_length=1,null=True, blank=True )


    first_name_of_guest_NO_1_R8  = models.CharField(max_length=260, null=True, blank=True)
    last_name_of_guest_NO_1_R8  = models.CharField(max_length=260, null=True, blank=True)
    guest_NO_1_check_in_R8       = models.DateField( null=True, blank=True)
    guest_NO_1_check_out_R8      = models.DateField( null=True, blank=True)


    first_name_of_guest_NO_2_R8  = models.CharField(max_length=260, null=True, blank=True)
    last_name_of_guest_NO_2_R8   = models.CharField(max_length=260, null=True, blank=True)
    guest_NO_2_check_in_R8       = models.DateField(null=True, blank=True)
    guest_NO_2_check_out_R8      = models.DateField(null=True, blank=True)






#999999999999999999999





    Room_9                       = models.CharField(choices=ROOM_TYPE, max_length=1,null=True, blank=True )


    first_name_of_guest_NO_1_R9  = models.CharField(max_length=260, null=True, blank=True)
    last_name_of_guest_NO_1_R9   = models.CharField(max_length=260, null=True, blank=True)
    guest_NO_1_check_in_R9       = models.DateField( null=True, blank=True)
    guest_NO_1_check_out_R9      = models.DateField( null=True, blank=True)


    first_name_of_guest_NO_2_R9  = models.CharField(max_length=260, null=True, blank=True)
    last_name_of_guest_NO_2_R9   = models.CharField(max_length=260, null=True, blank=True)
    guest_NO_2_check_in_R9       = models.DateField(null=True, blank=True)
    guest_NO_2_check_out_R9      = models.DateField(null=True, blank=True)






#1010101010101010




    Room_10                       = models.CharField(choices=ROOM_TYPE, max_length=1,null=True, blank=True )


    first_name_of_guest_NO_1_R10  = models.CharField(max_length=260, null=True, blank=True)
    last_name_of_guest_NO_1_R10   = models.CharField(max_length=260, null=True, blank=True)
    guest_NO_1_check_in_R10       = models.DateField( null=True, blank=True)
    guest_NO_1_check_out_R10      = models.DateField( null=True, blank=True)


    first_name_of_guest_NO_2_R10  = models.CharField(max_length=260, null=True, blank=True)
    last_name_of_guest_NO_2_R10   = models.CharField(max_length=260, null=True, blank=True)
    guest_NO_2_check_in_R10       = models.DateField(null=True, blank=True)
    guest_NO_2_check_out_R10      = models.DateField(null=True, blank=True)










#1111111111111111111







    Room_11                       = models.CharField(choices=ROOM_TYPE, max_length=1,null=True, blank=True )


    first_name_of_guest_NO_1_R11  = models.CharField(max_length=260, null=True, blank=True)
    last_name_of_guest_NO_1_R11   = models.CharField(max_length=260, null=True, blank=True)
    guest_NO_1_check_in_R11       = models.DateField( null=True, blank=True)
    guest_NO_1_check_out_R11      = models.DateField( null=True, blank=True)


    first_name_of_guest_NO_2_R11  = models.CharField(max_length=260, null=True, blank=True)
    last_name_of_guest_NO_2_R11   = models.CharField(max_length=260, null=True, blank=True)
    guest_NO_2_check_in_R11       = models.DateField(null=True, blank=True)
    guest_NO_2_check_out_R11      = models.DateField(null=True, blank=True)







#1212121212121212







    Room_12                       = models.CharField(choices=ROOM_TYPE, max_length=1,null=True, blank=True )


    first_name_of_guest_NO_1_R12  = models.CharField(max_length=260, null=True, blank=True)
    last_name_of_guest_NO_1_R12   = models.CharField(max_length=260, null=True, blank=True)
    guest_NO_1_check_in_R12       = models.DateField( null=True, blank=True)
    guest_NO_1_check_out_R12      = models.DateField( null=True, blank=True)


    first_name_of_guest_NO_2_R12  = models.CharField(max_length=260, null=True, blank=True)
    last_name_of_guest_NO_2_R12   = models.CharField(max_length=260, null=True, blank=True)
    guest_NO_2_check_in_R12       = models.DateField(null=True, blank=True)
    guest_NO_2_check_out_R12      = models.DateField(null=True, blank=True)







#131313131331313





    Room_13                       = models.CharField(choices=ROOM_TYPE, max_length=1,null=True, blank=True )


    first_name_of_guest_NO_1_R13  = models.CharField(max_length=260, null=True, blank=True)
    last_name_of_guest_NO_1_R13   = models.CharField(max_length=260, null=True, blank=True)
    guest_NO_1_check_in_R13       = models.DateField( null=True, blank=True)
    guest_NO_1_check_out_R13      = models.DateField( null=True, blank=True)


    first_name_of_guest_NO_2_R13  = models.CharField(max_length=260, null=True, blank=True)
    last_name_of_guest_NO_2_R13   = models.CharField(max_length=260, null=True, blank=True)
    guest_NO_2_check_in_R13       = models.DateField(null=True, blank=True)
    guest_NO_2_check_out_R13      = models.DateField(null=True, blank=True)







#141414141414141414



    Room_14                      = models.CharField(choices=ROOM_TYPE, max_length=1,null=True, blank=True )


    first_name_of_guest_NO_1_R14  = models.CharField(max_length=260, null=True, blank=True)
    last_name_of_guest_NO_1_R14   = models.CharField(max_length=260, null=True, blank=True)
    guest_NO_1_check_in_R14       = models.DateField( null=True, blank=True)
    guest_NO_1_check_out_R14      = models.DateField( null=True, blank=True)


    first_name_of_guest_NO_2_R14  = models.CharField(max_length=260, null=True, blank=True)
    last_name_of_guest_NO_2_R14   = models.CharField(max_length=260, null=True, blank=True)
    guest_NO_2_check_in_R14       = models.DateField(null=True, blank=True)
    guest_NO_2_check_out_R14      = models.DateField(null=True, blank=True)






#151515151515




    Room_15                      = models.CharField(choices=ROOM_TYPE, max_length=1,null=True, blank=True )


    first_name_of_guest_NO_1_R15  = models.CharField(max_length=260, null=True, blank=True)
    last_name_of_guest_NO_1_R15   = models.CharField(max_length=260, null=True, blank=True)
    guest_NO_1_check_in_R15       = models.DateField( null=True, blank=True)
    guest_NO_1_check_out_R15      = models.DateField( null=True, blank=True)


    first_name_of_guest_NO_2_R15  = models.CharField(max_length=260, null=True, blank=True)
    last_name_of_guest_NO_2_R15   = models.CharField(max_length=260, null=True, blank=True)
    guest_NO_2_check_in_R15       = models.DateField(null=True, blank=True)
    guest_NO_2_check_out_R15      = models.DateField(null=True, blank=True)







    def __str__(self):

        return f" Done:{self.ordered} - {self.item.title} - {self.First_Name}  {self.Last_Name} - {self.Company_Name} "
   
   # Moha 
  
    def get_total_item_price(self):

        return self.Nights *  self.item.price  * 1.20

    

    def get_total_without_tax(self):

        return self.Nights *  self.item.price  

    



    def get_total_discount_item_price(self):

        return self.Nights * self.item.discount_price   

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price() 


    def get_partial(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price() / 5
        return self.get_total_item_price() / 5


    def get_Tax(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price() / 5
        return self.get_total_without_tax() / 5



    class Meta:
        verbose_name = 'Detail'
        verbose_name_plural = 'Details'



class Payment(models.Model):
    user        = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, blank=True, null=True, editable=False)
    amount      = models.FloatField()
    Card_Number = models.CharField(max_length=16)
    Card_Holder = models.CharField(max_length=50)
    Expires     = models.CharField(max_length=6)
    CVC         = models.CharField(max_length=6)
    Terms       = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.Card_Holder} - {self.amount}"
    




class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()

    def __str__(self):
        return self.code


class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return f"{self.pk}"


def userprofile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        userprofile = UserProfile.objects.create(user=instance)


post_save.connect(userprofile_receiver, sender=settings.AUTH_USER_MODEL)






class Contact(models.Model):
    Your_Name    = models.CharField(max_length=250, null=False, blank=False)
    Your_Message = models.TextField(null=False, blank=False)
    Your_Email   = models.EmailField()
    time         = models.DateTimeField(auto_now=True)
    Your_Phone   = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return f'{self.Your_Name}'
    class Meta:
        verbose_name = 'Message' 
        verbose_name_plural =   'Messages'


class Signupmodel(models.Model):
    email = models.EmailField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'News Letter' 
        verbose_name_plural =   'News Letters'




class HomeContatcModel(models.Model):
    name = models.CharField(max_length=160)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.name
    class Meta:

        verbose_name = 'Home Page Contact Form'
        verbose_name_plural =   'Home Page Contact Forms'







class Csv(models.Model):
    file_name = models.FileField(upload_to="csv files")
    uploaded  = models.DateTimeField(auto_now_add=True)
    activated = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.file_name}"
    











