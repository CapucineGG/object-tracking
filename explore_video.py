import cv2

video = cv2.VideoCapture("data/vtest.avi")
ret, frame = video.read()

print(ret)
print(frame.shape)
print(frame.dtype)

fps= video.get(cv2.CAP_PROP_FPS)
frame_count= video.get(cv2.CAP_PROP_FRAME_COUNT)
frame_width= video.get(cv2.CAP_PROP_FRAME_WIDTH)
frame_height= video.get(cv2.CAP_PROP_FRAME_HEIGHT)

print(fps)
print(frame_count)
print(frame_width)
print(frame_height)

saved =cv2.imwrite("data/first_frame.jpg", frame)
print(saved)

video.release()