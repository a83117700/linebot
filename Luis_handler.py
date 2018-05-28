import requests
import json
class Luis_handler(object):
    def __init__(self, arg):
        super(Luis_handler, self).__init__()
        self.arg = arg

def luis(text):
    food = None
    flavor = None
    store = None
    size= None
    like = None
    url = 'https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/7ca058fb-ee2c-4627-9c9e-5922c72ee446?subscription-key=e6f7e8ca2aa849eba0ea0ccb28f1c03f&verbose=true&timezoneOffset=480&q='
    res = requests.get(url+text)
    json_text = json.loads(res.text)
    if((json_text['intents'][0]['intent']) == 'None'):
        return '輸入失敗，我看不懂'
    else:
        for entity in json_text['entities']:
            if(entity['type']=='喜好食物::類型'):
                if(entity['entity'] is None):
                    food = ''
                else:
                    food = entity['entity']
            if(entity['type']=='喜好食物::口味'):
                if(entity['entity'] is None):
                    flavor = ''
                else:
                    flavor = entity['entity']
            if(entity['type']=='喜好食物::店家'):
                if(entity['entity'] is None):
                    store = ''
                else:
                    store = entity['entity']
            if(entity['type']=='喜好食物::份量'):
                if(entity['entity'] is None):
                    size = ''
                else:
                    size = entity['entity']
            if(entity['type']=='喜好食物::喜好'):
                if(entity['entity'] is None):
                    like = ''
                else:
                    like = entity['entity']
            if(entity['type']=='喜好食物::不喜好'):
                if(entity['entity'] is None):
                    like = ''
                else:
                    like = entity['entity']
        food_entity = {'food':food, 'flavor':flavor, 'store':store, 'size':size, 'like':like}
    return food_entity