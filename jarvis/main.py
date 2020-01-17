from flask import Flask, jsonify, request
from funcs import *
import re

LOCATION = 'Melbourne'
QUERY = 'JARVIS define gravity'

app = Flask(__name__)

def parse(data, request_type):
    global LOCATION, QUERY

    print(request_type)

    #######################
    # INITIAL LAUNCH REQUEST
    if request_type == "LaunchRequest":
        msg = {
        "type": "SSML",
        "ssml": 
        f'''
        <speak>
            <voice name="Brian">
                <lang xml:lang="en-GB">
                    JARVIS is now on standby.
                </lang>
            </voice>
        </speak>
        '''
        }

        return msg
    #######################
    # END REQUEST
    if request_type == "SessionEndedRequest":
        msg = {
        "type": "SSML",
        "ssml": 
        f'''
        <speak>
            <voice name="Brian">
                <lang xml:lang="en-GB">
                    JARVIS is now shutting down. I will talk to you later sir.
                </lang>
            </voice>
        </speak>
        '''
        }

        return msg
    

    #######################
    # QUERY REQUEST
    if request_type == 'IntentRequest':
        msg = {"type": "SSML",
                    "ssml": 
                    f'''
                    <speak>
                        <voice name="Brian">
                            <lang xml:lang="en-GB">
                                Oops. You probably gave an invalid command sir. Please try again.
                            </lang>
                        </voice>
                    </speak>
                    '''
        }
        # ENSURE THIS WORKS FIRST
        try:
            intent = data['request']['intent']['slots']
            command = intent['instructions']['value'].casefold()
        except:
            print(data['request'])
            return msg
        #######################
        # LIST ALL HELP FUNCTIONS
        token = re.match('.*((what can)|help|list).*', command)
        if token and token.group(1):
            msg = {
            "type": "SSML",
            "ssml": 
            f'''
            <speak>
                <voice name="Brian">
                    <lang xml:lang="en-GB">
                        Hi, I am JARVIS, your personal assistant. I can do a weather check, update locations within Australia, query Wolfram Alpha and pay respects if required.
                    </lang>
                </voice>
            </speak>
            '''
            }
            return msg

        #######################
        # WEATHER BOT
        token = re.match('.*(weather).*', command)
        if token:
            msg = weather(LOCATION)
        #######################
        # REPLY TO WOLFRAM TO SEARCH
        token = re.match('.*(yes|search|(do it)).*', command)
        if token and token.group(1):
            msg = search(QUERY)
        #######################
        # LOCATION CHANGER
        token = re.match('.*(set|update|change|make).*(location|area|city|state|place) (to) .*', command)
        if token and token.group(1):
            match = token.group(3)
            idx = command.index(match)+len(match)+1
            loc = command[idx:]
            LOCATION, conf = set_loc(LOCATION, loc)
            msg = loc_confirm(LOCATION, conf)
        #######################
        # NUMBER FACT
        token = re.match('.*(fact).*(on|number|digit|integer|value).*[0-9]*.*', command)
        if token and token.group(1):
            match = token.group(2)
            idx = command.index(match)+len(match)+1
            num = command[idx:]
            msg = fact(num)
        #######################
        # WOLFRAM ALPHA
        token = re.match(".*((what is)|define|(where is)|whats|what's).*", command)
        if token and token.group(1):
            QUERY, msg = wolfram(QUERY, command)
        #######################
        # NEWS 
        token = re.match('.*(news).*(in|for|on|about|regarding).*', command)
        if token and token.group(1):
            match = token.group(2)
            idx = command.index(match)+len(match)+1
            category = command[idx:]
            msg = news(category)
        #######################
        # IRON MAN STYLE GREETING
        token = re.match('.*((good (morning|afternoon|evening|arvo))|(inform me)).*', command)
        if token and token.group(1):
            greeting = token.group(1)
            if greeting == "inform me":
                greeting = "Hello"
            msg = greeting_iron_man(LOCATION, greeting)
        #######################
        # PAY RESPECTS BOT
        token = re.match('.*(respec[ct]).*', command)
        if token and token.group(1):
            msg = respect()
        
    return msg

@app.route('/', methods=['POST'])
def jarvis():
    # Get Data
    data = request.get_json()
    request_type = data['request']['type']

    # Verify Request Type
    msg = parse(data, request_type)

    # Compile message to send back
    final = {
    "version": "0.1",
    "response": {
        "outputSpeech": msg,
        "shouldEndSession": False
        }
    }

    return jsonify(final)

# Repl.it specific config
app.run(host='0.0.0.0')


