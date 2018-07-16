from bottle import run,route,response,error,request,
from bottle import template,static_file
from l_ms_api.MessagingClient import MessagingClient
from l_ms_api.Tracer import Tracer
import os

cl = MessagingClient(channelAccessToken="INPUT_YOUR_TOKEN")
tracer = Tracer()
admin = "INPUT_YOUR_USER_ID"

def executer(msg):
        try:
            sys.stdout = open("temp.txt","w",encoding="utf8")
            exec(msg.replace("/exec",""))
            sys.stdout.close()
            sys.stdout = sys.__stdout__
            with open("temp.txt","r",encoding="utf8") as f:
                cl.addMessage(f.read())
            cl.replyMessage()
        except Exception as e:
            print(str(e))

def echoDisposer(op):
    if op["source"]["type"] == "user":
        # Execute message as Python Script
        if op["source"]["userId"] == admin and op["message"]["text"].startswith("/exec"):
            executer(op["message"]["text"])
        # Echo Message and userId
        else:
            cl.addMessage(op["message"]["text"])
            cl.addMessage(op["source"]["userId"])
            cl.replyMessage()
    elif op["source"]["type"] == "group":
        # Execute message as Python Script
        if op["source"]["userId"] == admin and op["message"]["text"].startswith("/exec"):
            executer(op["message"]["text"])
tracer.addEventInterrupt(26,echoDisposer)

@route('/')
def render_index():
    return "The Server is working fine."
@route('/callback')
def process_bot():
    tracer.trace(request)
    resp = HTTPResponse(status=200, body="Process Complete")
    return resp
@route('/robots.txt')
def render_robots():
    return static_file("robots.txt",root="./")
@route('/static/<filename:path>')
def render_static(filename):
    return static_file(filename, root="./static/")

@error(404)
def error_404(error):
    return "NotFound"
@error(500)
def error_500(error):
    return "InternalError"

#run(host='localhost', port=8080, debug=True)