# SolarHQ — Home Assistant App: Specificații Aplicație

> **Data**: 2026-03-25 | **Versiune**: 1.0.0

---

## 1. Ce face aplicația

SolarHQ este un app Home Assistant care monitorizează o instalație solară și calculează performanța ei financiară. Datele de energie vin automat din senzorii Home Assistant. Utilizatorul adaugă costurile instalației și prețurile energiei, iar aplicația calculează economiile, ROI-ul și când se amortizează investiția.

---

## 2. Modulul de Energie

### 2.1 Date înregistrate lunar

| Câmp | Unitate | Descriere |
|------|---------|-----------|
| Producție solar | kWh | Energia generată de panouri |
| Consum total | kWh | Energia consumată în casă |
| Import rețea | kWh | Energia cumpărată din rețea |
| Export rețea | kWh | Energia vândută în rețea |
| Încărcare baterie | kWh | Energia stocată în baterie |
| Descărcare baterie | kWh | Energia extrasă din baterie |

### 2.2 Sursa datelor

- Datele sunt sincronizate automat din senzorii Home Assistant (la fiecare oră)
- Utilizatorul selectează în Settings ce senzor HA corespunde fiecărui câmp
- Senzorii sunt descoperiți automat din instanța HA curentă
- Se poate și introduce manual dacă nu există senzori configurați

---

## 3. Modulul Financiar

### 3.1 Date introduse de utilizator

**Costuri instalație**
- Descriere componentă (ex: "Panouri solare", "Invertor", "Baterie")
- Valoare (RON/EUR/USD)
- Durată de viață estimată (ani) — folosit pentru calculul costului lunar per componentă

**Prețuri energie rețea** (per lună)
- Preț cumpărare kWh din rețea

**Prețuri prosumator** (per lună, opțional)
- Preț cumpărare kWh (import)
- Preț vânzare kWh (export)
- Tarif fix lunar
- Taxe

**Offset economii** (o singură dată)
- Economii acumulate înainte de prima înregistrare lunară (pentru cei care au instalația de mai mult timp)

### 3.2 Calcule automate (11 indicatori)

| Indicator | Formulă | Output |
|-----------|---------|--------|
| Economii totale | Offset + Σ(consum − import) × preț_lunar | RON acumulat |
| Investiție totală | Σ(toate costurile) | RON total investit |
| ROI | (Economii / Investiție) × 100 | % |
| Economie medie lunară | Economii totale / nr. luni | RON/lună |
| Perioadă amortizare | Investiție / Economie medie lunară | luni |
| Proiecție 5 ani fără solar | Consum mediu × Preț rețea × 60 luni | RON (ce ai fi plătit) |
| Cost kWh solar produs | Cost lunar componente / Producție medie solar | RON/kWh |
| Autoconsum | Consum − Import rețea | kWh + % din producție |
| Venit export | Export × Preț vânzare | RON |
| Capacitate instalată | Producție anuală / 1100 | kWp estimat |
| Analiză tendințe | Medii sezoniere, comparații anuale, prognoze ROI | grafice |

---

## 4. Dashboard

Pagina principală afișează starea curentă a instalației:

**Carduri KPI:**
- Economii acumulate total
- ROI curent (%)
- Timp până la amortizare (luni rămase)
- Cost kWh solar produs
- (dacă prosumator) Autosuficiență %, venit export, capacitate kWp

**Grafice:**

| # | Grafic | Tip |
|---|--------|-----|
| 1 | Economii lunare | Bar |
| 2 | Producție solar vs Consum | Line/Area |
| 3 | Import rețea lunar | Bar |
| 4 | Baterie încărcare/descărcare | Dual bar |
| 5 | Producție vs Consum (prosumator) | Dual axis |
| 6 | Bilanț energetic (autoconsum + export + import) | Stacked bar |
| 7 | Economii cumulative în timp | Area |
| 8 | Pattern sezonier (medii ian-dec) | Bar |
| 9 | Comparație an la an | Grouped bar |

---

## 5. Pagini Aplicație

| Pagină | Funcționalitate |
|--------|----------------|
| **Dashboard** | KPI-uri + toate graficele |
| **Energie** | Tabel înregistrări lunare + adăugare manuală |
| **Costuri** | Gestionare costuri instalație (add/edit/delete) |
| **Prețuri** | Prețuri rețea și prosumator per lună |
| **Tendințe** | Grafice sezoniere, YoY, prognoze amortizare |
| **Setări** | Selectare senzori HA + configurare generală |

---

## 6. Setări și Configurare

### 6.1 Opțiuni add-on (în UI-ul Supervisor HA)
- Limbă interfață (RO / EN)
- Monedă (RON / EUR / USD / GBP)
- Nivel log

### 6.2 Pagina Setări din aplicație
- Selectare senzori HA pentru fiecare câmp de energie
- Buton "Descoperă senzori" — listează toți senzorii energy/power din HA
- Buton "Sincronizare manuală" — forțare sync date din HA
- Vizualizare ultima sincronizare reușită

---

## 7. Export Date

- Buton "Export CSV" din Dashboard
- Fișier descărcat: `solarhq_YYYY-MM-DD.csv`
- Conținut: toate înregistrările lunare + indicatorii calculați

---

## 8. Integrare Home Assistant

- Senzorii sunt citiți prin Supervisor API intern (fără URL sau token manual)
- Sincronizare automată la fiecare oră în fundal
- Sincronizare la 10 minute pentru date în timp real (dacă configurate)
- Locația (numele casei) este preluată automat din configurația HA
- Accesul la aplicație este protejat de autentificarea HA (Ingress)

---

## 9. Stack Tehnic

| Layer | Tehnologie |
|-------|-----------|
| Backend API | FastAPI 0.135 + Uvicorn 0.42 |
| ORM async | SQLAlchemy 2.0 + aiosqlite 0.22 |
| Migrații DB | Alembic 1.18 |
| Validare date | Pydantic v2 |
| Task scheduling | APScheduler 3.11 |
| HTTP client | httpx 0.28 |
| Database | SQLite 3 (în `/data/`) |
| Frontend | Vue 3.5 + Vite 8 |
| State management | Pinia 3 |
| Router | Vue Router 5 |
| Charts | ApexCharts 5 + vue3-apexcharts |
| CSS | Tailwind CSS 4 |
| HTTP calls FE | Axios 1.13 |
| Process manager | s6-overlay v3 |
| Base image | ghcr.io/hassio-addons/base-python:3.11 (Alpine) |
