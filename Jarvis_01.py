import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import wikipedia
import pyjokes
import pyautogui
from plyer import notification
from bs4 import BeautifulSoup
import requests
import sys
import smtplib
import re
import time
import unicodedata
import string
import os

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate',180)

global receivers
global user_query

def speak(transcribed_query):
    print(transcribed_query)
    engine.say(transcribed_query)
    engine.runAndWait()

def remove_special_char(text):
  pattern  = r'[^a-zA-Z0-9]'
  return re.sub(pattern, ' ', text)
def remove_accent(text):
  new_text = unicodedata.normalize('NFKD',text).encode('ascii','ignore').decode('utf-8','ignore')
  return new_text

def remove_punctuations(messy_words):
  clean_list = [ch for ch in messy_words if ch not in string.punctuation]
  clean_str = "".join(clean_list)
  return clean_str

def wishme():
    speak('Jarvis Initiated ... ')
    hour = 0
    hour = int(datetime.datetime.now().hour)
    if hour >=0 and hour < 12:
        speak("good morning sir i am jarvis, please tell me how may i help you")
    elif hour >=12 and hour <18:
        speak("good afternoon sir i am jarvis, please tell me how may i help you")
    elif hour >= 18 and hour<21:
        speak("good evening sir i am jarvis, please tell me how may i help you")
    else:
        speak("good night sir ")


def input_query():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print('recognition is on....')
        recognizer.pause_threshold = 1
        recognizer.energy_threshold = 4000
        voice = recognizer.listen(source)
        try:
            query = recognizer.recognize_google(voice).lower()
            print('this is the query that was made....', query)
            return query
        except Exception as ex:
            print('An exception occurred', ex)


def report_time():
    current_time = datetime.datetime.now().strftime('%I:%M %p')
    return current_time


def make_request(url):
  response = requests.get(url,verify=False)
  return response.text

def email_sender(to,content):
    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)
    # start TLS for security
    s.starttls()
    # Authentication
    s.login("rkvishwakarma098@gmail.com", "rankush888@")
    # sending the mail
    s.sendmail("rkvishwakarma098@gmail.com",to, content)
    # terminating the session
    s.quit()



def activate_va():
    receivers = {'rankush':'rankushvishwakarma46@gmail.com','anita':'anitavishwakarma9808@gmail.com'}
    user_query = input_query()
    print('query-',user_query)
    if user_query is not None:
        if 'time' in user_query:
            current_time = report_time()
            #print(f"the current time is {current_time}")
            speak(f"the current time is {current_time}")
        elif 'open website' in user_query:
            speak(
                "which website you want me to open sir")
            website_name = input_query()
            print(website_name)
            #webbrowser.get(
            #    'C:/Program Files/Google/Chrome/Application/chrome.exe %s').open(website_name)
            webbrowser.open(f'https://www.{website_name}.com')
            speak(f"{website_name} opened.")
        elif 'wikipedia' in user_query:
            speak('Please tell me sir what is need to search on wikipedia')
            query = input_query()
            speak("Searching on Wikipedia")
            #user_query = user_query.replace('wikipedia', ' ')
            try:
                result = wikipedia.summary(query, sentences=4)
                result = remove_special_char(result)
                result= remove_accent(result)
                result = remove_punctuations(result)
                #print(result)
                speak(result)
            except requests.exceptions.SSLError as request_err:
                speak('sir we have got the request handshake error')
            except wikipedia.exceptions.PageError as p:
                speak('Sorry sir page not found')
            except ValueError as v:
                speak('use search function sir you have not said Title or Pageid')
            except wikipedia.exceptions.DisambiguationError as ambigious:
                speak('Ambiguity found on the keyword sir, please use wikipedia again')
        elif 'joke' in user_query:
            random_joke = pyjokes.get_joke()
            #print(random_joke)
            speak(random_joke)
        elif 'screenshot' in user_query:
            image = pyautogui.screenshot()
            image.save('screenshot.png')
            speak('Screenshot taken.')
        elif  'open google' in  user_query or( ('search' in user_query or 'open' in user_query) and  'google' in  user_query):
            speak("What do you want me to search for ? ")
            search_term = input_query()
            search_url = f"https://www.google.com/search?q={search_term}"
            webbrowser.open(search_url)
            #webbrowser.get(
            #    'C:/Program Files/Google/Chrome/Application/chrome.exe %s').open(search_url)
            speak(f"here are the results for the search term: {search_term}")
        elif 'close' in user_query:
            os.system("taskkill /im chrome.exe /f")
            speak('the chrome tabs have been closed sir ')
        elif 'youtube' in user_query or ( 'search' in user_query and 'youtube' in user_query):
            speak("which video you want to see sir ? ")
            search_term = input_query()
            url_query  = f'https://www.youtube.com/results?search_query={search_term}'
            webbrowser.open(url_query)
            speak(f"on youtube {search_term}  has been search you can watch the video sir")
        elif 'covid stats' in user_query or 'covid' in user_query:
            try:
              html_data = make_request('https://www.worldometers.info/coronavirus/')
              # print(html_data)
              soup = BeautifulSoup(html_data, 'html.parser')
              total_global_row = soup.find_all('tr', {'class': 'total_row'})[-1]
              total_cases = total_global_row.find_all('td')[2].get_text()
              new_cases = total_global_row.find_all('td')[3].get_text()
              total_recovered = total_global_row.find_all('td')[6].get_text()
              print('total cases : ', total_cases)
              print('new cases', new_cases[1:])
              print('total recovered', total_recovered)
              notification_message = f" Total cases : {total_cases}\n New cases : {new_cases[1:]}\n Total Recovered : {total_recovered}\n"
              notification.notify(
                title="COVID-19 Statistics",
                message=notification_message,
                timeout=5
              )
              speak("here are the stats for COVID-19")
            except requests.exceptions.SSLError as request_error:
                speak('sir i am getting HTTPS Connection Pool request error please use google search function ')
        elif 'send email' in user_query:
            speak('to whome i need to send the mail sir')
            to = input_query()
            if to in receivers:
                speak('What subject line i should text sir')
                subject = input_query()
                speak('please tell me the message need to be send')
                #content = False
                content = input_query()
                msg = f"Subject: {subject}\n\n{content}\n"
                email_sender(receivers[to],msg)
                speak('Email has been sent successfully sir')
            else:
                speak('sorry sir the email address does not exit in you address book, do you want me to set new address')
                req = input_query()
                if 'yes' in req and req is not None:
                    speak('tell me the short name of the person sir')
                    short_name = input_query()
                    if short_name not in receivers:
                        speak('tell me the user name of person email address')
                        username = input_query().replace(" ", "")
                        username = username + "@gmail.com"
                        receivers[short_name] = username
                        print(receivers)
                        speak('address book updated , thankyou')
                    else:
                        speak('this email address already exist , do you want me to remove from the address book')
                        flag = input_query()
                        if 'yes' in flag:
                            speak('tell me the short name of the person sir')
                            flag_name = input_query()
                            del receivers[flag_name]
                            print(receivers)
                            speak('updation successful sir')
        
                else:
                    speak('thankyou sir')
            
            
        else:
            speak('Thankyou sir I am leaving. ')
            sys.exit()
            #quit()
    else:
        speak('Sorry sir I did not get it')
if __name__ == "__main__":
    wishme()
    while True:
        activate_va()

