from django.contrib import admin
from .models import Chat
from import_export.admin import ImportExportModelAdmin
# Register your models here.


# @admin.register(Food)
# class FoodAdmin(ImportExportModelAdmin):
#     pass

@admin.register(Chat)
class ChatAdmin(ImportExportModelAdmin):
    list_display = ['chat_text','chat_wrong_intent','chat_date']
