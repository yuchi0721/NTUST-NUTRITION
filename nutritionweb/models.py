# coding=utf8
from django.db import models


# Create your models here.
from django.db import models


class lineUser(models.Model):
    userName = models.CharField(max_length=20, null=False)  # 使用者名稱
    userGender_choices = [('Male', 'male'), ('Female', 'female'), ]  # 性別選項
    userGender = models.CharField(choices=userGender_choices, default='Male', max_length=20)  # 性別欄位
    userWeight = models.IntegerField(null=False)  # 體重
    userHeight = models.IntegerField(null=False)  # 身高
    userAge = models.IntegerField(null=False)  # 年齡
    userId = models.CharField(max_length=128,primary_key=True)  # LINE_PROFILE_USER_ID

    def __str__(self):
        return self.userId


class Food(models.Model):
    food_id = models.AutoField(primary_key=True)  # 樣品編號
    food_name = models.CharField(max_length=100)  # 名稱
    food_power = models.FloatField(default=0.0, blank=True)  # 熱量
    food_protein = models.FloatField(default=0.0, blank=True)  # 蛋白質
    food_carbohydrate = models.FloatField(default=0.0, blank=True)  # 碳水化合物
    food_fat = models.FloatField(default=0.0, blank=True)  # 脂肪

    def __str__(self):
        return self.food_name


class userFood(models.Model):
    food_id = models.AutoField(primary_key=True)  # 樣品編號
    food_name = models.CharField(max_length=100)  # 名稱
    food_quantity = models.CharField(max_length=100)  # 數量
    food_power = models.FloatField(default=0.0, blank=True)  # 熱量
    food_protein = models.FloatField(default=0.0, blank=True)  # 蛋白質
    food_carbohydrate = models.FloatField(default=0.0, blank=True)  # 碳水化合物
    food_fat = models.FloatField(default=0.0, blank=True)  # 脂肪
    date = models.DateField(auto_now_add=False)
    userId = models.CharField(max_length=128, null=False)  # LINE_PROFILE_USER_ID

    def __str__(self):
        return self.food_name




