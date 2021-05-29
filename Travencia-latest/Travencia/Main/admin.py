from django.db import models
from django.contrib import admin
from tinymce.widgets import TinyMCE
from .mixins import SearchResultsAdminMixin

from .models import Item, OrderItem, Order, Payment, Coupon, Refund, Details, UserProfile, Contact, Signupmodel, HomeContatcModel, Csv

admin.site.site_header = "Travencia Admin"
admin.site.site_title = "Travencia Admin Portal"
admin.site.index_title = "Welcome to Travencia"

def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(refund_requested=False, refund_granted=True)


make_refund_accepted.short_description = 'Update orders to refund granted'

def hide_form(modeladmin, request, queryset):
    queryset.update(show=False)

hide_form.short_description = "Hide Forms"


def show_form(modeladmin, request, queryset):
    queryset.update(show=True)

show_form.short_description = "Show Forms"


class OrderAdmin(admin.ModelAdmin):
    list_display = [ 'Customer_Name',
                     'payment',
                
                    ]
    list_display_links = [
   
                    'Customer_Name',
                    'payment',
     
    ]
    list_filter = [
                    'Customer_Name',
                    'payment',]
    search_fields = [
        'id',
        'user__username',
        'ref_code'
    ]
    actions = [make_refund_accepted]


class AddressAdmin(admin.ModelAdmin):
    list_display = [
      
        'First_Name',
        'Last_Name',
        
    ]
    list_filter = [ 'First_Name','Last_Name']
    search_fields = [ 'First_Name','Last_Name' ]




class ItemAdmin(SearchResultsAdminMixin, admin.ModelAdmin):

    list_editable = [ 'image', 'convention_image']
  
    list_display = ['id',
                    'title',
                    'convention',
                    'convention_address',
                    'start_date',
                    'end_date',
                    'image',
                    'convention_image',               
                    'show',
   

                   
                  
                    ]
    list_display_links = [
                            'title',
                            'convention',
                            'convention_address',
                            'start_date',
                            'end_date',    
                            'show',

                        
                        ]
   # list_filter = [     'title',
   #                     'convention',
   #                     'show',
                        
                     
   #                    ]
    search_fields = [
                    '=title',
                    'convention',
                    'show',
                   
                  
                    ]

    actions = [hide_form, show_form]
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
        }



class orderitemadmin(admin.ModelAdmin):
    list_display = ['user',
                    'item',
               
                   
                  
                    ]
    list_display_links = [
                            'user',
                            'item',
                        
                        ]
    list_filter = [ 'user',
                    'item',
                       ]

'''                       
    search_fields = [
                    'user',
                    'item',

                    ]  
'''                          

admin.site.register(Item, ItemAdmin)
#admin.site.register(OrderItem, orderitemadmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment)
admin.site.register(Coupon)
admin.site.register(Refund)

admin.site.register(UserProfile)
admin.site.register(Contact)
admin.site.register(Signupmodel)
admin.site.register(HomeContatcModel)

admin.site.register(Details)


admin.site.register(Csv)








