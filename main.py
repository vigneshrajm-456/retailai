from ultralytics import YOLO
import cv2

person_model = YOLO("yolo11s.pt")
product_model = YOLO("models/product_model.pt")

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    if not ret:
        break

    # Run BOTH models on the original clean frame
    person_results = person_model(frame, conf=0.50, verbose=False)
    potazos_results = potazos_model(frame, conf=0.70, verbose=False)

    # Draw person detections
    output = person_results[0].plot()

    # Draw Potazos detections
    output = potazos_results[0].plot(img=output)

    cv2.imshow("RetailAI - Person + Potazos", output)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()