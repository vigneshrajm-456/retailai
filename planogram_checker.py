import cv2

# =========================
# PLANOGRAM CONFIGURATION
# =========================

IMAGE = r"V:\RetailAI\shelf.jpeg"

# Expected product for each slot
expected = {
    "Top-Left": "maggi",
    "Top-Right": "5050",
    "Bottom-Left": "potazos",
    "Bottom-Right": "dairy milk"
}

# Slot coordinates from our shelf image
slots = {
    "Top-Left": (260, 390, 700, 510),
    "Top-Right": (700, 390, 1190, 510),
    "Bottom-Left": (300, 680, 730, 770),
    "Bottom-Right": (730, 680, 1190, 770)
}

# =========================
# DUMMY DETECTIONS
# =========================
# We are pretending YOLO detected these products.
#
# Format:
# (product_name, center_x, center_y)

detections = [
    ("maggi", 450, 450),
    ("5050", 900, 450),
    ("potazos", 500, 720),
    ("dairy milk", 950, 720)
]

# =========================
# CHECK WHICH SLOT
# =========================

results = {}

for slot_name, (x1, y1, x2, y2) in slots.items():

    detected_product = None

    for product, cx, cy in detections:

        if x1 <= cx <= x2 and y1 <= cy <= y2:
            detected_product = product
            break

    expected_product = expected[slot_name]

    if detected_product is None:
        status = "MISSING"

    elif detected_product == expected_product:
        status = "CORRECT"

    else:
        status = "MISPLACED"

    results[slot_name] = {
        "expected": expected_product,
        "detected": detected_product,
        "status": status
    }

# =========================
# DISPLAY RESULTS
# =========================

print("\n==============================")
print("      PLANOGRAM RESULT")
print("==============================")

correct = 0

for slot, result in results.items():

    print(f"\n{slot}")
    print(f"Expected : {result['expected']}")
    print(f"Detected : {result['detected']}")
    print(f"Status   : {result['status']}")

    if result["status"] == "CORRECT":
        correct += 1

compliance = (correct / len(slots)) * 100

print("\n==============================")
print(f"Planogram Compliance: {compliance:.0f}%")
print("==============================")