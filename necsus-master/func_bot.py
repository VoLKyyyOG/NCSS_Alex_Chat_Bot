import random, requests, json
from flask import Flask, request, jsonify
from appid import KEY_WEATHER


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
    num = data.get('text','').split()[-1]
    response = json.loads(requests.get('http://api.openweathermap.org/data/2.5/weather',
                            params = dict(q="Melbourne", APPID=KEY_WEATHER, units="metric")
                            ).text)

    temp = response["main"]
    attr = response["weather"][0]

    message = {
        'author': 'WEATHER',
        'text': f"Today, there will be some {attr['main']} where it is expected to feel like {temp['feels_like']} degrees."
    }

    return jsonify(message)
  
app.run(host='0.0.0.0')
