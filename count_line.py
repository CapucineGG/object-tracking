from ultralytics import YOLO
import cv2

model = YOLO("yolov8n.pt")

video = cv2.VideoCapture("data/vtest.avi")

fps= video.get(cv2.CAP_PROP_FPS)
width= int(video.get(cv2.CAP_PROP_FRAME_WIDTH))      
height= int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

LINE_A=(450,350)
LINE_B=(750,250)

fourcc = cv2.VideoWriter_fourcc(*"mp4v")   # le "codec" = format de compression vidéo utilisé
out = cv2.VideoWriter("data/output_line.mp4", fourcc, fps, (width, height))

previous_side = {}
count = 0
entree=0
sortie=0

def quel_cote(px, py, x1, y1, x2, y2):
    signe = (x2 - x1) * (py - y1) - (y2 - y1) * (px - x1)
    if signe > 0:
        return "gauche"
    elif signe < 0:
        return "droite"
    else:
        return "sur la ligne"

while True:
    ret, frame = video.read()
    if not ret:
      break

    results = model.track(frame, persist=True, classes=[0])  # 0 = personne

    for box in results[0].boxes:
        if box.id is None:
            continue

        track_id = int(box.id)
        x1, y1, x2, y2 = box.xyxy[0]
        cy = (y1 + y2) / 2

        if track_id in previous_side:
            ancienne_side = previous_side[track_id]
            nouvelle_side = quel_cote((x1 + x2) / 2, cy, LINE_A[0], LINE_A[1], LINE_B[0], LINE_B[1])
            if ancienne_side != nouvelle_side:
                count += 1
                print(f"Objet {track_id} a traversé la ligne. Compteur: {count}")
                if ancienne_side == "gauche" and nouvelle_side == "droite":
                    entree += 1
                elif ancienne_side == "droite" and nouvelle_side == "gauche":
                    sortie += 1

        previous_side[track_id] = quel_cote((x1 + x2) / 2, cy, LINE_A[0], LINE_A[1], LINE_B[0], LINE_B[1])

    annotated = results[0].plot()

    texte = f"Compteur: {count} Entrée: {entree} Sortie: {sortie}"
    cv2.putText(annotated, texte, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    point1 = LINE_A
    point2 = LINE_B
    couleur = (0, 0, 255)  # rouge
    épaisseur = 2

    cv2.line(annotated, point1, point2, couleur, épaisseur)

    out.write(annotated)
    
video.release()
out.release()
