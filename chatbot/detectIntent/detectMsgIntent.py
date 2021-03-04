import os.path
import sys
import json
try:
    import apiai
except ImportError:
    sys.path.append(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
    import apiai

CLIENT_ACCESS_TOKEN = ["YOUR DIALOGFLOW ACCESS TOKEN"]  #dialogflow client access token


def detectMsgIntent(text):
    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

    request = ai.text_request()

    request.lang = 'tw'  # optional, default value equal 'en'

    request.query = text
    response = request.getresponse().read().decode()
    result = json.loads(response)
    print(result["result"]["metadata"]["intentName"])
    return result