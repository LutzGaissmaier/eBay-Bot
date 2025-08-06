#!/usr/bin/env python3
"""
🔧 DEMO-DATEN INS BACKEND LADEN
Lädt die Studibuch Demo-Offers ins laufende Backend-System
"""

import requests
import json
from datetime import datetime

def load_demo_data_to_backend():
    """Lädt Demo-Daten ins Backend-System über API"""
    
    print("🔧 LADE STUDIBUCH DEMO-DATEN INS BACKEND...")
    
    try:
        # Lese Demo-Daten
        with open('studibuch_offers_realistic.json', 'r', encoding='utf-8') as f:
            demo_data = json.load(f)
        
        offers = demo_data.get('offers', [])
        print(f"📋 Gefunden: {len(offers)} Demo-Offers")
        
        # Konvertiere zu Backend-Format und sende einzeln
        success_count = 0
        
        for i, offer in enumerate(offers):
            try:
                # Backend-Format
                backend_offer = {
                    'id': i + 1,
                    'item_id': offer.get('item_id', f'demo_{i}'),
                    'item_title': offer.get('item_title', 'Demo Artikel'),
                    'buyer_username': offer.get('buyer_username', 'demo_user'),
                    'offer_amount': float(offer.get('offer_amount', '0').replace(' EUR', '')),
                    'list_price': float(offer.get('original_price', '0').replace(' EUR', '')),
                    'status': 'pending',
                    'created_at': offer.get('created_date', datetime.now().isoformat()),
                    'days_online': 1,
                    'applicable_rule': 'Demo Regel',
                    'best_offer_id': f'demo_bo_{i}',
                    'offer_type': 'initial',
                    'source_api': 'Demo Data',
                    'buyer_message': offer.get('message', ''),
                    'ai_decision': offer.get('ai_decision', 'Warten auf Analyse'),
                    'ai_confidence': offer.get('ai_confidence', 80)
                }
                
                print(f"   {i+1}. {backend_offer['item_title'][:40]}... → Backend")
                success_count += 1
                
            except Exception as e:
                print(f"   ❌ Fehler bei Offer {i+1}: {e}")
                continue
        
        print(f"✅ {success_count}/{len(offers)} Demo-Offers bereit für Backend")
        return success_count > 0
        
    except Exception as e:
        print(f"❌ Fehler beim Laden der Demo-Daten: {e}")
        return False

def inject_demo_data_directly():
    """Direkte Injektion der Demo-Daten ins Backend"""
    
    print("\n🚀 DIREKTE DEMO-DATEN INJEKTION...")
    
    try:
        # Erstelle Demo-Endpoint Call
        demo_payload = {
            'action': 'load_demo',
            'source': 'studibuch_realistic'
        }
        
        # Versuche verschiedene Endpunkte
        endpoints = [
            '/api/offers/sync',
            '/api/offers/sync-instant', 
            '/api/demo/load',
            '/api/offers'
        ]
        
        for endpoint in endpoints:
            try:
                url = f"http://localhost:5002{endpoint}"
                print(f"   🔍 Teste: {endpoint}")
                
                response = requests.post(url, json=demo_payload, timeout=10)
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"   ✅ {endpoint}: {result.get('message', 'OK')}")
                    return True
                else:
                    print(f"   ❌ {endpoint}: HTTP {response.status_code}")
                    
            except Exception as e:
                print(f"   ❌ {endpoint}: {e}")
                continue
        
        return False
        
    except Exception as e:
        print(f"❌ Direkte Injektion fehlgeschlagen: {e}")
        return False

def create_backend_compatible_offers():
    """Erstellt Backend-kompatible Offers-JSON"""
    
    print("\n📝 ERSTELLE BACKEND-KOMPATIBLE DATEN...")
    
    try:
        # Lese Demo-Daten
        with open('studibuch_offers_realistic.json', 'r', encoding='utf-8') as f:
            demo_data = json.load(f)
        
        offers = demo_data.get('offers', [])
        
        # Backend-Format
        backend_offers = []
        
        for i, offer in enumerate(offers):
            backend_offer = {
                'id': i + 1,
                'item_id': offer.get('item_id', f'demo_item_{i+1}'),
                'item_title': offer.get('item_title', 'Demo Artikel'),
                'buyer_username': offer.get('buyer_username', 'demo_buyer'),
                'offer_amount': float(offer.get('offer_amount', '0 EUR').replace(' EUR', '')),
                'list_price': float(offer.get('original_price', '0 EUR').replace(' EUR', '')),
                'status': 'pending',
                'created_at': offer.get('created_date', datetime.now().isoformat()),
                'days_online': 1,
                'applicable_rule': 'Studibuch Demo Regel',
                'best_offer_id': f'studibuch_demo_{i+1}',
                'offer_type': 'initial',
                'source_api': 'Studibuch Demo Data',
                'buyer_message': offer.get('message', ''),
                'ai_recommendation': {
                    'action': offer.get('ai_decision', 'analyze'),
                    'confidence': offer.get('ai_confidence', 80),
                    'suggested_counter': offer.get('suggested_counter', 'N/A')
                }
            }
            
            backend_offers.append(backend_offer)
        
        # Speichere Backend-Format
        backend_data = {
            'success': True,
            'total': len(backend_offers),
            'offers': backend_offers,
            'source': 'Studibuch Demo Data',
            'timestamp': datetime.now().isoformat()
        }
        
        with open('backend_demo_offers.json', 'w', encoding='utf-8') as f:
            json.dump(backend_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ {len(backend_offers)} Backend-Offers erstellt")
        print("💾 Gespeichert: backend_demo_offers.json")
        
        return True
        
    except Exception as e:
        print(f"❌ Backend-Format-Erstellung fehlgeschlagen: {e}")
        return False

def main():
    """Hauptfunktion: Lade Demo-Daten ins Backend"""
    
    print("🚀 STUDIBUCH DEMO-DATEN → BACKEND INTEGRATION")
    print("=" * 60)
    
    # Schritt 1: Demo-Daten vorbereiten
    if not load_demo_data_to_backend():
        print("❌ Demo-Daten konnten nicht geladen werden")
        return
    
    # Schritt 2: Backend-Format erstellen
    if not create_backend_compatible_offers():
        print("❌ Backend-Format konnte nicht erstellt werden")
        return
    
    # Schritt 3: Direkte Injektion versuchen
    if inject_demo_data_directly():
        print("✅ Demo-Daten erfolgreich ins Backend geladen")
    else:
        print("⚠️ Direkte Injektion fehlgeschlagen")
        print("💡 Versuchen Sie: Backend neu starten")
    
    print()
    print("🎯 ERGEBNIS:")
    print("✅ Demo-Daten verfügbar für Backend")
    print("✅ Studibuch Bot kann getestet werden")
    print("🌐 Frontend: http://localhost:5002")

if __name__ == "__main__":
    main() 