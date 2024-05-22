from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserForm, UserProfileForm, TransactionForm, BudgetForm, GoalForm
from . import models
from django import forms
from django.db.models import Sum,Q
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse,JsonResponse
from datetime import datetime,date
import re

# Create your views here.

active= {'dashboard':0,'transaction':0,'add_transaction':0,'goal':0,'budget':0}
def index(request):
    return render(request,'index.html')

def register(request):
    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()
            return redirect('/login/')
        else:
            print(user_form.errors, profile_form.errors) 
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render (request, 'register.html', {'user_form': user_form, 'profile_form': profile_form,})

@login_required
def dashboard(request):
    current_date = date.today()
    results = models.Budget.objects.filter(
        Q(end_date__gte=current_date) & Q(user=request.user)
    )
    dic ={}
    data=[]

    for result in results:
        expenses = models.Transaction.objects.filter(Q(date__gte=result.start_date) & Q(date__lte=result.end_date) &
                                                    Q(user= request.user) &
                                                    Q(transaction_type='EXPENSE') &
                                                    Q(category=result.category)
                                                    ).values('category__name').annotate(total_amount=Sum('amount'))
        if expenses:
            dic = {}
            dic['category'] = result.category.name
            dic['budget'] = result.amount
            dic['expense'] = expenses[0]['total_amount']
            dic['expense_percentage'] = round((expenses[0]['total_amount'] / result.amount) * 100, 2)
            dic['amount_left'] = result.amount - expenses[0]['total_amount']
            data.append(dic)
        else:
            dic = {}
            dic['category'] = result.category.name
            dic['budget'] = result.amount
            dic['expense'] = 0
            dic['expense_percentage'] = 0
            dic['amount_left'] = result.amount
            data.append(dic)


    # user= request.user.id
    # user_income = models.Transaction.objects.filter(user=user, transaction_type='INCOME').aggregate(Sum('amount'))['amount__sum']
    dash_active = active
    dash_active['dashboard'] = 1
    context = {'dash_active':dash_active, 'data':data}
    return render(request, 'dashboard.html',context)   

def user_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        identifier = request.POST.get('identifier')
        password = request.POST.get('password')
        
        # Check if the identifier is an email or a username
        if re.match(r"[^@]+@[^@]+\.[^@]+", identifier):
            try:
                user = models.User.objects.get(email=identifier)
                username = user.username
            except models.User.DoesNotExist:
                user = None
        else:
            username = identifier
        
        user = authenticate(username=username, password=password)
        
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('dashboard'))
            else:
                return HttpResponse("Account is inactive")
        else:
            print("Someone tried to login and failed")
            print("Identifier: {}, Password: {}".format(identifier, password))
            # raise forms.ValidationError("Invalid username or password")
            return render(request, 'login.html', {'error_message': 'Invalid username or password'})


    return render(request, 'login.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required
def add_transaction(request):
    add_transaction_active = active
    add_transaction_active['add_transaction'] = 1
    user_name= request.user.username
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('dashboard')
    else:
        form = TransactionForm()
    return render(request, 'add_transaction.html', {'form': form,'user_name': user_name, 'add_transaction_active':add_transaction_active})

@login_required
def edit_transaction(request, transaction_id):
    transaction_instance = get_object_or_404(models.Transaction, id=transaction_id, user=request.user)
    if request.method=='POST':
        form = TransactionForm(data=request.POST, instance= transaction_instance)
        if form.is_valid():
            form.save()
            return redirect ("recent_transactions")
    else:
        form =TransactionForm(instance=transaction_instance)
    return render(request, 'add_transaction.html', {'form': form})

@login_required
def recent_transactions(request):
    transactions_active = active
    transactions_active['transaction'] = 1
    current_date = datetime.now()
    current_year = current_date.year
    current_month = current_date.month
    return render(request, 'recent_transaction.html', {'current_year': current_year, 'current_month': current_month, 'transactions_active':transactions_active})

@login_required
def create_budget(request):
    budget_active = active
    budget_active['budget'] = 1
    if request.method == 'POST':
        form = BudgetForm(data= request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('dashboard')
    else:
         form = BudgetForm
    return render(request, 'create_budget.html', {'form': form, 'budget_active':budget_active})

@login_required
def set_goal(request):
    goal_active = active
    goal_active['goal'] = 1
    if request.method == 'POST':
        form = GoalForm(data= request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('dashboard')
    else:
         form = GoalForm
    
    return render(request, 'set_goal.html', {'form': form, 'goal_active':goal_active})

def generate_colors(n):
    colors=[]
    for i in range(n):
        hue = (i * 360 // n) % 360
        color = f'hsl({hue}, 70%, 50%)'
        colors.append(color)
    return colors

@login_required
def get_expenses(request):
    now = datetime.now()
    current_month = now.month
    current_year = now.year
    expenses = models.Transaction.objects.filter(user= request.user,
                                                 transaction_type='EXPENSE',
                                                 date__year=current_year,
                                                 date__month=current_month).values('category__name').annotate(total_amount=Sum('amount'))
    labels=[]
    values=[]
    colors=generate_colors(len(expenses))
    for expense in expenses:
        labels.append(expense['category__name'])
        values.append(expense['total_amount'])
    data={
        'labels': labels,
        'values': values,
        'colors': colors
    }
    return JsonResponse(data)

@login_required
def get_transactions(request, year, month):
    transactions = models.Transaction.objects.filter(date__year=year, date__month=month,user=request.user)
    transaction_list = []
    for transaction in transactions:
        transaction_list.append({
            'id': transaction.id,
            'date': transaction.date.strftime('%d-%m-%y'),
            'amount': transaction.amount,
            'type': transaction.get_transaction_type_display(),
            'category': transaction.category.name,
        })
    return JsonResponse({'transactions': transaction_list})


# @login_required
# def calculate_budget(request):
    

