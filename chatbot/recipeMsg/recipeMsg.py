import requests
from bs4 import BeautifulSoup
from linebot.models import FlexSendMessage, TextSendMessage, QuickReply, QuickReplyButton, PostbackAction
import random
from about_nutrition_chatbot import settings
host=settings.host


def recipeTypeReply():
  q_reply = TextSendMessage(
    text='請選擇食譜類型呦🙇‍♂️',
    quick_reply=QuickReply(
      items=[
        QuickReplyButton(
          action=PostbackAction(label="雞肉🐓", data="c_recipe")
        ),
        QuickReplyButton(
          action=PostbackAction(label="牛肉🐂", data="b_recipe")
        ),
        QuickReplyButton(
          action=PostbackAction(label="魚肉🐟", data="f_recipe")
        ),
        QuickReplyButton(
          action=PostbackAction(label="豬肉🐖", data="p_recipe")
        ),
        QuickReplyButton(
          action=PostbackAction(label="增肌減脂🏋", data="a_recipe")
        ),
      ]

    )
  )
  return q_reply


def findRecipe(recipeType):
  headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}

  c_page = 'https://icook.tw/search/%E5%81%A5%E8%BA%AB/%E9%9B%9E%E8%82%89/'
  b_page = 'https://icook.tw/search/%E5%81%A5%E5%BA%B7/%E7%89%9B%E8%82%89/'
  f_page = 'https://icook.tw/search/%E5%81%A5%E5%BA%B7/%E9%AD%9A/'
  p_page = 'https://icook.tw/search/%E5%81%A5%E5%BA%B7/%E8%B1%AC/'
  a_page = 'https://icook.tw/search/%E5%A2%9E%E8%82%8C/'
  if recipeType == 'c_recipe':
    res = requests.get(c_page, headers=headers)
  elif recipeType == 'b_recipe':
    res = requests.get(b_page, headers=headers)
  elif recipeType == 'f_recipe':
    res = requests.get(f_page, headers=headers)
  elif recipeType == 'p_recipe':
    res = requests.get(p_page, headers=headers)
  elif recipeType == 'a_recipe':
    res = requests.get(a_page, headers=headers)

  soup = BeautifulSoup(res.text, 'html.parser')
  span_tag = soup.find_all('span', 'browse-recipe-name')
  p_tag = soup.find_all('p', 'browse-recipe-content-ingredient')
  a_tag = soup.find_all('a', 'browse-recipe-touch-link')
  li_tag = soup.find_all('li', 'browse-recipe-meta-fav')
  img_tag = soup.find_all('img', 'browse-recipe-cover-img img-responsive lazyload')
  nameList = []
  ingredientList = []
  hrefList = []
  goodList = []
  imgsrcList = []
  for item in img_tag:
    imgsrcList.append(str(item.get('data-src')))
  for item in li_tag:
    temp = item.text.strip().split('\xa0')
    goodList.append(str(temp[0]))
  for item in a_tag:
    hrefList.append(str('https://icook.tw' + item.get('href')))
  for item in span_tag:
    nameList.append(str(item.text.strip()))
  for item in p_tag:
    temp = item.text.strip().split('：')
    ingredientList.append(str(temp[1]))
  return getRecipe(imgsrcList, nameList, ingredientList, goodList, hrefList)
def getRecipe(img, name, ingredients, good, href):
  msg = FlexSendMessage(
    alt_text='recipe',
    contents={
      "type": "carousel",
      "contents": [
        {
          "type": "bubble",
          "size": "kilo",
          "hero": {
            "type": "image",
            "url": img[0],
            "size": "full",
            "aspectRatio": "20:13",
            "aspectMode": "cover",
          },
          "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": name[0],
                "weight": "bold",
                "size": "sm"
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
                        "text": "食材:",
                        "color": "#aaaaaa",
                        "size": "sm",
                        "flex": 2
                      },
                      {
                        "type": "text",
                        "text": ingredients[0],
                        "wrap": True,
                        "color": "#666666",
                        "size": "sm",
                        "flex": 5
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
                        "text": "讚數:",
                        "color": "#aaaaaa",
                        "size": "sm",
                        "flex": 2
                      },
                      {
                        "type": "text",
                        "text": good[0] + '👍',
                        "wrap": True,
                        "color": "#666666",
                        "size": "sm",
                        "flex": 5
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
            "contents": [
              {
                "type": "button",
                "style": "primary",
                "height": "sm",
                "action": {
                  "type": "uri",
                  "label": "詳細作法",
                  "uri": href[0]
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
        },
        {
          "type": "bubble",
          "size": "kilo",
          "hero": {
            "type": "image",
            "url": img[1],
            "size": "full",
            "aspectRatio": "20:13",
            "aspectMode": "cover",

          },
          "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": name[1],
                "weight": "bold",
                "size": "sm"
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
                        "text": "食材：",
                        "color": "#aaaaaa",
                        "size": "sm",
                        "flex": 2
                      },
                      {
                        "type": "text",
                        "text": ingredients[1],
                        "wrap": True,
                        "color": "#666666",
                        "size": "sm",
                        "flex": 5
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
                        "text": "讚數",
                        "color": "#aaaaaa",
                        "size": "sm",
                        "flex": 2
                      },
                      {
                        "type": "text",
                        "text": good[1] + '👍',
                        "wrap": True,
                        "color": "#666666",
                        "size": "sm",
                        "flex": 5
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
            "contents": [
              {
                "type": "button",
                "style": "primary",
                "height": "sm",
                "action": {
                  "type": "uri",
                  "label": "詳細作法",
                  "uri": href[1]
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
        },
        {
          "type": "bubble",
          "size": "kilo",
          "hero": {
            "type": "image",
            "url": img[2],
            "size": "full",
            "aspectRatio": "20:13",
            "aspectMode": "cover",
          },
          "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": name[2],
                "weight": "bold",
                "size": "sm"
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
                        "text": "食材：",
                        "color": "#aaaaaa",
                        "size": "sm",
                        "flex": 2
                      },
                      {
                        "type": "text",
                        "text": ingredients[2],
                        "wrap": True,
                        "color": "#666666",
                        "size": "sm",
                        "flex": 5
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
                        "text": "讚數",
                        "color": "#aaaaaa",
                        "size": "sm",
                        "flex": 2
                      },
                      {
                        "type": "text",
                        "text": good[2] + '👍',
                        "wrap": True,
                        "color": "#666666",
                        "size": "sm",
                        "flex": 5
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
            "contents": [
              {
                "type": "button",
                "style": "primary",
                "height": "sm",
                "action": {
                  "type": "uri",
                  "label": "詳細作法",
                  "uri": href[2]
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
        },
        {
          "type": "bubble",
          "size": "kilo",
          "hero": {
            "type": "image",
            "url": img[3],
            "size": "full",
            "aspectRatio": "20:13",
            "aspectMode": "cover",
          },
          "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": name[3],
                "weight": "bold",
                "size": "sm"
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
                        "text": "食材：",
                        "color": "#aaaaaa",
                        "size": "sm",
                        "flex": 2
                      },
                      {
                        "type": "text",
                        "text": ingredients[3],
                        "wrap": True,
                        "color": "#666666",
                        "size": "sm",
                        "flex": 5
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
                        "text": "讚數",
                        "color": "#aaaaaa",
                        "size": "sm",
                        "flex": 2
                      },
                      {
                        "type": "text",
                        "text": good[3] + '👍',
                        "wrap": True,
                        "color": "#666666",
                        "size": "sm",
                        "flex": 5
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
            "contents": [
              {
                "type": "button",
                "style": "primary",
                "height": "sm",
                "action": {
                  "type": "uri",
                  "label": "詳細作法",
                  "uri": href[3]
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
        },
        {
          "type": "bubble",
          "size": "kilo",
          "hero": {
            "type": "image",
            "url": img[4],
            "size": "full",
            "aspectRatio": "20:13",
            "aspectMode": "cover",
          },
          "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": name[4],
                "weight": "bold",
                "size": "sm"
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
                        "text": "食材：",
                        "color": "#aaaaaa",
                        "size": "sm",
                        "flex": 2
                      },
                      {
                        "type": "text",
                        "text": ingredients[4],
                        "wrap": True,
                        "color": "#666666",
                        "size": "sm",
                        "flex": 5
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
                        "text": "讚數",
                        "color": "#aaaaaa",
                        "size": "sm",
                        "flex": 2
                      },
                      {
                        "type": "text",
                        "text": good[4] + '👍',
                        "wrap": True,
                        "color": "#666666",
                        "size": "sm",
                        "flex": 5
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
            "contents": [
              {
                "type": "button",
                "style": "primary",
                "height": "sm",
                "action": {
                  "type": "uri",
                  "label": "詳細作法",
                  "uri": href[4]
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
        }
      ]
    }
  )
  return msg



