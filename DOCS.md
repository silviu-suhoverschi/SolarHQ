# SolarHQ — Documentation

SolarHQ is a Home Assistant add-on that monitors your solar energy installation and calculates financial performance: savings, ROI, payback period, and more.

---

## Installation

1. In Home Assistant, go to **Settings → Add-ons → Add-on Store**
2. Click the menu (⋮) and select **Repositories**
3. Add the SolarHQ repository URL and click **Add**
4. Find **SolarHQ** in the store and click **Install**
5. Configure the options (see below) and click **Start**
6. Open the **SolarHQ** panel from the HA sidebar

---

## Configuration Options

| Option | Description | Default | Values |
|--------|-------------|---------|--------|
| `log_level` | Logging verbosity | `info` | `trace`, `debug`, `info`, `notice`, `warning`, `error`, `fatal` |
| `language` | UI language | `ro` | `ro`, `en`, `de`, `fr`, `es` |
| `currency` | Currency for financial calculations | `RON` | `RON`, `EUR`, `USD`, `GBP` |

---

## First-Time Setup

### 1. Select Energy Sensors

Go to **Settings → HA Energy Sensors**:

1. Click **Discover Sensors** to auto-detect your energy entities from Home Assistant
2. Select the appropriate sensor for each category:
   - **Solar Production** — your solar inverter total energy sensor (`device_class: energy`)
   - **Grid Import** — energy consumed from the grid
   - **Grid Export** — energy fed back to the grid
   - **Load / Consumption** — total household consumption
   - **Battery Charge** — *(optional)* battery charging energy
   - **Battery Discharge** — *(optional)* battery discharging energy
3. Click **Save Sensor Config**
4. Click **Sync Now** to import up to 13 months of historical data from HA

> **Tip:** Sensors must have `device_class: energy` and `state_class: total_increasing` to appear in discovery.

### 2. Configure Your Solar System

In **Settings → Solar System**:

- **Initial Investment** — total cost of your solar installation (panels, inverter, installation)
- **Currency** — currency for the investment amount

### 3. Configure Pricing

In the **Pricing** section:

- Add your grid electricity rate (price per kWh you pay)
- Add your prosumer export rate if you receive compensation for grid export
- Use `flat`, `peak`, or `offpeak` tiers for time-of-use pricing

---

## KPI Reference

| KPI | Description | Good Value |
|-----|-------------|------------|
| **ROI %** | Return on investment to date: `(savings / investment) × 100` | >50% after 5 years |
| **Payback Period** | Years until investment is fully recovered | <10 years |
| **Self-Consumption Rate** | % of solar energy used directly (not exported) | >60% |
| **Solar Price** | Effective cost per kWh produced: `investment / total_kWh` | <0.10 RON/kWh |
| **Capacity Factor** | Actual vs. theoretical maximum output | 15–20% in Romania |
| **Export Income** | Total revenue from grid export at prosumer rate | — |
| **Autarky Rate** | % of consumption covered by solar | >50% is excellent |

---

## Manual Data Entry

If HA energy sensors are not available or you want to correct a month:

1. Go to **Energy** and click **+ Add Record**
2. Enter the year, month, and kWh values for each field
3. Battery fields are optional — leave blank if no battery

Similarly, add installation or subscription costs in the **Costs** section.

---

## CSV Export

Click **Export CSV** in the Energy view toolbar to download all monthly records with calculated self-consumption, cost data, and source metadata as a `.csv` file (`solarhq_export.csv`).

---

## Trends & Forecasts

The **Trends** view shows:

- **Seasonal Pattern** — average solar production per month across all years
- **Year over Year** — annual solar production and savings comparison
- **ROI Forecast** — 3-scenario projection (base / optimistic +30% / pessimistic -30%) over the recorded period

---

## Troubleshooting

### Add-on won't start
- Check the add-on logs: **Settings → Add-ons → SolarHQ → Logs**
- Verify the `/data` directory is writable (mapped in add-on config)
- Ensure no other service is using port 8099

### No sensors discovered
- Ensure `homeassistant_api: true` is set in the add-on configuration
- Verify your sensors have `device_class: energy` set in HA
- Try restarting Home Assistant and then the add-on
- Check that the `SUPERVISOR_TOKEN` environment variable is present in the container logs (should never be logged directly)

### Dashboard shows zero values
- Verify sensor configuration is saved in Settings
- Run a manual sync: **Settings → Sync Now**
- Confirm sensors have long-term statistics (LTS) recorded in HA Recorder
- HA requires at least a few days of data before LTS statistics are available

### HA Sync shows no data for recent months
- HA only stores LTS statistics after sensors have been tracked for at least 5 days
- Check `ha addon logs solarhq` for sync errors

### UI not loading / blank page
- Hard-refresh the browser (Ctrl+Shift+R)
- Check browser console for JavaScript errors
- Ensure the `../static/` directory was populated during the Docker build

---

## FAQ

**Q: Can I use this without HA energy sensors?**
A: Yes. Manually enter monthly kWh values in the **Energy** section. All financial calculations work with manual data.

**Q: Does this replace the HA Energy Dashboard?**
A: No. SolarHQ complements it — HA Energy Dashboard tracks real-time usage, SolarHQ focuses on financial performance, ROI, and long-term trends.

**Q: Is my data sent anywhere?**
A: No. All data is stored in a local SQLite database at `/data/solarhq.db` inside your HA instance. The add-on makes no external network connections.

**Q: How often does the sync run automatically?**
A: Every hour, at the top of the hour (`:00`). You can also trigger it manually from Settings.

**Q: Can I edit data that was synced from HA?**
A: Yes. Synced records appear with an "HA Sync" badge but can be edited or deleted manually. The next sync will not overwrite manual edits — it performs an upsert only on fields from HA.

**Q: What happens to my data after an add-on update?**
A: Data in `/data/solarhq.db` is preserved. Alembic migrations run automatically on startup and apply schema changes without dropping data.

**Q: Which architectures are supported?**
A: amd64 (NUC, VMs), aarch64 (Raspberry Pi 4), and armv7 (older Raspberry Pi).

---

## References

- [Home Assistant Add-on Development](https://developers.home-assistant.io/docs/add-ons/)
- [HA Energy Sensors documentation](https://www.home-assistant.io/docs/energy/)
- [HA Ingress documentation](https://developers.home-assistant.io/docs/add-ons/presentation#ingress)
