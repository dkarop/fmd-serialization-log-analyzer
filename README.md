# FMD Serialization Log Analyzer

## Overview
A lightweight, fast Python utility designed for industrial Track & Trace (Serialization) environments. This script parses production JSON logs to identify critical compliance anomalies, such as duplicate serial numbers (SNs) and network timeout events during API syncing with external hubs (e.g., EMVS).

## Features
* **Duplicate Detection:** Scans commissioning events to ensure zero duplicate serial numbers are processed.
* **Network Health Monitoring:** Identifies and extracts failed sync events (timeouts) to alert IT operations.
* **Production-Ready Logging:** Utilizes standard Python logging for easy integration with Syslog or SIEM platforms.

## Prerequisites
* Python 3.8+
* No external dependencies required (uses built-in Python libraries).

## Usage
1. Place your production log file in an accessible directory (e.g., `/var/log/production/fmd_events.log`).
2. Update the `log_file_path` variable in the script if necessary.
3. Execute the script:
```bash
   python analyze_fmd_logs.py
```
## Example Output
2026-06-14 10:15:00,123 - CRITICAL - FMD_ANALYZER - Compliance Alert: Found 2 duplicate serial numbers!

2026-06-14 10:15:00,124 - WARNING - FMD_ANALYZER - Network Alert: 1 events failed to sync (timeouts).

2026-06-14 10:15:00,125 - INFO - FMD_ANALYZER - Analysis Complete. Report: {'duplicates_found': ['SN123456789', 'SN987654321'], 'failed_sync_events': ['Event_ID_402']}
