#!/usr/bin/env python3
"""
📡 ENDPOINT FÜR REALISTISCHE OFFERS
Lädt die realistischen Best Offers für das Frontend
"""

from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

def load_realistic_offers():
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

@app.route('/api/offers/realistic', methods=['GET'])
def get_realistic_offers():
    """Liefert die realistischen Best Offers"""
    data = load_realistic_offers()
    return jsonify(data)

@app.route('/api/offers', methods=['GET'])
def get_offers():
    """Standard Offers Endpoint - liefert realistische Daten"""
    data = load_realistic_offers()
    
    # Format für Frontend-Kompatibilität
    return jsonify({
        "offers": data.get("offers", []),
        "total": data.get("total_offers", 0),
        "success": data.get("success", True),
        "message": data.get("message", "Realistische Best Offers geladen")
    })

@app.route('/api/offers/load-realistic', methods=['POST'])
def load_offers_endpoint():
    """Lädt realistische Offers (für Frontend-Button)"""
    data = load_realistic_offers()
    return jsonify(data)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health Check"""
    return jsonify({
        "status": "OK",
        "message": "Realistic Offers Server läuft",
        "endpoints": [
            "/api/offers",
            "/api/offers/realistic", 
            "/api/offers/load-realistic"
        ]
    })

@app.route('/')
def home():
    """Home Route"""
    return jsonify({
        "service": "eBay Best Offers API",
        "status": "Running",
        "data_source": "Realistische Offers",
        "frontend_url": "http://localhost:5002"
    })

if __name__ == '__main__':
    print("🚀 STARTE REALISTIC OFFERS SERVER")
    print("=" * 40)
    print("🌐 Frontend: http://localhost:3000")
    print("📡 API: http://localhost:5000")
    print("📋 Offers: http://localhost:5000/api/offers")
    print("🔗 Health: http://localhost:5000/api/health")
    print()
    
    # Prüfe ob Daten vorhanden sind
    if os.path.exists('realistic_offers_frontend.json'):
        print("✅ Realistische Offers gefunden")
        with open('realistic_offers_frontend.json', 'r') as f:
            data = json.load(f)
            print(f"📊 {data.get('total_offers', 0)} Offers verfügbar")
    else:
        print("❌ Keine Offers-Datei gefunden")
        print("💡 Führe 'python3 create_realistic_offers.py' aus")
    
    print()
    app.run(host='0.0.0.0', port=5000, debug=True) 