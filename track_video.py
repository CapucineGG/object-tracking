from ultralytics import YOLO
import cv2

model = YOLO("yolov8n.pt")

video = cv2.VideoCapture("data/vtest.avi")

fps= video.get(cv2.CAP_PROP_FPS)
width= int(video.get(cv2.CAP_PROP_FRAME_WIDTH))      
height= int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

fourcc = cv2.VideoWriter_fourcc(*"mp4v")   # le "codec" = format de compression vidéo utilisé
out = cv2.VideoWriter("data/output_tracked.mp4", fourcc, fps, (width, height))

while True:
    ret, frame = video.read()
    if not ret:
      break

    results = model.track(frame, persist=True)
    annotated = results[0].plot()

    out.write(annotated)
    
video.release()
out.release()
