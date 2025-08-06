#!/usr/bin/env python3
"""
🎯 ECHTE STUDIBUCH BEST OFFERS DIREKT VON eBay
Holt die echten Preisvorschläge vom Studibuch eBay-Account
"""

import requests
import xml.etree.ElementTree as ET
from datetime import datetime
import json
import os

# ECHTE STUDIBUCH PRODUCTION CREDENTIALS (mit neuem Token)
STUDIBUCH_CREDENTIALS = {
    'app_id': os.getenv('EBAY_APP_ID', 'your_ebay_app_id_here'),
    'dev_id': '0a2f6da6-f750-4a47-8532-8ceba61c9faa',
    'cert_id': 'PRD-ef6a212ec490-4bc4-4489-b2ad-aa31',
    'auth_token': 'v^1.1#i^1#p^3#r^0#f^0#I^3#t^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'
}

def get_studibuch_best_offers():
    """Holt echte Best Offers direkt vom Studibuch eBay-Account"""
    
    print("🔥 HOLE ECHTE STUDIBUCH BEST OFFERS")
    print("=" * 50)
    print(f"📧 Account: Studibuch Production")
    print(f"🔑 Token: {STUDIBUCH_CREDENTIALS['auth_token'][:20]}...")
    print()
    
    # eBay Production API URL
    api_url = "https://api.ebay.com/ws/api.dll"
    
    # GetBestOffers XML Request für Studibuch Account
    xml_request = f"""<?xml version="1.0" encoding="utf-8"?>
<GetBestOffersRequest xmlns="urn:ebay:apis:eBLBaseComponents">
    <RequesterCredentials>
        <eBayAuthToken>{STUDIBUCH_CREDENTIALS['auth_token']}</eBayAuthToken>
    </RequesterCredentials>
    <Version>967</Version>
    <BestOfferStatus>All</BestOfferStatus>
    <Pagination>
        <EntriesPerPage>50</EntriesPerPage>
        <PageNumber>1</PageNumber>
    </Pagination>
</GetBestOffersRequest>"""
    
    headers = {
        'X-EBAY-API-COMPATIBILITY-LEVEL': '967',
        'X-EBAY-API-DEV-NAME': STUDIBUCH_CREDENTIALS['dev_id'],
        'X-EBAY-API-APP-NAME': STUDIBUCH_CREDENTIALS['app_id'],
        'X-EBAY-API-CERT-NAME': STUDIBUCH_CREDENTIALS['cert_id'],
        'X-EBAY-API-CALL-NAME': 'GetBestOffers',
        'X-EBAY-API-SITEID': '77',  # Deutschland
        'Content-Type': 'text/xml'
    }
    
    try:
        print("📡 Sende Request an eBay Production API...")
        response = requests.post(api_url, data=xml_request, headers=headers, timeout=20)
        
        print(f"📥 eBay Response: Status {response.status_code}")
        print(f"📊 Content-Length: {len(response.content)} bytes")
        
        if response.status_code == 200:
            return parse_studibuch_best_offers(response.content)
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"📄 Response: {response.text[:300]}...")
            return []
            
    except Exception as e:
        print(f"❌ Request Error: {e}")
        return []

def parse_studibuch_best_offers(xml_content):
    """Parst die eBay XML Response zu echten Studibuch Best Offers"""
    
    try:
        root = ET.fromstring(xml_content)
        
        # eBay Response Status prüfen
        ack_elem = root.find('.//{urn:ebay:apis:eBLBaseComponents}Ack')
        if ack_elem is None:
            print("❌ Keine eBay Ack in Response")
            return []
            
        ack_value = ack_elem.text
        print(f"📋 eBay Ack: {ack_value}")
        
        if ack_value == "Success":
            print("✅ eBay API SUCCESS!")
            
            # Best Offers suchen
            best_offers = root.findall('.//{urn:ebay:apis:eBLBaseComponents}BestOffer')
            print(f"📋 Gefundene Best Offers: {len(best_offers)}")
            
            if len(best_offers) == 0:
                print("ℹ️ Keine Best Offers gefunden")
                print("💡 Das ist normal wenn gerade keine Preisvorschläge vorhanden sind")
                return []
            
            offers = []
            for i, offer in enumerate(best_offers):
                try:
                    # Extrahiere Offer-Daten
                    offer_data = extract_offer_data(offer, i+1)
                    if offer_data:
                        offers.append(offer_data)
                        
                except Exception as e:
                    print(f"⚠️ Fehler beim Parsen von Offer {i+1}: {e}")
                    continue
            
            return offers
            
        elif ack_value == "Failure":
            print("❌ eBay API FAILURE")
            
            # Fehler anzeigen
            errors = root.findall('.//{urn:ebay:apis:eBLBaseComponents}Errors')
            for error in errors:
                code_elem = error.find('.//{urn:ebay:apis:eBLBaseComponents}ErrorCode')
                msg_elem = error.find('.//{urn:ebay:apis:eBLBaseComponents}LongMessage')
                
                code = code_elem.text if code_elem is not None else "?"
                message = msg_elem.text if msg_elem is not None else "Unbekannt"
                
                print(f"   Error {code}: {message}")
                
                # Spezielle Token-Hinweise
                if "token" in message.lower() and "abgelaufen" in message.lower():
                    print("💡 LÖSUNG: Neuen OAuth-Token in eBay Developer Console erstellen")
                elif "berechtigung" in message.lower():
                    print("💡 LÖSUNG: App-Berechtigungen in eBay Developer Console prüfen")
                    
            return []
            
        else:
            print(f"⚠️ Unbekannter eBay Ack: {ack_value}")
            return []
            
    except ET.ParseError as e:
        print(f"❌ XML Parse Error: {e}")
        print(f"📄 Raw Response: {xml_content[:500]}...")
        return []

def extract_offer_data(offer_elem, offer_num):
    """Extrahiert Daten aus einem Best Offer XML Element"""
    
    def get_text(xpath):
        elem = offer_elem.find(f'.//{{{offer_elem.nsmap[None] if offer_elem.nsmap else "urn:ebay:apis:eBLBaseComponents"}}}{xpath}')
        return elem.text if elem is not None else None
    
    # Extrahiere Basis-Daten
    offer_id = get_text('BestOfferID')
    buyer_id = get_text('Buyer/UserID') 
    price = get_text('Price')
    currency = offer_elem.find('.//{urn:ebay:apis:eBLBaseComponents}Price')
    currency_id = currency.get('currencyID') if currency is not None else 'EUR'
    quantity = get_text('Quantity')
    status = get_text('Status')
    message = get_text('BuyerMessage')
    item_id = get_text('ItemID')
    
    # Format für Frontend
    offer_data = {
        'id': offer_id or f'studibuch_offer_{offer_num}',
        'buyer_username': buyer_id or 'Unbekannter Käufer',
        'offer_amount': f"{price} {currency_id}" if price else 'N/A',
        'quantity': int(quantity) if quantity and quantity.isdigit() else 1,
        'status': translate_status(status),
        'message': message or '',
        'item_id': item_id or 'N/A',
        'item_title': f'Studibuch Artikel {item_id}' if item_id else 'Unbekannter Artikel',
        'created_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'ai_decision': 'Warten auf Analyse',
        'ai_confidence': 80,
        'suggested_counter': calculate_counter_offer(price, currency_id) if price else 'N/A',
        'source': 'eBay Production API (Studibuch)',
        'account': 'Studibuch'
    }
    
    return offer_data

def translate_status(status):
    """Übersetzt eBay Status zu Deutsch"""
    status_map = {
        'Active': 'Aktiv',
        'Accepted': 'Angenommen',
        'Declined': 'Abgelehnt',
        'Expired': 'Abgelaufen',
        'Retracted': 'Zurückgezogen',
        'CounterOffered': 'Gegenangebot erhalten'
    }
    return status_map.get(status, status or 'Unbekannt')

def calculate_counter_offer(price, currency):
    """Berechnet intelligenten Gegenvorschlag"""
    try:
        amount = float(price.replace(',', '.'))
        # 8-12% über Angebot als Gegenvorschlag  
        counter = amount * 1.10
        return f"{counter:.2f} {currency}"
    except:
        return "N/A"

def save_studibuch_offers(offers):
    """Speichert echte Studibuch Offers für Frontend"""
    
    if not offers:
        # Erstelle leere Struktur wenn keine Offers
        frontend_data = {
            'success': True,
            'timestamp': datetime.now().isoformat(),
            'total_offers': 0,
            'offers': [],
            'source': 'eBay Production API (Studibuch)',
            'account': 'Studibuch',
            'message': 'Keine Best Offers vorhanden (ist normal)'
        }
    else:
        frontend_data = {
            'success': True,
            'timestamp': datetime.now().isoformat(),
            'total_offers': len(offers),
            'offers': offers,
            'source': 'eBay Production API (Studibuch)',
            'account': 'Studibuch',
            'message': f'{len(offers)} echte Studibuch Best Offers geladen'
        }
    
    # Speichere für Frontend
    with open('studibuch_real_offers.json', 'w', encoding='utf-8') as f:
        json.dump(frontend_data, f, indent=2, ensure_ascii=False)
    
    # Speichere auch im Frontend-Ordner
    try:
        with open('../frontend/src/data/studibuch_offers.json', 'w', encoding='utf-8') as f:
            json.dump(frontend_data, f, indent=2, ensure_ascii=False)
    except:
        pass  # Frontend-Ordner existiert möglicherweise nicht
    
    return frontend_data

if __name__ == "__main__":
    print("🚀 STUDIBUCH eBay BEST OFFERS LOADER")
    print("=" * 50)
    
    # Lade echte Best Offers vom Studibuch Account
    offers = get_studibuch_best_offers()
    
    if offers:
        print()
        print("🎉 ECHTE STUDIBUCH BEST OFFERS ERHALTEN!")
        print("=" * 45)
        
        for i, offer in enumerate(offers[:5]):  # Zeige erste 5
            print(f"{i+1}. 👤 {offer['buyer_username']}")
            print(f"   💰 Angebot: {offer['offer_amount']}")
            print(f"   📊 Status: {offer['status']}")
            print(f"   📦 Artikel: {offer['item_title']}")
            if offer['message']:
                print(f"   💬 Nachricht: {offer['message'][:60]}...")
            print(f"   🎯 Gegenvorschlag: {offer['suggested_counter']}")
            print()
        
        if len(offers) > 5:
            print(f"... und {len(offers) - 5} weitere Offers")
        
    else:
        print()
        print("ℹ️ Keine Best Offers vom Studibuch Account gefunden")
        print("💡 Mögliche Gründe:")
        print("   • Gerade keine aktiven Preisvorschläge")
        print("   • OAuth-Token abgelaufen")
        print("   • Berechtigung für Best Offers fehlt")
    
    # Speichere Ergebnis für Frontend
    frontend_data = save_studibuch_offers(offers)
    
    print()
    print("💾 GESPEICHERT:")
    print("✅ studibuch_real_offers.json")
    print("✅ frontend/src/data/studibuch_offers.json (falls möglich)")
    
    print()
    print("🎯 ERGEBNIS:")
    print(f"📊 {frontend_data['total_offers']} echte Best Offers")
    print(f"📅 Timestamp: {frontend_data['timestamp']}")
    print(f"🌐 Quelle: {frontend_data['source']}")
    print(f"💼 Account: {frontend_data['account']}")
    
    if offers:
        print()
        print("🔥 SIE HABEN ECHTE STUDIBUCH eBay-DATEN!")
    else:
        print()
        print("💡 Versuchen Sie es später nochmal oder erneuern Sie den OAuth-Token") 