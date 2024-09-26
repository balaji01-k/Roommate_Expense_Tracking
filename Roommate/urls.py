"""
URL configuration for Roommate project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from our_expense import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', views.Dashboard.as_view()),
    
    # path('base', views.basetmp),
    
    # AddRoommate
    path('addroommate', views.AddRoommateView.as_view()),
    path('edit-roommate/<int:id>', views.EditRoommate),
    path('delete-roommate/<int:id>', views.DeleteRoommate),
    
    # Expense
    path('expense/', views.ExpenseView.as_view()),
    path('edit-expense/<int:id>', views.EditExpense),
    path('delete-expense/<int:id>', views.DeleteExpense),
    
    # CalculateExpense
    path('calculate_expense', views.CalculateExpenseView.as_view()),
    
    # PUB_Bill
    path('PUB_bill', views.PUB_BillView.as_view()),
    path('edit-PUB_bill/<int:id>', views.EditPUB_Bill),
    path('delete-PUB_bill/<int:id>', views.DeletePUB_Bill),

]

