from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.Item)
admin.site.register(models.Sr)
admin.site.register(models.Customer)
admin.site.register(models.Supplier)
admin.site.register(models.SaleItem)
admin.site.register(models.Memo)
admin.site.register(models.PurchaseItem)
admin.site.register(models.PurchaseMemo)
