from django.shortcuts import render,redirect

from django.views.generic import View

from revenue.models import Transaction

from django import forms

from django.contrib.auth.models import User

from django.contrib.auth import authenticate,login,logout

from django.utils import timezone

from django.db.models import Sum

from django.utils.decorators import method_decorator

from django.contrib import messages

from django.views.decorators.cache import never_cache

# Create your views here.

# decorators



def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.error(request,"invalid session")
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper
decs=[signin_required,never_cache]


## trasaction add view
# edit and updated

class TransactionForm(forms.ModelForm):
    class Meta:
        model=Transaction
        exclude=("created_date","user")
        ##design of add page 
        # widgets only for model form
        widgets={
            "title":forms.TextInput(attrs={"class":"form-control"}),
            "amount":forms.NumberInput(attrs={"class":"form-control"}),
            "type":forms.Select(attrs={"class":"form-control form-select"}),
            "category":forms.Select(attrs={"class":"form-control form-select"})
        }

        # # fields="__all__"
        # # fields=["field1","field2",]

# registration form

class RegistrationForm(forms.ModelForm):
    class Meta:
        model=User
        fields=["username","email","password"]
        widgets={
            "username":forms.TextInput(attrs={"class":"form-control"}),
            "email":forms.EmailInput(attrs={"class":"form-control"}),
            "password":forms.PasswordInput(attrs={"class":"form-control"})
        }


# not using model form beacuse no need to upadte and edit 
        
class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))


# # view for creating transaction
# # url: localhost:8000/transaction/add/
# method get,post
@method_decorator(decs,name="dispatch")
class TransactionListView(View):
    def get(self,request,*args,**kwargs):
        # to get difrent track for difrent user
        qs=Transaction.objects.filter(user=request.user)
        curr_month=timezone.now().month
        curr_year=timezone.now().year
        data=Transaction.objects.filter(
            created_date__month=curr_month,
            created_date__year=curr_year,
            user=request.user
        ).values("type").annotate(type_sum=Sum("amount"))
        cat_qs=Transaction.objects.filter(
            created_date__month=curr_month,
            created_date__year=curr_year,
            user=request.user
        ).values("category").annotate(cat_sum=Sum("amount"))
        print(cat_qs)
        
        # expense_trans=Transaction.objects.filter(
        #     user=request.user,
        #     type="expense",
        #     created_date__month=curr_month,
        #     created_date__year=curr_year
        # ).aggregate(Sum("amount"))
        # curr_month=timezone.now().month
        # curr_year=timezone.now().year
        # income_trans=Transaction.objects.filter(
        #     user=request.user,
        #     type="income",
        #     created_date__month=curr_month,
        #     created_date__year=curr_year
        # ).aggregate(Sum("amount"))
        # print(expense_trans)
        # print(income_trans)

        return render(request,"transaction_list.html",{"data":qs,"type_total":data,"cat_sum":cat_qs})
    
@method_decorator(decs,name="dispatch")
class TransactionCreateView(View):

    def get(self,request,*args,**kwargs):
        form=TransactionForm()
        return render(request,"transaction_add.html",{"form":form}) 
    def post(self,request,*args,**kwargs):
        form=TransactionForm(request.POST)

        if form.is_valid():
            # to avoid multilple name come for same user ex: each time cart adding no need same user
            # form.instance.user=request.user
            # form.save()
            data=form.cleaned_data
            Transaction.objects.create(**data,user=request.user)
            messages.success(request,"Transaction has been added successfully")

            return redirect("transaction-list")
        else:
             messages.error(request,"Failed to add transaction")
             return render(request,"transaction_add.html",{"form":form,}) 



# #trasaction details
# url:localhost:8000/transactions/{id}/
#method:get
@method_decorator(decs,name="dispatch")
class TransactionDetailView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Transaction.objects.get(id=id)
        return render(request,"transaction_detail.html",{"data":qs}) 

##trasaction delete view
##url: localhost:8000/transactions/{id}/remove
@method_decorator(decs,name="dispatch")  
class TransactionDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Transaction.objects.filter(id=id).delete()
        return redirect("transaction-list")

## trasaction update/edit view
# url:localhost:8000/transaction/<>/change/
@method_decorator(decs,name="dispatch")
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
            messages.success(request,"Transaction has been Edited successfully")

            return redirect("transaction-list")
        else:
            messages.error(request,"Transaction edit failed")

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
@method_decorator(never_cache,name="dispatch")     
class SignInView(View):
    def get(self,request,*args,**kwargs):
        form=LoginForm()
        return render(request,"signin.html",{"form":form})
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
                # request.user => anonymus user(user has no session)
                return redirect("transaction-list")
        print("invalid")
        return render(request,"signin.html",{"form":form})


# signout
@method_decorator(decs,name="dispatch")    
class SignOutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("signin")





        




