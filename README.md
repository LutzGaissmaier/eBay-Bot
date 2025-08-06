# eBay Preisvorschlags-Bot - Lokale Installation

Ein intelligenter Bot für automatische eBay-Preisverhandlungen mit menschlichem Verhalten.

## 🚀 Schnellstart

```bash
# 1. Repository klonen
git clone https://github.com/LutzGaissmaier/eBay-Bot.git
cd eBay-Bot

# 2. Backend starten
cd backend
pip install -r requirements.txt
python hauptserver.py

# 3. Frontend starten (optional, für Entwicklung)
cd ../frontend
npm install
npm run dev

# 4. Browser öffnen
http://localhost:5002 (Backend-API)
http://localhost:3000 (Frontend)
```

## 📋 Systemanforderungen

- **Python 3.8+** (empfohlen: 3.11)
- **Node.js 18+** (nur für Frontend-Entwicklung)
- **Internetverbindung** für eBay API-Calls
- **eBay Developer Account** mit Trading API-Zugang

## 🎯 Features

### ✅ **Vollautomatische Preisverhandlungen**
- KI-basierte Entscheidungsfindung mit OpenAI
- Menschliches Verhalten gegen Bot-Erkennung
- Zeitverzögerte Antworten (2-30 Minuten)

### ✅ **Intelligente Regelsets**
- **Mehrere Verhandlungsregeln** für verschiedene Szenarien
- **Zeitbasierte Regeln** je nach Angebotslaufzeit
- **Shopware-Integration** für Einkaufspreise
- **Vollständige Nachvollziehbarkeit** aller Aktionen

### ✅ **Professionelles Dashboard**
- Mobile-optimierte Benutzeroberfläche
- Regel-Management mit Übersicht und Editor
- Detaillierte Statistiken und Protokolle
- Echtzeit-Synchronisation mit eBay

## 📁 Projektstruktur

```
eBay-Bot/
├── backend/                # Backend (Flask)
│   ├── hauptserver.py      # Zentrale API & Einstiegspunkt
│   ├── token_backend/      # Token-Management & OAuth
│   ├── angebote/           # Angebots-Logik & Daten
│   ├── schnittstelle/      # eBay API-Anbindung (Trading/Sell)
│   ├── skripte/            # Hilfs- und Importscripte
│   ├── tests/              # Tests für Backend
│   ├── static/             # Statische Dateien (Frontend-Build)
│   └── backend.log         # Zentrales Logfile
├── frontend/               # React-Frontend
│   ├── src/
│   │   ├── components/
│   │   │   ├── panels/         # Haupt-UI-Panels
│   │   │   ├── management/     # Management-Komponenten
│   │   │   └── ui/             # UI-Bausteine
│   │   └── data/               # Beispieldaten
│   └── package.json
├── docs/                   # Dokumentation
└── examples/               # Beispielregeln & Konfigurationen
```

## 🏗️ Architekturüberblick

- **Backend:**
  - Zentrale API in `backend/hauptserver.py` (Flask)
  - Token- und Angebotslogik modular ausgelagert
  - Zentrales Logging in `backend.log`
- **Frontend:**
  - Moderne React-App mit klarer Komponentenstruktur
  - Panels, Management und UI getrennt
- **Kommunikation:**
  - REST-API (JSON) zwischen Frontend und Backend

## ⚙️ Installation & Konfiguration

Siehe detaillierte Anleitung in `docs/INSTALLATION.md`

## 🔧 Einstiegspunkte & wichtige Abläufe

- **Backend-Start:** `python backend/hauptserver.py`
- **Frontend-Start:** `npm run dev` im frontend-Ordner
- **API-Dokumentation:** siehe Endpunkte in `hauptserver.py`
- **Logs:** Alle Backend-Aktionen in `backend/backend.log`

## 📞 Support

- **Installation**: `docs/INSTALLATION.md`
- **Benutzerhandbuch**: `docs/USER_GUIDE.md`
- **Beispiele**: `examples/` Verzeichnis

---

**Entwickelt für professionelle eBay-Verkäufer** 🎯
