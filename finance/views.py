from pyexpat.errors import messages
from django.shortcuts import render, redirect
from django.views import View
from finance.forms import RegisterForm ,TransactionForm , GoalForm
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from finance.models import Transaction , Goal
from django.db.models import Sum
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404



class RegisterView(View):
    def get(self, request, *args, **kwargs):
        form = RegisterForm()
        return render(request, 'finance/register.html', {'form': form})
    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # login(request, user) #to login the user directly after registration
            return redirect('/accounts/login/?registered=true')
        return render(request, 'finance/register.html', {'form': form})
    
class DashbaordView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        transactions = Transaction.objects.filter(user=request.user).order_by('-date')[:5]
        goals = Goal.objects.filter(user=request.user)

        total_income = Transaction.objects.filter(
            user=request.user, transaction_type='Income'
        ).aggregate(Sum('amount'))['amount__sum'] or 0

        total_expense = Transaction.objects.filter(
            user=request.user, transaction_type='Expense'
        ).aggregate(Sum('amount'))['amount__sum'] or 0

        net_saving = total_income - total_expense

        for goal in goals:
            if goal.target_amount and goal.target_amount > 0:
                progress = (goal.current_amount / goal.target_amount) * 100
                goal.progress_percent = round(progress, 2)

                if goal.completed:
                    goal.status_message = ""  # Hide message if already completed
                    goal.amount_needed = 0
                else:
                    if net_saving >= goal.target_amount:
                        goal.status_message = "✅ You can achieve this goal with your current savings!"
                        goal.amount_needed = 0
                    else:
                        goal.status_message = f"💡 You need ₹{goal.target_amount - net_saving:.2f} more to achieve this goal."
                        goal.amount_needed = round(goal.target_amount - net_saving, 2)
            else:
                goal.progress_percent = 0
                goal.status_message = "⚠️ No valid target amount set for this goal."
                goal.amount_needed = None

        context = {
            'user': request.user,
            'transactions': transactions,
            'goals': goals,
            'total_income': total_income,
            'total_expense': total_expense,
            'net_saving': net_saving,
        }

        return render(request, 'finance/dashboard.html', context)

    
class TrasactionCreateView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        form = TransactionForm()
        return render(request, 'finance/transaction_form.html',{'form':form})
    def post(self, request, *args, **kwargs):
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('dashboard')  # Replace 'home' with your actual URL name
        return render(request, 'finance/transaction_form.html', {'form': form})

class TransactionListView(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
        transaction = Transaction.objects.filter(user=request.user)
        return render(request,'finance/transaction_list.html',{'transaction':transaction})

class GoalCreateView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        form = GoalForm()
        return render(request, 'finance/goal_form.html',{'form':form})
    
    def post(self, request, *args, **kwargs):
        form = GoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            return redirect('dashboard')  # Replace 'home' with your actual URL name
        return render(request, 'finance/goal_form.html', {'form': form})
    
class MarkGoalCompletedView(LoginRequiredMixin, View):
    def post(self, request, goal_id):
        goal = Goal.objects.get(id=goal_id, user=request.user)
        goal.completed = True
        goal.save()
        return redirect('dashboard')  # 🔁 redirect to dashboard

class DeleteGoalView(LoginRequiredMixin, View):
    def post(self, request, goal_id):
        goal = get_object_or_404(Goal, id=goal_id, user=request.user)
        goal.delete()
        return redirect('dashboard')   
