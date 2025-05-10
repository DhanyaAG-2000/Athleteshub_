from django.contrib import admin

from .models import Transactions,Payment

# Register your models here.

admin.site.register(Payment)
admin.site.register(Transactions)


