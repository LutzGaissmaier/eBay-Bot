#!/usr/bin/env python3
"""
🔧 STUDIBUC OAUTH FEHLER-BEHEBUNG
Behebt den "invalid_request" Fehler von eBay OAuth
"""

import webbrowser
import urllib.parse

import os
CLIENT_ID = os.getenv("EBAY_APP_ID", "your_ebay_app_id_here")

print("🔧 STUDIBUC OAUTH FEHLER-BEHEBUNG")
print("=" * 50)
print("❌ Fehler erkannt: invalid_request")
print("💡 Problem: OAuth-Parameter nicht korrekt")
print()

print("🔍 MÖGLICHE URSACHEN:")
print("1. Redirect URI nicht im eBay Portal konfiguriert")
print("2. App-Einstellungen nicht korrekt")
print("3. Falsche Scope-Parameter")
print()

# VERSCHIEDENE KONFIGURATIONEN TESTEN
configs = [
    {
        "name": "Standard Out-of-Band",
        "redirect_uri": "urn:ietf:wg:oauth:2.0:oob",
        "scopes": ["https://api.ebay.com/oauth/api_scope"]
    },
    {
        "name": "App-ID als Redirect",
        "redirect_uri": CLIENT_ID,
        "scopes": ["https://api.ebay.com/oauth/api_scope"]
    },
    {
        "name": "Localhost Redirect",
        "redirect_uri": "http://localhost:8080",
        "scopes": ["https://api.ebay.com/oauth/api_scope"]
    },
    {
        "name": "Minimale Scopes",
        "redirect_uri": "urn:ietf:wg:oauth:2.0:oob",
        "scopes": [
            "https://api.ebay.com/oauth/api_scope",
            "https://api.ebay.com/oauth/api_scope/sell.inventory.readonly"
        ]
    }
]

print("🚀 LÖSUNGSOPTIONEN:")
print("-" * 30)

for i, config in enumerate(configs, 1):
    scope_str = urllib.parse.quote(' '.join(config['scopes']))
    auth_url = f"https://auth.ebay.com/oauth2/authorize?client_id={CLIENT_ID}&redirect_uri={urllib.parse.quote(config['redirect_uri'])}&response_type=code&scope={scope_str}"
    
    print(f"\n{i}. {config['name']}")
    print(f"   Redirect URI: {config['redirect_uri']}")
    print(f"   Scopes: {len(config['scopes'])} Berechtigung(en)")
    print(f"   URL: {auth_url[:80]}...")

print()
print("💡 EMPFEHLUNG:")
print("1. Zuerst eBay Developer Portal prüfen")
print("2. Dann Option 1 (Out-of-Band) testen")
print("3. Falls Problem: Option 2 (App-ID) testen")

choice = input("\n🔧 Welche Option testen? (1-4): ").strip()

if choice in ['1', '2', '3', '4']:
    config = configs[int(choice) - 1]
    
    scope_str = urllib.parse.quote(' '.join(config['scopes']))
    auth_url = f"https://auth.ebay.com/oauth2/authorize?client_id={CLIENT_ID}&redirect_uri={urllib.parse.quote(config['redirect_uri'])}&response_type=code&scope={scope_str}"
    
    print(f"\n🚀 TESTE OPTION {choice}: {config['name']}")
    print("=" * 60)
    print(auth_url)
    print("=" * 60)
    
    open_browser = input("\n🌐 Browser öffnen? (j/n): ").lower()
    if open_browser in ['j', 'ja', 'y', 'yes', '']:
        try:
            webbrowser.open(auth_url)
            print("✅ Browser geöffnet!")
        except:
            print("❌ Browser-Fehler")
    
    print()
    print("📋 FALLS WEITERHIN FEHLER:")
    print("1. eBay Developer Portal öffnen:")
    print("   https://developer.ebay.com/my/keys")
    print("2. Studibuc-Studibuc-PRD App auswählen")
    print("3. 'Application Settings' → 'Redirect URIs'")
    print("4. Hinzufügen:")
    for cfg in configs:
        print(f"   - {cfg['redirect_uri']}")

else:
    print("\n🔍 MANUELLE PRÜFUNG:")
    print("-" * 30)
    print("1. eBay Developer Portal öffnen:")
    print("   https://developer.ebay.com/my/keys")
    print()
    print("2. Studibuc-Studibuc-PRD App prüfen:")
    print("   ✅ App-Status: Production")
    print("   ✅ Redirect URIs: Konfiguriert")
    print("   ✅ Scopes: Berechtigt")
    print()
    print("3. Häufige Redirect URIs:")
    print("   - urn:ietf:wg:oauth:2.0:oob")
    print(f"   - {CLIENT_ID}")
    print("   - http://localhost:8080")

print()
print("🎯 NACH DER BEHEBUNG:")
print("python3 studibuc_automatik.py")
print("→ Sollte dann funktionieren!") 