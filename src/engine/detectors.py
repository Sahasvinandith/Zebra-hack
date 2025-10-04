# @algorithm ScanAvoidance | Detects when RFID sees an item but no POS scan exists
def detect_scan_avoidance(rfid_event, pos_buffer):
    sku = rfid_event["data"]["sku"]
    found = any(pos["data"]["sku"] == sku for pos in pos_buffer)
    if not found:
        return {"type": "SCAN_AVOIDANCE", "sku": sku}
    return None

# @algorithm BarcodeSwitching | Detects mismatches between POS and Vision
def detect_barcode_switching(pos_event, vision_event, product_db):
    if not vision_event:
        return None
    if pos_event["data"]["sku"] != vision_event["data"]["predicted_product"]:
        pos_price = product_db[pos_event["data"]["sku"]]["price"]
        vision_price = product_db[vision_event["data"]["predicted_product"]]["price"]
        if vision_price > pos_price:
            return {"type": "BARCODE_SWITCHING", "sku": pos_event["data"]["sku"]}
    return None

# @algorithm WeightDiscrepancy | Detects mismatch between scanned item weight vs scale
def detect_weight_discrepancy(pos_event, scale_weight, product_db):
    sku = pos_event["data"]["sku"]
    expected_weight = product_db[sku]["weight"]
    if abs(scale_weight - expected_weight) > 50:  # 50g tolerance
        return {"type": "WEIGHT_DISCREPANCY", "sku": sku}
    return None
