import requests
import requests.packages.urllib3
import urllib3
from linebot.models import MessageEvent, TextSendMessage, TextMessage, FlexSendMessage, ImageSendMessage, PostbackEvent, \
    BubbleContainer, ImageComponent, BoxComponent, TextComponent, ButtonComponent, URIAction, SpacerComponent, \
    CarouselContainer

def create_location_flex_message():

    bubble=BubbleContainer(
        body=BoxComponent(
            layout='vertical',
            contents=[
                TextComponent(
                    text='告訴我你在哪裡呀👉👈',
                    weight='bold',
                    size='xl',
                )

            ]

        ),
        footer=BoxComponent(
            layout='vertical',
            spacing='sm',
            contents=[
                ButtonComponent(
                    style='primary',
                    height='sm',
                    action=URIAction(
                        label='送出我的位置',
                        uri='https://line.me/R/nv/location/',

                    ),
                    color="#EA8244"

                ),
                SpacerComponent(
                    size='sm'
                )
            ],
            flex=0,
        )

    )
    return FlexSendMessage(alt_text="送出位置", contents=bubble)
def creat_gym_flex_message(name,vicinity,opening_hous,rating,picture,url):
    msg=FlexSendMessage(alt_text="附近健身房",
                        contents={
  "type": "carousel",
  "contents": [
    {
      "type": "bubble",
      "hero": {
        "type": "image",
        "url": picture[0],
        "size": "full",
        "aspectRatio": "20:13",
        "aspectMode": "cover",
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "spacing": "md",
        "contents": [
          {
            "type": "text",
            "text": name[0],
            "size": "sm",
            "weight": "bold"
          },
          {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
              {
                "type": "box",
                "layout": "baseline",
                "contents": [
                  {
                    "type": "text",
                    "text": "地址：",
                    "weight": "bold",
                    "flex": 0,
                    "color": "#aaaaaa"
                  },
                  {
                    "type": "text",
                    "text": vicinity[0],
                    "size": "sm",
                    "align":"end",
                    "wrap": True,
                  }
                ]
              },
              {
                "type": "box",
                "layout": "baseline",
                "contents": [
                  {
                    "type": "text",
                    "text": "營業時間：",
                    "weight": "bold",
                    "margin": "sm",
                    "flex": 0,
                    "color": "#aaaaaa"
                  },
                  {
                    "type": "text",
                    "text": opening_hous[0],
                    "size": "sm",
                    "align": "end",
                      "wrap": True,
                  }
                ]
              },
              {
                "type": "box",
                "layout": "baseline",
                "contents": [
                  {
                    "type": "text",
                    "text": "評價：",
                    "weight": "bold",
                    "color": "#aaaaaa"
                  },
                  {
                    "type": "text",
                    "text": rating[0],
                    "align": "end",
                    "weight": "regular"
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
        "contents": [

          {
            "type": "button",
            "style": "primary",
            "color": "#2E2E2E",
            "action": {
              "type": "uri",
              "label": "Google Map",
              "uri": url[0]
            }
          }
        ]
      }
    },
    {
      "type": "bubble",
      "hero": {
        "type": "image",
        "url": picture[1],
        "size": "full",
        "aspectRatio": "20:13",
        "aspectMode": "cover",

      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "spacing": "md",
        "contents": [
          {
            "type": "text",
            "text": name[1],
            "size": "sm",
            "weight": "bold"
          },
          {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
              {
                "type": "box",
                "layout": "baseline",
                "contents": [
                  {
                    "type": "text",
                    "text": "地址：",
                    "weight": "bold",
                    "margin": "sm",
                    "flex": 0,
                    "color": "#aaaaaa"
                  },
                  {
                    "type": "text",
                    "text": vicinity[1],
                    "size": "sm",
                    "align": "end",
                      "wrap": True,
                  }
                ]
              },
              {
                "type": "box",
                "layout": "baseline",
                "contents": [
                  {
                    "type": "text",
                    "text": "營業時間：",
                    "weight": "bold",
                    "margin": "sm",
                    "flex": 0,
                    "color": "#aaaaaa"
                  },
                  {
                    "type": "text",
                    "text": opening_hous[1],
                    "size": "sm",
                    "align": "end",
                      "wrap": True,
                  }
                ]
              },
              {
                "type": "box",
                "layout": "baseline",
                "contents": [
                  {
                    "type": "text",
                    "text": "評價：",
                    "weight": "bold",
                    "color": "#aaaaaa"
                  },
                  {
                    "type": "text",
                    "text": rating[1],
                    "align": "end",
                    "weight": "regular"
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
        "contents": [

          {
            "type": "button",
            "style": "primary",
            "color": "#2E2E2E",
            "action": {
              "type": "uri",
              "label": "Google Map",
              "uri": url[1]
            }
          }
        ]
      }
    },
    {
      "type": "bubble",
      "hero": {
        "type": "image",
        "url": picture[2],
        "size": "full",
        "aspectRatio": "20:13",
        "aspectMode": "cover",

      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "spacing": "md",
        "contents": [
          {
            "type": "text",
            "text": name[2],
            "size": "sm",
            "weight": "bold"
          },
          {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
              {
                "type": "box",
                "layout": "baseline",
                "contents": [
                  {
                    "type": "text",
                    "text": "地址：",
                    "weight": "bold",
                    "margin": "sm",
                    "flex": 0,
                    "color": "#aaaaaa"
                  },
                  {
                    "type": "text",
                    "text": vicinity[2],
                    "size": "sm",
                    "align": "end",
                      "wrap": True,
                  }
                ]
              },
              {
                "type": "box",
                "layout": "baseline",
                "contents": [
                  {
                    "type": "text",
                    "text": "營業時間：",
                    "weight": "bold",
                    "margin": "sm",
                    "flex": 0,
                    "color": "#aaaaaa"
                  },
                  {
                    "type": "text",
                    "text": opening_hous[2],
                    "size": "sm",
                    "align": "end",
                      "wrap": True,
                  }
                ]
              },
              {
                "type": "box",
                "layout": "baseline",
                "contents": [
                  {
                    "type": "text",
                    "text": "評價：",
                    "weight": "bold",
                    "color": "#aaaaaa"
                  },
                  {
                    "type": "text",
                    "text": rating[2],
                    "align": "end",
                    "weight": "regular"
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
        "contents": [

          {
            "type": "button",
            "style": "primary",
            "color": "#2E2E2E",
            "action": {
              "type": "uri",
              "label": "Google Map",
              "uri": url[2]
            }
          }
        ]
      }
    },
    {
      "type": "bubble",
      "hero": {
        "type": "image",
        "url": picture[3],
        "size": "full",
        "aspectRatio": "20:13",
        "aspectMode": "cover",

      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "spacing": "md",
        "contents": [
          {
            "type": "text",
            "text": name[3],
            "size": "sm",
            "weight": "bold"
          },
          {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
              {
                "type": "box",
                "layout": "baseline",
                "contents": [
                  {
                    "type": "text",
                    "text": "地址：",
                    "weight": "bold",
                    "margin": "sm",
                    "flex": 0,
                    "color": "#aaaaaa"
                  },
                  {
                    "type": "text",
                    "text": vicinity[3],
                    "size": "sm",
                    "align": "end",
                      "wrap": True,
                  }
                ]
              },
              {
                "type": "box",
                "layout": "baseline",
                "contents": [
                  {
                    "type": "text",
                    "text": "營業時間：",
                    "weight": "bold",
                    "margin": "sm",
                    "flex": 0,
                    "color": "#aaaaaa"
                  },
                  {
                    "type": "text",
                    "text": opening_hous[3],
                    "size": "sm",
                    "align": "end",
                      "wrap": True,
                  }
                ]
              },
              {
                "type": "box",
                "layout": "baseline",
                "contents": [
                  {
                    "type": "text",
                    "text": "評價：",
                    "weight": "bold",
                    "color": "#aaaaaa"
                  },
                  {
                    "type": "text",
                    "text": rating[3],
                    "align": "end",
                    "weight": "regular"
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
        "contents": [
          {
            "type": "button",
            "style": "primary",
            "color": "#2E2E2E",
            "action": {
              "type": "uri",
              "label": "Google Map",
              "uri": url[3]
            }
          }
        ]
      }
    },
    {
      "type": "bubble",
      "hero": {
        "type": "image",
        "url": picture[4],
        "size": "full",
        "aspectRatio": "20:13",
        "aspectMode": "cover",

      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "spacing": "md",
        "contents": [
          {
            "type": "text",
            "text": name[4],
            "size": "sm",
            "weight": "bold"
          },
          {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
              {
                "type": "box",
                "layout": "baseline",
                "contents": [
                  {
                    "type": "text",
                    "text": "地址：",
                    "weight": "bold",
                    "margin": "sm",
                    "flex": 0,
                    "color": "#aaaaaa"
                  },
                  {
                    "type": "text",
                    "text": vicinity[4],
                    "size": "sm",
                    "align": "end",
                      "wrap": True,
                  }
                ]
              },
              {
                "type": "box",
                "layout": "baseline",
                "contents": [
                  {
                    "type": "text",
                    "text": "營業時間：",
                    "weight": "bold",
                    "margin": "sm",
                    "flex": 0,
                    "color": "#aaaaaa"
                  },
                  {
                    "type": "text",
                    "text": opening_hous[4],
                    "size": "sm",
                    "align": "end",
                      "wrap": True,
                  }
                ]
              },
              {
                "type": "box",
                "layout": "baseline",
                "contents": [
                  {
                    "type": "text",
                    "text": "評價：",
                    "weight": "bold",
                    "color": "#aaaaaa"
                  },
                  {
                    "type": "text",
                    "text":rating[4],
                    "align": "end",
                    "weight": "regular"
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
        "contents": [

          {
            "type": "button",
            "style": "primary",
            "color": "#2E2E2E",
            "action": {
              "type": "uri",
              "label": "Google Map",
              "uri": url[4]
            }
          }
        ]
      }
    }
  ]
}
                        )
    return msg

def findGym(latitude, longitude):
    urllib3.disable_warnings()
    locationUrl = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=" + latitude + "," + longitude + "&radius=5000&types=gym&key=["YOUR GOOGLE MAP API KEY"]"
    r = requests.get(
        locationUrl,
        verify=False)
    # 對網頁進行equest

    # print(r.status_code)

    list_of_dicts = r.json()
    name_list = list()
    vicinity_list = list()
    opening_hours_list = list()
    photo_pic_url_list = list()
    rating_list = list()
    url_list = list()
    j = 0
    # print(type(r))
    # print(type(list_of_dicts))
    for i in list_of_dicts["results"]:
        if j < 5:
            pid = i["place_id"]  # 店的placeID
            dr = requests.get(
                "https://maps.googleapis.com/maps/api/place/details/json?place_id=" + pid + "&language=zh-TW&fields=name,vicinity,photos,rating,url,opening_hours&key=["YOUR GOOGLE MAP API KEY"]",
                verify=False)
            place_details = dr.json()
            # ↑抓個別detail資料
            name = place_details["result"].get("name", "沒有名稱")  # 店名
            name_list.append(name)
            vicinity = place_details["result"].get("vicinity", "沒有地址")  # 地址
            vicinity_list.append(vicinity)
            # 營業時間
            try:
                opening_hours = place_details["result"].get("opening_hours").get("weekday_text", "no time")
            except:
                opening_hours = "no time"
            if opening_hours == "no time":
                opening = "沒有營業時間"
            else:
                opening = opening_hours[0] + "\n" + opening_hours[1] + "\n" + opening_hours[2] + "\n" + opening_hours[
                    3] + "\n" + opening_hours[4] + "\n" + opening_hours[5] + "\n" + opening_hours[6]
            opening_hours_list.append(opening)
            # 圖片網址
            try:
                photos_reference = place_details["result"]["photos"][0].get("photo_reference", "沒有照片")
            except:
                photos_reference = "none"
            if photos_reference == "none":
                photo_pic_url = "https://helloyishi.com.tw/wp-content/uploads/2019/01/%E9%81%8B%E5%8B%95%E5%A5%BD%E8%99%95.jpg"
            else:
                photo_pic_url = "https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference=" + photos_reference + "&key=["YOUR GOOGLE MAP API KEY"]"
            photo_pic_url_list.append(photo_pic_url)
            rating = int(place_details["result"].get("rating", "0"))  # 評價
            rating_list.append(str(rating) + "顆星")
            url = place_details["result"].get("url", "沒有網址")  # 地圖網址
            url_list.append(url)
            # print("店名:", name, "地址:", vicinity, "營業時間:", opening, "照片ref", photo_pic_url, "評價", rating, "網址", url)
            j += 1
        else:
            break

    # print(name_list, vicinity_list, opening_hours_list, photo_pic_url_list, url_list, rating_list)

    return creat_gym_flex_message(name_list, vicinity_list, opening_hours_list, rating_list, photo_pic_url_list,
                                  url_list)
