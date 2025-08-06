#!/usr/bin/env python3
"""
🔄 STUDIBUC OAUTH TOKEN FLOW
Vollständiger OAuth-Flow für echte Studibuc eBay-Daten

Kurzanleitung:
---------------
1. Trage App-ID (Client ID), Cert-ID (Client Secret) und Redirect URI unten ein.
2. Starte das Script. Es zeigt dir eine URL – diese im Browser öffnen und eBay-Login durchführen.
3. Nach erfolgreicher Anmeldung wirst du zu deiner Redirect-URL weitergeleitet, dort im Link steht ?code=... (Kopieren!)
4. Füge den 'code' im Script ein, dann läuft es automatisch weiter und zeigt dir Access- und Refresh-Token an.
"""

import requests
import base64
import urllib.parse

# STUDIBUC CREDENTIALS (aus Umgebungsvariablen)
import os
CLIENT_ID     = os.getenv('EBAY_APP_ID', 'your_ebay_app_id_here')
CLIENT_SECRET = os.getenv('EBAY_CERT_ID', 'your_ebay_cert_id_here')
REDIRECT_URI  = os.getenv('EBAY_REDIRECT_URI', 'urn:ietf:wg:oauth:2.0:oob')
SCOPES = [
    "https://api.sandbox.ebay.com/oauth/api_scope",
    "https://api.sandbox.ebay.com/oauth/api_scope/sell.marketing.readonly",
    "https://api.sandbox.ebay.com/oauth/api_scope/sell.marketing",
    "https://api.sandbox.ebay.com/oauth/api_scope/sell.inventory.readonly",
    "https://api.sandbox.ebay.com/oauth/api_scope/sell.inventory",
    "https://api.sandbox.ebay.com/oauth/api_scope/sell.account.readonly",
    "https://api.sandbox.ebay.com/oauth/api_scope/sell.account",
    "https://api.sandbox.ebay.com/oauth/api_scope/sell.fulfillment.readonly",
    "https://api.sandbox.ebay.com/oauth/api_scope/sell.fulfillment"
] # Erweiterte Scopes für Trading API + Best Offers

# 1. OAUTH LINK GENERIEREN
scope_str = urllib.parse.quote(' '.join(SCOPES))
auth_url = f"https://auth.sandbox.ebay.com/oauth2/authorize?client_id={CLIENT_ID}&redirect_uri={urllib.parse.quote(REDIRECT_URI)}&response_type=code&scope={scope_str}"

print("\n🚀 STUDIBUC EBAY OAUTH FLOW")
print("=" * 60)
print("📧 Account: Studibuc Production")
print("🔧 App: Studibuc-Studibuc-PRD")
print()
print("1. Bitte diese URL im Browser öffnen, einloggen und Zugang erlauben:\n")
print("🌐 OAUTH URL:")
print("-" * 60)
print(auth_url)
print("-" * 60)
print()
print("2. Kopiere den Code (?code=...) aus der Adresszeile nach Login.\n")

# 2. USER CODE EINLESEN
CODE = input("📋 Gib den 'code' hier ein: ").strip()

if not CODE:
    print("❌ Kein Code eingegeben!")
    exit(1)

print(f"\n📥 Code erhalten: {CODE[:50]}...")

# 3. ACCESS TOKEN HOLEN
print("\n🔄 Tausche Code gegen Token...")
url = "https://api.sandbox.ebay.com/identity/v1/oauth2/token"
client_creds = f"{CLIENT_ID}:{CLIENT_SECRET}"
b64_creds = base64.b64encode(client_creds.encode()).decode()
headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Authorization": f"Basic {b64_creds}",
}
data = {
    "grant_type": "authorization_code",
    "code": CODE,
    "redirect_uri": REDIRECT_URI
}

resp = requests.post(url, headers=headers, data=data)

if resp.ok:
    tokens = resp.json()
    print("\n🎉 TOKEN ERFOLGREICH ERHALTEN!")
    print("=" * 60)
    
    access_token = tokens.get('access_token')
    refresh_token = tokens.get('refresh_token')
    expires_in = tokens.get('expires_in')
    refresh_expires_in = tokens.get('refresh_token_expires_in')
    
    print(f"🔑 Access Token:  {access_token}")
    print(f"⏰ Gültig (Sek):  {expires_in}")
    print(f"🔄 Refresh Token: {refresh_token}")
    print(f"⏰ Refresh gültig (Sek): {refresh_expires_in}")
    
    print("\n📋 TOKEN-INFO:")
    print(f"📏 Access Token Länge: {len(access_token)} Zeichen")
    print(f"🔤 Token Format: {access_token[:20]}...")
    
    # Speichere Token
    import json
    from datetime import datetime
    
    token_data = {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'expires_in': expires_in,
        'refresh_token_expires_in': refresh_expires_in,
        'token_type': tokens.get('token_type', 'Bearer'),
        'scope': tokens.get('scope'),
        'created_at': datetime.now().isoformat(),
        'account': 'Studibuc',
        'app_id': CLIENT_ID
    }
    
    with open('studibuc_oauth_token.json', 'w', encoding='utf-8') as f:
        json.dump(token_data, f, indent=2, ensure_ascii=False)
    
    print("💾 Token gespeichert: studibuc_oauth_token.json")
    
    # Erstelle Backend-Update Script
    print("\n🔧 ERSTELLE BACKEND-UPDATE...")
    
    update_script = f'''#!/usr/bin/env python3
"""
AUTO-GENERIERT: Studibuc Backend Token Update
"""

import re

NEW_TOKEN = '{access_token}'

print("🔧 Aktualisiere Backend mit neuem Studibuc Token...")

# Update main.py
try:
    with open('main.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Ersetze Token
    pattern = r"'auth_token': 'v\\^[^']+'"
    replacement = f"'auth_token': '{{NEW_TOKEN}}'"
    
    updated_content = re.sub(pattern, replacement, content)
    
    with open('main.py', 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print("✅ Token in main.py aktualisiert!")
    print("🔄 Starten Sie den Server neu:")
    print("   python3 main.py")
    print()
    print("🚀 Dann testen:")
    print("   curl http://localhost:5002/api/test-ebay-connection")
    
except Exception as e:
    print(f"❌ Fehler beim Update: {{e}}")
    print("💡 Manuell einsetzen:")
    print(f"   Token: {{NEW_TOKEN}}")
'''
    
    with open('update_studibuc_backend.py', 'w', encoding='utf-8') as f:
        f.write(update_script)
    
    print("✅ Update-Script erstellt: update_studibuc_backend.py")
    
    print("\n🎯 NÄCHSTE SCHRITTE:")
    print("1. python3 update_studibuc_backend.py")
    print("2. Backend neu starten")
    print("3. Echte Studibuc Best Offers abrufen!")
    
    print("\n🔗 Access Token für API-Calls:")
    print("   Header: Authorization: Bearer " + access_token)
    
else:
    print("\n❌ FEHLER BEIM TOKEN-TAUSCH:")
    print(f"📊 Status Code: {resp.status_code}")
    print(f"📄 Response: {resp.text}")
    
    if resp.status_code == 400:
        print("\n💡 MÖGLICHE URSACHEN:")
        print("• Authorization Code ist abgelaufen")
        print("• Redirect URI stimmt nicht überein")
        print("• App-Konfiguration im eBay Portal prüfen")
    elif resp.status_code == 401:
        print("\n💡 MÖGLICHE URSACHEN:")
        print("• Client ID oder Client Secret falsch")
        print("• App nicht für Production freigegeben") 