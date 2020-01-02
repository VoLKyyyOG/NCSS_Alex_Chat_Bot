import random, requests, json
from flask import Flask, request, jsonify
from appid import *

app = Flask(__name__)

@app.route('/ack', methods=['GET', 'POST'])
def ack():
  # Create a message to send to the server
  message = {
	'author': 'ACK',
	'text': f'I got your message',
  }

  # Return the JSON
  return jsonify(message)

@app.route('/echo', methods=['POST'])
def echo():
  # Read the message from NeCSuS
  data = request.get_json()
  text = data.get('text').split()[1:]

  # Create a message to send to the server
  message = {
    'author': 'ECHO',
    'text': f'You said: {" ".join(text)}',
  }

  # Return the JSON
  return jsonify(message)

@app.route('/roll', methods=['POST'])
def roll():
  # Get the message data from NeCSuS
  data = request.get_json()
  author = data.get('author', 'Someone')
  command = data.get('text', '')
  sides = int(command.split()[-1])

  # Reply to the message
  message = {
    'author': 'GAMBLE',
    'text': f'{author} rolled a {sides} sided dice and got a {random.randint(1, sides)}.',
  }

  # Return the JSON
  return jsonify(message)

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

@app.route('/weather', methods=['POST'])
def weather():
    data = request.get_json()
    response = json.loads(requests.get('http://api.openweathermap.org/data/2.5/weather',
                            params = dict(q="Melbourne", APPID=KEY_WEATHER, units="metric")
                            ).text)

    temp = response["main"]
    attr = response["weather"][0]

    if attr['main'] == "Clear":
        text = f"Today, the weather is {attr['main']} with a maximum temperature of {temp['temp_max']} degrees."
    else:
        text = f"Today, there will be some {attr['main']} with a maximum temperature of {temp['temp_max']} degrees."

    message = {
        'author': 'WEATHER',
        'text': text
    }

    return jsonify(message)
  
@app.route('/wolfram', methods=['POST'])
def wolfram():
    data = request.get_json()
    q = data.get('text','').split()[-1]
    response = requests.get(f'http://api.wolframalpha.com/v2/query?input={q}&appid={KEY_WOLFRAM}').text

    message = {
        'author': 'WOLFRAM',
        'text': response
    }

    return jsonify(message)

@app.route('/japan_place', methods=['POST'])
def find():
    data = request.get_json()
    command = data.get('text').split(",")
    query, loc = ''.join(command[0].split()[1:]), ''.join(command[1])

    URL1 = f"https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={loc},JP&inputtype=textquery&key={API_KEY}"

    placeid = requests.get(URL1).json()['candidates'][0]['place_id']
    URL2 = f"https://maps.googleapis.com/maps/api/place/details/json?placeid={placeid}&key={API_KEY}"

    response = requests.get(URL2).json()
    coord = ','.join(str(i) for i in response['result']['geometry']['location'].values())

    URL3 = f"https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={query}&inputtype=textquery&fields=formatted_address,name,opening_hours,rating&locationbias=circle:2000@{coord}&key={API_KEY}"

    response = requests.get(URL3).json()['candidates'][0]


    name = response['name']
    rating = response['rating']
    address = []

    for word in response['formatted_address'].split(', '):
        if not "Tokyo" in word and not "Japan" in word:
            address.append(word)

    message = {
        'author': 'JAP_BOT',
        'text': f"The closest place is {name} with a {rating} star rating. They are located at {', '.join(address)}."
    }

    return jsonify(message)


app.run(host='0.0.0.0')
