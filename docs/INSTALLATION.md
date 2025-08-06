# Installation & Setup - eBay Preisvorschlags-Bot

## 📋 Voraussetzungen

### System-Requirements
- **Betriebssystem**: Windows 10+, macOS 10.15+, oder Linux
- **Python**: Version 3.8 oder höher (empfohlen: 3.11)
- **RAM**: Mindestens 2GB verfügbar
- **Festplatte**: 500MB freier Speicherplatz
- **Internet**: Stabile Verbindung für API-Calls

### eBay Developer Account
1. **eBay Developer Account** erstellen: https://developer.ebay.com
2. **Trading API-Zugang** beantragen
3. **Production Keys** generieren (nicht Sandbox!)
4. **Auth Token** für Ihr eBay-Konto erstellen

### OpenAI Account (optional, aber empfohlen)
- **OpenAI API-Key** für intelligente Entscheidungen
- Kostenlos bis zu einem gewissen Limit

## 🚀 Schritt-für-Schritt Installation

### Schritt 1: Python Installation prüfen

```bash
# Python Version prüfen
python --version
# oder
python3 --version

# Sollte 3.8+ anzeigen
```

**Falls Python nicht installiert:**
- **Windows**: https://python.org/downloads
- **macOS**: `brew install python3` oder python.org
- **Linux**: `sudo apt install python3 python3-pip`

### Schritt 2: Projekt entpacken

```bash
# ZIP-Datei entpacken
unzip eBay-Bot-Lokal.zip
cd eBay-Bot-Lokal

# Struktur prüfen
ls -la
# Sollte zeigen: backend/ frontend/ docs/ examples/
```

### Schritt 3: Backend konfigurieren

```bash
# In Backend-Verzeichnis wechseln
cd backend

# Abhängigkeiten installieren
pip install -r requirements.txt
# oder bei Problemen:
pip3 install -r requirements.txt
```

### Schritt 4: Umgebungsvariablen konfigurieren

```bash
# Konfigurationsdatei erstellen
cp .env.example .env

# Mit Texteditor öffnen und ausfüllen
nano .env
# oder
notepad .env
```

**Wichtige Konfiguration in `.env`:**

```env
# Ihre echten eBay-Zugangsdaten
EBAY_APP_ID=your_ebay_app_id_here
EBAY_DEV_ID=0a2f6da6-f750-4a47-8532-8ceba61c9faa
EBAY_CERT_ID=PRD-ef6a212ec490-4bc4-4489-b2ad-aa31
EBAY_AUTH_TOKEN=v^1.1#i^1#f^0#p^1#I^3#r^0#t^H4sI...
EBAY_SANDBOX=false

# OpenAI für KI-Entscheidungen
OPENAI_API_KEY=sk-ihr-key-hier

# Server-Einstellungen
PORT=5000
FLASK_ENV=production
```

### Schritt 5: System starten

```bash
# Backend starten
python main.py

# Erfolgsmeldung sollte erscheinen:
# ✅ eBay Preisvorschlags-Bot gestartet
# 🌐 Dashboard: http://localhost:5000
```

### Schritt 6: Dashboard öffnen

1. **Browser öffnen**
2. **URL aufrufen**: http://localhost:5000
3. **Dashboard sollte laden**

## ⚙️ Erste Konfiguration

### 1. eBay API-Verbindung testen

1. **Einstellungen** → **API-Konfiguration**
2. **Verbindung testen** klicken
3. **Erfolgsmeldung** sollte erscheinen

### 2. Erste Verhandlungsregel erstellen

1. **Einstellungen** → **Verhandlungsregeln**
2. **Neue Regel** klicken
3. **Beispielwerte**:
   - Regelname: "Standard-Regel"
   - Mindestpreis: 70%
   - Auto-Annahme: 95%
   - Auto-Ablehnung: 60%
4. **Regel aktivieren** und **speichern**

### 3. System testen

1. **Angebote** → **Synchronisieren**
2. **Aktuelle eBay-Angebote** sollten geladen werden
3. **Testlauf** mit einem Angebot

## 🔧 Erweiterte Konfiguration

### Shopware-Integration (optional)

```env
# In .env hinzufügen
SHOPWARE_URL=https://ihr-shop.de
SHOPWARE_CLIENT_ID=ihr-client-id
SHOPWARE_CLIENT_SECRET=ihr-client-secret
```

### Automatischer Start (optional)

**Windows - Batch-Datei erstellen:**
```batch
@echo off
cd /d "C:\Pfad\zu\eBay-Bot-Lokal\backend"
python main.py
pause
```

**Linux/macOS - Service erstellen:**
```bash
# systemd Service für automatischen Start
sudo nano /etc/systemd/system/ebay-bot.service
```

## 🚨 Problemlösung

### Häufige Probleme

**1. "ModuleNotFoundError"**
```bash
# Lösung: Abhängigkeiten neu installieren
pip install --upgrade -r requirements.txt
```

**2. "Port bereits belegt"**
```bash
# Lösung: Port in .env ändern
PORT=5001
```

**3. "eBay API Fehler"**
- **Auth Token prüfen** (läuft ab!)
- **Sandbox-Modus deaktiviert?**
- **Internetverbindung stabil?**

**4. "OpenAI API Fehler"**
- **API-Key korrekt?**
- **Guthaben vorhanden?**
- **Rate Limits beachtet?**

### Logs prüfen

```bash
# Backend-Logs anzeigen
tail -f logs/ebay-bot.log

# Oder im Dashboard: Protokoll-Tab
```

### Support

Bei Problemen:
1. **Logs prüfen** (Protokoll-Tab)
2. **Konfiguration überprüfen** (.env-Datei)
3. **Internetverbindung testen**
4. **eBay Developer Console** prüfen

## 🎯 Nächste Schritte

Nach erfolgreicher Installation:

1. **Benutzerhandbuch lesen**: `docs/USER_GUIDE.md`
2. **Beispielregeln importieren**: `examples/sample_rules.json`
3. **Produktionsumgebung** einrichten
4. **Monitoring** aktivieren

---

**Bei Fragen zur Installation kontaktieren Sie den Support** 📞

