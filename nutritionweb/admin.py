# coding=utf8
from django.contrib import admin
from nutritionweb.models import lineUser,Food,userFood


# Register your models here.
@admin.register((lineUser))
class lineUserAdmin(admin.ModelAdmin):
    list_display = ['userName', 'userGender', 'userHeight', 'userWeight', 'userAge', 'userId']
    list_filter = ['userName', 'userGender']
    search_fields = ['userName']
    ordering = ['userId']

@admin.register((Food))
class FoodAdmin(admin.ModelAdmin):
    list_display = ['food_name']
    ordering = ['food_id']

@admin.register((userFood))
class userFoodAdmin(admin.ModelAdmin):
    list_display = ['userId','food_name','date']
    search_fields = ['userId']
    ordering = ['userId','date']

