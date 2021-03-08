import requests
import json
import pyttsx3
import speech_recognition as sr 
import re
import time
import threading

API_KEY = "tFbH47y3D0NL"
PROJECY_TOKEN = "t59JiTB6LRpo"
RUN_TOKEN = "t-SkR77OvUAV"


class Data:
    def __init__(self,api_key,project_token):
        self.api_key = api_key
        self.project_token = project_token
        self.params = {
            "api_key": self.api_key
        }

        self.data = self.get_data()
    
    def get_data(self):
        responce = requests.get(f'https://www.parsehub.com/api/v2/projects/{PROJECY_TOKEN}/last_ready_run/data',params = {"api_key": API_KEY})
        data = json.loads(responce.text)
        return data

    def get_total_cases(self):
        data = self.data['totals']

        for content in data:
            if content["name"] == "Coronavirus Cases:":
                return content["total_num"]
    
    def get_total_deaths(self):
        data = self.data['totals']

        for content in data:
            if content['name'] == "Deaths:":
                return content['total_num']
                
    def get_country_data(self, country):
        data = self.data['Country']

        for content in data:
            if content['name'].lower() == country.lower():
                return content

            return "0"
        
    def get_country_list(self):
        countries = []
        for country in self.data['Country']:
            countries.append(country['name'].lower())
        
        return countries

    def update_data():
        responce = requests.post(f'https://www.parsehub.com/api/v2/projects/{PROJECY_TOKEN}/run/data',params = self.params)
        

        def poll():
            time.sleep(0.1)
            old_data = self.data
            while True:
                new_data = self.get_data()
                if old_data != self.get_data():
                    self.data = new_data
                    print("Data updated")
                time.sleep(5)
        t = threading.Thread(target=poll)
        t.start()

#print(data.get_country_cases('USA')['total_cases'])
#print(data.get_country_list())
#print(data.data)
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
#speak('Hi')

def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ""
        
        try:
            said = r.recognize_google(audio)
        except Exception as e:
            print("Execteption",str(e))
        
    return said.lower()

def main():
    print(f"SAY NUMBER OF TOTAL COVID CASES FOR TOTAL CASES GLOBALY \n SAY NUMBER OF TOTAL DEATHS FOR NUMBER OF DEATHS FROM COVID GOLBALY \n SAY NUMBER OF CASES IN... THEN NAME OF COUNTRY \n WE ARE WORKING ON FIXING THIS FOR COUNTRY WIDE DAETHS FOR COVID")
    print("Started")
    data = Data(API_KEY, PROJECY_TOKEN)
    End_Praseh = "stop"
    country_list = data.get_country_list()
    Total_PATTERNS = {
                    re.compile("[\w\s]+ total [\w\s] + cases"):data.get_total_cases,
                    re.compile("[\w\s]+ total cases"):data.get_total_cases,
                    re.compile("[\w\s]+ total [\w\s] + deaths"):data.get_total_deaths,
                    re.compile("[\w\s]+ total death"):data.get_total_deaths
                    }
    COUNTRY_PATTERNS = {
                    re.compile("[\w\s]+ cases [\w\s] +"): lambda country: data.get_country_data(country)['total_cases']
                    #re.compile("[\w\s]+ deaths [\w\s] +"): lambda country: data.get_country_data(country)['total_deaths']
    
                    }
    UPDATE_DATA = 'update'
    while True:
        print("Listening...")
        text = get_audio()
        print(text)
        result = ""

        for pattern, func in Total_PATTERNS.items():
            if pattern.match(text):
                result = func()
                break

        for pattern, func in COUNTRY_PATTERNS.items():
            if pattern.match(text):
                words = set(text.split(" "))
                for country in country_list:
                    if country in words:
                        result = func(country)
                        break
        
        if result:
            speak(result)
        
        if text == UPDATE_DATA:
            result = "THE DATA ID BEING UPDATED SO YOU CAN GET THE BEST RESULTS THIS MAY TAKE A MOMENT!"
            data.update_data
        if text.find(End_Praseh) != -1:
            print("Exit")
            break

main()
