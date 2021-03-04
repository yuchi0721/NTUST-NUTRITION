import datetime
import sys
import matplotlib.pyplot as plt
from linebot.models import TextSendMessage, FlexSendMessage, QuickReply, QuickReplyButton, PostbackAction

from about_nutrition_chatbot import settings
from nutritionweb.models import userFood,lineUser
from matplotlib.font_manager import FontProperties
# font = FontProperties(fname="STHeiti Medium.ttc",size=12)
host=settings.host
def exercise_frq():
    q_reply = TextSendMessage(
        text='請問您的運動頻率',
        quick_reply=QuickReply(
            items=[
                QuickReplyButton(
                    action=PostbackAction(label="我就是不運動", data="rarely")
                ),
                QuickReplyButton(
                    action=PostbackAction(label="一週一天", data="seldom")
                ),
                QuickReplyButton(
                    action=PostbackAction(label="一週三天", data="often")
                ),
                QuickReplyButton(
                    action=PostbackAction(label="一週5天", data="alotof")
                ),
                QuickReplyButton(
                    action=PostbackAction(label="天天運動乖寶寶", data="everyday")
                ),
            ]

        )
    )
    return q_reply
def analysisTemplate():
    msg=FlexSendMessage(alt_text="分析選項",contents={
  "type": "bubble",
  "hero": {
    "type": "image",
    "url": host+"/Media/images/LOGO2.png",
      "aspectRatio":"1000:333",
      "backgroundColor":"#2e2e2e",
    "aspectMode": "cover",
    "size": "full"
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "分析📋",
        "align": "center",
        "size": "xl",
        "color": "#FFFFFF",
        "weight": "bold"
      }
    ]
  },
  "footer": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "button",
        "action": {
          "type": "uri",
          "label": "食物佔總熱量比📊",
          "uri": "https://liff.line.me/1653914885-NxVOe0ZJ"
        },
        "style": "primary",
        "margin": "sm",
        "color": "#EA8244"
      },
      {
        "type": "button",
        "action": {
          "type": "uri",
          "label": "三大營養素占總量比📊",
          "uri": "https://liff.line.me/1653914885-pVe9myRE"
        },
        "style": "primary",
        "margin": "sm",
        "color": "#EA8244"
      },
        {
            "type": "button",
            "action": {
                "type": "uri",
                "label": "當週飲食熱量分析📊",
                "uri": "https://liff.line.me/1653914885-pLwx0ZKq"
            },
            "style": "primary",
            "margin": "sm",
            "color": "#EA8244"
        }
    ]
  },
  "styles": {
    "body": {
      "backgroundColor": "#2E2E2E"
    },
    "footer": {
      "backgroundColor": "#2E2E2E"
    }
  }
}

)
    return msg
def get_week(date):
    today = datetime.datetime.strptime(date,"%Y-%m-%d")
    month = today.month
    year = today.year
    day = today.day
    weekday = today.weekday()

    start = today + datetime.timedelta(0 - weekday)
    Tue = today + datetime.timedelta(1 - weekday)
    Wed = today + datetime.timedelta(2 - weekday)
    Thu = today + datetime.timedelta(3 - weekday)
    Fri = today + datetime.timedelta(4 - weekday)
    Sat = today + datetime.timedelta(5 - weekday)
    end = today + datetime.timedelta(6 - weekday)

    start = datetime.datetime(start.year, start.month, start.day)
    Tue = datetime.datetime(Tue.year, Tue.month, Tue.day)
    Wed = datetime.datetime(Wed.year, Wed.month, Wed.day)
    Thu = datetime.datetime(Thu.year, Thu.month, Thu.day)
    Fri = datetime.datetime(Fri.year, Fri.month, Fri.day)
    Sat = datetime.datetime(Sat.year, Sat.month, Sat.day)
    end = datetime.datetime(end.year,end.month,end.day)

    return start,Tue,Wed,Thu,Fri,Sat, end

def drawPie_kcal(userId,date):

    results = userFood.objects.filter(userId=userId,date=date)
    labels = []
    size = []
    Kcal_sum = 0
    for result in results:
        labels.append(result.food_name)
        size.append(result.food_power)
        Kcal_sum += result.food_power
    plt.figure(figsize=(6, 9))
    plt.rcParams['font.family'] = ['Noto Sans CJK TC']
    plt.rcParams['axes.unicode_minus'] = False
    plt.pie(size,  # 數值
            labels=labels,  # 標籤
            autopct="%1.1f%%",  # 將數值百分比並留到小數點一位
              # 設定分隔的區塊位置
            pctdistance=0.6, # 數字距圓心的距離
            shadow=False)  # 設定陰影
    plt.axis('equal')  # 使圓餅圖比例相等
    plt.title(date+"食物佔總熱量比例")  # 設定標題及其文字大小
    plt.legend(loc="best")  # 設定圖例及其位置為最佳

    plt.savefig("Media/" +userId+date+"foodkcalpercent.png",  # 儲存圖檔
                bbox_inches='tight',  # 去除座標軸占用的空間
                pad_inches=0.0)  # 去除所有白邊
    plt.close()
    return Kcal_sum
def calculate_Tdee(userId,freq):

    result = lineUser.objects.get(userId=userId)
    gender=str(result.userGender)
    userHeight=result.userHeight
    userWeight=result.userWeight
    userAge=result.userAge
    if (gender == "Male") :
        Bmr=(13.7 * userWeight)+(5.0 * userHeight)-(6.8 * userAge)+66
        if freq=="rarely":
            tdee=round(Bmr,0)*1.2
        elif freq=="seldom":
            tdee = round(Bmr, 0) * 1.375
        elif freq == "often":
            tdee = round(Bmr, 0) * 1.55
        elif freq == "alotof":
            tdee = round(Bmr, 0) * 1.725
        elif freq == "everyday":
            tdee = round(Bmr, 0) * 1.9
    else :
        Bmr=(9.6 * userWeight)+(1.8 * userHeight)-(4.7 * userAge)+655
        if freq == "rarely":
            tdee = round(Bmr, 0) * 1.2
        elif freq == "seldom":
            tdee = round(Bmr, 0) * 1.375
        elif freq == "often":
            tdee = round(Bmr, 0) * 1.55
        elif freq == "alotof":
            tdee = round(Bmr, 0) * 1.725
        elif freq == "everyday":
            tdee = round(Bmr, 0) * 1.9
    return tdee_flexMessage(str(round(tdee,1)),str(round(Bmr,1)))

def drawPie_three(userId,date):

    results = userFood.objects.filter(userId=userId,date=date)
    fat_sum=0
    protein_sum=0
    cy_sum=0

    for r in results:
        fat_sum+= r.food_fat
        cy_sum += r.food_carbohydrate
        protein_sum += r.food_protein
    plt.figure(figsize=(6, 9))
    labels = ["蛋白質","碳水","脂肪"]
    size = [protein_sum,cy_sum,fat_sum]
    plt.rcParams['font.family'] = ['Noto Sans CJK TC']
    plt.rcParams['axes.unicode_minus'] = False
    plt.pie(size,  # 數值
            labels=labels,  # 標籤
            autopct="%1.1f%%", # 將數值百分比並留到小數點一位
            # 設定分隔的區塊位置
            pctdistance=0.6,  # 數字距圓心的距離
            shadow=False)  # 設定陰影

    plt.axis('equal')  # 使圓餅圖比例相等
    plt.title(date + "三大營養素佔總熱量比例")  # 設定標題及其文字大小
    plt.legend(loc="best")  # 設定圖例及其位置為最佳
    plt.savefig("Media/" +userId + date + "threepercent.png",
                # 儲存圖檔
                bbox_inches='tight',  # 去除座標軸占用的空間
                pad_inches=0.0)  # 去除所有白邊
    plt.close()

    print('ok')

def draw_week(userId,datelist):
    kcal_list = list()
    formatDatelist=list()
    for j in datelist:
        results = userFood.objects.filter(userId=userId,date=j)
        kcalSum=0
        if len(results)==0:
            kcal_list.append(0)
        else:
            for r in results:
                kcalSum += r.food_power
            kcal_list.append(int(kcalSum))
    print(kcal_list)
    for i in datelist:
        formatDatelist.append(i.split('2020-')[1])
    bar_width = 0.2
    data=plt.bar(formatDatelist, kcal_list,bar_width, label='總熱量(大卡)', facecolor='#9999ff')
    plt.rcParams['font.sans-serif'] = ['Noto Sans CJK TC']
    plt.title(datelist[0]+"至"+datelist[6]+  "總熱量分析", {"fontsize": 18, })  # 設定標題及其文字大小
    plt.legend(loc="best")  # 設定圖例及其位置為最佳
    def createLabels(data):
        for item in data:
            height = item.get_height()
            plt.text(
                item.get_x() + item.get_width() / 2.,
                height,
                '%d' % int(height),
                ha="center",
                va="bottom",
            )
    createLabels(data)
    plt.savefig("Media/" + userId + datelist[0]+"-"+datelist[6] + "total_kcal.png",
                # 儲存圖檔
                  # 去除座標軸占用的空間
                )  # 去除所有白邊
    plt.close()
    print('ok')

def tdee_flexMessage(tdee,bmr):
    msg=FlexSendMessage(alt_text="Tdee計算結果",contents={
  "type": "bubble",
  "hero": {
    "type": "image",
    "url": host+"/static/images/LOGO2.png",
    "aspectRatio": "1000:333",
    "aspectMode": "cover",
    "backgroundColor": "#2e2e2e",
    "size": "full"
  },
  "body": {
    "type": "box",
    "layout": "vertical",
      "backgroundColor": "#2e2e2e",
    "contents": [
      {
        "type": "text",
        "text": "計算結果",
          "color": "#FFFFFF",
        "weight": "bold",
        "size": "xl",
        "gravity": "center",
        "align": "center"
      },
      {
        "type": "box",
        "layout": "vertical",
        "margin": "lg",
        "spacing": "sm",
        "contents": [
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "TDEE（每日消耗總熱量）：",
                "color": "#FFFFFF",
                "size": "sm",
                "flex": 1,
                "wrap": True,
                "position": "relative"
              }
            ]
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                  "color": "#FFFFFF",
                "text": tdee+"(Kcal)"
              }
            ]
          },
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "BMR（基礎代謝率）：",
                "color": "#FFFFFF",
                "size": "sm",
                "flex": 1,
                "wrap": True
              }
            ]
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": bmr+"(Kcal)",
                  "color": "#FFFFFF",
              }
            ]
          }
        ]
      }
    ]
  },
  "footer": {
    "type": "box",
    "layout": "vertical",
    "spacing": "sm",
      "backgroundColor": "#2e2e2e",
    "contents": [
      {
        "type": "button",
        "style": "primary",
        "height": "sm",
        "action": {
          "type": "postback",
          "label": "按我介紹TDEE與BMR😊",
          "data": "what_is_tdee"
        },
        "color": "#EA8244"
      },
      {
        "type": "spacer",
        "size": "sm"
      }
    ],
    "flex": 0
  }
})
    return msg
def what_is_tdee():
    bmr_introdution="就是你一整天都不動\n要維持你身體的運作會消耗的最低能量\nBMR會隨著年齡跟體重的變化改變\n年紀越大->BMR下降\n體重減輕->BMR下降"
    tdee_introduction="根據你的基礎代謝率和運動程度\n推算所得出你每日會消耗的總熱量\n當你知道你攝入熱量的數值之後\n想要達到減脂的目的\nTDEE>攝入熱量\n反之你要增肌\n攝入熱量>TDEE"
    msg=FlexSendMessage(alt_text="TDEE與BMR介紹",contents={
  "type": "bubble",
  "hero": {
    "type": "image",
    "url": host+"/Media/images/LOGO2.png",
    "aspectRatio": "1000:333",
    "aspectMode": "cover",
    "backgroundColor": "#2e2e2e",
    "size": "full"
  },
  "body": {
    "type": "box",
    "layout": "vertical",
      "backgroundColor": "#2e2e2e",
    "contents": [
      {
        "type": "text",
        "text": "TDEE與BMR介紹🔍",
          "color": "#EA8244",
        "weight": "bold",
        "size": "xl",
        "gravity": "center",
        "align": "center"
      },
      {
        "type": "box",
        "layout": "vertical",
        "margin": "lg",
        "spacing": "sm",
        "contents": [
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "TDEE（每日消耗總熱量）",
                "color": "#EA8244",
                "size": "xl",
                "flex": 1,
                "wrap": True,
                "position": "relative",
                "align": "center",
                  "weight": "bold"
              }
            ]
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                  "align": "center",
                  "color": "#FFFFFF",
                  "wrap": True,
                  "size": "sm",
                "text": tdee_introduction
              }
            ]
          },
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "BMR（基礎代謝率）",
                "color": "#EA8244",
                "size": "xl",
                "flex": 1,
                "wrap": True,
                "align": "center",
                  "weight": "bold"
              }
            ]
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                  "wrap": True,
                  "align": "center",
                  "size": "sm",
                "text": bmr_introdution,
                  "color": "#FFFFFF",
              }
            ]
          }
        ]
      }
    ]
  },
  "footer": {
    "type": "box",
    "layout": "vertical",
    "spacing": "sm",
      "backgroundColor": "#2e2e2e",
    "contents": [
      {
        "type": "button",
        "style": "primary",
        "height": "sm",
        "action": {
          "type": "uri",
          "label": "開始記錄飲食吧🍽",
          "uri": "https://liff.line.me/1653914885-DLXGeq3b"
        },
        "color": "#EA8244"
      },
      {
        "type": "spacer",
        "size": "sm"
      }
    ],
    "flex": 0
  }
})
    return msg


