from django import forms
from django.contrib.admin import widgets
import datetime
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from bootstrap_datepicker_plus import DatePickerInput
from .models import Item, Contact, Signupmodel, Details, Csv
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

def present_or_future_date(value):
    if value < datetime.date.today():
        raise forms.ValidationError("The date cannot be in the past!")
    return value


ROOM_TYPE = (
    ('S', 'single'),
    ('D', 'Double')
)



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



Number_OF_Guests = (
    (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15),)


PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'PayPal')
)


class CheckoutForm(forms.Form):
    First_Name = forms.CharField(label="",widget=forms.TextInput(attrs={
    'class':'form-control',


    }))
    Last_Name = forms.CharField(label="",widget=forms.TextInput(attrs={
    'class':'form-control',


    }))

    EMail = forms.EmailField(label="",widget=forms.EmailInput(attrs={
        'class':'form-control',
        
      
    }))

    Company_Name = forms.CharField(label="",required=True, widget=forms.TextInput(attrs={
        'class':'form-control',
      
    }))

    zip = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class':'form-control',
        

    }) )



    Phone_Number = forms.CharField(label="",required=True,min_length=9, max_length=16, widget=forms.TextInput(attrs={
        'class':'form-control',
     
    }))


    Number_OF_Guests = forms.ChoiceField(choices=Number_OF_Guests, label='No. of Rooms', widget=forms.Select(attrs={
        
        'id':'Monty'
    })) 


    Room_1= forms.ChoiceField(choices=ROOM_TYPE, initial='S', widget=forms.RadioSelect(attrs={
        'placehoder':'Room Type',      
    }))


    first_name_of_guest_NO_1_R1 = forms.CharField(max_length=260,label='', widget=forms.TextInput(attrs={
        'class':'form-control', 
        'placeholder':'First Name'
    }))
    last_name_of_guest_NO_1_R1 = forms.CharField(max_length=260,label='', widget=forms.TextInput(attrs={
        'class':'form-control', 
        'placeholder':'Last Name'
    }))

    first_name_of_guest_NO_2_R1= forms.CharField(max_length=260, required=False, label=''  ,widget=forms.TextInput(attrs={
        'class':'form-control', 
        'placeholder':' ',
        'id':'DG2-R1'
    }))

    last_name_of_guest_NO_2_R1= forms.CharField(max_length=260, required=False, label=''  ,widget=forms.TextInput(attrs={
        'class':'form-control', 
        'placeholder':' ',
        'id':'DG2-R1'
    }))

#    duration_guest_NO_1_R1         = forms.DurationField(required=False) 
    guest_NO_1_check_in_R1         =  forms.DateField(label='Check-in',   widget=DatePickerInput(attrs={
        'id':'room_one_guest_one', 
        
    }).start_of('event days'), required=True,  validators=[present_or_future_date])
    guest_NO_1_check_out_R1        =    forms.DateField(label='Check-out',  widget=DatePickerInput().end_of('event days'), required=True, validators=[present_or_future_date])
    guest_NO_2_check_in_R1         =   forms.DateField(label='Check-in',  widget=DatePickerInput().start_of('event days'),   required=False,)
    guest_NO_2_check_out_R1        =   forms.DateField(label='Check-out', widget=DatePickerInput().end_of('event days'),     required=False)




## 2222222222222222222222222222


    Room_2= forms.ChoiceField(choices=ROOM_TYPE, initial='S', required=False,  widget=forms.RadioSelect(attrs={
        'placehoder':'Room Type',      
    }))


    first_name_of_guest_NO_1_R2  = forms.CharField(max_length=260,label='',required=False, widget=forms.TextInput(attrs={
        'class':'form-control', 
        'placeholder':' '
    }))
    last_name_of_guest_NO_1_R2  = forms.CharField(max_length=260,label='',required=False, widget=forms.TextInput(attrs={
        'class':'form-control', 
        'placeholder':' '
    }))

    first_name_of_guest_NO_2_R2 = forms.CharField(max_length=260, required=False,label=''  ,widget=forms.TextInput(attrs={
        'class':'form-control', 
        'placeholder':' ',
         
    }))

    last_name_of_guest_NO_2_R2 = forms.CharField(max_length=260, required=False, label=''  ,widget=forms.TextInput(attrs={
        'class':'form-control', 
        'placeholder':'',
         
    }))

    guest_NO_1_check_in_R2         =   forms.DateField(widget=DatePickerInput().start_of('event days'),label="Check-in", required=False)
    guest_NO_1_check_out_R2        =   forms.DateField(widget=DatePickerInput().end_of('event days'),label="Check-out", required=False)

    guest_NO_2_check_in_R2         =   forms.DateField(widget=DatePickerInput().start_of('event days'), label="Check-in", required=False)
    guest_NO_2_check_out_R2        =   forms.DateField(widget=DatePickerInput().end_of('event days'), label="Check-out", required=False)










# 3333333333333333333333

    
    Room_3= forms.ChoiceField(choices=ROOM_TYPE, initial='S', required=False,  widget=forms.RadioSelect(attrs={
        'placehoder':'Room Type',      
    }))


    first_name_of_guest_NO_1_R3  = forms.CharField(max_length=260,label='', required=False, widget=forms.TextInput(attrs={
        'class':'form-control', 
        'placeholder':' '
    }))
    last_name_of_guest_NO_1_R3  = forms.CharField(max_length=260, label='',required=False, widget=forms.TextInput(attrs={
        'class':'form-control', 
        'placeholder':' '
    }))

    first_name_of_guest_NO_2_R3 = forms.CharField(max_length=260, required=False, label=''  ,widget=forms.TextInput(attrs={
        'class':'form-control', 
        'placeholder':' ',
         
    }))

    last_name_of_guest_NO_2_R3 = forms.CharField(max_length=260, required=False, label=''  ,widget=forms.TextInput(attrs={
        'class':'form-control', 
        'placeholder':' ',
         
    }))

    guest_NO_1_check_in_R3         =   forms.DateField(widget=DatePickerInput().start_of('event days'), label="Check-in", required=False)
    guest_NO_1_check_out_R3        =   forms.DateField(widget=DatePickerInput().end_of('event days'), label="Check-out", required=False)

    guest_NO_2_check_in_R3        =   forms.DateField(widget=DatePickerInput().start_of('event days'),  label="Check-in", required=False)
    guest_NO_2_check_out_R3        =   forms.DateField(widget=DatePickerInput().end_of('event days'), label="Check-out", required=False)






#444444444444444



    Room_4                          =forms.ChoiceField(choices=ROOM_TYPE, initial='S', required=False,  widget=forms.RadioSelect(attrs={
        'placehoder':'Room Type',      
    }))


    first_name_of_guest_NO_1_R4      =forms.CharField(max_length=260,label='', required=False, widget=forms.TextInput(attrs={
        'class':'form-control', 
        'placeholder':' ',
        'id':'rm4'
    }))
    last_name_of_guest_NO_1_R4       =forms.CharField(max_length=260, label='',required=False, widget=forms.TextInput(attrs={
        'class':'form-control', 
        'placeholder':' '
    }))





    first_name_of_guest_NO_2_R4       =forms.CharField(max_length=260, required=False, label=''  ,widget=forms.TextInput(attrs={
        'class':'form-control', 
        'placeholder':' ',
         
    }))

    last_name_of_guest_NO_2_R4        =forms.CharField(max_length=260, required=False, label=''  ,widget=forms.TextInput(attrs={
        'class':'form-control', 
        'placeholder':' ',
         
    }))

    guest_NO_1_check_in_R4           =forms.DateField(widget=DatePickerInput().start_of('event days'), label="Check-in", required=False)
    guest_NO_1_check_out_R4          =forms.DateField(widget=DatePickerInput().end_of('event days'), label="Check-out", required=False)


    guest_NO_2_check_in_R4            =forms.DateField(widget=DatePickerInput().start_of('event days'), label="Check-in", required=False)
    guest_NO_2_check_out_R4           =forms.DateField(widget=DatePickerInput().end_of('event days'), label="Check-out", required=False)







#555555555555555555555555555





    Room_5                          =forms.ChoiceField(choices=ROOM_TYPE, initial='S', required=False,  widget=forms.RadioSelect(attrs={
        'placehoder':'Room Type',      
    }))


    first_name_of_guest_NO_1_R5      =forms.CharField(max_length=260,label='', required=False, widget=forms.TextInput(attrs={
        'class':'form-control', 
        'placeholder':' '
    }))
    last_name_of_guest_NO_1_R5       =forms.CharField(max_length=260, label='',required=False, widget=forms.TextInput(attrs={
        'class':'form-control', 
        'placeholder':' '
    }))

    guest_NO_1_check_in_R5           =forms.DateField(widget=DatePickerInput().start_of('event days'), label="Check-in", required=False)
    guest_NO_1_check_out_R5          =forms.DateField(widget=DatePickerInput().end_of('event days'), label="Check-out", required=False)





    first_name_of_guest_NO_2_R5       =forms.CharField(max_length=260, required=False, label=''  ,widget=forms.TextInput(attrs={
        'class':'form-control', 
        'placeholder':' ',
         
    }))

    last_name_of_guest_NO_2_R5       =forms.CharField(max_length=260, required=False, label=''  ,widget=forms.TextInput(attrs={
        'class':'form-control', 
        'placeholder':' ',
         
    }))


    guest_NO_2_check_in_R5           =forms.DateField(widget=DatePickerInput().start_of('event days'),  label="Check-in", required=False)
    guest_NO_2_check_out_R5           =forms.DateField(widget=DatePickerInput().end_of('event days'), label="Check-out", required=False)








#6666666666666666666





    Room_6                          =forms.ChoiceField(choices=ROOM_TYPE, initial='S', required=False,  widget=forms.RadioSelect(attrs={
        'placehoder':'Room Type',      
    }))


    first_name_of_guest_NO_1_R6      =forms.CharField(max_length=260,label='', required=False, widget=forms.TextInput(attrs={
        'class':'form-control', 
        'placeholder':' '
    }))
    last_name_of_guest_NO_1_R6       =forms.CharField(max_length=260, label='',required=False, widget=forms.TextInput(attrs={
        'class':'form-control', 
        'placeholder':' '
    }))

    guest_NO_1_check_in_R6           =forms.DateField(widget=DatePickerInput().start_of('event days'), label="Check-in", required=False)
    guest_NO_1_check_out_R6          =forms.DateField(widget=DatePickerInput().end_of('event days'), label="Check-out", required=False)





    first_name_of_guest_NO_2_R6       =forms.CharField(max_length=260, required=False, label=''  ,widget=forms.TextInput(attrs={
        'class':'form-control', 
        'placeholder':' ',
         
    }))

    last_name_of_guest_NO_2_R6       =forms.CharField(max_length=260, required=False, label=''  ,widget=forms.TextInput(attrs={
        'class':'form-control', 
        'placeholder':' ',
         
    }))


    guest_NO_2_check_in_R6           =forms.DateField(widget=DatePickerInput().start_of('event days'),  label="Check-in", required=False)
    guest_NO_2_check_out_R6           =forms.DateField(widget=DatePickerInput().end_of('event days'), label="Check-out", required=False)




#777777777777777777




    Room_7                          =forms.ChoiceField(choices=ROOM_TYPE, initial='S', required=False,  widget=forms.RadioSelect(attrs={
        'placehoder':'Room Type',      
    }))


    first_name_of_guest_NO_1_R7      =forms.CharField(max_length=260,label='', required=False, widget=forms.TextInput(attrs={
        'class':'form-control', 
        'placeholder':' '
    }))
    last_name_of_guest_NO_1_R7       =forms.CharField(max_length=260, label='',required=False, widget=forms.TextInput(attrs={
        'class':'form-control', 
        'placeholder':' '
    }))

    guest_NO_1_check_in_R7           =forms.DateField(widget=DatePickerInput().start_of('event days'), label="Check-in", required=False)
    guest_NO_1_check_out_R7          =forms.DateField(widget=DatePickerInput().end_of('event days'), label="Check-out", required=False)





    first_name_of_guest_NO_2_R7       =forms.CharField(max_length=260, required=False, label=''  ,widget=forms.TextInput(attrs={
        'class':'form-control', 
        'placeholder':' ',
         
    }))

    last_name_of_guest_NO_2_R7       =forms.CharField(max_length=260, required=False, label=''  ,widget=forms.TextInput(attrs={
        'class':'form-control', 
        'placeholder':' ',
         
    }))


    guest_NO_2_check_in_R7           =forms.DateField(widget=DatePickerInput().start_of('event days'),  label="Check-in", required=False)
    guest_NO_2_check_out_R7           =forms.DateField(widget=DatePickerInput().end_of('event days'), label="Check-out", required=False)




#888888888888888888888888






    Room_8                          =forms.ChoiceField(choices=ROOM_TYPE, initial='S', required=False,  widget=forms.RadioSelect(attrs={
        'placehoder':'Room Type',      
    }))


    first_name_of_guest_NO_1_R8      =forms.CharField(max_length=260,label='', required=False, widget=forms.TextInput(attrs={
        'class':'form-control', 
        'placeholder':' '
    }))
    last_name_of_guest_NO_1_R8       =forms.CharField(max_length=260, label='',required=False, widget=forms.TextInput(attrs={
        'class':'form-control', 
        'placeholder':' '
    }))

    guest_NO_1_check_in_R8           =forms.DateField(widget=DatePickerInput().start_of('event days'), label="Check-in", required=False)
    guest_NO_1_check_out_R8          =forms.DateField(widget=DatePickerInput().end_of('event days'), label="Check-out", required=False)





    first_name_of_guest_NO_2_R8       =forms.CharField(max_length=260, required=False, label=''  ,widget=forms.TextInput(attrs={
        'class':'form-control', 
        'placeholder':' ',
         
    }))

    last_name_of_guest_NO_2_R8       =forms.CharField(max_length=260, required=False, label=''  ,widget=forms.TextInput(attrs={
        'class':'form-control', 
        'placeholder':' ',
         
    }))


    guest_NO_2_check_in_R8           =forms.DateField(widget=DatePickerInput().start_of('event days'),  label="Check-in", required=False)
    guest_NO_2_check_out_R8           =forms.DateField(widget=DatePickerInput().end_of('event days'), label="Check-out", required=False)








#999999999999999999









    Room_9                          =forms.ChoiceField(choices=ROOM_TYPE, initial='S', required=False,  widget=forms.RadioSelect(attrs={
        'placehoder':'Room Type',      
    }))


    first_name_of_guest_NO_1_R9      =forms.CharField(max_length=260,label='', required=False, widget=forms.TextInput(attrs={
        'class':'form-control', 
        'placeholder':' '
    }))
    last_name_of_guest_NO_1_R9       =forms.CharField(max_length=260, label='',required=False, widget=forms.TextInput(attrs={
        'class':'form-control', 
        'placeholder':' '
    }))

    guest_NO_1_check_in_R9          =forms.DateField(widget=DatePickerInput().start_of('event days'), label="Check-in", required=False)
    guest_NO_1_check_out_R9          =forms.DateField(widget=DatePickerInput().end_of('event days'), label="Check-out", required=False)





    first_name_of_guest_NO_2_R9       =forms.CharField(max_length=260, required=False, label=''  ,widget=forms.TextInput(attrs={
        'class':'form-control', 
        'placeholder':' ',
         
    }))

    last_name_of_guest_NO_2_R9       =forms.CharField(max_length=260, required=False, label=''  ,widget=forms.TextInput(attrs={
        'class':'form-control', 
        'placeholder':' ',
         
    }))


    guest_NO_2_check_in_R9           =forms.DateField(widget=DatePickerInput().start_of('event days'),  label="Check-in", required=False)
    guest_NO_2_check_out_R9           =forms.DateField(widget=DatePickerInput().end_of('event days'), label="Check-out", required=False)





#101010101010101




    Room_10                            =forms.ChoiceField(choices=ROOM_TYPE, initial='S', required=False,  widget=forms.RadioSelect(attrs={
        'placehoder':'Room Type',      
    }))


    first_name_of_guest_NO_1_R10        =forms.CharField(max_length=260,label='', required=False, widget=forms.TextInput(attrs={
        'class':'form-control', 
        'placeholder':' '
    }))
    last_name_of_guest_NO_1_R10         =forms.CharField(max_length=260, label='',required=False, widget=forms.TextInput(attrs={
        'class':'form-control', 
        'placeholder':' '
    }))

    guest_NO_1_check_in_R10            =forms.DateField(widget=DatePickerInput().start_of('event days'), label="Check-in", required=False)
    guest_NO_1_check_out_R10           =forms.DateField(widget=DatePickerInput().end_of('event days'), label="Check-out", required=False)





    first_name_of_guest_NO_2_R10       =forms.CharField(max_length=260, required=False, label=''  ,widget=forms.TextInput(attrs={
        'class':'form-control', 
        'placeholder':' ',
         
    }))

    last_name_of_guest_NO_2_R10        =forms.CharField(max_length=260, required=False, label=''  ,widget=forms.TextInput(attrs={
        'class':'form-control', 
        'placeholder':' ',
         
    }))


    guest_NO_2_check_in_R10            =forms.DateField(widget=DatePickerInput().start_of('event days'),         label="Check-in", required=False)
    guest_NO_2_check_out_R10           =forms.DateField(widget=DatePickerInput().end_of('event days'), label="Check-out", required=False)





#11111111111111111111





    Room_11                            =forms.ChoiceField(choices=ROOM_TYPE, initial='S', required=False,  widget=forms.RadioSelect(attrs={
        'placehoder':'Room Type',      
    }))


    first_name_of_guest_NO_1_R11        =forms.CharField(max_length=260,label='', required=False, widget=forms.TextInput(attrs={
        'class':'form-control', 
        'placeholder':' '
    }))
    last_name_of_guest_NO_1_R11         =forms.CharField(max_length=260, label='',required=False, widget=forms.TextInput(attrs={
        'class':'form-control', 
        'placeholder':' '
    }))

    guest_NO_1_check_in_R11            =forms.DateField(widget=DatePickerInput().start_of('event days'), label="Check-in", required=False)
    guest_NO_1_check_out_R11           =forms.DateField(widget=DatePickerInput().end_of('event days'), label="Check-out", required=False)





    first_name_of_guest_NO_2_R11       =forms.CharField(max_length=260, required=False, label=''  ,widget=forms.TextInput(attrs={
        'class':'form-control', 
        'placeholder':' ',
         
    }))

    last_name_of_guest_NO_2_R11        =forms.CharField(max_length=260, required=False, label=''  ,widget=forms.TextInput(attrs={
        'class':'form-control', 
        'placeholder':' ',
         
    }))


    guest_NO_2_check_in_R11            =forms.DateField(widget=DatePickerInput().start_of('event days'),  label="Check-in", required=False)
    guest_NO_2_check_out_R11           =forms.DateField(widget=DatePickerInput().end_of('event days'), label="Check-out", required=False)





#121212121212212212








    Room_12                            =forms.ChoiceField(choices=ROOM_TYPE, initial='S', required=False,  widget=forms.RadioSelect(attrs={
        'placehoder':'Room Type',      
    }))


    first_name_of_guest_NO_1_R12        =forms.CharField(max_length=260,label='', required=False, widget=forms.TextInput(attrs={
        'class':'form-control', 
        'placeholder':' '
    }))
    last_name_of_guest_NO_1_R12         =forms.CharField(max_length=260, label='',required=False, widget=forms.TextInput(attrs={
        'class':'form-control', 
        'placeholder':' '
    }))

    guest_NO_1_check_in_R12            =forms.DateField(widget=DatePickerInput().start_of('event days'), label="Check-in", required=False)
    guest_NO_1_check_out_R12           =forms.DateField(widget=DatePickerInput().end_of('event days'), label="Check-out", required=False)





    first_name_of_guest_NO_2_R12       =forms.CharField(max_length=260, required=False, label=''  ,widget=forms.TextInput(attrs={
        'class':'form-control', 
        'placeholder':' ',
         
    }))

    last_name_of_guest_NO_2_R12        =forms.CharField(max_length=260, required=False, label=''  ,widget=forms.TextInput(attrs={
        'class':'form-control', 
        'placeholder':' ',
         
    }))


    guest_NO_2_check_in_R12            =forms.DateField(widget=DatePickerInput().start_of('event days'),  label="Check-in", required=False)
    guest_NO_2_check_out_R12          =forms.DateField(widget=DatePickerInput().end_of('event days'), label="Check-out", required=False)






#13131313131313113





    Room_13                            =forms.ChoiceField(choices=ROOM_TYPE, initial='S', required=False,  widget=forms.RadioSelect(attrs={
        'placehoder':'Room Type',      
    }))


    first_name_of_guest_NO_1_R13        =forms.CharField(max_length=260,label='', required=False, widget=forms.TextInput(attrs={
        'class':'form-control', 
        'placeholder':' '
    }))
    last_name_of_guest_NO_1_R13         =forms.CharField(max_length=260, label='',required=False, widget=forms.TextInput(attrs={
        'class':'form-control', 
        'placeholder':' '
    }))

    guest_NO_1_check_in_R13            =forms.DateField(widget=DatePickerInput().start_of('event days'), label="Check-in", required=False)
    guest_NO_1_check_out_R13           =forms.DateField(widget=DatePickerInput().end_of('event days'), label="Check-out", required=False)





    first_name_of_guest_NO_2_R13       =forms.CharField(max_length=260, required=False, label=''  ,widget=forms.TextInput(attrs={
        'class':'form-control', 
        'placeholder':' ',
         
    }))

    last_name_of_guest_NO_2_R13        =forms.CharField(max_length=260, required=False, label=''  ,widget=forms.TextInput(attrs={
        'class':'form-control', 
        'placeholder':' ',
         
    }))


    guest_NO_2_check_in_R13            =forms.DateField(widget=DatePickerInput().start_of('event days'),  label="Check-in", required=False)
    guest_NO_2_check_out_R13          =forms.DateField(widget=DatePickerInput().end_of('event days'), label="Check-out", required=False)





#14141414141141









    Room_14                            =forms.ChoiceField(choices=ROOM_TYPE,  initial='S', required=False,  widget=forms.RadioSelect(attrs={
        'placehoder':'Room Type',      
    }))


    first_name_of_guest_NO_1_R14        =forms.CharField(max_length=260,label='', required=False, widget=forms.TextInput(attrs={
        'class':'form-control', 
        'placeholder':' '
    }))
    last_name_of_guest_NO_1_R14         =forms.CharField(max_length=260, label='',required=False, widget=forms.TextInput(attrs={
        'class':'form-control', 
        'placeholder':' '
    }))

    guest_NO_1_check_in_R14            =forms.DateField(widget=DatePickerInput().start_of('event days'), label="Check-in", required=False)
    guest_NO_1_check_out_R14           =forms.DateField(widget=DatePickerInput().end_of('event days'), label="Check-out", required=False)





    first_name_of_guest_NO_2_R14       =forms.CharField(max_length=260, required=False, label=''  ,widget=forms.TextInput(attrs={
        'class':'form-control', 
        'placeholder':' ',
         
    }))

    last_name_of_guest_NO_2_R14        =forms.CharField(max_length=260, required=False, label=''  ,widget=forms.TextInput(attrs={
        'class':'form-control', 
        'placeholder':' ',
         
    }))


    guest_NO_2_check_in_R14            =forms.DateField(widget=DatePickerInput().start_of('event days'),  label="Check-in", required=False)
    guest_NO_2_check_out_R14           =forms.DateField(widget=DatePickerInput().end_of('event days'), label="Check-out", required=False)







#1515151511551515





    Room_15                            =forms.ChoiceField(choices=ROOM_TYPE, initial='S', required=False,  widget=forms.RadioSelect(attrs={
        'placehoder':'Room Type',      
    }))


    first_name_of_guest_NO_1_R15        =forms.CharField(max_length=260,label='', required=False, widget=forms.TextInput(attrs={
        'class':'form-control', 
        'placeholder':' '
    }))
    last_name_of_guest_NO_1_R15         =forms.CharField(max_length=260, label='',required=False, widget=forms.TextInput(attrs={
        'class':'form-control', 
        'placeholder':' '
    }))

    guest_NO_1_check_in_R15            =forms.DateField(widget=DatePickerInput().start_of('event days'), label="Check-in", required=False)
    guest_NO_1_check_out_R15           =forms.DateField(widget=DatePickerInput().end_of('event days'),  label="Check-out", required=False)





    first_name_of_guest_NO_2_R15      =forms.CharField(max_length=260, required=False, label=''  ,widget=forms.TextInput(attrs={
        'class':'form-control', 
        'placeholder':' ',
         
    }))

    last_name_of_guest_NO_2_R15        =forms.CharField(max_length=260, required=False, label=''  ,widget=forms.TextInput(attrs={
        'class':'form-control', 
        'placeholder':' ',
         
    }))


    guest_NO_2_check_in_R15            =forms.DateField(widget=DatePickerInput().start_of('event days'),  label="Check-in", required=False)
    guest_NO_2_check_out_R15           =forms.DateField(widget=DatePickerInput().end_of('event days'), label="Check-out", required=False)


























class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Promo code',
        'aria-label': 'Recipient\'s username',
        'aria-describedby': 'basic-addon2'
    }))


class RefundForm(forms.Form):
    ref_code = forms.CharField()
    message = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 4
    }))
    email = forms.EmailField()


class PaymentForm(forms.Form):
    stripeToken = forms.CharField(required=False)
    save = forms.BooleanField(required=False)
    use_default = forms.BooleanField(required=False)


class payform(forms.Form):
    Card_Number =forms.CharField(max_length=16, min_length=16, label='Card Number',widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder':'',
        'id':'card_number',

    }))
    Card_Holder =forms.CharField(max_length=50, label='Card Holder',widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder':'',
   

    }))

    Expires =forms.CharField( max_length=6,label='Expires',widget=forms.TextInput(attrs={
        'class': 'input-field',
        'placeholder':'',
   

    }))


    CVC =forms.CharField(max_length=6, label='CVC',widget=forms.TextInput(attrs={
        'class': 'input-field',
        'placeholder':'',
   

    }))

   
   

    Terms = forms.BooleanField(required=True,label="by clicking checkout button i agree to terms and conditions")






'''
class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ('id', 'title', 'description', 'date', 'start_time',
                  'end_time')

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['date'].widget = widgets.AdminDateWidget()
        self.fields['start_time'].widget = widgets.AdminTimeWidget()
        self.fields['end_time'].widget = widgets.AdminTimeWidget()



'''











class EmailSignupForm(forms.ModelForm):

    class Meta:
        model = Signupmodel
        fields = ('email', )



class HomeContatct(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control text-white',
        'placeholder':'Name'

    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class':'form-control text-white',
        'placeholder':'Email'


    }))
    message = forms.CharField(widget=forms.Textarea(attrs={
        'class':'form-control text-white',
        'placeholder':'Your Message',
        'rows':8
    }))





class AddressTow(forms.ModelForm):
    class Meta:
        model = Details
        fields = "__all__"


#        widgets = {
#            'name': Textarea(attrs={'cols': 80, 'rows': 20}),
#        }









class ContactHome(forms.ModelForm):
    Your_Name = forms.CharField(label="", widget=forms.TextInput(attrs={
        'class':'form-control', 
        'placeholder':'   Name',
        'id':'whity',
    }))
    Your_Email = forms.EmailField(label="",widget=forms.EmailInput(attrs={
        'class':'form-control', 
        'placeholder':'   Email',
         'id':'whity',

    }))
    Your_Phone=  forms.CharField(label="",required=False,widget=forms.TextInput(attrs={
        'class':'form-control', 
        'placeholder':'   Phone',
        'id':'whity',
    }))
    Your_Message = forms.CharField(label="",widget=forms.Textarea(attrs={
        'class':'form-control', 
        'placeholder':'   Message',
        'rows':8,
        'id':'whity',

    }))

    class Meta:
        model = Contact
        fields = ("__all__")



class Csv_form(forms.ModelForm):
    file_name = forms.FileField( widget=forms.FileInput(attrs={
        'class':'form-control-file', 
     
    }))
    
    class Meta:
        model = Csv
        fields = ("file_name",)
