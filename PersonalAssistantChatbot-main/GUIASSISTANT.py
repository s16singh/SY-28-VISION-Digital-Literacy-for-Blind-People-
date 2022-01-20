#########################
# GLOBAL VARIABLES USED #
#########################
ai_name = 'VISION'.lower()
EXIT_COMMANDS = ['bye','exit','quit']

rec_email, rec_phoneno = "", ""
WAEMEntry = None

avatarChoosen = 0
choosedAvtrImage = None

botChatTextBg = "#007cc7"
botChatText = "white"
userChatTextBg = "#4da8da"



chatBgColor = '#12232e'
background = '#203647'
textColor = 'white'
AITaskStatusLblBG = '#203647'
KCS_IMG = 1 #0 for light, 1 for dark
voice_id = 0 #0 for female, 1 for male
ass_volume = 1 #max volume
ass_voiceRate = 200 #normal voice rate

####################################### IMPORTING MODULES ###########################################
""" User Created Modules """
try:
	import normalChat
	import math_function
	import appControl
	import webScrapping
	import game
	from userHandler import UserData
	import timer
	from FACE_UNLOCKER import clickPhoto, viewPhoto
	import dictionary
	import ToDo
	import fileHandler
except Exception as e:
	raise e

""" System Modules """
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
	from tkinter import messagebox
	from tkinter import colorchooser
	from PIL import Image, ImageTk
	from time import sleep
	from threading import Thread
except Exception as e:
	print(e)

########################################## LOGIN CHECK ##############################################
try:
	user = UserData()
	user.extractData()
	ownerName = user.getName().split()[0]
	ownerDesignation = "Sir"
	if user.getGender()=="Female": ownerDesignation = "Ma'am"
	ownerPhoto = user.getUserPhoto()
except Exception as e:
	print("You're not Registered Yet !\nRun SECURITY.py file to register your face.")
	raise SystemExit


########################################## BOOT UP WINDOW ###########################################
def ChangeSettings(write=False):
	import pickle
	global background, textColor, chatBgColor, voice_id, ass_volume, ass_voiceRate, AITaskStatusLblBG, KCS_IMG, botChatTextBg, botChatText, userChatTextBg
	setting = {'background': background,
				'textColor': textColor,
				'chatBgColor': chatBgColor,
				'AITaskStatusLblBG': AITaskStatusLblBG,
				'KCS_IMG': KCS_IMG,
				'botChatText': botChatText,
				'botChatTextBg': botChatTextBg,
				'userChatTextBg': userChatTextBg,
				'voice_id': voice_id,
				'ass_volume': ass_volume,
				'ass_voiceRate': ass_voiceRate
			}
	if write:
		with open('userData/settings.pck', 'wb') as file:
			pickle.dump(setting, file)
		return
	try:
		with open('userData/settings.pck', 'rb') as file:
			loadSettings = pickle.load(file)
			background = loadSettings['background']
			textColor = loadSettings['textColor']
			chatBgColor = loadSettings['chatBgColor']
			AITaskStatusLblBG = loadSettings['AITaskStatusLblBG']
			KCS_IMG = loadSettings['KCS_IMG']
			botChatText = loadSettings['botChatText']
			botChatTextBg = loadSettings['botChatTextBg']
			userChatTextBg = loadSettings['userChatTextBg']
			voice_id = loadSettings['voice_id']
			ass_volume = loadSettings['ass_volume']
			ass_voiceRate = loadSettings['ass_voiceRate']
	except Exception as e:
		pass

if os.path.exists('userData/settings.pck')==False:
	ChangeSettings(True)
	
def getChatColor():
	global chatBgColor
	chatBgColor = myColor[1]
	colorbar['bg'] = chatBgColor
	chat_frame['bg'] = chatBgColor
	root1['bg'] = chatBgColor

def changeTheme():
	global background, textColor, bg, AITaskStatusLblBG, KCS_IMG, botChatText, botChatTextBg, userChatTextBg, chatBgColor
	if themeValue.get()==1:
		background, textColor, AITaskStatusLblBG, KCS_IMG = "#203647", "white", "#203647",1
		cbl['image'] = cblDarkImg
		kbBtn['image'] = kbphDark
		settingBtn['image'] = sphDark
		AITaskStatusLbl['bg'] = AITaskStatusLblBG
		botChatText, botChatTextBg, userChatTextBg = "white", "#007cc7", "#4da8da"
		chatBgColor = "#12232e"
		colorbar['bg'] = chatBgColor
		
		
	else:
		background, textColor, AITaskStatusLblBG, KCS_IMG = "#F6FAFB", "#303E54", "#14A769", 0
		cbl['image'] = cblLightImg
		kbBtn['image'] = kbphLight
		settingBtn['image'] = sphLight
		AITaskStatusLbl['bg'] = AITaskStatusLblBG
		botChatText, botChatTextBg, userChatTextBg = "#494949", "#EAEAEA", "#23AE79"
		chatBgColor = "#F6FAFB"
		colorbar['bg'] = '#E8EBEF'
		

	root['bg'], root2['bg'] = background, background
	settingsFrame['bg'] = background
	settingsLbl['fg'], userPhoto['fg'], userName['fg'], assLbl['fg'], voiceRateLbl['fg'], volumeLbl['fg'], themeLbl['fg'], chooseChatLbl['fg'] = textColor, textColor, textColor, textColor, textColor, textColor, textColor, textColor
	settingsLbl['bg'], userPhoto['bg'], userName['bg'], assLbl['bg'], voiceRateLbl['bg'], volumeLbl['bg'], themeLbl['bg'], chooseChatLbl['bg'] = background, background, background, background, background, background, background, background
	s.configure('Wild.TRadiobutton', background=background, foreground=textColor)
	volumeBar['bg'], volumeBar['fg'], volumeBar['highlightbackground'] = background, textColor, background
	chat_frame['bg'], root1['bg'] = chatBgColor, chatBgColor
	userPhoto['activebackground'] = background
	ChangeSettings(True)

def changeVoice(e):
	global voice_id
	voice_id=0
	if assVoiceOption.get()=='Male': voice_id=1
	engine.setProperty('voice', voices[voice_id].id)
	ChangeSettings(True)

def changeVolume(e):
	global ass_volume
	ass_volume = volumeBar.get() / 100
	engine.setProperty('volume', ass_volume)
	ChangeSettings(True)

def changeVoiceRate(e):
	global ass_voiceRate
	temp = voiceOption.get()
	if temp=='Very Low': ass_voiceRate = 100
	elif temp=='Low': ass_voiceRate = 150
	elif temp=='Fast': ass_voiceRate = 250
	elif temp=='Very Fast': ass_voiceRate = 300
	else: ass_voiceRate = 200
	print(ass_voiceRate)
	engine.setProperty('rate', ass_voiceRate)
	ChangeSettings(True)

ChangeSettings()

############################################ SET UP VOICE ###########################################
try:
	engine = pyttsx3.init()
	voices = engine.getProperty('voices')
	engine.setProperty('voice', voices[voice_id].id) #male
	engine.setProperty('volume', ass_volume)
except Exception as e:
	print(e)


####################################### SET UP TEXT TO SPEECH #######################################
def speak(text, display=False, icon=False):
	AITaskStatusLbl['text'] = 'Speaking...'
	if icon: Label(chat_frame, image=botIcon, bg=chatBgColor).pack(anchor='w',pady=0)
	if display: attachTOframe(text, True)
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
			if iconDisplay: Label(chat_frame, image=userIcon, bg=chatBgColor).pack(anchor='e',pady=0)
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
		if query == 'None': continue
		if isContain(query, EXIT_COMMANDS):
			speak("Shutting down the System. Good Bye !", True, True)
			break
		else: main(query.lower())
	appControl.Win_Opt('close')

def keyboardInput(e):
	user_input = UserField.get().lower()
	if user_input!="":
		clearChatScreen()
		if isContain(user_input, EXIT_COMMANDS):
			speak("Shutting down the System. Good Bye !", True, True)
		else:
			Label(chat_frame, image=userIcon, bg=chatBgColor).pack(anchor='e',pady=0)
			attachTOframe(user_input.capitalize())
			Thread(target=main, args=(user_input,)).start()
		UserField.delete(0, END)

def Wishme():
	speak("Hello World ! I am Vision .", True)
	speak("Who are you ?",True)
	uname = record()
	hour = int(datetime.datetime.now().hour)
	if hour >= 6 and hour <= 12:
		speak("Good Morning !!", True)
		speak(uname,True)
	elif hour > 12 and hour <= 18:
		speak("Good Afternoon !!",True)
		speak(uname, True)
	else:
		speak("Good Evening !!",True)
		speak(uname,True)
	#speak("You can speak keyword 'command' to view list of instructions which you can give me",True)
	speak("How can I Help you ?", True)

def screenShot():
   today_date = datetime.date.today()
   today_date=(str(today_date)).replace('-','')
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
        speak("Today is " + day_of_the_week, True)

def cpu():
    usage = str(ps.cpu_percent())
    speak("CPU is at " + usage, True)
    battery = ps.sensors_battery()
    speak("Battery is at " + str(battery.percent), True)
###################################### TASK/COMMAND HANDLER #########################################
def isContain(txt, lst):
	for word in lst:
		if word in txt:
			return True
	return False

def main(text):
	if 'screenshot' in text:
		screenShot()
		speak('Done', True)

	elif 'command' in text:
		speak("These are some of the commands which you can ask me to execute:\nscreenshot\nmessage\ntype\nprint\nwho is (wiki)\ntime\nplay youtube\nsearch",True)

	elif 'date' in text:
		speak(str(datetime.date.today()), True)

	elif ' day' in text:
		tellDay()

	elif 'usage' in text:
		cpu()

	elif 'play' in text:
		song = text.replace('play','')
		speak('Playing' + song, True)
		pywhatkit.playonyt(song)

	elif "joke" in text:
		speak('Here is a joke...', True)
		speak(pyjokes.get_joke(), True)

	elif 'time' in text:
		time = datetime.datetime.now().strftime('%I:%M %p')
		speak('Current time is ' + time, True) 
	
	elif 'who is' in text:
		person = text.replace('who is ','')
		info = wikipedia.summary(person,2)
		person1=person.title()
		person2=person1.replace(' ','_')
		webbrowser.open('https://en.wikipedia.org/wiki/'+person2)
		speak(info,True)
		
	elif 'search' in text:
		search = text.replace('search', '')
		pywhatkit.search(search)
		
	elif 'open whatsapp' in text:
		speak('Opening whatsapp',True)
		pywhatkit.open_web()
		
	elif 'open youtube' in text:
		speak("Here you go to Youtube\n",True)
		webbrowser.open("https://www.youtube.com/")
		
	elif 'open stack overflow' in text:
		speak("Here you go to Stack Over flow .  Happy coding",True)
		webbrowser.open("https://www.stackoverflow.com")
		
	elif 'open github' in text:
		speak("Here you go to GitHub .  Happy coding",True)
		webbrowser.open("https://www.github.com")
		
	elif 'open gmail' in text:
		webbrowser.open_new_tab("https://mail.google.com/")
		speak("Google Mail open now",True)

	elif 'message' in text:
		speak('Whom do you want to send message ?',True)
		number = record()
		speak('What is the message ?',True)
		message = record()
		speak('Sending message',True)
		pywhatkit.sendwhatmsg_instantly('+91'+number,message,10,'chrome',False)
		speak('Sent',True)
		
	elif 'question' in text:
		speak('I can answer to computational and geographical questions . Ask me .', True)
		question = record()
		app_id = "JT8TUV-LGHQ6Q2UTK "
		client = wolframalpha.Client(app_id)
		res = client.query(question)
		answer = next(res.results).text
		speak(answer,True)

	elif 'flip a coin' in text or 'toss a coin' in text:
		speak("Ok sir , flipping a coin!")
		coin = ['heads', 'tails']
		toss = random.choice(coin)
		speak("I flipped the coin and got " + toss,True)
		
	elif 'roll a dice' in text:
		speak("Ok sir, rolling a dice for you!",True)
		dice = ['1', '2', '3', '4', '5', '6']
		roll = random.choice(dice)
		speak("I rolled a dice and got " + roll,True)
		
	elif 'class' in text:
		speak("Which class do you want do attend ?",True)
		
	elif 'mechatronics and robotics' in text or 'robotics' in text:
		webbrowser.open("https://meet.google.com/nhz-jfnf-bgf")
		
	elif 'python' in text or 'computing with python' in text:
		webbrowser.open("https://meet.google.com/xow-pdxg-jvy")
		
	elif 'cognitive aptitude' in text:
		webbrowser.open("https://meet.google.com/pjw-dkdz-tid")
		
	elif 'mad lab' in text or 'mobile application development' in text:
		webbrowser.open_new_tab("http://meet.google.com/uxp-iauu-avo")
		
	elif "weather" in text:
		api_key = "6295fdcf4580213693535279071b2ce2"
		base_url = "https://api.openweathermap.org/data/2.5/weather?"
		speak("Where do you want me to check the weather ?",True)
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
				 str(weather_description),True)
				 
	elif 'good morning' in text :
		speak('Good Morning',True)
	elif 'good afternoon' in text :
		speak('Good afternoon',True)
	elif 'good evening' in text :
		speak('Good evening',True)
	elif 'good night' in text :
		speak('Good night',True)

	elif 'print' in text:
		speak("What should I type?",True)
		data = record()
		speak('Done',True)
		remember = open('print.txt', 'w')
		remember.write(data)
		remember.close()
		filename = tempfile.mktemp("print.txt")
		open(filename,"w").write(data)
		os.startfile(filename,"print")
	
	elif 'type' in text:
		speak("What should I type?",True)
		data = record()
		speak('Done',True)
		today_date = datetime.date.today()
		today_time = datetime.datetime.now().strftime('%I:%M %p')
		remember = open('data.txt', 'a')
		remember.write('DATE:' + str(today_date) + '\n' + 'TIME:' + today_time + ':    ' + data + '\n' + '\n')
		remember.close()

	elif 'remember' in text:
		remember = open("data.txt",'r')
		speak('you said me to read that' + remember.read(),True)
		remember.close()
		
	elif 'read text file' in text:
		speak('Which text file do you want me to read?',True)
		file_name = record()
		remember = open(file_name + '.txt', 'r')
		speak(remember.read(),True)
		remember.close()

	elif 'log out' in text:
		os.system("shutdown -l")
		
	elif 'shutdown' in text:
		os.system("shutdown /s /t 1")
		
	elif 'restart' in text:
		os.system("shutdown /s /t 1")
		
	elif 'how are you' in text:
		speak("I am fine, Thank you. How are you ?",True)
		
	elif 'fine' in text or "good" in text:
		speak("It's good to know that your fine",True)
		
	elif 'thank you' in text:
		speak("My pleasure sir",True)
		
	elif 'bye' in text or 'exit' in text or 'quit' in text:
		speak("Shutting down the System. Good Bye Sir!",True)
		exit()
		
	elif 'who are you' in text:
		speak("I am Vision, your personal assistant",True)
		
	elif "who made you" in text or "who created you" in text:
		speak("I was created by Shruti,  Akash,  Vishal and Shreyansh  , the S Y 28 Group.",True)





##################################### DELETE USER ACCOUNT #########################################
def deleteUserData():
	result = messagebox.askquestion('Alert', 'Are you sure you want to delete your Face Data ?')
	if result=='no': return
	messagebox.showinfo('Clear Face Data', 'Your face has been cleared\nRegister your face again to use.')
	import shutil
	shutil.rmtree('userData')
	root.destroy()

						#####################
						####### GUI #########
						#####################

############ ATTACHING BOT/USER CHAT ON CHAT SCREEN ###########
def attachTOframe(text,bot=False):
	if bot:
		botchat = Label(chat_frame,text=text, bg=botChatTextBg, fg=botChatText, justify=LEFT, wraplength=250, font=('Montserrat',12, 'bold'))
		botchat.pack(anchor='w',ipadx=5,ipady=5,pady=5)
	else:
		userchat = Label(chat_frame, text=text, bg=userChatTextBg, fg='white', justify=RIGHT, wraplength=250, font=('Montserrat',12, 'bold'))
		userchat.pack(anchor='e',ipadx=2,ipady=2,pady=5)

def clearChatScreen():
	for wid in chat_frame.winfo_children():
		wid.destroy()

### SWITCHING BETWEEN FRAMES ###
def raise_frame(frame):
	frame.tkraise()
	clearChatScreen()

################# SHOWING DOWNLOADED IMAGES ###############
img0, img1, img2, img3, img4 = None, None, None, None, None
def showSingleImage(type, data=None):
	global img0, img1, img2, img3, img4
	try:
		img0 = ImageTk.PhotoImage(Image.open('Downloads/0.jpg').resize((90,110), Image.ANTIALIAS))
	except:
		pass
	img1 = ImageTk.PhotoImage(Image.open('extrafiles/images/heads.jpg').resize((220,200), Image.ANTIALIAS))
	img2 = ImageTk.PhotoImage(Image.open('extrafiles/images/tails.jpg').resize((220,200), Image.ANTIALIAS))
	img4 = ImageTk.PhotoImage(Image.open('extrafiles/images/WeatherImage.png'))

	if type=="weather":
		weather = Frame(chat_frame)
		weather.pack(anchor='w')
		Label(weather, image=img4, bg=chatBgColor).pack()
		Label(weather, text=data[0], font=('Arial Bold', 45), fg='white', bg='#3F48CC').place(x=65,y=45)
		Label(weather, text=data[1], font=('Montserrat', 15), fg='white', bg='#3F48CC').place(x=78,y=110)
		Label(weather, text=data[2], font=('Montserrat', 10), fg='white', bg='#3F48CC').place(x=78,y=140)
		Label(weather, text=data[3], font=('Arial Bold', 12), fg='white', bg='#3F48CC').place(x=60,y=160)

	elif type=="wiki":
		Label(chat_frame, image=img0, bg='#EAEAEA').pack(anchor='w')
	elif type=="head":
		Label(chat_frame, image=img1, bg='#EAEAEA').pack(anchor='w')
	elif type=="tail":
		Label(chat_frame, image=img2, bg='#EAEAEA').pack(anchor='w')
	else:
		img3 = ImageTk.PhotoImage(Image.open('extrafiles/images/dice/'+type+'.jpg').resize((200,200), Image.ANTIALIAS))
		Label(chat_frame, image=img3, bg='#EAEAEA').pack(anchor='w')
	
def showImages(query):
	global img0, img1, img2, img3
	webScrapping.downloadImage(query)
	w, h = 150, 110
	#Showing Images
	imageContainer = Frame(chat_frame, bg='#EAEAEA')
	imageContainer.pack(anchor='w')
	#loading images
	img0 = ImageTk.PhotoImage(Image.open('Downloads/0.jpg').resize((w,h), Image.ANTIALIAS))
	img1 = ImageTk.PhotoImage(Image.open('Downloads/1.jpg').resize((w,h), Image.ANTIALIAS))
	img2 = ImageTk.PhotoImage(Image.open('Downloads/2.jpg').resize((w,h), Image.ANTIALIAS))
	img3 = ImageTk.PhotoImage(Image.open('Downloads/3.jpg').resize((w,h), Image.ANTIALIAS))
	#Displaying
	Label(imageContainer, image=img0, bg='#EAEAEA').grid(row=0, column=0)
	Label(imageContainer, image=img1, bg='#EAEAEA').grid(row=0, column=1)
	Label(imageContainer, image=img2, bg='#EAEAEA').grid(row=1, column=0)
	Label(imageContainer, image=img3, bg='#EAEAEA').grid(row=1, column=1)


############################# WAEM - WhatsApp Email ##################################
def sendWAEM():
	global rec_phoneno, rec_email
	data = WAEMEntry.get()
	rec_email, rec_phoneno = data, data
	WAEMEntry.delete(0, END)
	appControl.Win_Opt('close')
def send(e):
	sendWAEM()

def WAEMPOPUP(Service='None', rec='Reciever'):
	global WAEMEntry
	PopUProot = Tk()
	PopUProot.title(f'{Service} Service')
	PopUProot.configure(bg='white')

	if Service=="WhatsApp": PopUProot.iconbitmap("extrafiles/images/whatsapp.ico")
	else: PopUProot.iconbitmap("extrafiles/images/email.ico")
	w_width, w_height = 410, 200
	s_width, s_height = PopUProot.winfo_screenwidth(), PopUProot.winfo_screenheight()
	x, y = (s_width/2)-(w_width/2), (s_height/2)-(w_height/2)
	PopUProot.geometry('%dx%d+%d+%d' % (w_width,w_height,x,y-30)) #center location of the screen
	Label(PopUProot, text=f'Reciever {rec}', font=('Arial', 16), bg='white').pack(pady=(20, 10))
	WAEMEntry = Entry(PopUProot, bd=10, relief=FLAT, font=('Arial', 12), justify='center', bg='#DCDCDC', width=30)
	WAEMEntry.pack()
	WAEMEntry.focus()

	SendBtn = Button(PopUProot, text='Send', font=('Arial', 12), relief=FLAT, bg='#14A769', fg='white', command=sendWAEM)
	SendBtn.pack(pady=20, ipadx=10)
	PopUProot.bind('<Return>', send)
	PopUProot.mainloop()

######################## CHANGING CHAT BACKGROUND COLOR #########################
def getChatColor():
	global chatBgColor
	myColor = colorchooser.askcolor()
	if myColor[1] is None: return
	chatBgColor = myColor[1]
	colorbar['bg'] = chatBgColor
	chat_frame['bg'] = chatBgColor
	root1['bg'] = chatBgColor
	ChangeSettings(True)

chatMode = 1
def changeChatMode():
	global chatMode
	if chatMode==1:
		# appControl.volumeControl('mute')
		VoiceModeFrame.pack_forget()
		TextModeFrame.pack(fill=BOTH)
		UserField.focus()
		chatMode=0
	else:
		# appControl.volumeControl('full')
		TextModeFrame.pack_forget()
		VoiceModeFrame.pack(fill=BOTH)
		root.focus()
		chatMode=1

############################################## GUI #############################################

def onhover(e):
	userPhoto['image'] = chngPh
def onleave(e):
	userPhoto['image'] = userProfileImg

def UpdateIMAGE():
	global ownerPhoto, userProfileImg, userIcon

	os.system('python ChooseAvatarPIC.py')
	u = UserData()
	u.extractData()
	ownerPhoto = u.getUserPhoto()
	userProfileImg = ImageTk.PhotoImage(Image.open("extrafiles/images/avatars/a"+str(ownerPhoto)+".png").resize((120, 120)))

	userPhoto['image'] = userProfileImg
	userIcon = PhotoImage(file="extrafiles/images/avatars/ChatIcons/a"+str(ownerPhoto)+".png")

def SelectAvatar():	
	Thread(target=UpdateIMAGE).start()


#####################################  MAIN GUI ####################################################

#### SPLASH/LOADING SCREEN ####
def progressbar():
	s = ttk.Style()
	s.theme_use('clam')
	s.configure("white.Horizontal.TProgressbar", foreground='white', background='white')
	progress_bar = ttk.Progressbar(splash_root,style="white.Horizontal.TProgressbar", orient="horizontal",mode="determinate", length=303)
	progress_bar.pack()
	splash_root.update()
	progress_bar['value'] = 0
	splash_root.update()
 
	while progress_bar['value'] < 100:
		progress_bar['value'] += 5
		# splash_percentage_label['text'] = str(progress_bar['value']) + ' %'
		splash_root.update()
		sleep(0.1)

def destroySplash():
	splash_root.destroy()

if __name__ == '__main__':
	splash_root = Tk()
	splash_root.configure(bg='#3895d3')
	splash_root.overrideredirect(True)
	splash_label = Label(splash_root, text="Processing...", font=('montserrat',15),bg='#3895d3',fg='white')
	splash_label.pack(pady=40)
	# splash_percentage_label = Label(splash_root, text="0 %", font=('montserrat',15),bg='#3895d3',fg='white')
	# splash_percentage_label.pack(pady=(0,10))

	w_width, w_height = 400, 200
	s_width, s_height = splash_root.winfo_screenwidth(), splash_root.winfo_screenheight()
	x, y = (s_width/2)-(w_width/2), (s_height/2)-(w_height/2)
	splash_root.geometry('%dx%d+%d+%d' % (w_width,w_height,x,y-30))

	progressbar()
	splash_root.after(10, destroySplash)
	splash_root.mainloop()	

	root = Tk()
	root.title('VISION')
	w_width, w_height = 400, 650
	s_width, s_height = root.winfo_screenwidth(), root.winfo_screenheight()
	x, y = (s_width/2)-(w_width/2), (s_height/2)-(w_height/2)
	root.geometry('%dx%d+%d+%d' % (w_width,w_height,x,y-30)) #center location of the screen
	root.configure(bg=background)
	# root.resizable(width=False, height=False)
	root.pack_propagate(0)

	root1 = Frame(root, bg=chatBgColor)
	root2 = Frame(root, bg=background)
	root3 = Frame(root, bg=background)

	for f in (root1, root2, root3):
		f.grid(row=0, column=0, sticky='news')	
	
	################################
	########  CHAT SCREEN  #########
	################################

	#Chat Frame
	chat_frame = Frame(root1, width=380,height=551,bg=chatBgColor)
	chat_frame.pack(padx=10)
	chat_frame.pack_propagate(0)

	bottomFrame1 = Frame(root1, bg='#dfdfdf', height=100)
	bottomFrame1.pack(fill=X, side=BOTTOM)
	VoiceModeFrame = Frame(bottomFrame1, bg='#dfdfdf')
	VoiceModeFrame.pack(fill=BOTH)
	TextModeFrame = Frame(bottomFrame1, bg='#dfdfdf')
	TextModeFrame.pack(fill=BOTH)

	# VoiceModeFrame.pack_forget()
	TextModeFrame.pack_forget()

	cblLightImg = PhotoImage(file='extrafiles/images/centralButton.png')
	cblDarkImg = PhotoImage(file='extrafiles/images/centralButton1.png')
	if KCS_IMG==1: cblimage=cblDarkImg
	else: cblimage=cblLightImg
	cbl = Label(VoiceModeFrame, fg='white', image=cblimage, bg='#dfdfdf')
	cbl.pack(pady=17)
	AITaskStatusLbl = Label(VoiceModeFrame, text='    Offline', fg='white', bg=AITaskStatusLblBG, font=('montserrat', 16))
	AITaskStatusLbl.place(x=140,y=32)
	
	#Settings Button
	sphLight = PhotoImage(file = "extrafiles/images/setting.png")
	sphLight = sphLight.subsample(2,2)
	sphDark = PhotoImage(file = "extrafiles/images/setting1.png")
	sphDark = sphDark.subsample(2,2)
	if KCS_IMG==1: sphimage=sphDark
	else: sphimage=sphLight
	settingBtn = Button(VoiceModeFrame,image=sphimage,height=30,width=30, bg='#dfdfdf',borderwidth=0,activebackground="#dfdfdf",command=lambda: raise_frame(root2))
	settingBtn.place(relx=1.0, y=30,x=-20, anchor="ne")	
	
	#Keyboard Button
	kbphLight = PhotoImage(file = "extrafiles/images/keyboard.png")
	kbphLight = kbphLight.subsample(2,2)
	kbphDark = PhotoImage(file = "extrafiles/images/keyboard1.png")
	kbphDark = kbphDark.subsample(2,2)
	if KCS_IMG==1: kbphimage=kbphDark
	else: kbphimage=kbphLight
	kbBtn = Button(VoiceModeFrame,image=kbphimage,height=30,width=30, bg='#dfdfdf',borderwidth=0,activebackground="#dfdfdf", command=changeChatMode)
	kbBtn.place(x=25, y=30)

	#Mic
	micImg = PhotoImage(file = "extrafiles/images/mic.png")
	micImg = micImg.subsample(2,2)
	micBtn = Button(TextModeFrame,image=micImg,height=30,width=30, bg='#dfdfdf',borderwidth=0,activebackground="#dfdfdf", command=changeChatMode)
	micBtn.place(relx=1.0, y=30,x=-20, anchor="ne")	
	
	#Text Field
	TextFieldImg = PhotoImage(file='extrafiles/images/textField.png')
	UserFieldLBL = Label(TextModeFrame, fg='white', image=TextFieldImg, bg='#dfdfdf')
	UserFieldLBL.pack(pady=17, side=LEFT, padx=10)
	UserField = Entry(TextModeFrame, fg='white', bg='#203647', font=('Montserrat', 16), bd=6, width=22, relief=FLAT)
	UserField.place(x=20, y=30)
	UserField.insert(0, "Ask me anything...")
	UserField.bind('<Return>', keyboardInput)
	
	#User and Bot Icon
	userIcon = PhotoImage(file="extrafiles/images/avatars/ChatIcons/a"+str(ownerPhoto)+".png")
	botIcon = PhotoImage(file="extrafiles/images/assistant2.png")
	botIcon = botIcon.subsample(2,2)
	

	###########################
	########  SETTINGS  #######
	###########################

	settingsLbl = Label(root2, text='Settings', font=('Arial Bold', 15), bg=background, fg=textColor)
	settingsLbl.pack(pady=10)
	separator = ttk.Separator(root2, orient='horizontal')
	separator.pack(fill=X)
	#User Photo
	userProfileImg = Image.open("extrafiles/images/avatars/a"+str(ownerPhoto)+".png")
	userProfileImg = ImageTk.PhotoImage(userProfileImg.resize((120, 120)))
	userPhoto = Button(root2, image=userProfileImg, bg=background, bd=0, relief=FLAT, activebackground=background, command=SelectAvatar)
	userPhoto.pack(pady=(20, 5))

	#Change Photo
	chngPh = ImageTk.PhotoImage(Image.open("extrafiles/images/avatars/changephoto2.png").resize((120, 120)))
	
	userPhoto.bind('<Enter>', onhover)
	userPhoto.bind('<Leave>', onleave)

	#Username
	userName = Label(root2, text=ownerName, font=('Arial Bold', 15), fg=textColor, bg=background)
	userName.pack()

	#Settings Frame
	settingsFrame = Frame(root2, width=300, height=300, bg=background)
	settingsFrame.pack(pady=20)

	assLbl = Label(settingsFrame, text='Assistant Voice', font=('Arial', 13), fg=textColor, bg=background)
	assLbl.place(x=0, y=20)
	n = StringVar()
	assVoiceOption = ttk.Combobox(settingsFrame, values=('Female', 'Male'), font=('Arial', 13), width=13, textvariable=n)
	assVoiceOption.current(voice_id)
	assVoiceOption.place(x=150, y=20)
	assVoiceOption.bind('<<ComboboxSelected>>', changeVoice)

	voiceRateLbl = Label(settingsFrame, text='Voice Rate', font=('Arial', 13), fg=textColor, bg=background)
	voiceRateLbl.place(x=0, y=60)
	n2 = StringVar()
	voiceOption = ttk.Combobox(settingsFrame, font=('Arial', 13), width=13, textvariable=n2)
	voiceOption['values'] = ('Very Low', 'Low', 'Normal', 'Fast', 'Very Fast')
	voiceOption.current(ass_voiceRate//50-2) #100 150 200 250 300
	voiceOption.place(x=150, y=60)
	voiceOption.bind('<<ComboboxSelected>>', changeVoiceRate)
	
	volumeLbl = Label(settingsFrame, text='Volume', font=('Arial', 13), fg=textColor, bg=background)
	volumeLbl.place(x=0, y=105)
	volumeBar = Scale(settingsFrame, bg=background, fg=textColor, sliderlength=30, length=135, width=16, highlightbackground=background, orient='horizontal', from_=0, to=100, command=changeVolume)
	volumeBar.set(int(ass_volume*100))
	volumeBar.place(x=150, y=85)



	themeLbl = Label(settingsFrame, text='Theme', font=('Arial', 13), fg=textColor, bg=background)
	themeLbl.place(x=0,y=143)
	themeValue = IntVar()
	s = ttk.Style()
	s.configure('Wild.TRadiobutton', font=('Arial Bold', 10), background=background, foreground=textColor, focuscolor=s.configure(".")["background"])
	darkBtn = ttk.Radiobutton(settingsFrame, text='Dark', value=1, variable=themeValue, style='Wild.TRadiobutton', command=changeTheme, takefocus=False)
	darkBtn.place(x=150,y=145)
	lightBtn = ttk.Radiobutton(settingsFrame, text='Light', value=2, variable=themeValue, style='Wild.TRadiobutton', command=changeTheme, takefocus=False)
	lightBtn.place(x=230,y=145)
	themeValue.set(1)
	if KCS_IMG==0: themeValue.set(2)


	chooseChatLbl = Label(settingsFrame, text='Chat Background', font=('Arial', 13), fg=textColor, bg=background)
	chooseChatLbl.place(x=0,y=180)
	cimg = PhotoImage(file = "extrafiles/images/colorchooser.png")
	cimg = cimg.subsample(3,3)
	colorbar = Label(settingsFrame, bd=3, width=18, height=1, bg=chatBgColor)
	colorbar.place(x=150, y=180)
	if KCS_IMG==0: colorbar['bg'] = '#E8EBEF'
	Button(settingsFrame, image=cimg, relief=FLAT, command=getChatColor).place(x=261, y=180)

	backBtn = Button(settingsFrame, text='   Back   ', bd=0, font=('Arial 12'), fg='white', bg='#14A769', relief=FLAT, command=lambda:raise_frame(root1))
	clearFaceBtn = Button(settingsFrame, text='   Clear Facial Data   ', bd=0, font=('Arial 12'), fg='white', bg='#14A769', relief=FLAT, command=deleteUserData)
	backBtn.place(x=5, y=250)
	clearFaceBtn.place(x=120, y=250)

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