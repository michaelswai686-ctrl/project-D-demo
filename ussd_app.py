from flask import Flask, request, jsonify
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

# In-memory session storage (for demonstration purposes)
# In a real app, use Redis or a database
sessions = {}

def get_menu(level, input_data=None):
    menus = {
        "main": "Welcome to TZ Service!\n1. My Account\n2. Services\n3. Contact Us\n0. Exit",
        "account": "My Account:\n1. Check Balance\n2. My Profile\n99. Back",
        "services": "Our Services:\n1. Internet Bundles\n2. Voice Bundles\n99. Back",
        "contact": "Contact Us:\nEmail: support@tzservice.co.tz\nPhone: +255 700 000 000\n99. Back",
        "balance": "Your balance is TZS 5,000.\n99. Back",
        "profile": "Name: John Doe\nNumber: {msisdn}\n99. Back",
        "internet": "Internet Bundles:\n1. 1GB - 2000/=\n2. 5GB - 7000/=\n99. Back",
        "voice": "Voice Bundles:\n1. 50 Min - 1000/=\n2. 200 Min - 3000/=\n99. Back",
        "exit": "Thank you for using TZ Service. Goodbye!"
    }
    return menus.get(level, menus["main"])

@app.route('/ussd', methods=['POST'])
def ussd_callback():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    msisdn = data.get('msisdn')
    session_id = data.get('session_id')
    command = data.get('command')
    user_input = data.get('payload', {}).get('response', '0')

    logging.info(f"Received USSD: msisdn={msisdn}, session_id={session_id}, command={command}, input={user_input}")

    # Initialize session if it's a new request
    if command == 'initiate':
        sessions[session_id] = {'level': 'main'}
        response_text = get_menu('main')
        next_command = 'continue'
    elif session_id not in sessions:
        # If session not found but not initiate, start from main
        sessions[session_id] = {'level': 'main'}
        response_text = get_menu('main')
        next_command = 'continue'
    else:
        current_level = sessions[session_id]['level']
        
        # Simple State Machine Logic
        if current_level == 'main':
            if user_input == '1':
                sessions[session_id]['level'] = 'account'
                response_text = get_menu('account')
                next_command = 'continue'
            elif user_input == '2':
                sessions[session_id]['level'] = 'services'
                response_text = get_menu('services')
                next_command = 'continue'
            elif user_input == '3':
                sessions[session_id]['level'] = 'contact'
                response_text = get_menu('contact')
                next_command = 'continue'
            elif user_input == '0':
                response_text = get_menu('exit')
                next_command = 'terminate'
                del sessions[session_id]
            else:
                response_text = "Invalid option.\n" + get_menu('main')
                next_command = 'continue'
        
        elif current_level == 'account':
            if user_input == '1':
                sessions[session_id]['level'] = 'balance'
                response_text = get_menu('balance')
                next_command = 'continue'
            elif user_input == '2':
                sessions[session_id]['level'] = 'profile'
                response_text = get_menu('profile').format(msisdn=msisdn)
                next_command = 'continue'
            elif user_input == '99':
                sessions[session_id]['level'] = 'main'
                response_text = get_menu('main')
                next_command = 'continue'
            else:
                response_text = "Invalid option.\n" + get_menu('account')
                next_command = 'continue'

        elif current_level in ['services', 'internet', 'voice']:
            if current_level == 'services':
                if user_input == '1':
                    sessions[session_id]['level'] = 'internet'
                    response_text = get_menu('internet')
                elif user_input == '2':
                    sessions[session_id]['level'] = 'voice'
                    response_text = get_menu('voice')
                elif user_input == '99':
                    sessions[session_id]['level'] = 'main'
                    response_text = get_menu('main')
                else:
                    response_text = "Invalid option.\n" + get_menu('services')
            else: # internet or voice submenus
                if user_input == '99':
                    sessions[session_id]['level'] = 'services'
                    response_text = get_menu('services')
                else:
                    response_text = "Request processed.\n99. Back"
            next_command = 'continue'

        elif current_level in ['contact', 'balance', 'profile']:
            if user_input == '99':
                sessions[session_id]['level'] = 'main' if current_level == 'contact' else 'account'
                response_text = get_menu(sessions[session_id]['level'])
                next_command = 'continue'
            else:
                response_text = "Invalid option.\n99. Back"
                next_command = 'continue'
        
        else:
            response_text = get_menu('main')
            next_command = 'continue'
            sessions[session_id]['level'] = 'main'

    response_data = {
        "msisdn": msisdn,
        "operator": data.get('operator', 'vodacom'),
        "session_id": session_id,
        "command": next_command,
        "payload": {
            "request_id": data.get('payload', {}).get('request_id', '0'),
            "response": response_text
        }
    }
    
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
