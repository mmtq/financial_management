from django.urls import path
from . import views
from django.conf.urls.static import static
from financial_management import settings

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register),
    path('login/', views.user_login),
    path('logout/', views.user_logout),
    path('dashboard/', views.dashboard,name='dashboard'),
    path('add-transaction/', views.add_transaction),
    path('create-budget/', views.create_budget),
    path('set-goal/', views.set_goal),
    path('edit-transaction/<int:transaction_id>/', views.edit_transaction, name='edit_transaction'),
    path('recent-transactions/', views.recent_transactions, name='recent_transactions'),
    path('get_transactions/<int:year>/<int:month>/', views.get_transactions, name='get_transactions'),
    path('get_expenses/', views.get_expenses, name='get_expenses'),
    # path('get_budget/', views.calculate_budget, name='get_budget'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])


