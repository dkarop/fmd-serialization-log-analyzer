import json
import logging
from collections import defaultdict
from typing import List, Dict

# Ρύθμιση Logging για περιβάλλον παραγωγής
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - FMD_ANALYZER - %(message)s'
)

def analyze_serialization_logs(log_file_path: str) -> Dict[str, List[str]]:
    """
    Parses production Track & Trace logs to identify duplicate serial numbers
    and network timeout events during API syncing.
    """
    duplicates = defaultdict(int)
    failed_syncs = []
    
    try:
        with open(log_file_path, 'r') as file:
            for line_number, line in enumerate(file, start=1):
                try:
                    event = json.loads(line.strip())
                    
                    # Έλεγχος για διπλότυπα Serial Numbers
                    if event.get("event_type") == "commissioning":
                        sn = event.get("serial_number")
                        if sn:
                            duplicates[sn] += 1
                            
                    # Έλεγχος για Network Timeouts (π.χ. προς τον EMVS hub)
                    if event.get("status") == "timeout":
                        failed_syncs.append(event.get("event_id", f"Unknown_ID_Line_{line_number}"))
                        
                except json.JSONDecodeError:
                    logging.warning(f"Corrupted JSON format at line {line_number}")
                    
    except FileNotFoundError:
        logging.error(f"Log file {log_file_path} not found. Check network share availability.")
        return {}

    # Φιλτράρισμα μόνο των πραγματικών διπλότυπων
    actual_duplicates = {sn: count for sn, count in duplicates.items() if count > 1}
    
    if actual_duplicates:
        logging.critical(f"Compliance Alert: Found {len(actual_duplicates)} duplicate serial numbers!")
    if failed_syncs:
        logging.warning(f"Network Alert: {len(failed_syncs)} events failed to sync (timeouts).")

    return {
        "duplicates_found": list(actual_duplicates.keys()),
        "failed_sync_events": failed_syncs
    }

if __name__ == "__main__":
    # Παράδειγμα εκτέλεσης σε τοπικό αρχείο
    report = analyze_serialization_logs("/var/log/production/fmd_events.log")
    logging.info(f"Analysis Complete. Report: {report}")
