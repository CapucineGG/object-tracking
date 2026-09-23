from ultralytics import YOLO
import cv2

LINE_Y = 300

model = YOLO("yolov8n.pt")

video = cv2.VideoCapture("data/vtest.avi")

fps= video.get(cv2.CAP_PROP_FPS)
width= int(video.get(cv2.CAP_PROP_FRAME_WIDTH))      
height= int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

fourcc = cv2.VideoWriter_fourcc(*"mp4v")   # le "codec" = format de compression vidéo utilisé
out = cv2.VideoWriter("data/output_line.mp4", fourcc, fps, (width, height))

previous_y = {}
count = 0

while True:
    ret, frame = video.read()
    if not ret:
      break

    results = model.track(frame, persist=True)

    for box in results[0].boxes:
        if box.id is None:
            continue

        track_id = int(box.id)
        x1, y1, x2, y2 = box.xyxy[0]
        cy = (y1 + y2) / 2

        if track_id in previous_y:
            ancienne_position = previous_y[track_id]
            if (ancienne_position < LINE_Y and cy >= LINE_Y) or (ancienne_position >= LINE_Y and cy < LINE_Y):
                count += 1
                print(f"Objet {track_id} a traversé la ligne. Compteur: {count}")

        previous_y[track_id] = cy

    annotated = results[0].plot()

    texte = f"Compteur: {count}"
    cv2.putText(annotated, texte, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    point1 = (0, LINE_Y)
    point2 = (width, LINE_Y)
    couleur = (0, 0, 255)  # rouge
    épaisseur = 2

    cv2.line(annotated, point1, point2, couleur, épaisseur)

    out.write(annotated)
    
video.release()
out.release()
