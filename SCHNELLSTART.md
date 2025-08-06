# 🚀 Schnellstart - eBay Preisvorschlags-Bot

## ⚡ In 5 Minuten startklar

### 1. Entpacken & Verzeichnis öffnen
```bash
unzip eBay-Bot-Lokal.zip
cd eBay-Bot-Lokal/backend
```

### 2. Python-Abhängigkeiten installieren
```bash
pip install -r requirements.txt
```

### 3. Konfiguration erstellen
```bash
cp .env.example .env
```

**Wichtig**: `.env` mit Ihren eBay-Zugangsdaten ausfüllen!

### 4. System starten
```bash
python main.py
```

### 5. Dashboard öffnen
Browser: **http://localhost:5000**

## 🎯 Erste Schritte im Dashboard

1. **Einstellungen** → **API-Konfiguration** → **Verbindung testen**
2. **Einstellungen** → **Verhandlungsregeln** → **Neue Regel** erstellen
3. **Angebote** → **Synchronisieren** → Erste eBay-Angebote laden

## ⚙️ Empfohlene Erst-Konfiguration

**Standard-Regel für Einsteiger:**
- Regelname: "Meine erste Regel"
- Mindestpreis: 75%
- Auto-Annahme: 95%
- Auto-Ablehnung: 65%
- Verhandlungston: Freundlich
- Wartezeit: 20 Minuten

## 🆘 Probleme?

**Python nicht gefunden?**
```bash
python3 main.py
```

**Port belegt?**
```bash
# In .env ändern:
PORT=5001
```

**eBay-Verbindung fehlgeschlagen?**
- Auth Token prüfen (läuft ab!)
- Sandbox-Modus deaktiviert?

## 📚 Weitere Hilfe

- **Detaillierte Installation**: `docs/INSTALLATION.md`
- **Vollständiges Handbuch**: `docs/USER_GUIDE.md`
- **Beispielkonfigurationen**: `examples/`

---

**Viel Erfolg!** 🎯

