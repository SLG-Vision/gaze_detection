from components.face_detection import HaarCascade
from components.face_landmark import FaceLandmarkTracking
from components.pupil_detection import PupilDetection
from components.pnp_solver import PnPSolver

import cv2
import numpy as np


vid = cv2.VideoCapture(0)

landmark_tracking = FaceLandmarkTracking()
pupil_detection = PupilDetection()
# np.load('calib_results.npz')
pnp_solver = PnPSolver(np.load('calib_results.npz'))

while(True):
    ret, frame = vid.read()
    #frame = cv2.imread("rdg.jpg")
    framebg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    for face in landmark_tracking.face_analysis(framebg):
        image_points = np.array([
            face.get("traits").get("nose"),
            face.get("traits").get("chin"),
            face.get("eye_corners").get("sx_out"),
            face.get("eye_corners").get("dx_out"),
            face.get("traits").get("mouth_sx"),
            face.get("traits").get("mouth_dx"),
        ], dtype="double")

        nose_end_point2D, roll, pitch, yaw = pnp_solver.pose(
            frame.shape, image_points)

        frame = cv2.line(frame, tuple(image_points[0].ravel().astype(int)), tuple(
            nose_end_point2D[0].ravel().astype(int)), (255, 0, 0), 3)
        frame = cv2.line(frame, tuple(image_points[0].ravel().astype(int)), tuple(
            nose_end_point2D[1].ravel().astype(int)), (0, 255, 0), 3)
        frame = cv2.line(frame, tuple(image_points[0].ravel().astype(int)), tuple(
            nose_end_point2D[2].ravel().astype(int)), (0, 0, 255), 3)

        if roll is not None and pitch is not None and yaw is not None:
            cv2.putText(frame, "Roll:" + str(round(roll, 3)), (500, 50),
                        cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1, cv2.LINE_AA)
            cv2.putText(frame, "Pitch:" + str(round(pitch, 3)), (500, 70),
                        cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1, cv2.LINE_AA)
            cv2.putText(frame, "Yaw:" + str(round(yaw, 3)), (500, 90),
                        cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1, cv2.LINE_AA)

    cv2.imshow('frame',  frame)
    # cv2.waitKey(10000)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


vid.release()
