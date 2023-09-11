import cv2
import mediapipe as mp
from .type_exercise import TypeOfExercise

camera = cv2.VideoCapture(-1)

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def generate_frames(workout,sets,reps):
    global stage, set_counter, rep_counter
    ## Setup mediapipe instance
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while camera.isOpened():
            ret, frame = camera.read()
            # Recolor image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            # Make detection
            results = pose.process(image)

            # Recolor back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # Extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark

                set_counter, rep_counter, stage = TypeOfExercise(landmarks).calculate_exercise(image, workout, sets, reps)

            except:
                pass

            # Setup status box
            if stage == "Completed":
                cv2.rectangle(image, (170, 170), (400, 210), (0, 0, 255), -1)
                cv2.putText(image, stage,
                            (200, 200),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                TypeOfExercise(landmarks).reset_counters()
                stop_camera()
            else:
                cv2.rectangle(image, (0, 0), (100, 60), (245, 117, 16), -1)

                # Set data
                cv2.putText(image, 'SETS', (15, 15),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
                cv2.putText(image, str(set_counter),
                            (65, 15),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

                # Rep data
                cv2.putText(image, 'REPS', (15, 45),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
                cv2.putText(image, str(rep_counter),
                            (65, 45),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

                # Render detections
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                          mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                          mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                                      )
            ret, buffer = cv2.imencode('.jpg', image)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def stop_camera():
    #Stop camera
    if camera.isOpened():
        camera.release()

def start_camera():
    #Start camera
    if not camera.isOpened():
        camera.open(0)




