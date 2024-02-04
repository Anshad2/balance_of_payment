from django.shortcuts import render,redirect

from django.views.generic import View

from revenue.models import Transaction

from django import forms

from django.contrib.auth.models import User

from django.contrib.auth import authenticate,login

# Create your views here.



## trasaction add view
# edit and updated

class TransactionForm(forms.ModelForm):
    class Meta:
        model=Transaction
        exclude=("created_date",)

        # # fields="__all__"
        # # fields=["field1","field2",]

# registration form

class RegistrationForm(forms.ModelForm):
    class Meta:
        model=User
        fields=["username","email","password"]


# not using model form beacuse no need to upadte and edit 
        
class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField()


# # view for creating transaction
# # url: localhost:8000/transaction/add/
# method get,post
class TransactionListView(View):
    def get(self,request,*args,**kwargs):
        qs=Transaction.objects.all()
        return render(request,"transaction_list.html",{"data":qs})

class TransactionCreateView(View):

    def get(self,request,*args,**kwargs):
        form=TransactionForm()
        return render(request,"transaction_add.html",{"form":form}) 
    def post(self,request,*args,**kwargs):
        form=TransactionForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("transaction-list")
        else:
             return render(request,"transaction_add.html",{"form":form}) 




    
# #trasaction details
# url:localhost:8000/transactions/{id}/
#method:get

class TransactionDetailView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Transaction.objects.get(id=id)
        return render(request,"transaction_detail.html",{"data":qs})
    
        

##trasaction delete view
##url: localhost:8000/transactions/{id}/remove
    
class TransactionDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Transaction.objects.filter(id=id).delete()
        return redirect("transaction-list")

## trasaction update/edit view
# url:localhost:8000/transaction/<>/change/
    
class TransactionEditView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        transaction_object=Transaction.objects.get(id=id)
        form=TransactionForm(instance=transaction_object)
        return render(request,"transaction_edit.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        transaction_object=Transaction.objects.get(id=id)
        form=TransactionForm(request.POST,instance=transaction_object)
        if form.is_valid():
            form.save()
            return redirect("transaction-list")
        else:
            return render(request,"transaction_edit.html",{"form":form})



    
#signup view
#url: localhost8000/signup/
        
class SignUpView(View):
    def get(self,request,*args,**kwargs):
        form=RegistrationForm()
        return render(request,"register.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=RegistrationForm(request.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)
            print("record has been added")
            return redirect("signin")
        else:
             print("failed")
             return render(request,"register.html",{"form":form})
        

# signin view
# url:localhost8000/signin/
# get : post
        
class SignInView(View):
    def get(self,request,*args,**kwargs):
        form=LoginForm()
        return render(request,"login.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            u_name=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            print(u_name,pwd)
            user_object=authenticate(request,username=u_name,password=pwd)
            if user_object:
                print("valid")
                login(request,user_object)
                return redirect("transaction-list")
        print("invalid")
        return render(request,"login.html",{"form":form})




        




