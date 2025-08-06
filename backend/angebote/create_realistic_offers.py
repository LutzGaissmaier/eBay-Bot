#!/usr/bin/env python3
"""
🎯 REALISTISCHE PREISVORSCHLÄGE FÜR FRONTEND
Erstellt echte eBay-ähnliche Best Offers im Frontend-Format
"""

import json
from datetime import datetime, timedelta
import random

def create_realistic_best_offers():
    """Erstellt realistische Best Offers wie sie von eBay kommen würden"""
    
    # Realistische deutsche eBay-Käufer
    buyers = [
        "bargain_hunter_2024", "student_saver", "bucher_sammler", 
        "preishit_finder", "schnäppchen_jäger", "uni_student_21",
        "buch_liebhaber", "lese_ratte", "studienhelfer", "wissen_sammler"
    ]
    
    # Realistische Artikel (Bücher für Studibuch)
    articles = [
        ("Mathematik für Informatiker", 45.00, "383274829"),
        ("BWL Grundlagen kompakt", 25.50, "394857201"), 
        ("Physik Experimentalphysik", 89.00, "372058392"),
        ("Chemie Organische Chemie", 67.50, "385629147"),
        ("Geschichte Deutschlands", 32.00, "391847362"),
        ("Englisch Cambridge Grammar", 28.90, "387294751"),
        ("Statistik für Wirtschaftswissenschaften", 55.00, "376492018"),
        ("Programmieren lernen mit Python", 39.99, "394857201")
    ]
    
    # Status-Typen für Best Offers
    statuses = ["Aktiv", "Warten auf Antwort", "Neuer Vorschlag", "Gegenangebot erhalten"]
    
    offers = []
    
    for i in range(8):  # 8 realistische Angebote
        article_title, original_price, item_id = random.choice(articles)
        buyer = random.choice(buyers)
        
        # Realistische Angebots-Logik (70-90% des Originalpreises)
        offer_percentage = random.uniform(0.70, 0.90)
        offer_amount = original_price * offer_percentage
        
        # Gegenvorschlag (5-15% über Angebot)
        counter_percentage = random.uniform(1.05, 1.15) 
        counter_amount = offer_amount * counter_percentage
        
        # Realistische Nachrichten
        messages = [
            "Hallo, wäre das Buch für diesen Preis verfügbar? Bin Student und würde es dringend brauchen.",
            "Ich biete Ihnen diesen Preis für das Buch. Ist das in Ordnung?",
            "Könnten Sie mit diesem Preis leben? Das Buch ist für mein Studium.",
            "Wäre dieser Preis möglich? Vielen Dank!",
            "Ist das Buch noch verfügbar? Würde diesen Preis zahlen.",
            "",  # Manche haben keine Nachricht
            "Brauche das Buch für die Uni, wäre der Preis ok?",
            "Hallo, könnten wir uns auf diesen Preis einigen?"
        ]
        
        # Zeitstempel (letzte 3 Tage)
        created_time = datetime.now() - timedelta(hours=random.randint(1, 72))
        
        offer = {
            "id": f"bestOffer_{item_id}_{i+1}",
            "buyer_username": buyer,
            "offer_amount": f"{offer_amount:.2f} EUR",
            "quantity": 1,
            "status": random.choice(statuses),
            "message": random.choice(messages),
            "item_id": item_id,
            "item_title": article_title,
            "original_price": f"{original_price:.2f} EUR",
            "created_date": created_time.strftime('%Y-%m-%d %H:%M:%S'),
            "ai_decision": random.choice([
                "Annehmen empfohlen", 
                "Gegenangebot senden", 
                "Ablehnen", 
                "Warten auf Analyse"
            ]),
            "ai_confidence": random.randint(65, 95),
            "suggested_counter": f"{counter_amount:.2f} EUR",
            "discount_percentage": f"{((original_price - offer_amount) / original_price * 100):.1f}%",
            "profit_margin": f"{(counter_amount - offer_amount):.2f} EUR"
        }
        
        offers.append(offer)
    
    return offers

def save_frontend_ready_data():
    """Speichert die Daten im exakten Frontend-Format"""
    
    offers = create_realistic_best_offers()
    
    frontend_data = {
        "success": True,
        "timestamp": datetime.now().isoformat(),
        "total_offers": len(offers),
        "source": "eBay Production API (Simulation)",
        "message": f"{len(offers)} realistische Best Offers für Frontend",
        "offers": offers,
        "metadata": {
            "currency": "EUR",
            "site": "eBay Deutschland", 
            "seller": "Studibuch",
            "api_version": "967"
        }
    }
    
    # Speichere für Frontend
    with open('realistic_offers_frontend.json', 'w', encoding='utf-8') as f:
        json.dump(frontend_data, f, indent=2, ensure_ascii=False)
    
    # Speichere auch kompakt für direkten Import
    with open('../frontend/src/data/offers.json', 'w', encoding='utf-8') as f:
        json.dump(frontend_data, f, indent=2, ensure_ascii=False)
    
    return frontend_data, offers

if __name__ == "__main__":
    print("🚀 ERSTELLE REALISTISCHE PREISVORSCHLÄGE")
    print("=" * 50)
    
    frontend_data, offers = save_frontend_ready_data()
    
    print()
    print("🎉 REALISTISCHE BEST OFFERS ERSTELLT:")
    print("=" * 40)
    
    for i, offer in enumerate(offers[:5]):  # Zeige erste 5
        print(f"{i+1}. 📚 {offer['item_title']}")
        print(f"   👤 Käufer: {offer['buyer_username']}")
        print(f"   💰 Originalpreis: {offer['original_price']}")
        print(f"   💸 Angebot: {offer['offer_amount']} ({offer['discount_percentage']} Rabatt)")
        print(f"   📊 Status: {offer['status']}")
        print(f"   🎯 KI-Empfehlung: {offer['ai_decision']} ({offer['ai_confidence']}%)")
        print(f"   ↗️ Gegenvorschlag: {offer['suggested_counter']}")
        if offer['message']:
            print(f"   💬 Nachricht: {offer['message'][:60]}...")
        print()
    
    print("💾 GESPEICHERT:")
    print("✅ realistic_offers_frontend.json (Backend)")
    print("✅ frontend/src/data/offers.json (Frontend)")
    
    print()
    print("🌐 BEREIT FÜR FRONTEND!")
    print(f"📋 {len(offers)} Preisvorschläge im Frontend-Format")
    print("🎯 Enthält: Käufer, Preise, Status, KI-Empfehlungen, Gegenvorschläge")
    
    print()
    print("📝 FRONTEND INTEGRATION:")
    print("1. JSON-Datei ist im Frontend-Ordner")
    print("2. Direkt importierbar in React-Komponenten") 
    print("3. Realistische eBay-Daten für Development")
    print("4. Kann später durch echte API ersetzt werden") 