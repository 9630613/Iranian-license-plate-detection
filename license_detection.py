import torch
import cv2
import time
import psutil
# torch.hub.load('the directory of yolo file', 'custom', 'the directory of trained algorithm' ,source='local')
model = torch.hub.load('directory of yolo file', 'custom', 'best.pt', source='local')
model.cpu()
time_count = 0
cap = cv2.VideoCapture('video.mp4 or camera')  # input of video
count = 0  # the counter for the number of detected data
target = 5  # the number for setting selected frames of video
i = target

while True:
    start_time = time.time()
    ret, frame = cap.read()
    if ret:
        if i == 0:
            i = target
            im = frame
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            model.conf = 0.35  # NMS confidence threshold
            results = model(frame, size=640)  # includes NMS
            res = results.xyxy[0]  # extracting the coordinates of a license plate rectangle
            re = res.tolist()  # converting to a list

            if re:  # if the model detected any plates
                results.save()  # saving the result picture in "runs/ detect/ exp*"
                Cord = re[0]
                # separating the coordinates
                x_min = int(Cord[0])
                x_max = int(Cord[2])
                y_min = int(Cord[1])
                y_max = int(Cord[3])
                # cropping the detected picture
                crop_img = im[y_min - 1:y_max + 1, x_min - 1:x_max + 1]
                # saving the cropped images with the coordinates in 2 files(license_plate, license_index)
                cv2.imwrite('license_plate/frame%d.jpg' % count, crop_img)
                with open('license_index/frame%d.txt' % count, 'w+') as w:
                    w.write(str(Cord))
                count += 1
                # accounting the time for each process
                end_time = time.time()
                time_count = end_time - start_time
                print(f'The process time is : {time_count } sec')
        i -= 1
        cv2.imshow('frame', frame)
        cv2.waitKey(30)
