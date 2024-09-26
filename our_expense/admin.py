from django.contrib import admin
from our_expense import models

admin.site.register(models.AddRoommateModel)
admin.site.register(models.ExpenseModel)
admin.site.register(models.PUB_BillModel)