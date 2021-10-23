import json
import urllib.request

def handler(event, context):
    for message_event in json.loads(event['body'])['events']:
        url = 'https://api.line.me/v2/bot/message/reply'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + "NhMQQyqeSZsjUWLEaXgMa0TX9+L7siWTQWbrAPR++Q4uLnkOrMQuLtjDzl7epKePB6s21qBgiB9qvthwqoeyn/qI7iTg+0pa9ZTncfbo/UrXM4D264PTEkwq8mG/l74EeZjAbrU947+R/sVYnX+AjgdB04t89/1O/w1cDnyilFU="
        }
        
        message = get_message()
        
        body = {
            'replyToken': message_event['replyToken'],
            'messages': [
                {
                    "type": "text",
                    "text": message,
                }
            ]
        }

        req = urllib.request.Request(url, data=json.dumps(body).encode('utf-8'), method='POST', headers=headers)
        
        with urllib.request.urlopen(req) as res:
            logger.info(res.read().decode("utf-8"))

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
    
def get_message():
    return "hello world"