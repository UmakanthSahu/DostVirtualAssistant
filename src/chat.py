from model import NueralNet
from nltk_utils import *

import requests
from random import choice
import datetime
from json import load
import torch

import wikipedia
import speech_recognition as sr
import webbrowser
from os import system
import subprocess
import win32com.client as win32
import win32gui

edgepath = "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"
chromepath = "C:/ProgramFiles(x86)/Google/Chrome/Application/chrome.exe"

def weather():
    res = requests.get('https://ipinfo.io/')
    data = res.json()

    location = data['city']

    complete_api_link ="http://api.openweathermap.org/data/2.5/weather?appid=4578c4231438a2b339c6b12f30f78648&q="+location
    api_link = requests.get(complete_api_link)
    api_data = api_link.json()

    temp_city = ((api_data['main']['temp']) - 273.15)
    temp_city = "{:.2f}".format(temp_city) 
    weather_desc = api_data['weather'][0]['description']
    hmdt = api_data['main']['humidity']
    wind_spd = api_data['wind']['speed']
    date_time = datetime.datetime.now().strftime("%d %b %Y | %I:%M:%S %p IST")

    return f"\nWeather Stats for - {location}  || {date_time}\nCurrent temperature is : {temp_city} deg C\nCurrent weather desc   : {weather_desc}\nCurrent Humidity           : {hmdt}\nCurrent wind speed       : {wind_spd} kmph"



def openUP(app):
    def windowEnumerationHandler(hwnd, top_windows):
        top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))
    
    results = []
    top_windows = []
    win32gui.EnumWindows(windowEnumerationHandler, top_windows)

    for i in top_windows:
        if app in i[1].lower():
            #print(i)
            win32gui.ShowWindow(i[0],5)
            win32gui.SetForegroundWindow(i[0])
            break

def openWord():
    word = win32.Dispatch('Word.Application')
    word.Visible = 1

    doc = word.Documents.Add()
    word.ActiveDocument.ActiveWindow.View.Type = 3

    openUP("word")

def openExcel():
    excel = win32.Dispatch('Excel.Application')
    excel.Visible = 1
    excel.Workbooks.Add()
    openUP("excel")

def openPPT():
    ppt = win32.Dispatch('Powerpoint.Application')
    ppt.Visible = 1
    ppt.Presentations.Add()
    openUP("powerpoint")

device = 'cpu'
with open('intents.json','r') as f:
    intents = load(f)

FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data["all_words"]
tags = data["tags"]
model_state =  data["model_state"]

model = NueralNet(input_size,hidden_size,output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "DOST"

def get_response(msg):
    sentence = tokenize(msg)
    x = bag_of_words(sentence,all_words)
    x = x.reshape(1,x.shape[0])
    x = torch.from_numpy(x)

    output = model(x)
    _,predicted = torch.max(output,dim=1)
    tag = tags[predicted.item()]

    probs = torch.softmax(output,dim =1)
    prob = probs[0][predicted.item()]
    
    
    
    # probability 
    print("prob:",prob)
    if(prob.item()>0.90):
        for intent in intents["intents"]:
            if( tag == intent["tag"]):
                print(tag)
                string = choice(intent["responses"])
                if(string.startswith("A:")):
                    string  = string.replace("A: ","")
                    try:
                        print(string)
                        exec(string)
                        print(tag,string)
                        return "executed open "+tag
                    except Exception:
                        return "Could not execute "+ tag +" due to application loading error. Please make sure application is installed" 
                elif(string.startswith("R:")):
                    string = string.replace("R: ","")
                    resp = []
                    exec(string)
                    t = []
                    exec("t.append(resp[0])")
                    print(t[0])
                    return t[0]
                elif(string.startswith("wikipedia:")):
                    try:
                        msg = msg.replace("wikipedia",'')
                        msg = wikipedia.summary(msg,sentences=2)
                        print(msg)
                        print(type(msg))
                        return msg
                    except Exception as e:
                        return str(e)+"\nPlease be more specific and re-enter."
                else:
                    return string
    else:
        try:
            msg = msg.replace("compute","")
            msg = msg.replace("evaluate","")
            
            return eval(msg.replace(" ",""))
        except Exception as e:
            print("excp",e)
            pass
        
    msg = msg.replace("?","")
    msg = msg.replace(".","")
    msg = msg.replace("+","")
    msg = msg.replace("/","")
    msg = msg.replace("-","")
    
    if 'none' in msg.lower():
        return "Say something..."
    
    msg = f'https://duckduckgo.com/?q={msg}'
    print(msg)
    webbrowser.open(msg)
    return  "I donot understand Sorry..But I'm trying to search in web."

#get_response("search for Sundar pichai on wikipedia")
#print(weather())
