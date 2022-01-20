ai_name = 'VISION'.lower()
EXIT_COMMANDS = ['bye', 'exit', 'quit']
botChatTextBg = "#007cc7"
botChatText = "white"
userChatTextBg = "#4da8da"
chatBgColor = '#12232e'
textColor = 'white'
AITaskStatusLblBG = '#203647'
voice_id = 0  # 0 for female, 1 for male
try:
    import pyautogui
    import datetime
    import pyjokes
    import pywhatkit
    import psutil as ps
    import wikipedia
    import random
    import webbrowser
    import wolframalpha
    import requests
    import tempfile
    import os
    import speech_recognition as sr
    import pyttsx3
    from tkinter import *
    from tkinter import ttk
    from time import sleep
    from threading import Thread
except Exception as e:
    print(e)
############################################ SET UP VOICE ###########################################
try:
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[voice_id].id)  # male
    engine.setProperty('volume', ass_volume)
except Exception as e:
    print(e)


####################################### SET UP TEXT TO SPEECH #######################################
def speak(text, display=False, icon=False):
    AITaskStatusLbl['text'] = 'Speaking...'
    if icon:
        Label(chat_frame, image=botIcon, bg=chatBgColor).pack(
            anchor='w', pady=0)
    if display:
        attachTOframe(text, True)
    print('\n'+ai_name.upper()+': '+text)
    try:
        engine.say(text)
        engine.runAndWait()
    except:
        print("Try not to type more...")

####################################### SET UP SPEECH TO TEXT #######################################


def record(clearChat=True, iconDisplay=True):
    print('\nListening...')
    AITaskStatusLbl['text'] = 'Listening...'
    r = sr.Recognizer()
    r.dynamic_energy_threshold = False
    r.energy_threshold = 4000
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        said = ""
        try:
            AITaskStatusLbl['text'] = 'Processing...'
            said = r.recognize_google(audio)
            print(f"\nUser said: {said}")
            if clearChat:
                clearChatScreen()
            if iconDisplay:
                Label(chat_frame, image=userIcon, bg=chatBgColor).pack(
                    anchor='e', pady=0)
            attachTOframe(said)
        except Exception as e:
            print(e)
            # speak("I didn't get it, Say that again please...")
            if "connection failed" in str(e):
                speak("Your System is Offline...", True, True)
            return 'None'
    return said.lower()


def voiceMedium():
    while True:
        query = record()
        if query == 'None':
            continue
        if isContain(query, EXIT_COMMANDS):
            speak("Shutting down the System. Good Bye !", True, True)
            break
        else:
            main(query.lower())
    appControl.Win_Opt('close')


def keyboardInput(e):
    user_input = UserField.get().lower()
    if user_input != "":
        clearChatScreen()
        if isContain(user_input, EXIT_COMMANDS):
            speak("Shutting down the System. Good Bye !", True, True)
        else:
            Label(chat_frame, image=userIcon, bg=chatBgColor).pack(
                anchor='e', pady=0)
            attachTOframe(user_input.capitalize())
            Thread(target=main, args=(user_input,)).start()
        UserField.delete(0, END)


def Wishme():
    speak("Hello World ! I am Vision .", True)
    speak("Who are you ?", True)
    uname = record()
    hour = int(datetime.datetime.now().hour)
    if hour >= 6 and hour <= 12:
        speak("Good Morning !!", True)
        speak(uname, True)
    elif hour > 12 and hour <= 18:
        speak("Good Afternoon !!", True)
        speak(uname, True)
    else:
        speak("Good Evening !!", True)
        speak(uname, True)
        speak("You can speak keyword 'command' to view list of instructions which you can give me", True)
    speak("How can I Help you ?", True)


def screenShot():
    today_date = datetime.date.today()
    today_date = (str(today_date)).replace('-', '')
    today_time = datetime.datetime.now().strftime('%H%M%S')
    img = pyautogui.screenshot()
    img.save(r"Files and Document/ss_"+str(today_date)+today_time+".jpg")


def tellDay():
    day = datetime.datetime.today().weekday() + 1

    Day_dict = {1: 'Monday', 2: 'Tuesday',
                3: 'Wednesday', 4: 'Thursday',
                5: 'Friday', 6: 'Saturday',
                7: 'Sunday'}

    if day in Day_dict.keys():
        day_of_the_week = Day_dict[day]
        speak("Today" + day_of_the_week, True)


def cpu():
    usage = str(ps.cpu_percent())
    speak("CPU is at" + usage, True)
    battery = ps.sensors_battery()
    speak("Battery is at" + str(battery.percent), True)
###################################### TASK/COMMAND HANDLER #########################################


def main(text):
    if 'screenshot' in text:
        screenShot()
        speak('Done', True)

    elif 'command' in text:
        speak("These are some of the commands which you can ask me to execute:\nscreenshot\nmessage\ntype\nprint\nwho is (wiki)\ntime\nplay youtube\nsearch", True)

    elif 'date' in text:
        speak(str(datetime.date.today()), True)

    elif ' day' in text:
        tellDay()

    elif 'usage' in text:
        cpu()

    elif 'play' in text:
        song = text.replace('play', '')
        speak('Playing' + song, True)
        pywhatkit.playonyt(song)

    elif "joke" in text:
        speak('Here is a joke...', True)
        speak(pyjokes.get_joke(), True)

    elif 'time' in text:
        time = datetime.datetime.now().strftime('%I:%M %p')
        speak('Current time is' + time, True)

    elif 'who is' in text:
        person = text.replace('who is ', '')
        info = wikipedia.summary(person, 2)
        person1 = person.title()
        person2 = person1.replace(' ', '_')
        webbrowser.open('https://en.wikipedia.org/wiki/'+person2)
        speak(info, True)

    elif 'search' in text:
        search = text.replace('search', '')
        pywhatkit.search(search)

    elif 'open whatsapp' in text:
        speak('Opening whatsapp', True)
        pywhatkit.open_web()

    elif 'open youtube' in text:
        speak("Here you go to Youtube\n", True)
        webbrowser.open("https://www.youtube.com/")

    elif 'open stackoverflow' in text:
        speak("Here you go to Stack Over flow .  Happy coding", True)
        webbrowser.open("https://www.stackoverflow.com")

    elif 'open github' in text:
        speak("Here you go to GitHub .  Happy coding", True)
        webbrowser.open("https://www.github.com")

    elif 'open gmail' in text:
        webbrowser.open_new_tab("https://mail.google.com/")
        speak("Google Mail open now", True)

    elif 'message' in text:
        speak('Whom do you want to send message ?', True)
        number = record()
        speak('What is the message ?', True)
        message = record()
        speak('Sending message', True)
        pywhatkit.sendwhatmsg_instantly(
            '+91'+number, message, 10, 'chrome', False)
        speak('Sent', True)

    elif 'question' in text:
        speak('I can answer to computational and geographical questions . Ask me .', True)
        question = record()
        app_id = "JT8TUV-LGHQ6Q2UTK "
        client = wolframalpha.Client(app_id)
        res = client.query(question)
        answer = next(res.results).text
        speak(answer, True)

    elif 'flip a coin' in text or 'toss a coin' in text:
        speak("Ok sir , flipping a coin!")
        coin = ['heads', 'tails']
        toss = random.choice(coin)
        speak("I flipped the coin and got" + toss, True)

    elif 'roll a dice' in text:
        speak("Ok sir, rolling a dice for you!", True)
        dice = ['1', '2', '3', '4', '5', '6']
        roll = random.choice(dice)
        speak("I rolled a dice and got" + roll, True)

    elif 'class' in text:
        speak("Which class do you want do attend ?", True)

    elif 'mechatronics and robotics' in text or 'robotics' in text:
        webbrowser.open("https://meet.google.com/nhz-jfnf-bgf")

    elif 'python' in text or 'computing with python' in text:
        webbrowser.open("https://meet.google.com/xow-pdxg-jvy")

    elif 'cognitive aptitude' in text or 'ca' in text:
        webbrowser.open("https://meet.google.com/pjw-dkdz-tid")

    elif 'mad lab' in text or 'mobile application development' in text:
        webbrowser.open_new_tab("http://meet.google.com/uxp-iauu-avo")

    elif "weather" in text:
        api_key = "6295fdcf4580213693535279071b2ce2"
        base_url = "https://api.openweathermap.org/data/2.5/weather?"
        speak("Where do you want me to check the weather ?", True)
        city_name = record()
        complete_url = base_url + "appid=" + api_key + "&q=" + city_name
        response = requests.get(complete_url)
        x = response.json()
        if x["cod"] != "404":
            y = x["main"]
            current_temperature = y["temp"]
            current_humidiy = y["humidity"]
            z = x["weather"]
            weather_description = z[0]["description"]
            speak(" Temperature in kelvin unit is " +
                  str(current_temperature) +
                  "\n humidity in percentage is " +
                  str(current_humidiy) +
                  "\n description  " +
                  str(weather_description), True)

    elif 'good morning' in text:
        speak('Good Morning', True)
    elif 'good afternoon' in text:
        speak('Good afternoon', True)
    elif 'good evening' in text:
        speak('Good evening', True)
    elif 'good night' in text:
        speak('Good night', True)

    elif 'print' in text:
        speak("What should I type?", True)
        data = record()
        speak('Done', True)
        remember = open('print.txt', 'w')
        remember.write(data)
        remember.close()
        filename = tempfile.mktemp("print.txt")
        open(filename, "w").write(data)
        os.startfile(filename, "print")

    elif 'type' in text:
        speak("What should I type?", True)
        data = record()
        speak('Done', True)
        today_date = datetime.date.today()
        today_time = datetime.datetime.now().strftime('%I:%M %p')
        remember = open('data.txt', 'a')
        remember.write('DATE:' + str(today_date) + '\n' +
                       'TIME:' + today_time + ':    ' + data + '\n' + '\n')
        remember.close()

    elif 'remember' in text:
        remember = open("data.txt", 'r')
        speak('you said me to read that' + remember.read(), True)
        remember.close()

    elif 'read text file' in text:
        speak('Which text file do you want me to read?', True)
        file_name = record()
        remember = open(file_name + '.txt', 'r')
        speak('you said me to read that' + remember.read(), True)
        remember.close()

    elif 'log out' in text:
        os.system("shutdown -l")

    elif 'shutdown' in text:
        os.system("shutdown /s /t 1")

    elif 'restart' in text:
        os.system("shutdown /s /t 1")

    elif 'how are you' in text:
        speak("I am fine, Thank you. How are you ?", True)

    elif 'fine' in text or "good" in text:
        speak("It's good to know that your fine", True)

    elif 'thank you' in text:
        speak("My pleasure sir", True)

    elif 'bye' in text or 'exit' in text or 'quit' in text:
        speak("Shutting down the System. Good Bye Sir!", True)
        exit()

    elif 'who are you' in text:
        speak("I am Vision, your personal assistant", True)

    elif "who made you" in text or "who created you" in text:
        speak("I was created by Shruti,  Akash,  Amitab,  Shreyas,  Vishal and Ritika  , the R6 Group.", True)

        #####################
        ####### GUI #########
        #####################

############ ATTACHING BOT/USER CHAT ON CHAT SCREEN ###########


def attachTOframe(text, bot=False):
    if bot:
        botchat = Label(chat_frame, text=text, bg=botChatTextBg, fg=botChatText,
                        justify=LEFT, wraplength=250, font=('Montserrat', 12, 'bold'))
        botchat.pack(anchor='w', ipadx=5, ipady=5, pady=5)
    else:
        userchat = Label(chat_frame, text=text, bg=userChatTextBg, fg='white',
                         justify=RIGHT, wraplength=250, font=('Montserrat', 12, 'bold'))
        userchat.pack(anchor='e', ipadx=2, ipady=2, pady=5)


def clearChatScreen():
    for wid in chat_frame.winfo_children():
        wid.destroy()


if __name__ == '__main__':
    try:
        # pass
        Thread(target=voiceMedium).start()
    except:
        pass
    try:
        # pass
        Thread(target=webScrapping.dataUpdate).start()
    except Exception as e:
        print('System is Offline...')

    root.iconbitmap('extrafiles/images/assistant2.ico')
    raise_frame(root1)
    Wishme()
    Thread(target=voiceMedium).start()
    root.mainloop()
