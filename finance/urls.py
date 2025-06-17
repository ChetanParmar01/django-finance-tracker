
from django.urls import include, path
from finance.views import RegisterView , DashbaordView ,TrasactionCreateView , TransactionListView , GoalCreateView , MarkGoalCompletedView , DeleteGoalView

urlpatterns = [
   path('register/' ,RegisterView.as_view(),name="register" ),
   path('' ,DashbaordView.as_view(),name="dashboard" ),
   path('transaction/add/' ,TrasactionCreateView.as_view(),name="transaction_add" ),
   path('transactions/' ,TransactionListView.as_view(),name="transaction_list" ),
   path('', include('django.contrib.auth.urls')),  # ✅ for login/logout/password views
   path('goal/add/' , GoalCreateView.as_view(),name='goal_add'),
   path('goal/<int:goal_id>/complete/', MarkGoalCompletedView.as_view(), name='mark_goal_completed'),
   path('goal/<int:goal_id>/delete/', DeleteGoalView.as_view(), name='delete_goal'),
]