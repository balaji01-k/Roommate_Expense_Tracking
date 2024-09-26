from django.db import models


class AddRoommateModel(models.Model):
    name = models.CharField(max_length=100)
    phone = models.IntegerField()
    joined_date = models.DateField()
    
class ExpenseModel(models.Model):
    name = models.ForeignKey(AddRoommateModel, on_delete=models.SET_NULL, null=True)
    date = models.DateField()
    item_name = models.CharField(max_length=300)
    price = models.IntegerField()

class PUB_BillModel(models.Model):
    Previous_EB_Date = models.DateField(null=True, blank=True)
    Previous_month_EB_Total_Reading = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    Current_EB_Date = models.DateField(null=True, blank=True)
    Current_month_EB_Total_Reading = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    EB_Unit_Cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    Refuse_Removal_Amount =models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    Water_Utility_Amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    GST = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    Total_Units = models.FloatField(null=True, blank=True) 
    total_amt = models.FloatField(null=True, blank=True)
    