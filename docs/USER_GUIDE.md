# Benutzerhandbuch - eBay Preisvorschlags-Bot

## 🎯 Übersicht

Der eBay Preisvorschlags-Bot automatisiert Ihre Preisverhandlungen mit intelligenten, menschlich wirkenden Antworten.

## 📊 Dashboard

### Hauptübersicht
- **Gesamt Angebote**: Alle eingegangenen Preisvorschläge
- **Wartend**: Noch zu bearbeitende Angebote  
- **Angenommen**: Erfolgreich verkaufte Artikel
- **Erfolgsrate**: Prozentsatz erfolgreicher Verhandlungen

### Synchronisieren-Button
- **Grün (Aktiv)**: System läuft und überwacht eBay
- **Grau (Inaktiv)**: Manuelle Synchronisation erforderlich
- **Klick**: Sofortige Aktualisierung der Angebote

## 🛒 Angebote-Verwaltung

### Angebots-Übersicht
Jedes Angebot zeigt:
- **Artikel**: Name und eBay-Item-ID
- **Angebotspreis**: Vorgeschlagener Preis vs. Verkaufspreis
- **Käufer**: eBay-Benutzername
- **Status**: Wartend/Angenommen/Abgelehnt/Gegenangebot
- **Laufzeit**: Wie lange das Angebot bereits online ist
- **Aktionen**: Manuell bearbeiten oder analysieren

### Angebots-Status
- 🟡 **Wartend**: Noch nicht bearbeitet
- 🟢 **Angenommen**: Verkauf erfolgreich
- 🔴 **Abgelehnt**: Angebot zu niedrig
- 🔵 **Gegenangebot**: Bot hat Gegenvorschlag gemacht
- ⚪ **Abgelaufen**: Zeitlimit überschritten

### Manuelle Bearbeitung
1. **Angebot auswählen**
2. **Aktion wählen**:
   - **Annehmen**: Sofortiger Verkauf
   - **Ablehnen**: Höfliche Absage
   - **Gegenangebot**: Eigenen Preis vorschlagen
3. **Nachricht anpassen** (optional)
4. **Senden**

## ⚙️ Einstellungen

### API-Konfiguration

**eBay Trading API**
- **Application ID**: Ihre eBay App-ID
- **Developer ID**: Ihre eBay Developer-ID  
- **Certificate ID**: Ihr eBay-Zertifikat
- **Auth Token**: Ihr eBay-Authentifizierungstoken
- **Sandbox-Modus**: Für Tests (deaktivieren für Produktion!)

**OpenAI Integration**
- **API Key**: Für intelligente KI-Entscheidungen
- **Verbindung testen**: Prüft API-Zugang

### Verhandlungsregeln

#### Regel-Übersicht
- **Aktive Regeln**: Grün markiert mit ✓
- **Inaktive Regeln**: Grau dargestellt
- **Bearbeiten**: Klick auf Regel öffnet Editor
- **Löschen**: Regel dauerhaft entfernen

#### Regel-Editor
**Grundeinstellungen**
- **Regelname**: Eindeutige Bezeichnung
- **Regeltyp**: Allgemein oder Zeitbasiert
- **Aktiv**: Ein/Aus-Schalter

**Preislogik**
- **Mindestpreis (%)**: Untergrenze (z.B. 70% = nie unter 70% des Verkaufspreises)
- **Auto-Annahme (%)**: Automatisch annehmen ab diesem Wert (z.B. 95%)
- **Auto-Ablehnung (%)**: Automatisch ablehnen unter diesem Wert (z.B. 60%)
- **Max. Rabatt (%)**: Maximaler Nachlass bei Gegenangeboten

**Verhandlungsverhalten**
- **Max. Gegenangebote**: Wie oft nachverhandeln (1-3)
- **Verhandlungston**: Freundlich/Professionell/Bestimmt
- **Wartezeit**: Antwortzeit in Minuten (2-30)

#### Zeitbasierte Regeln
**Anwendung nach Angebotslaufzeit:**
- **0-7 Tage**: Neue Angebote (konservative Preise)
- **8-21 Tage**: Mittlere Laufzeit (moderate Flexibilität)  
- **22+ Tage**: Alte Angebote (maximale Flexibilität)

**Beispiel-Konfiguration:**
```
Neue Angebote (0-7 Tage):
- Mindestpreis: 80%
- Auto-Annahme: 95%
- Max. Rabatt: 10%

Alte Angebote (22+ Tage):
- Mindestpreis: 65%
- Auto-Annahme: 90%  
- Max. Rabatt: 20%
```

### Verhalten-Einstellungen

**Menschliches Verhalten**
- **Antwortzeiten**: Zufällige Verzögerungen (2-30 Min)
- **Sprachvariationen**: Verschiedene Formulierungen
- **Wochenend-Modus**: Langsamere Antworten Sa/So
- **Pausen**: Keine Antworten nachts (22-8 Uhr)

**Rate Limiting**
- **Max. Antworten/Stunde**: Schutz vor Spam-Verdacht
- **Tägliches Limit**: Maximale Aktivität pro Tag
- **Pause nach Fehlern**: Wartezeit bei API-Problemen

## 📋 Protokoll & Monitoring

### Aktivitäts-Log
- **Zeitstempel**: Wann passierte was
- **Aktion**: Was wurde gemacht
- **Angebot**: Welches Angebot betroffen
- **Ergebnis**: Erfolg oder Fehler
- **Details**: Zusätzliche Informationen

### Filter-Optionen
- **Datum**: Bestimmter Zeitraum
- **Typ**: Nur bestimmte Aktionen
- **Status**: Erfolg/Fehler/Warnung
- **Angebot**: Spezifisches Angebot

### Export-Funktionen
- **CSV-Export**: Für Excel-Analyse
- **PDF-Report**: Zusammenfassung für Buchhaltung
- **API-Log**: Technische Details für Support

## 🎯 Arbeitsabläufe

### Tägliche Routine
1. **Dashboard prüfen**: Neue Angebote?
2. **Synchronisieren**: Aktuelle Daten laden
3. **Wartende Angebote**: Manuelle Prüfung bei Bedarf
4. **Protokoll checken**: Fehler oder Auffälligkeiten?

### Wöchentliche Wartung
1. **Erfolgsrate analysieren**: Regeln optimieren?
2. **Neue Regeln testen**: A/B-Tests mit verschiedenen Strategien
3. **Protokoll-Export**: Daten für Analyse sichern
4. **System-Updates**: Neue Features installieren

### Monatliche Optimierung
1. **Statistiken auswerten**: Welche Regeln funktionieren?
2. **Preisstrategien anpassen**: Marktentwicklung berücksichtigen
3. **Shopware-Daten aktualisieren**: Neue Einkaufspreise
4. **Performance-Tuning**: System-Geschwindigkeit optimieren

## 🚨 Problemlösung

### Häufige Situationen

**"Keine neuen Angebote"**
- Synchronisieren-Button klicken
- eBay-Verbindung prüfen
- Auth Token noch gültig?

**"Bot antwortet nicht"**
- Regel aktiviert?
- OpenAI-Guthaben vorhanden?
- Rate Limits erreicht?

**"Falsche Entscheidungen"**
- Regeln zu aggressiv/konservativ?
- Mindestpreise anpassen
- KI-Prompts optimieren

**"API-Fehler"**
- Internetverbindung stabil?
- eBay-Server erreichbar?
- Protokoll für Details prüfen

### Notfall-Aktionen

**System sofort stoppen**
1. **Auto-Modus deaktivieren**
2. **Alle Regeln pausieren**  
3. **Manuelle Kontrolle übernehmen**

**Daten-Backup**
1. **Protokoll exportieren**
2. **Regeln sichern**
3. **Konfiguration kopieren**

## 💡 Tipps & Tricks

### Optimale Regelkonfiguration
- **Konservativ starten**: Lieber vorsichtig beginnen
- **A/B-Tests**: Verschiedene Strategien parallel testen
- **Marktbeobachtung**: Konkurrenzpreise berücksichtigen
- **Saisonalität**: Regeln je nach Jahreszeit anpassen

### Maximale Erfolgsrate
- **Schnelle Antworten**: Käufer warten nicht lange
- **Freundlicher Ton**: Höflichkeit verkauft besser
- **Faire Preise**: Gier schadet dem Geschäft
- **Flexibilität**: Bei alten Angeboten kompromissbereit sein

### Rechtliche Hinweise
- **Impressumspflicht**: Bei gewerblichem Verkauf
- **Widerrufsrecht**: Verbraucherrechte beachten
- **Steuerliche Pflichten**: Gewinne ordnungsgemäß versteuern
- **eBay-Richtlinien**: Plattform-Regeln einhalten

---

**Viel Erfolg mit Ihrem eBay-Preisvorschlags-Bot!** 🎯💰

