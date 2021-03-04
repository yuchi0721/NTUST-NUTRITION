import pymysql
from django.shortcuts import render,redirect
from django.http import HttpResponse
from datetime import datetime
from .models import lineUser,userFood,Food
from django.views.decorators.csrf import csrf_exempt
MYSQL_HOST = '140.118.9.126'
MYSQL_PORT = 32768
MYSQL_DB = 'chatbot_db'
MYSQL_USER = 'root'
MYSQL_PASS = 'password'


# Create your views here.
def choose_date_week(request):
    if request.method=="POST":
        userid = request.POST['userId']
        print(userid)
        userfooddate = userFood.objects.filter(userId=userid).values_list('date').distinct()
        datelist = list()
        j = len(userfooddate)
        for i in range(j):
            datelist.append(str(userfooddate[i][0].strftime("%Y-%m-%d")))
        isDatelistEmpty = bool(len(datelist) == 0)
    return render(request, "choose_date_week.html", locals())

def choose_date_three(request):
    if request.method=="POST":
        userid = request.POST['userId']
        print(userid)
        userfooddate = userFood.objects.filter(userId=userid).values_list('date').distinct()
        datelist = list()
        j = len(userfooddate)
        for i in range(j):
            datelist.append(str(userfooddate[i][0].strftime("%Y-%m-%d")))
        isDatelistEmpty = bool(len(datelist) == 0)

    return render(request, "choose_date_three.html", locals())

def choose_date(request):
    if request.method=="POST":
        userid = request.POST['userId']
        print(userid)
        userfooddate = userFood.objects.filter(userId=userid).values_list('date').distinct()
        datelist = list()
        j = len(userfooddate)
        for i in range(j):
            datelist.append(str(userfooddate[i][0].strftime("%Y-%m-%d")))
        isDatelistEmpty = bool(len(datelist) == 0)

    return render(request, "choose_date.html", locals())

def history(request,userId=None,mode=None,food_id=None): #歷史紀錄頁面
    if mode=="look":
        userfood_date = userFood.objects.filter(userId=userId).values_list('date').distinct()
        datelist = list()

        protein_sum = 0
        fat_sum = 0
        cy_sum = 0
        power_sum = 0
        userid = userId
        date_count = len(userfood_date)
        for i in range(date_count):
            datelist.append(str(userfood_date[i][0].strftime("%Y-%m-%d")))
        isDatelistEmpty = bool(len(datelist) == 0)
        if request.method == "POST":
            date = request.POST["date"]
            userfood = userFood.objects.filter(userId=userId, date=date)
            userfood_protein = userFood.objects.filter(userId=userId, date=date).values_list('food_protein')
            userfood_power = userFood.objects.filter(userId=userId, date=date).values_list('food_power')
            userfood_fat = userFood.objects.filter(userId=userId, date=date).values_list('food_fat')
            userfood_carbohydrate = userFood.objects.filter(userId=userId, date=date).values_list('food_carbohydrate')
            for i in range(len(userfood_protein)):
                protein_sum += userfood_protein[i][0]
            for i in range(len(userfood_power)):
                power_sum += userfood_power[i][0]
            for i in range(len(userfood_fat)):
                fat_sum += userfood_fat[i][0]
            for i in range(len(userfood_carbohydrate)):
                cy_sum += userfood_carbohydrate[i][0]
        return render(request, "history.html", locals())
    elif mode=="delete":
            food_id = food_id
            print(food_id)
            print(userFood.objects.get(food_id=food_id))
            unit=userFood.objects.filter(food_id=food_id)
            unit.delete()
            userfood_date = userFood.objects.filter(userId=userId).values_list('date').distinct()
            datelist = list()
            protein_sum = 0
            fat_sum = 0
            cy_sum = 0
            power_sum = 0
            userid = userId
            date_count = len(userfood_date)
            for i in range(date_count):
                datelist.append(str(userfood_date[i][0].strftime("%Y-%m-%d")))
            isDatelistEmpty = bool(len(datelist) == 0)
            if request.method == "POST":
                date = request.POST["date"]
                userfood = userFood.objects.filter(userId=userId, date=date)
                userfood_protein = userFood.objects.filter(userId=userId, date=date).values_list('food_protein')
                userfood_power = userFood.objects.filter(userId=userId, date=date).values_list('food_power')
                userfood_fat = userFood.objects.filter(userId=userId, date=date).values_list('food_fat')
                userfood_carbohydrate = userFood.objects.filter(userId=userId, date=date).values_list(
                    'food_carbohydrate')
                for i in range(len(userfood_protein)):
                    protein_sum += userfood_protein[i][0]
                for i in range(len(userfood_power)):
                    power_sum += userfood_power[i][0]
                for i in range(len(userfood_fat)):
                    fat_sum += userfood_fat[i][0]
                for i in range(len(userfood_carbohydrate)):
                    cy_sum += userfood_carbohydrate[i][0]
            return render(request, "history.html", locals())
    return render(request, "history.html",locals())
def about_us(request): #關於我們頁面
    return render(request, "about_us.html")
def findFood(request): #找食物頁面

    if request.method == 'POST':
        food_name = request.POST['food_name']
        try:
            food = Food.objects.get(food_name=food_name)
            print(Food.objects.get(food_name=food_name))
            return render(request, 'diet.html', locals())

        except:

            print('food Not Exist')
            return render(request, 'diet.html', locals())

    return render(request,"findfood.html")
def close(request):
    return render(request,"close.html")
def index(request): #TDEE計算機
    return render(request, 'index.html')
def check_userdata_exist(userId):  #確認使用者是否註冊
    results = connect_mysql(userId)
    userId1= len(results)
    if userId1!=0:
        return True
    else:
        return False

def connect_mysql(userId):  #連線資料庫
    global connect, cursor
    connect = pymysql.connect(host = MYSQL_HOST, port = MYSQL_PORT ,db = MYSQL_DB, user = MYSQL_USER, password = MYSQL_PASS,
            charset = 'utf8', use_unicode = True)
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM chatbot_db.nutritionweb_lineuser WHERE USERID='%s'"%(userId))
    result = cursor.fetchall()
    return result
def edit(request,userId=None,mode=None): #修改使用者資料
    if mode == "edit": #如果是由 <listAll.html> 按 編輯1 鈕
        user = lineUser.objects.get(userId=userId)  #取得要修改的資料紀錄
        return render(request,'edit.html',locals())
    elif mode =="save": #如果是由<edit.html>按submit
        user = lineUser.objects.get(userId=userId)  #取得要修改的資料紀錄
        user.userName = request.POST['userName']    #取得表單輸入資料
        user.userGender = request.POST['userGender']
        user.userAge = request.POST['userAge']
        user.userHeight = request.POST['userHeight']
        user.userWeight = request.POST['userWeight']
        user.save()
        message = "已修改"
        return render(request,'edit.html', locals())


def listall(request): #所有使用者資料
    users=lineUser.objects.all()
    return render(request,'listAll.html',locals())
@csrf_exempt
def diet(request):
    #紀錄飲食/花費頁面
    if request.method == 'POST':
        food_name = request.POST['food_name']
        food_quantity = int(request.POST['food_quantity'])
        food_power = int(float(request.POST['food_power']))
        food_protein = int(float(request.POST['food_protein']))
        food_carbohydrate = int(float(request.POST['food_carbohydrate']))
        food_fat = int(float(request.POST['food_fat']))
        date=request.POST['datepicker']
        userId = request.POST['userId']
        print(date)
        unit = userFood.objects.create(date=date,food_name=food_name, food_quantity=food_quantity, food_power=food_power * food_quantity,
                                           food_protein=food_protein* food_quantity,
                                           food_carbohydrate=food_carbohydrate* food_quantity, food_fat=food_fat* food_quantity, userId=userId)
        if not Food.objects.filter(food_name=food_name).exists():
            unit2 = Food.objects.create(food_name=food_name, food_power=food_power, food_protein=food_protein,
                                    food_carbohydrate=food_carbohydrate, food_fat=food_fat)
            unit2.save()
        unit.save()
    return render(request, 'diet.html', locals())
@csrf_exempt
def post1(request): #新增使用者頁面
    if request.method =='POST':
        userName = request.POST['userName']
        userAge = request.POST['userAge']
        userGender = request.POST['userGender']
        userHeight = request.POST['userHeight']
        userWeight = request.POST['userWeight']
        userId =request.POST['userId']
        print("from web:"+str(userId))
        
        unit = lineUser.objects.create(userName=userName, userAge=userAge, userGender=userGender,userHeight=userHeight, userWeight=userWeight,userId=userId)
        unit.save()
    return render(request,'post1.html',locals())
