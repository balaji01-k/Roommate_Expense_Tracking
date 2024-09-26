from django.shortcuts import render, redirect
from django.views import View
from our_expense import models
from django.db.models import Sum
from django.utils import timezone
from django.db.models.functions import TruncMonth
from django.utils.dateparse import parse_date
# Create your views here.


class Dashboard(View):
    def get(self, request):
        selected_month = request.GET.get('month')
        if not selected_month:
            current_date = timezone.now()
            default_month = 9
            default_year = current_date.year
            selected_month = f'{default_year}-{default_month:02d}'
            year, month = default_year, default_month
            
        else:
            year, month = map(int, selected_month.split('-'))  

        roommate_count = 0
        total_expense_this_month = 0
        last_pub_bill_amount = 0
        data_table = []
     
        if month == 9:
            roommate_count = models.AddRoommateModel.objects.count()
            expense_data = models.ExpenseModel.objects.filter(
                date__year=year, date__month=month
            ).aggregate(total_expense=Sum('price'))

            total_expense_this_month = expense_data['total_expense'] or 0

            pub_bill = models.PUB_BillModel.objects.order_by('Current_EB_Date').first()
            last_pub_bill_amount = pub_bill.total_amt if pub_bill else 0

          
            roommates = models.AddRoommateModel.objects.all()
            pub_bill_per_person = last_pub_bill_amount / roommates.count() if roommates.exists() else 0

            for roommate in roommates:
                total_purchase = models.ExpenseModel.objects.filter(
                    name=roommate, date__year=year, date__month=month
                ).aggregate(Sum('price'))['price__sum'] or 0

                food_expense_per_person = total_expense_this_month / roommates.count() if roommates.exists() else 0
                total_amount = food_expense_per_person + pub_bill_per_person
                balance = total_amount - total_purchase

                data_table.append({
                    'name': roommate.name,
                    'food_expense': f"${food_expense_per_person:.2f}",
                    'pub_bill': f"${pub_bill_per_person:.2f}",
                    'total_amount': f"${total_amount:.2f}",
                    'purchase_amount': f"${total_purchase:.2f}",
                    'balance': f"${balance:.2f}",
                })

        datas = {
            'roommate_count': roommate_count,
            'total_expense_this_month': f"${total_expense_this_month:.2f}",
            'last_pub_bill_amount': f"${last_pub_bill_amount:.2f}",
            'data_table': data_table,
            'selected_month': selected_month,  }
        return render(request, 'dashboard.html', datas)

    
# def basetmp(request):
#     return render(request, 'base.html')

# AddRoommateView
class AddRoommateView(View):
    def get(self, request):
        add_roommate_g = models.AddRoommateModel.objects.all()
        datas = {
            'add_roommate_g': add_roommate_g,
        }
        return render(request, 'addroommate.html', datas)
    
    def post(self, request):
        name = request.POST.get('name')
        phone = request.POST.get('phone_number')
        joined_date = request.POST.get('joined_date')
        add_roommate_p = models.AddRoommateModel(name=name, phone=phone, joined_date=joined_date)
        add_roommate_p.save()
        return redirect('/addroommate')
    
def EditRoommate(request, id):
    edit_roommate = models.AddRoommateModel.objects.get(id=id)
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone_number')
        joined_date = request.POST.get('joined_date')
        
        edit_roommate.name = name
        edit_roommate.phone = phone
        edit_roommate.joined_date = joined_date
        edit_roommate.save()
        
        return redirect('/addroommate')
    
    datas = {
        'edit_roommate': edit_roommate
    }
    return render(request, 'addroommate.html', datas)

    
def DeleteRoommate(request, id):
    delete_roommate = models.AddRoommateModel.objects.get(id=id)
    delete_roommate.delete()
    return redirect('/addroommate')

    
# ExpenseView
class ExpenseView(View):
    def get(self, request):
        expense_g = models.ExpenseModel.objects.all()
        add_roommate_g = models.AddRoommateModel.objects.all()
        current_date = timezone.now()
        total_expense_this_month = models.ExpenseModel.objects.filter(
            date__year=current_date.year, date__month=current_date.month
        ).aggregate(Sum('price'))['price__sum'] or 0
        datas = {
            'expense_g': expense_g,
            'add_roommate_g': add_roommate_g,
            'total_expense_this_month': total_expense_this_month,
        }
        return render(request, 'expense.html', datas) 
    
    def post(self, request):
        name = request.POST.get('name')
        get_name = models.AddRoommateModel.objects.get(id=name)
        date = request.POST.get('date')
        item_name = request.POST.get('item_name')
        price = request.POST.get('price')
        expense_p = models.ExpenseModel(name=get_name, date=date, item_name=item_name, price=price)
        expense_p.save()
        return redirect('/expense')
    
def EditExpense(request, id):
    edit_expense = models.ExpenseModel.objects.get(id=id)
    add_roommate_g = models.AddRoommateModel.objects.all()
    
    if request.method == 'POST':
        name = request.POST.get('name')
        date = request.POST.get('date')
        item_name = request.POST.get('item_name')
        price = request.POST.get('price')
        
        roommate_name = models.AddRoommateModel.objects.get(id=name)
         
        edit_expense.name = roommate_name
        edit_expense.date = date
        edit_expense.item_name = item_name
        edit_expense.price = price
        edit_expense.save()
        
        return redirect('/expense')
    
    datas = {
        'edit_expense': edit_expense,
        'add_roommate_g': add_roommate_g,
    }
    print(datas)
    return render(request, 'expense.html', datas)
    
def DeleteExpense(request, id):
    delete_expense = models.ExpenseModel.objects.get(id=id)
    delete_expense.delete()
    return redirect('/expense')    


# CalculateExpenseView
class CalculateExpenseView(View):
    def get(self, request):
        return self.render_expense_view(request)

    def post(self, request):
        return self.render_expense_view(request)

    def render_expense_view(self, request):
        expense_data = models.ExpenseModel.objects.annotate(
            month=TruncMonth('date')
        ).values('month').annotate(total_expense=Sum('price'))

        total_expense_this_month = 0
        month = None

        if expense_data.exists():
            latest_month_data = expense_data.latest('month')
            month = latest_month_data['month']
            total_expense_this_month = latest_month_data['total_expense']

        roommates = models.AddRoommateModel.objects.all()
        num_roommates = roommates.count()

      
        days_present_list = []
        
     
        for i in range(num_roommates):
            days_present = request.POST.get(f'days_present_{i}', 30)  
            days_present_list.append(int(days_present))

        data_list = []
        for i, roommate in enumerate(roommates):
            days_present = days_present_list[i]
            per_day_expense = total_expense_this_month / 30 if 30 else 0 
            per_person_per_day = per_day_expense / num_roommates if num_roommates else 0
            amount_to_pay = per_person_per_day * days_present

            data_list.append({
                'name': roommate.name,
                'month': month.strftime('%b, %Y') if month else 'No data',
                'per_day': f"${per_person_per_day:.2f}",
                'no_of_days': days_present,
                'amount_to_pay': f"${amount_to_pay:.2f}",
            })

        datas = {
            'data_list': data_list,
            'total_expense_this_month': f"${total_expense_this_month:.2f}",
        }
        return render(request, 'calculate_expense.html', datas)



class PUB_BillView(View):
    def get(self, request):
        pub_bill = models.PUB_BillModel.objects.all()
        datas={
            'pub_bill': pub_bill
        }
        return render(request, 'PUB_bill.html', datas) 
    
    def post(self, request):
        Previous_EB_Date = request.POST.get('Previous_EB_Date')
        Previous_month_EB_Total_Reading = request.POST.get('Previous_month_EB_Total_Reading')
        Current_EB_Date = request.POST.get('Current_EB_Date')
        Current_month_EB_Total_Reading = request.POST.get('Current_month_EB_Total_Reading')
        EB_Unit_Cost = request.POST.get('EB_Unit_Cost')
        Refuse_Removal_Amount = request.POST.get('Refuse_Removal_Amount')
        Water_Utility_Amount = request.POST.get('Water_Utility_Amount')
        GST = request.POST.get('GST')
        
        Previous_EB_Date = parse_date(Previous_EB_Date) if Previous_EB_Date else None
        Current_EB_Date = parse_date(Current_EB_Date) if Current_EB_Date else None
        
        total_units = float(Current_month_EB_Total_Reading) - float(Previous_month_EB_Total_Reading)
        total = (total_units * float(EB_Unit_Cost)) + float(Refuse_Removal_Amount) + float(Water_Utility_Amount)
        add_GST = (total * float(GST)) / 100
        total = total + add_GST
        
        pub_bill = models.PUB_BillModel(Previous_EB_Date=Previous_EB_Date, Previous_month_EB_Total_Reading=Previous_month_EB_Total_Reading,
                                        Current_EB_Date=Current_EB_Date,Current_month_EB_Total_Reading=Current_month_EB_Total_Reading,
                                        EB_Unit_Cost=EB_Unit_Cost, Refuse_Removal_Amount=Refuse_Removal_Amount,
                                        Water_Utility_Amount=Water_Utility_Amount, GST=GST, 
                                        Total_Units=total_units, total_amt=total)
        pub_bill.save()
        return redirect('/PUB_bill')
    
def EditPUB_Bill(request, id):
    edit_PUB_bill = models.PUB_BillModel.objects.get(id=id)
    print(request.method, request.POST)
    if request.method == 'POST':
        Previous_EB_Date = request.POST.get('Previous_EB_Date')
        Previous_month_EB_Total_Reading = request.POST.get('Previous_month_EB_Total_Reading')
        Current_EB_Date = request.POST.get('Current_EB_Date')
        Current_month_EB_Total_Reading = request.POST.get('Current_month_EB_Total_Reading')
        EB_Unit_Cost = request.POST.get('EB_Unit_Cost')
        Refuse_Removal_Amount = request.POST.get('Refuse_Removal_Amount')
        Water_Utility_Amount = request.POST.get('Water_Utility_Amount')
        GST = request.POST.get('GST')
        
        edit_PUB_bill.Previous_EB_Date = Previous_EB_Date
        edit_PUB_bill.Previous_month_EB_Total_Reading = Previous_month_EB_Total_Reading
        edit_PUB_bill.Current_EB_Date = Current_EB_Date
        edit_PUB_bill.Current_month_EB_Total_Reading = Current_month_EB_Total_Reading
        edit_PUB_bill.EB_Unit_Cost = EB_Unit_Cost
        edit_PUB_bill.Refuse_Removal_Amount = Refuse_Removal_Amount
        edit_PUB_bill.Water_Utility_Amount = Water_Utility_Amount
        edit_PUB_bill.GST = GST
        edit_PUB_bill.save()
        
        return redirect('/PUB_bill')
    
    datas = {
        'edit_PUB_bill': edit_PUB_bill
    }
    return render(request, 'PUB_bill.html', datas)
    
def DeletePUB_Bill(request, id):
    delete_PUB_bill = models.PUB_BillModel.objects.get(id=id)
    delete_PUB_bill.delete()
    return redirect('/PUB_bill')      