import re
import datetime

from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpRequest
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage, TextMessage, FlexSendMessage, ImageSendMessage, PostbackEvent, \
    BubbleContainer, ImageComponent, BoxComponent, TextComponent, ButtonComponent, URIAction, SpacerComponent, \
    CarouselContainer, LocationMessage, TemplateSendMessage, MessageAction, ConfirmTemplate, PostbackAction, QuickReply, \
    QuickReplyButton, FillerComponent
from about_nutrition_chatbot import settings
from nutritionweb.models import lineUser,userFood
from .models import Chat
from chatbot.recipeMsg.recipeMsg import recipeTypeReply,findRecipe
from chatbot.userMsg.userMsg import creat_user_flex_message
from chatbot.locationMsg.locationMsg import creat_gym_flex_message,create_location_flex_message,findGym
from chatbot.detectIntent.detectMsgIntent import detectMsgIntent
from chatbot.analysis.analysis import drawPie_kcal,calculate_Tdee,drawPie_three,get_week,draw_week,tdee_flexMessage,what_is_tdee,exercise_frq,analysisTemplate
import requests.packages.urllib3
import logging
import json
# Create your views here.

#line bot token and channel secret
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(settings.LINE_CHANNEL_SECRET)
host=settings.host

logger = logging.getLogger("django")





@csrf_exempt
def callback(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        try:
            handler.handle(body, signature)

        except InvalidSignatureError:
            return HttpResponseBadRequest()
        return HttpResponse()
    else:
        return HttpResponseBadRequest()

@handler.add(event=PostbackEvent)
def handle_postback(event:PostbackEvent):#處理postback事件

    data=str(event.postback.data).split("&")
    query=data[0]
    userId=event.source.user_id
    profile = line_bot_api.get_profile(userId)
    if query =='action=userData':#點選使用者紀錄回傳flexMessage
        if lineUser.objects.filter(userId=userId).exists():
            line_bot_api.reply_message(event.reply_token, creat_user_flex_message(profile))
        else:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="查詢資料錯誤 重新加入吧!!!"))
            line_bot_api.link_rich_menu_to_user(event.source.user_id,"richmenu-c1aa8fe9f8e87ea89c9f4cda38cfaaf9")
    elif query =='action=mainMenu':#跳回主richMenu
        line_bot_api.link_rich_menu_to_user(userId, "richmenu-e653dbdf393102df174783d3ec5eb3ff")
    elif query == 'action=recordMenu':  #紀錄richMenu
        line_bot_api.link_rich_menu_to_user(userId, "richmenu-1d661deca5e0c683e96ba1f1310ed827")
    elif query =='action=diet_or_cost':#花費飲食紀錄web
        uri ='https://liff.line.me/1653914885-DLXGeq3b'
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=uri))
    elif query =='action=history':#歷史紀錄web
        today = str(datetime.datetime.now().year) + "-" + str(datetime.datetime.now().month) + "-" + str(datetime.datetime.now().day)
        line_bot_api.reply_message(event.reply_token, history_flexMessage(userId,today))
    elif query =='action=nearby_Gym':#附近健身房flexMessage
        line_bot_api.reply_message(event.reply_token, create_location_flex_message())
    elif query =='action=recipe':#食譜flexMessage
        line_bot_api.reply_message(event.reply_token,recipeTypeReply())
    elif query == 'action=analyze':  # 分析msg
        line_bot_api.reply_message(event.reply_token,analysisTemplate())
    elif query == "action=reject":
        params=str(event.postback.data).split("action=reject&")[1]
        text=params.split("&intent=")[0].split("text=")[1] #get text=msg content
        intent=params.split("&intent=")[1] #get intent content
        unit=Chat.objects.create(chat_user=userId,chat_text=text,chat_wrong_intent=intent,chat_isCorrect=False)
        unit.save()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="不好意思，麻煩請你再更清楚告訴我你想做什麼。"))
    elif query == 'c_recipe':
        line_bot_api.reply_message(event.reply_token, findRecipe(query))
    elif query == 'b_recipe':
        line_bot_api.reply_message(event.reply_token, findRecipe(query))
    elif query == 'f_recipe':
        line_bot_api.reply_message(event.reply_token, findRecipe(query))
    elif query == 'p_recipe':
        line_bot_api.reply_message(event.reply_token, findRecipe(query))
    elif query == 'a_recipe':
        line_bot_api.reply_message(event.reply_token, findRecipe(query))
    elif query =='tdee':
        if lineUser.objects.filter(userId=userId).exists():
            line_bot_api.reply_message(event.reply_token, exercise_frq())
        else:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="不好意思，您還沒加入蓋營養唷~"))
    elif query =='rarely':
        line_bot_api.reply_message(event.reply_token,calculate_Tdee(userId,query))
    elif query =='seldom':
        line_bot_api.reply_message(event.reply_token,calculate_Tdee(userId,query))
    elif query =='often':
        line_bot_api.reply_message(event.reply_token,calculate_Tdee(userId,query))
    elif query =='alotof':
        line_bot_api.reply_message(event.reply_token,calculate_Tdee(userId,query))
    elif query =='everyday':
        line_bot_api.reply_message(event.reply_token,calculate_Tdee(userId,query))
    elif query=='what_is_tdee':
        line_bot_api.reply_message(event.reply_token,what_is_tdee())


@handler.add(event=MessageEvent, message=TextMessage)
def handle_message(event: MessageEvent):
    message = TextSendMessage(text=event.message.text)
    user_id = event.source.user_id
    try:
        strin = "新增個人資料\n使用者編號:" + str(user_id)
        matchObjTotal = re.match(r"^analyse_kacl[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]", message.text)
        matchObjThree = re.match(r"^analyse_three[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]", message.text)
        matchObjWeek = re.match(r"^analyse_week[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]", message.text)
        print((event.message.text == strin))
        if message.text == strin:
            if lineUser.objects.filter(userId=user_id).exists():  # 檢查資料庫是否存在使用者資料
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text="已成功加入囉~"))
                profile = line_bot_api.get_profile(user_id)
                line_bot_api.push_message(user_id, creat_user_flex_message(profile))
                line_bot_api.link_rich_menu_to_user(user_id, "richmenu-e653dbdf393102df174783d3ec5eb3ff")
                print(event.message.text)
        elif matchObjTotal:
            date = re.split("analyse_kacl", message.text)[1]
            total_kcal = drawPie_kcal(user_id, date)

            line_bot_api.reply_message(event.reply_token, ImageSendMessage(
                original_content_url=host + "/Media/" + user_id + date + "foodkcalpercent.png",
                preview_image_url=host + "/Media/" + user_id + date + "foodkcalpercent.png"))
            line_bot_api.push_message(user_id, TextSendMessage(text="📢您今日攝取總熱量為\n" + str(total_kcal) + "大卡"))
        elif matchObjThree:
            date = re.split("analyse_three", message.text)[1]
            drawPie_three(user_id, date)
            line_bot_api.reply_message(event.reply_token, ImageSendMessage(
                original_content_url=host + "/Media/" + user_id + date + "threepercent.png",
                preview_image_url=host + "/Media/" + user_id + date + "threepercent.png"))
            line_bot_api.push_message(user_id,
                                      TextSendMessage(text="📢每日建議攝取比例\n🍳蛋白質10-20%\n🍔脂肪20-30%\n🍚碳水化合物50-60%"))
        elif matchObjWeek:
            date = re.split("analyse_week", message.text)[1]
            datetime_list=get_week(date)
            weekDay_list = list()
            for i in datetime_list:
                weekDay_list.append(str(i.date()))
            draw_week(user_id,weekDay_list)
            line_bot_api.push_message(user_id, ImageSendMessage(
                original_content_url=host + "/Media/" + user_id +  weekDay_list[0]+"-" +weekDay_list[6]+ "total_kcal.png",
                preview_image_url=host + "/Media/" + user_id +  weekDay_list[0]+"-" +weekDay_list[6]+ "total_kcal.png"))
        elif event.message.text == "/help":
            msgText="💡小技巧：\n您可以直接輸入按鈕名稱\n例如：\n輸入 紀錄飲食 \n輸入 健身房"
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=msgText))
        else:
            intentResult = detectMsgIntent(event.message.text)
            intent = intentResult["result"]["metadata"]["intentName"]
            responesText = intentResult["result"]["fulfillment"]["speech"]
            chatText=event.message.text
            rejectData="action=reject&text="+chatText+"&intent="+intent
            if intent == "recordDiet":  # record diet
                replyMsg = TemplateSendMessage(alt_text=intent, template=ConfirmTemplate(
                    title='recordDietConfirm',
                    text=responesText,
                    actions=[
                        URIAction(
                            label="是",
                            uri="https://liff.line.me/1653914885-DLXGeq3b"  # 紀錄飲食頁面
                        ),
                        PostbackAction(
                            label="不是",
                            data=rejectData,

                        )
                    ])
                                               )
                line_bot_api.reply_message(event.reply_token, replyMsg)
            elif intent == "analysis":  # analysis
                replyMsg = TemplateSendMessage(alt_text=intent, template=ConfirmTemplate(
                    title='AnalysisConfirm',
                    text=responesText,
                    actions=[
                        PostbackAction(
                            label="是",  # 確認是否要分析
                            data="action=analyze"
                        ),
                        PostbackAction(
                            label="不是",
                            data=rejectData,
                        )
                    ])
                                               )
                line_bot_api.reply_message(event.reply_token, replyMsg)
            elif intent == "dietHistory":  # see diet history
                replyMsg = TemplateSendMessage(alt_text=intent, template=ConfirmTemplate(
                    title='DietHistoryConfirm',
                    text=responesText,
                    actions=[
                        PostbackAction(
                            label="是",  # 確認是否要查看歷史紀錄
                            data="action=history"
                        ),
                        PostbackAction(
                            label="不是",
                            data=rejectData,
                        )
                    ])
                                               )
                line_bot_api.reply_message(event.reply_token, replyMsg)
            elif intent == "recordUserInfo":  # record user's information
                replyMsg = TemplateSendMessage(alt_text=intent, template=ConfirmTemplate(
                    title='UserInfoConfirm',
                    text=responesText,
                    actions=[
                        PostbackAction(
                            label="是",
                            data="action=userData"  # 紀錄頁面
                        ),
                        PostbackAction(
                            label="不是",
                            data=rejectData,
                        )
                    ])
                                               )
                line_bot_api.reply_message(event.reply_token, replyMsg)
            elif intent == "findGym":  # find nearest gym
                replyMsg = TemplateSendMessage(alt_text=intent, template=ConfirmTemplate(
                    title='findGymConfirm',
                    text=responesText,
                    actions=[
                        PostbackAction(
                            label="是",  # 確認是否要尋找健身房
                            data="action=nearby_Gym"
                        ),
                        PostbackAction(
                            label="不是",
                            data=rejectData
                        )
                    ])
                                               )
                line_bot_api.reply_message(event.reply_token, replyMsg)
            elif intent == "recipe":
                replyMsg = TemplateSendMessage(alt_text=intent, template=ConfirmTemplate(
                    title='RankConfirm',
                    text=responesText,
                    actions=[
                        PostbackAction(
                            label="是",  # 確認是否要推薦食譜
                            data="action=recipe"
                        ),
                        PostbackAction(
                            label="不是",
                            data=rejectData,
                        )
                    ])
                                               )
                line_bot_api.reply_message(event.reply_token, replyMsg)
            elif intent == "welcome":  # reply welcom msg
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=responesText))
            else:  # otherwise
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=responesText))
    except LineBotApiError as e:
        print(e)
@handler.add(event=MessageEvent, message=LocationMessage) #find gym , and reply gym flex message
def handle_location_message(event: MessageEvent):
    user_id = event.source.user_id
    try:
        user_location_latitude=event.message.latitude
        user_location_longitude = event.message.longitude
        print(user_location_latitude,user_location_longitude)
        line_bot_api.reply_message(event.reply_token,findGym(str(user_location_latitude),str(user_location_longitude)))
    except LineBotApiError as e:
          print(e)

def history_flexMessage(userid,date):
    uri = host + "/nutritionweb/history/" + userid+"/look/0"
    results = userFood.objects.filter(userId=userid,date=date)
    length=len(results)
    def item_loop(length):
        item_list=list()
        iniitem = BoxComponent(

            background_color="#EA8244",
            layout='baseline',
            contents=[
                TextComponent(
                    type="text",
                    text="您於今日還沒有紀錄喔!!!!",
                    color="#FFFFFF",
                    size="xl",
                    wrap=True,
                    align="center",
                ),
            ]
        )
        if length == 0:
            item_list.append(iniitem)
        elif length>10:
            item = BoxComponent(
                background_color="#EA8244",
                layout='baseline',
                contents=[
                    TextComponent(
                        type="text",
                        text="您紀錄太多筆無法喔，可以點擊下方按鈕查看紀錄",
                        color="#FFFFFF",
                        size="xl",
                        wrap=True,
                        align="center",
                    ),
                ]
            )
        else:
            for result in results:
                item = BoxComponent(
                    background_color="#EA8244",
                    layout='baseline',
                        contents=[
                            TextComponent(
                                type="text",
                                text=str(result.food_name),
                                color="#FFFFFF",
                                size="xs",
                                wrap=True,
                                align="center",
                            ),
                            TextComponent(
                                type="text",
                                text=str(result.food_quantity),
                                color="#FFFFFF",
                                size="xs",
                                wrap=True,
                                align="center",
                            ),
                            TextComponent(
                                type="text",
                                text=str(result.food_power),
                                color="#FFFFFF",
                                size="xs",
                                wrap=True,
                                align="center",
                            ),
                            TextComponent(
                                type="text",
                                text=str(result.food_protein),
                                color="#FFFFFF",
                                size="xs",
                                wrap=True,
                                align="center",
                            ),
                            TextComponent(
                                type="text",
                                text=str(result.food_carbohydrate),
                                color="#FFFFFF",
                                size="xs",
                                wrap=True,
                                align="center",
                            ),
                            TextComponent(
                                type="text",
                                text=str(result.food_fat),
                                color="#FFFFFF",
                                size="xs",
                                wrap=True,
                                align="center",
                            ),
                        ]
                    )
                item_list.append(item)

        return item_list

    temp1 = item_loop(length)
    i=0
    temp=[]
    while i < 11:
        if i<len(temp1):
            temp.append(temp1[i])
        else:
            temp.append(BoxComponent(background_color="#EA8244",layout='baseline',contents=[FillerComponent(flex=0)]))
        i+=1
    container = BubbleContainer(
        size='giga',
        body=BoxComponent(
            layout='vertical',
            background_color="#2e2e2e",
            size='sm',
            contents=[
                BoxComponent(
                    layout='vertical',
                    background_color="#2e2e2e",
                    contents=[
                        TextComponent(
                            text='今日飲食紀錄🍽',
                            weight="bold",
                            size="xl",
                            style="normal",
                            decoration="none",
                            gravity="center",
                            align="center",
                            color="#ffffff",
                            offset_bottom="1.25%",
                        ),
                        BoxComponent(
                            layout='baseline',
                            background_color="#EA8244",
                            contents=[
                                TextComponent(
                                    type="text",
                                    text="食物",
                                    size="sm",
                                    align="center",
                                    weight="bold",
                                ),
                                TextComponent(
                                    type='text',
                                    text="數量",
                                    wrap=True,
                                    size="sm",
                                    align="center",
                                    weight="bold",

                                ),
                                TextComponent(
                                    type='text',
                                    text="熱量",
                                    wrap=True,
                                    size="sm",
                                    align="center",
                                    weight="bold",
                                ),
                                TextComponent(
                                    type='text',
                                    text="蛋白質",
                                    wrap=True,
                                    size="sm",
                                    align="center",
                                    weight="bold",
                                ),
                                TextComponent(
                                    type='text',
                                    text="碳水",
                                    wrap=True,
                                    size="sm",
                                    align="center",
                                    weight="bold",
                                ),
                                TextComponent(
                                    type='text',
                                    text="脂肪",
                                    wrap=True,
                                    size="sm",
                                    align="center",
                                    weight="bold",
                                )
                            ]
                        ),
                        temp[0],
                        temp[1],
                        temp[2],
                        temp[3],
                        temp[4],
                        temp[5],
                        temp[6],
                        temp[7],
                        temp[8],
                        temp[9],
                        temp[10],
                    ]
                ),
            ],
        ),
        footer=BoxComponent(
            background_color="#2e2e2e",
            layout='vertical',
            spacing='sm',
            contents=[
                ButtonComponent(
                    style="primary",
                    height="sm",
                    action=URIAction(label="點我查看更多紀錄👀",
                                     uri=uri),
                    color="#EA8244",
                    gravity="center",
                ),
                SpacerComponent(size='sm'),
            ],
            flex=0,
        )
    )



    return FlexSendMessage(alt_text="今日飲食紀錄", contents=container)