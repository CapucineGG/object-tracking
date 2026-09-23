from ultralytics import YOLO
import cv2

model = YOLO("yolov8n.pt")

results = model("data/first_frame.jpg")

print(results[0])

for box in results[0].boxes:
    class_id = int(box.cls)
    class_name = model.names[class_id]
    confidence = float(box.conf)
    x1, y1, x2, y2 = box.xyxy[0]
    print(f"{class_name} - confiance: {confidence:.2f} - boîte: ({x1:.0f}, {y1:.0f}) à ({x2:.0f}, {y2:.0f})")


annotated = results[0].plot()
cv2.imwrite("data/first_frame_detected.jpg", annotated)