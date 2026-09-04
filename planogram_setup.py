import cv2

IMAGE = r"V:\RetailAI\shelf.jpeg"

img = cv2.imread(IMAGE)

if img is None:
    print("Image not found!")
    exit()

# Resize for easier viewing
scale = 0.6
display = cv2.resize(img, None, fx=scale, fy=scale)

# Draw approximate 4 shelf slots
# Coordinates are based on your uploaded shelf image
slots = {
    "Top-Left (Maggi)": (260, 390, 700, 510),
    "Top-Right (5050)": (700, 390, 1190, 510),
    "Bottom-Left (Potazos)": (300, 680, 730, 770),
    "Bottom-Right (Dairy Milk)": (730, 680, 1190, 770),
}

for name, (x1, y1, x2, y2) in slots.items():

    # Scale coordinates
    p1 = (int(x1 * scale), int(y1 * scale))
    p2 = (int(x2 * scale), int(y2 * scale))

    cv2.rectangle(display, p1, p2, (0, 255, 0), 2)
    cv2.putText(
        display,
        name,
        (p1[0], p1[1] - 8),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (0, 255, 0),
        2
    )

cv2.imshow("RetailAI - Planogram Slots", display)

print("4 Planogram slots:")
for name, coords in slots.items():
    print(name, ":", coords)

print("\nPress Q to close.")

while True:
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

cv2.destroyAllWindows()