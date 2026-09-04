from ultralytics import YOLO
import cv2

# ==========================================
# MODELS
# ==========================================

person_model = YOLO(r"V:\RetailAI\yolo11s.pt")

product_model = YOLO(
    r"V:\RetailAI\runs\detect\train-3\weights\best.pt"
)

# ==========================================
# WEBCAM
# ==========================================

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("ERROR: Webcam not found")
    exit()

# ==========================================
# PLANOGRAM
# ==========================================

expected = {
    "Top-Left": "maggi",
    "Top-Right": "5050",
    "Bottom-Left": "potazos",
    "Bottom-Right": "dairy milk"
}

# ------------------------------------------
# TEMPORARY SLOT COORDINATES
# 640 x 480 webcam
# We will adjust these after seeing shelf.
# ------------------------------------------

slots = {
    "Top-Left": (50, 100, 320, 240),
    "Top-Right": (320, 100, 590, 240),

    "Bottom-Left": (50, 240, 320, 400),
    "Bottom-Right": (320, 240, 590, 400)
}

# ==========================================
# MAIN LOOP
# ==========================================

while True:

    ret, frame = cap.read()

    if not ret:
        print("ERROR: Cannot read webcam")
        break

    # ======================================
    # PERSON DETECTION
    # ======================================

    person_results = person_model(
        frame,
        conf=0.50,
        verbose=False
    )

    # Draw person detections
    for box in person_results[0].boxes:

        cls = int(box.cls[0])

        # COCO class 0 = person
        if cls != 0:
            continue

        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
        confidence = float(box.conf[0])

        cv2.rectangle(
            frame,
            (int(x1), int(y1)),
            (int(x2), int(y2)),
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            f"PERSON {confidence:.2f}",
            (int(x1), int(y1) - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2
        )

    # ======================================
    # PRODUCT DETECTION
    # ======================================

    product_results = product_model(
        frame,
        conf=0.50,
        verbose=False
    )

    detections = []

    for box in product_results[0].boxes:

        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()

        cls = int(box.cls[0])
        confidence = float(box.conf[0])

        product = product_model.names[cls]

        # Product center
        cx = int((x1 + x2) / 2)
        cy = int((y1 + y2) / 2)

        detections.append(
            (product, cx, cy, confidence)
        )

        # Product bounding box
        cv2.rectangle(
            frame,
            (int(x1), int(y1)),
            (int(x2), int(y2)),
            (255, 0, 0),
            2
        )

        cv2.putText(
            frame,
            f"{product} {confidence:.2f}",
            (int(x1), int(y1) - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 0, 0),
            2
        )

    # ======================================
    # PLANOGRAM CHECK
    # ======================================

    correct = 0

    for slot_name, (x1, y1, x2, y2) in slots.items():

        detected_product = None

        for product, cx, cy, confidence in detections:

            if x1 <= cx <= x2 and y1 <= cy <= y2:

                detected_product = product
                break

        expected_product = expected[slot_name]

        # ------------------------------
        # STATUS
        # ------------------------------

        if detected_product is None:

            status = "MISSING"

        elif detected_product == expected_product:

            status = "CORRECT"
            correct += 1

        else:

            status = "MISPLACED"

        # ------------------------------
        # DRAW SLOT
        # ------------------------------

        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            (255, 255, 0),
            2
        )

        cv2.putText(
            frame,
            f"{slot_name}: {status}",
            (x1, y1 - 8),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.45,
            (255, 255, 0),
            2
        )

    # ======================================
    # COMPLIANCE
    # ======================================

    compliance = (correct / 4) * 100

    cv2.putText(
        frame,
        f"Planogram Compliance: {compliance:.0f}%",
        (20, 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.75,
        (0, 255, 255),
        2
    )

    # ======================================
    # DISPLAY
    # ======================================

    cv2.imshow(
        "RetailAI - Person + Product + Planogram",
        frame
    )

    # Q = quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()