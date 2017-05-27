# coding=utf-8
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from wikipedia import wikipedia

app = Flask(__name__)


def remove_head(from_this, remove_this):
    if from_this.endswith(remove_this):
        from_this = from_this[:-len(remove_this)].strip()
    elif from_this.startswith(remove_this):
        from_this = from_this[len(remove_this):].strip()
    return from_this


def get_reply(message):
    message = message.lower().strip()
    answer = ""

    if "weather" in message:
        answer = "get the weather using a weather API"
    # is the keyword "wolfram" in the message? Ex: "wolfram integral of x + 1"
    elif "wolfram" in message:
        answer = "get a response from the Wolfram Alpha API"

    # is the keyword "wiki" in the message? Ex: "wiki donald trump"
    elif "wiki" in message:
        message = remove_head(message, "wiki")
        try:
            answer = wikipedia.summary(message)
        except:
            answer = "Request was not found using wiki. Be more specific?"

    # is the keyword “some_keyword” in the message? You can create your own custom
    # requests! Ex: “schedule Monday”
    elif "some_keyword" in message:
        answer = "some response"

    # the message contains no keyword. Display a help prompt to identify possible
    # commands
    else:
        answer = "\n Welcome! These are the commands you may use: \nWOLFRAM \"wolframalpha request\" \nWIKI \"wikipedia request\"\nWEATHER \"place\"\nSOME_KEYWORD \"some custom request\"\n"

    if len(answer) > 1500:
        answer = answer[0:1500] + "..."
    return answer


@app.route('/', methods=['POST'])
def sms():
    message_body = request.form['Body']
    response = MessagingResponse()
    reply_text = get_reply(message_body)

    response.message('Hi\n\n' + reply_text)
    return str(response)


if __name__ == '__main__':
    app.run()
