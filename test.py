from flask import Flask, jsonify
app = Flask('app')

@app.route('/ack', methods=['GET', 'POST'])
def ack():
  # Create a message to send to the server
  message = {
	'author': 'ACK bot',
	'text': f'I got your message',
  }

  # Return the JSON
  return jsonify(message)

app.run(host='0.0.0.0')