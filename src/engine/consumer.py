from collections import deque
from .detectors import (
    detect_scan_avoidance,
    detect_barcode_switching,
    detect_weight_discrepancy
)

alerts_store = deque(maxlen=200)

def process_event(source, event):
    generated_alerts = []

    if source == "rfid":
        alert = detect_scan_avoidance(event, [])
        if alert:
            alerts_store.append(alert)
            generated_alerts.append(alert)

    if source == "pos":
        vision_event = None
        scale_weight = event["data"].get("weight_g", 0)
        product_db = {
            event["data"]["sku"]: {
                "price": event["data"].get("price", 0),
                "weight": event["data"].get("weight_g", 0),
            }
        }

        alert = detect_barcode_switching(event, vision_event, product_db)
        if alert:
            alerts_store.append(alert)
            generated_alerts.append(alert)

        alert = detect_weight_discrepancy(event, scale_weight, product_db)
        if alert:
            alerts_store.append(alert)
            generated_alerts.append(alert)

    return generated_alerts

def get_alerts():
    return list(alerts_store)
