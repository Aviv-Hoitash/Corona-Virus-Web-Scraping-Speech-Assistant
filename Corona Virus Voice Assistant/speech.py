import playsound #To let the computer talk
import speech_recognition as sr #to understand speech input
from gtts import gTTS #to get speech input
import datetime #to handle the speech files
import os #to handle the speech files
from data import * #Importing the data that was created in the other file

WAKE = "hey Tosh" #The wake(what to say to make the computer take input, you can change this and nothing will change just remember what the wake is and it has to have hey or some word that isn't in the name)

#List of countries
country_lists = ['north america', 'south america', 'europe', 'asia', 'africa', 'oceania', 'world', 'usa', 'brazil',
                 'russia', 'spain', 'uk', 'italy', 'france', 'germany', 'india', 'turkey', 'peru', 'iran', 'chile',
                 'canada', 'mexico', 'saudi arabia', 'pakistan', 'belgium', 'qatar', 'netherlands', 'bangladesh',
                 'belarus', 'ecuador', 'sweden', 'singapore', 'uae', 'portugal', 'south africa', 'switzerland',
                 'colombia', 'kuwait', 'indonesia', 'ireland', 'poland', 'egypt', 'ukraine', 'romania', 'philippines',
                 'israel', 'dominican republic', 'japan', 'austria', 'argentina', 'afghanistan', 'panama', 'denmark',
                 'south korea', 'serbia', 'kazakhstan', 'bahrain', 'oman', 'nigeria', 'bolivia', 'algeria', 'czechia',
                 'armenia', 'norway', 'moldova', 'morocco', 'ghana', 'malaysia', 'australia', 'finland', 'iraq',
                 'cameroon', 'azerbaijan', 'honduras', 'sudan', 'guatemala', 'luxembourg', 'hungary', 'tajikistan',
                 'guinea', 'uzbekistan', 'senegal', 'djibouti', 'thailand', 'drc', 'greece', 'ivory coast', 'gabon',
                 'bulgaria', 'bosnia and herzegovina', 'el salvador', 'croatia', 'north macedonia', 'cuba', 'somalia',
                 'kenya', 'estonia', 'haiti', 'iceland', 'kyrgyzstan', 'mayotte', 'maldives', 'lithuania', 'sri lanka',
                 'slovakia', 'new zealand', 'slovenia', 'venezuela', 'nepal', 'equatorial guinea', 'guinea-bissau',
                 'mali', 'lebanon', 'albania', 'hong kong', 'tunisia', 'latvia', 'ethiopia', 'zambia', 'costa rica',
                 'south sudan', 'paraguay', 'car', 'niger', 'cyprus', 'sierra leone', 'burkina faso', 'uruguay',
                 'andorra', 'chad', 'nicaragua', 'madagascar', 'georgia', 'jordan', 'diamond princess', 'san marino',
                 'malta', 'jamaica', 'congo', 'channel islands', 'tanzania', 'mauritania', 'sao tome and principe',
                 'french guiana', 'réunion', 'palestine', 'taiwan', 'togo', 'cabo verde', 'uganda', 'rwanda',
                 'isle of man', 'mauritius', 'vietnam', 'montenegro', 'yemen', 'eswatini', 'liberia', 'malawi',
                 'mozambique', 'myanmar', 'benin', 'martinique', 'faeroe islands', 'mongolia', 'zimbabwe', 'gibraltar',
                 'guadeloupe', 'guyana', 'brunei', 'cayman islands', 'bermuda', 'libya', 'cambodia', 'syria',
                 'trinidad and tobago', 'comoros', 'bahamas', 'aruba', 'monaco', 'barbados', 'angola', 'liechtenstein',
                 'sint maarten', 'burundi', 'french polynesia', 'macao', 'bhutan', 'saint martin', 'eritrea',
                 'botswana', 'st. vincent grenadines', 'antigua and barbuda', 'gambia', 'timor-leste', 'grenada',
                 'namibia', 'curaçao', 'laos', 'new caledonia', 'belize', 'fiji', 'saint lucia', 'dominica',
                 'saint kitts and nevis', 'suriname', 'falkland islands', 'greenland', 'turks and caicos',
                 'vatican city', 'montserrat', 'seychelles', 'ms zaandam', 'western sahara', 'british virgin islands',
                 'papua new guinea', 'caribbean netherlands', 'st. barth', 'anguilla', 'lesotho',
                 'saint pierre miquelon', 'china']

#List of columns
column_names = ["country", "total cases", "new cases", "total deaths", "new deaths", "total recovered",
                "active cases", "critical cases", "cases per million people", "deaths per million people",
                "total tests", "tests per million people", "population"]

#Function to speak
def speak(text):
    tts = gTTS(text=text, lang="en") #Creats a text to speech object that speaks the text input in englis
    
    #Creats a filename whith the time in it so it can never be repeated
    date_string = datetime.datetime.now().strftime("%d%m%Y%H%M%S")
    filename = "voice" + date_string + ".mp3"
    tts.save(filename)
    playsound.playsound(filename)#playsound plays the mp3 file created by the text to speech object
    os.remove(filename) #deletes the file


#Function to get audio input
def get_audio():
    r = sr.Recognizer() #creats a recognizer object
    with sr.Microphone() as source: #using the users michrophone
        audio = r.listen(source) #audio is the recognizer object listing to the source which is the michrophone
        said = ""

        try: #put in a try and except block because there can be many errors like not having a mic or using headphones which won't work
            said = r.recognize_google(audio) #said is the recognized text of audio 
            print(said)
        except Exception as e:
            pass

    return said #Return what the user said so that the computer can use it later to speak

specific = False
asking = True

while asking: #runs forever until broken
    text = get_audio() #Listens for user speech
    print("I'm Listening")
    if text.count(WAKE) > 0: #if the computer hears the wake text
        speak("Talk please") #lets user know that the computer heard them
        print("Talk Please")
        text = get_audio() #listens again

        if text == "quit":
            print("Program Quit")
            asking = False
        
        for country in country_lists:
            if country in text.lower(): #if the user said a country
                for col in column_names:
                    if col in text: #if the user said any of the columns
                        print("getting data....")
                        speech_data = get_data(country,col.title())#use the get_data function from the other file to return the country and data
                        print(speech_data)
                        speak(speech_data) #speak the data
                        specific = True #the user wanted a specific column
                        break
                    else:
                        specific = False #the user did not want a specific coulumn

                if not specific: #if the user did not want a specific column
                    print("getting data....")
                    speech_data = get_data(country) # the data is assumed to be all of the columns
                    print(speech_data)
                    speak(speech_data) #speak the data 
                    break

        #Simple questions and answers
        if "hello" in text:
            speak("hello, how are you?")
            print("hello, how are you")

        if "what is your name" in text.lower():
            speak("My name is{}".format(WAKE.split[1::]))
            print("My name is{}".format(WAKE.split[1::]))
            
