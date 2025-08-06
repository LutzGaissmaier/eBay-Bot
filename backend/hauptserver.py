import os
import json
import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from dotenv import load_dotenv
import threading
import base64

app = Flask(__name__)
CORS(app)

# .env laden
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

# === API ENDPUNKTE ===

# eBay-Konfiguration (aus Umgebungsvariablen)
EBAY_CONFIG = {
    'client_id': os.getenv('EBAY_APP_ID', 'your_ebay_app_id_here'),
    'client_secret': os.getenv('EBAY_CERT_ID', 'your_ebay_cert_id_here'),
    'dev_id': os.getenv('EBAY_DEV_ID', 'your_ebay_dev_id_here'),
    'auth_token': os.getenv('EBAY_AUTH_TOKEN', ''),
}

# Logging-Konfiguration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('backend.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Beispiel-Logging in TokenManager und Endpunkten:
# logger.info('Nachricht') / logger.error('Fehler')

# Beispiel: Logging in TokenManager anpassen
TOKENS_FILE = 'tokens.json'
tokens_lock = threading.Lock()

def lade_tokens():
    if not os.path.exists(TOKENS_FILE):
        return []
    with tokens_lock, open(TOKENS_FILE, 'r') as f:
        return json.load(f)

def speichere_tokens(tokens):
    with tokens_lock, open(TOKENS_FILE, 'w') as f:
        json.dump(tokens, f, indent=2, ensure_ascii=False)

def get_aktiver_token():
    tokens = lade_tokens()
    for t in tokens:
        if t.get('active'):
            return t
    return tokens[0] if tokens else None

@app.route('/api/tokens', methods=['GET'])
def list_tokens():
    return jsonify(lade_tokens())

@app.route('/api/tokens', methods=['POST'])
def add_token():
    data = request.get_json()
    name = data.get('name')
    access_token = data.get('access_token')
    refresh_token = data.get('refresh_token')
    if not name or not access_token:
        return jsonify({'error': 'Name und Access Token erforderlich'}), 400
    tokens = lade_tokens()
    for t in tokens:
        t['active'] = False
    new_token = {
        'name': name,
        'access_token': access_token,
        'refresh_token': refresh_token,
        'active': True
    }
    tokens.append(new_token)
    speichere_tokens(tokens)
    return jsonify({'success': True, 'tokens': tokens})

@app.route('/api/tokens/<name>', methods=['DELETE'])
def delete_token(name):
    tokens = lade_tokens()
    tokens = [t for t in tokens if t['name'] != name]
    if tokens:
        tokens[0]['active'] = True
    speichere_tokens(tokens)
    return jsonify({'success': True, 'tokens': tokens})

@app.route('/api/tokens/activate/<name>', methods=['POST'])
def activate_token(name):
    tokens = lade_tokens()
    found = False
    for t in tokens:
        t['active'] = (t['name'] == name)
        if t['active']:
            found = True
    if not found:
        return jsonify({'error': 'Token nicht gefunden'}), 404
    speichere_tokens(tokens)
    return jsonify({'success': True, 'tokens': tokens})

@app.route('/api/tokens/refresh/<name>', methods=['POST'])
def refresh_token(name):
    tokens = lade_tokens()
    token = next((t for t in tokens if t['name'] == name), None)
    if not token or not token.get('refresh_token'):
        return jsonify({'error': 'Kein Refresh Token für diesen Account'}), 400
    # eBay OAuth Refresh Flow
    url = "https://api.sandbox.ebay.com/identity/v1/oauth2/token"
    client_id = EBAY_CONFIG['client_id']
    client_secret = EBAY_CONFIG['client_secret']
    b64_creds = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {b64_creds}",
    }
    data = {
        "grant_type": "refresh_token",
        "refresh_token": token['refresh_token'],
        "scope": "https://api.ebay.com/oauth/api_scope"
    }
    try:
        import requests
        response = requests.post(url, headers=headers, data=data, timeout=15)
        if response.status_code == 200:
            token_data = response.json()
            token['access_token'] = token_data.get('access_token')
            token['last_refresh'] = datetime.now().isoformat()
            token['refresh_error'] = None
            speichere_tokens(tokens)
            return jsonify({'success': True, 'access_token': token['access_token'], 'expires_in': token_data.get('expires_in')})
        else:
            token['refresh_error'] = f"HTTP {response.status_code}: {response.text[:200]}"
            speichere_tokens(tokens)
            return jsonify({'error': 'Refresh fehlgeschlagen', 'details': response.text}), 400
    except Exception as e:
        token['refresh_error'] = str(e)
        speichere_tokens(tokens)
        return jsonify({'error': str(e)}), 500

# Für alle eBay-API-Calls: aktiven Token verwenden
class TokenManager:
    def __init__(self):
        self.refresh_token = None
        self.token_expires_at = None
        self.last_check = None
        self.is_valid = False
        self.auto_refresh_enabled = False
        self.load_token_data()

    def load_token_data(self):
        aktiver = get_aktiver_token()
        if aktiver:
            self.access_token = aktiver['access_token']
            self.refresh_token = aktiver.get('refresh_token')
        else:
            self.access_token = ''
            self.refresh_token = None

    def save_token_data(self):
        pass  # Tokens werden zentral verwaltet

    def test_token(self):
        self.load_token_data()
        if not self.access_token:
            logger.warning('Kein Access Token vorhanden.')
            return False
        xml_request = f'''<?xml version="1.0" encoding="utf-8"?>\n<GetUserRequest xmlns="urn:ebay:apis:eBLBaseComponents">\n    <RequesterCredentials>\n        <eBayAuthToken>{self.access_token}</eBayAuthToken>\n    </RequesterCredentials>\n    <Version>967</Version>\n</GetUserRequest>'''
        headers = {
            'X-EBAY-API-COMPATIBILITY-LEVEL': '967',
            'X-EBAY-API-DEV-NAME': EBAY_CONFIG['dev_id'],
            'X-EBAY-API-APP-NAME': EBAY_CONFIG['client_id'],
            'X-EBAY-API-CERT-NAME': EBAY_CONFIG['client_secret'],
            'X-EBAY-API-CALL-NAME': 'GetUser',
            'X-EBAY-API-SITEID': '77',
            'Content-Type': 'text/xml'
        }
        try:
            response = requests.post('https://api.sandbox.ebay.com/ws/api.dll', data=xml_request, headers=headers, timeout=10)
            if response.status_code == 200:
                root = ET.fromstring(response.content)
                ack = root.find('.//{urn:ebay:apis:eBLBaseComponents}Ack')
                if ack is not None and ack.text == "Success":
                    self.is_valid = True
                    self.last_check = datetime.now()
                    self.save_token_data()
                    logger.info('Token erfolgreich getestet und gültig.')
                    return True
                else:
                    self.is_valid = False
                    logger.warning('Token-Test fehlgeschlagen: Kein Success-Ack.')
                    return False
            else:
                self.is_valid = False
                logger.error(f'Token-Test HTTP-Fehler: {response.status_code}')
                return False
        except Exception as e:
            self.is_valid = False
            logger.error(f"Token-Test Exception: {e}")
            return False

    def get_status(self):
        return {
            'access_token': self.access_token[:50] + '...' if self.access_token and len(self.access_token) > 50 else '',
            'refresh_token': bool(self.refresh_token),
            'expires_at': self.token_expires_at.isoformat() if self.token_expires_at else None,
            'last_check': self.last_check.isoformat() if self.last_check else None,
            'is_valid': self.is_valid,
            'auto_refresh_enabled': self.auto_refresh_enabled
        }

token_manager = TokenManager()

def lade_angebote():
    """Lädt die realistischen Offers aus der JSON-Datei"""
    try:
        with open('realistic_offers_frontend.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"Fehler beim Laden der Offers: {e}")
        return {
            "success": False,
            "message": "Keine Offers gefunden",
            "offers": [],
            "total_offers": 0
        }

@app.route('/api/offers', methods=['GET'])
def get_offers():
    data = lade_angebote()
    return jsonify({
        "offers": data.get("offers", []),
        "total": data.get("total_offers", 0),
        "success": data.get("success", True),
        "message": data.get("message", "Realistische Best Offers geladen")
    })

@app.route('/api/stats', methods=['GET'])
def get_stats():
    # Platzhalter: Demo-Statistiken
    stats = {
        'total_offers': 2,
        'pending_offers': 2,
        'accepted_offers': 0,
        'rejected_offers': 0,
        'success_rate': 0
    }
    return jsonify(stats)

@app.route('/api/token-status', methods=['GET'])
def get_token_status():
    try:
        status = token_manager.get_status()
        return jsonify(status)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/sync', methods=['POST'])
def sync_data():
    try:
        # Token vor Sync prüfen
        if not token_manager.test_token():
            return jsonify({'error': 'Token ungültig - bitte erneuern'}), 401
        
        # Lade aktuelle Angebote
        data = lade_angebote()
        
        return jsonify({
            'success': True,
            'offers': data.get('offers', []),
            'total_offers': data.get('total_offers', 0),
            'sync_time': datetime.now().isoformat(),
            'message': 'Synchronisation erfolgreich'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/test-token', methods=['POST'])
def test_token():
    try:
        if token_manager.test_token():
            return jsonify({'success': True, 'message': 'Token ist gültig'})
        else:
            return jsonify({'error': 'Token ist ungültig'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True) 