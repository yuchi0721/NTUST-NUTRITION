from linebot.models import MessageEvent, TextSendMessage, TextMessage, FlexSendMessage, ImageSendMessage, PostbackEvent, \
    BubbleContainer, ImageComponent, BoxComponent, TextComponent, ButtonComponent, URIAction, SpacerComponent, \
    CarouselContainer
from nutritionweb.models import lineUser
from about_nutrition_chatbot import settings
host=settings.host

def creat_user_flex_message(userProfile):
    global userName,userGender,userWeight,userAge,userId
    result = lineUser.objects.get(userId=userProfile.user_id)
    userName = result.userName
    userGender = result.userGender
    userWeight = result.userWeight
    userHeight = result.userHeight
    userAge = result.userAge
    userId = result.userId
    print(userName)
    userBmi = round(userWeight / (userHeight / 100) ** 2, 2)

    bubble = BubbleContainer(
        size='kilo',
        hero=ImageComponent(
            url=userProfile.picture_url,
            size='full',
            aspectRatio="20:13",
            aspectMode="cover",
        ),
        body=BoxComponent(
            layout='vertical',
            size='sm',
            contents=[
                BoxComponent(
                    layout='vertical',
                    margin='sm',
                    spacing='sm',
                    contents=[
                        TextComponent(
                            text='個人基本資料',
                            weight="bold",
                            size="lg",
                            style="normal",
                            decoration="none",
                            gravity="center",
                            align="center"
                        ),
                        BoxComponent(
                            layout='vertical',
                            margin='sm',
                            spacing='sm',
                            contents=[
                                BoxComponent(
                                    layout="baseline",
                                    pacing="sm",
                                    contents=[
                                        TextComponent(
                                            type="text",
                                            text="用戶名：",
                                            color="#aaaaaa",
                                            size="sm",
                                            flex=2
                                        ),
                                        TextComponent(
                                            type='text',
                                            text=str(userName),
                                            wrap=True,
                                            color="#666666",
                                            size="sm",
                                            flex=3,
                                        )
                                    ])

                            ]
                        ),
                        BoxComponent(
                            layout='vertical',
                            margin='sm',
                            spacing='sm',
                            contents=[
                                BoxComponent(
                                    layout="baseline",
                                    spacing="sm",
                                    contents=[
                                        TextComponent(
                                            type="text",
                                            text="性別：",
                                            color="#aaaaaa",
                                            size="sm",
                                            flex=2
                                        ),
                                        TextComponent(
                                            type='text',
                                            text=str(userGender),
                                            wrap=True,
                                            color="#666666",
                                            size="sm",
                                            flex=5,
                                        )
                                    ])

                            ]
                        ),
                        BoxComponent(
                            layout='vertical',
                            margin='sm',
                            spacing='sm',
                            contents=[
                                BoxComponent(
                                    layout="baseline",
                                    spacing="sm",
                                    contents=[
                                        TextComponent(
                                            type="text",
                                            text="年齡：",
                                            color="#aaaaaa",
                                            size="sm",
                                            flex=2
                                        ),
                                        TextComponent(
                                            type='text',
                                            text=str(userAge),
                                            wrap=True,
                                            color="#666666",
                                            size="sm",
                                            flex=5,
                                        )
                                    ])

                            ]
                        ),
                        BoxComponent(
                            layout='vertical',
                            margin='sm',
                            spacing='sm',
                            contents=[
                                BoxComponent(
                                    layout="baseline",
                                    spacing="sm",contents=[
                                            TextComponent(
                                                type="text",
                                                text="身高：",
                                                color="#aaaaaa",
                                                size="sm",
                                                flex=2
                                            ),
                                            TextComponent(
                                                type='text',
                                                text=str(userHeight),
                                                wrap=True,
                                                color="#666666",
                                                size="sm",
                                                flex=5,
                                            )
                                        ])

                                ]
                            ),
                            BoxComponent(
                                layout='vertical',
                                margin='sm',
                                spacing='sm',
                                contents=[
                                    BoxComponent(
                                        layout="baseline",
                                        spacing="sm",
                                        contents=[
                                            TextComponent(
                                                type="text",
                                                text="體重：",
                                                color="#aaaaaa",
                                                size="sm",
                                                flex=2
                                            ),
                                            TextComponent(
                                                type='text',
                                                text=str(userWeight),
                                                wrap=True,
                                                color="#666666",
                                                size="sm",
                                                flex=5,
                                            )
                                        ])

                                ]
                            ),
                            BoxComponent(
                                layout='vertical',
                                margin='sm',
                                spacing='sm',
                                contents=[
                                    BoxComponent(
                                        layout="baseline",
                                        spacing="sm",
                                        contents=[
                                            TextComponent(
                                                type="text",
                                                text="BMI：",
                                                color="#aaaaaa",
                                                size="sm",
                                                flex=2
                                            ),
                                            TextComponent(
                                                type="text",
                                                text=str(userBmi),
                                                wrap=True,
                                                color="#666666",
                                                size="sm",
                                                flex=5,
                                            )
                                        ])
                                ]
                            ),

                        ],
                    )
                ],
            ),
            footer=BoxComponent(
                layout='vertical',
                spacing='sm',
                contents=[
                    ButtonComponent(
                        style="primary",
                        height="sm",
                        action=URIAction(label="編輯",
                                         uri=host+"/nutritionweb/edit/" + userId + "/edit"),
                        color="#EA8244",
                        gravity="center",
                    ),
                    SpacerComponent(size='sm'),
                ],
                flex=0,
            )

        )
    return FlexSendMessage(alt_text="檢視個人基本資料", contents=bubble)


