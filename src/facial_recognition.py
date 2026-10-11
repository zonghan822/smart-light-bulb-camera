"""Live facial recognition using a webcam and the CodeProject.AI Server.

Each frame is sent to the server's face recognition endpoint. The names of
recognised people are printed to stdout (picked up by Node-RED's exec node),
and the latest frame is saved so the dashboard can display it.

Adapted from https://github.com/DeepQuestAI/DeepStackExamples
"""

import cv2
import requests
import sys
from options import Options


def main():

    opts = Options()
    cap = cv2.VideoCapture(0)

    frame_index = 0
    skip_frame  = 5

    # Turn on camera if off
    if not cap.isOpened():
        cap.open(0)

    while True:
        predict = []

        # Get frame from camera
        ret, frame = cap.read()
        if not ret:
            continue

        # Encode the image
        retval, new_frame = cv2.imencode('.jpg', frame)

        # Save the image for the Node-RED dashboard
        cv2.imwrite(filename=str(opts.framePath), img=frame)

        # Send image to model for prediction
        response = requests.post(opts.endpoint("vision/face/recognize"),
                                 files={"image": new_frame},
                                 data={"min_confidence": 0.6}).json()

        # Get predictions
        if response["success"] == True:
            predictions = response['predictions']
        else:
            predictions = []

        for user in predictions:
            print(user["userid"], end="")

        for user in predictions:
            predict.append(user["userid"])

        predict_str = ', '.join(predict)

        # Draw a bounding box around each detected face
        for prediction in predictions:
            red, green, blue = 200, 100, 200
            frame = cv2.rectangle(frame,
                                  (prediction['x_min'], prediction['y_min']),
                                  (prediction['x_max'], prediction['y_max']),
                                  (red, green, blue), 1)

        cv2.putText(frame, predict_str, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        cv2.imshow('Image Viewer', frame)

        frame_index += 1

        if skip_frame > 1:
            if frame_index % skip_frame != 0:
                continue

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    sys.exit()


if __name__ == "__main__":
    main()
