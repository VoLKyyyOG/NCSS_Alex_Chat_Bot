from keys import *
from geotext import GeoText
import requests, json, datetime, pytz

def fact(num):
    if not num.isdigit():
        text = "Try again with a valid number!"
    else:
        text = requests.get(f'http://numbersapi.com/{num}').text

    msg = {"type": "SSML",
        "ssml": 
        f'''
        <speak>
            <voice name="Brian">
                <lang xml:lang="en-GB">
                    {text}
                </lang>
            </voice>
        </speak>
        '''
    }

    return msg

#######################
#######################
#######################

def respect():
    msg = {"type": "SSML",
        "ssml": 
        f'''
        <speak>
            <voice name="Brian">
                <lang xml:lang="en-GB">
                    F in the chat. 
                </lang>
            </voice>
        </speak>
        '''
    }

    return msg

#######################
#######################
#######################

def wolfram(QUERY, command):
    q = "+".join(command.split())

    text = requests.get(f"http://api.wolframalpha.com/v1/spoken?appid={KEY_WOLFRAM}&i={q}%3f&units=metric").text

    if "did not understand" in text or "spoken result available" in text:
        text = "I'm unable to answer this at the moment. Shall I consult Bing? Nah, I'm joking - I can ask Duck Duck Go if you would like?"
        QUERY = q

    msg = {"type": "SSML",
        "ssml": 
        f'''
        <speak>
            <voice name="Brian">
                <lang xml:lang="en-GB">
                    {text}.
                </lang>
            </voice>
        </speak>
        '''
    }

    return QUERY, msg

def search(q):
    msg = {
        "type": "SSML",
        "ssml": 
        f'''
        <speak>
            <voice name="Brian">
                <lang xml:lang="en-GB">
                    You see, I actually can't do this yet, oops.
                </lang>
            </voice>
        </speak>
        '''
    }

    return msg

#######################
#######################
#######################

def greeting_iron_man(loc, greeting):
    # Get current time given location
    tzone = pytz.timezone(f'Australia/{loc.title()}')
    time = datetime.datetime.now(tzone).strftime("%I:%M %p").replace('PM','P.M.').replace('AM','A.M.')

    # Get current weather given location
    response = requests.get(f"https://api.openweathermap.org/data/2.5/forecast/daily?q={loc},AU&cnt=1&APPID={KEY_WEATHER}&units=metric").json()

    main = response['list'][0]
    temp = int(main['temp']['max'])
    wtype = main['weather'][0]['main']
    fdesc = main['weather'][0]['description']

    if wtype == "Clear":
        desc = f"and the {fdesc}"
    elif wtype == "Clouds":
        desc = f"with {fdesc}"
    elif wtype == "Rain":
        desc = f"with {fdesc}"
    else:
        desc = ""

    weather = f'''
    The weather in {loc.title()} is currently {temp} degrees {desc}.
    '''

    # Get news (thanks news.api)
    response = requests.get(f"https://newsapi.org/v2/top-headlines?country=au&apiKey={NEWS_KEY}").json()
    article = [i for i in response['articles'] if i['description'] != None][0]
    source, desc = article['source']['name'], article['description']

    news = f'''
    From {source} this morning, {desc}
    '''

    # GREETING
    text = f'''
    {greeting.title()}. <break time="0.25s"/> It's {time} <break time="0.25s"/> {weather} <break time="0.25s"/> {news}
    '''
    msg = {
        "type": "SSML",
        "ssml": 
        f'''
        <speak>
            <voice name="Brian">
                <lang xml:lang="en-GB">
                    {text}
                </lang>
            </voice>
        </speak>
        '''
    }

    return msg

#######################
#######################
#######################

def weather(loc):
    response = requests.get(f"https://api.openweathermap.org/data/2.5/forecast/daily?q={loc},AU&cnt=1&APPID={KEY_WEATHER}&units=metric").json()

    main = response['list'][0]
    temp = int(main['temp']['max'])
    wtype = main['weather'][0]['main']
    fdesc = main['weather'][0]['description']

    if wtype == "Clear":
        desc = f"and the {fdesc}"
    elif wtype == "Clouds":
        desc = f"with {fdesc}"
    elif wtype == "Rain":
        desc = f"with {fdesc}"
    else:
        desc = ""

    text = f'''
    The weather in {loc.title()} is currently {temp} degrees {desc}.
    '''
    msg = {
        "type": "SSML",
        "ssml": 
        f'''
        <speak>
            <voice name="Brian">
                <lang xml:lang="en-GB">
                    {text}
                </lang>
            </voice>
        </speak>
        '''
    }

    return msg

#######################
#######################
#######################

def set_loc(LOCATION, loc):
    from city import cities
    if loc.casefold() in cities:
        return (loc.title(), True)
    return ('Melbourne', False)

def loc_confirm(LOCATION, conf):
    if conf:
        text = f"Location has been updated to {LOCATION}."
    else:
        text = f"An invalid location was given, so the location was set to Melbourne by default."
    
    msg = {
        "type": "SSML",
        "ssml": 
        f'''
        <speak>
            <voice name="Brian">
                <lang xml:lang="en-GB">
                    {text}
                </lang>
            </voice>
        </speak>
        '''
    }

    return msg

#######################
#######################
#######################

def news(category):
    # news api.org
    response = requests.get(f"https://newsapi.org/v2/top-headlines?q={category}&language=en&sortBy=popularity&apiKey={NEWS_KEY}").json()

    numArticles = response.get('totalResults', 0)

    if numArticles == 0:
        response = requests.get(f"https://newsapi.org/v2/everything?q={category}&language=en&sortBy=popularity&apiKey={NEWS_KEY}").json()

        numArticles = response['totalResults']
        
        # retry with everything category
        if numArticles == 0:
            text = "There are no articles corresponding to your specified category. Would you like to try again?"
        else:
            print("Using everything parameter")
            article = [i for i in response['articles'] if i['description'] != None][0]
            source, desc, title = article['source']['name'], article['description'], article['title']

            text = f'''
            From {source}, the most trending article is quote; {title}. Here's a short description; {desc}
            '''

    else:
        article = [i for i in response['articles'] if i['description'] != None][0]
        source, desc, title = article['source']['name'], article['description'], article['title']

        text = f'''
        From {source}, the most trending article is quote; {title}. Here's a short description; {desc}
        '''

    msg = {
        "type": "SSML",
        "ssml": 
        f'''
        <speak>
            <voice name="Brian">
                <lang xml:lang="en-GB">
                    {text}
                </lang>
            </voice>
        </speak>
        '''
    }

    return msg



