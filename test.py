import random, requests, json
from flask import Flask, request, jsonify

KEY_WEATHER = "f4ae90e2d9ebd6134141f4509741c3d8"
KEY_WOLFRAM = "GERJER-AYYEHAG4UX"
API_KEY = "AIzaSyCbghCD_G0nXdxIKFzoBDctLwUNqsW7Ma4"

app = Flask(__name__)

@app.route('/fact', methods=['POST'])
def fact():
    data = request.get_json()
    num = data.get('text','').split()[-1]
    response = requests.get(f'http://numbersapi.com/{num}').text

    message = {
        'author': 'FACTS',
        'text': response
    }
    
    return jsonify(message)   

@app.route('/insult', methods=['POST'])
def insult():
    data = request.get_json()
    name = data.get('text','').split()[-1]
    response = requests.get("https://insult.mattbas.org/api/insult").text.split()[2:]

    message = {
        'author': 'SIT DOWN',
        'text': f"{name.title()} is {' '.join(response)}."
    }

    if name.casefold() == "sakthi":
        message['text'] = "Hi suckthi - hahaha did you get that?"
    
    return jsonify(message)   

@app.route('/apologize', methods=['POST'])
def sorry():
    data = request.get_json()
    name = data.get('text','').split()[-1]

    message = {
        'author': 'IM SORRY',
        'text': f"{name.title()}, I apologize on behalf of insult bot."
    }

    if name.casefold() == "sakthi":
        message['text'] = "Sorry not sorry."
    
    return jsonify(message)  


@app.route('/weather', methods=['POST'])
def weather():
    loc = 'sydney'
    data = request.get_json()
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

    message = {
        'author': 'WEATHER',
        'text': weather
    }

    return jsonify(message)

@app.route('/find', methods=['POST'])
def find():
    data = request.get_json()
    command = data.get('text').split(",")
    
    try:
        query, loc, code = ''.join(command[0].split()[1:]), ''.join(command[1]), command[2]
    except:
        message = {
        'author': 'FINDER',
        'text': "The usage for this bot is: `find PLACE/QUERY, LOCATION, COUNTRY`."
        }
        return message

    # TODO allow a country to be specified
    URL1 = f"https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={loc},{code}&inputtype=textquery&key={API_KEY}"

    placeid = requests.get(URL1).json()['candidates'][0]['place_id']
    URL2 = f"https://maps.googleapis.com/maps/api/place/details/json?placeid={placeid}&key={API_KEY}"

    response = requests.get(URL2).json()
    coord = ','.join(str(i) for i in response['result']['geometry']['location'].values())

    URL3 = f"https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={query}&inputtype=textquery&fields=formatted_address,name,opening_hours,rating&locationbias=circle:2000@{coord}&key={API_KEY}"

    response = requests.get(URL3).json()['candidates'][0]

    name = response['name']
    rating = response['rating']
    address = []

    # a shit way of shortening the address (instead of including the city and country too)
    for word in response['formatted_address'].split(', '):
        if not code.casefold() in word.casefold():
            address.append(word)

    message = {
        'author': 'FINDER',
        'text': f"The closest place is {name} with a {rating} star rating. They are located at {', '.join(address)}."
    }

    return jsonify(message)

# Broken!!!
@app.route('/wolfram', methods=['POST'])
def wolfram():
    data = request.get_json()
    q = data.get('text','').split()[1:]

    print('+'.join(q))

    response = requests.get(f"http://api.wolframalpha.com/v1/spoken?appid={KEY_WOLFRAM}&i={'+'.join(q)}%3f&units=metric").text

    if "did not understand" in response or "spoken results available" in response:
        response = "Please Try Again!"

    message = {
        'author': 'WOLFRAM',
        'text': response
    }


    return jsonify(message)

app.run(host='0.0.0.0')
