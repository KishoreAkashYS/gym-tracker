import mediapipe as mp
from .body_angle import BodyAngle
import cv2
import numpy as np
import threading
import pyttsx3

mp_pose = mp.solutions.pose

class TypeOfExercise(BodyAngle):
    set_counter = 1
    rep_counter = 0
    threshold = 0
    stage = ""

    def __init__(self, landmarks):
        super().__init__(landmarks)

    def reset_counters(self):
        TypeOfExercise.set_counter = 1
        TypeOfExercise.rep_counter = 0
        TypeOfExercise.threshold = 0
        TypeOfExercise.stage = ""

    def push_up(self, image, sets, reps):
        # Calculate angle
        elbow_angle = self.left_elbow_angle()
        shoulder_angle = self.left_shoulder_angle()
        hip_angle = self.left_hip_angle()

        #Visualize angle
        cv2.putText(image, str(round(elbow_angle[0], 2)),
                    tuple(np.multiply(elbow_angle[1], [640, 480]).astype(int)),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3, cv2.LINE_AA
                    )

        cv2.putText(image, str(round(shoulder_angle[0], 2)),
                    tuple(np.multiply(shoulder_angle[1], [640, 480]).astype(int)),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3, cv2.LINE_AA
                    )

        cv2.putText(image, str(round(hip_angle[0], 2)),
                    tuple(np.multiply(hip_angle[1], [640, 480]).astype(int)),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3, cv2.LINE_AA
                    )

        # pushup counter logic
        if TypeOfExercise.set_counter <= sets:
            if TypeOfExercise.rep_counter < reps:
                if elbow_angle[0] > 160 and shoulder_angle[0] > 40 and hip_angle[0] > 160:
                    TypeOfExercise.stage = "down"
                if elbow_angle[0] <= 90 and hip_angle[0] > 160 and TypeOfExercise.stage == "down":
                    TypeOfExercise.stage = "up"
                    TypeOfExercise.rep_counter += 1
                    threading.Thread(target=self.spell_out_rep_counter).start()
            else:
                TypeOfExercise.set_counter += 1
                TypeOfExercise.rep_counter = 0
        else:
            TypeOfExercise.stage = "Completed"

        return [TypeOfExercise.set_counter, TypeOfExercise.rep_counter, TypeOfExercise.stage]

    def pull_up(self, sets, reps):
        #Obtain average of both left and right elbow and nose landmarks

        avg_elbow = (self.landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y +
                     self.landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y) / 2

        nose_y = self.landmarks[mp_pose.PoseLandmark.NOSE.value].y

        #Pull up logic
        if TypeOfExercise.set_counter <= sets:
            if TypeOfExercise.rep_counter < reps:
                if nose_y > avg_elbow:
                    TypeOfExercise.stage = "down"
                if nose_y < avg_elbow and TypeOfExercise.stage == "down":
                    TypeOfExercise.stage = "up"
                    TypeOfExercise.rep_counter += 1
                    threading.Thread(target=self.spell_out_rep_counter).start()
            else:
                TypeOfExercise.set_counter += 1
                TypeOfExercise.rep_counter = 0
        else:
            TypeOfExercise.stage = "Completed"

        return [TypeOfExercise.set_counter, TypeOfExercise.rep_counter, TypeOfExercise.stage]

    def squat(self, image, sets, reps):
        #Calculate angle
        hip_angle = self.left_hip_angle()
        knee_angle = self.left_knee_angle()

        #Visualize angle
        cv2.putText(image, str(round(hip_angle[0], 2)),
                    tuple(np.multiply(hip_angle[1], [640, 480]).astype(int)),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3, cv2.LINE_AA
                    )

        cv2.putText(image, str(round(knee_angle[0], 2)),
                    tuple(np.multiply(knee_angle[1], [640, 480]).astype(int)),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3, cv2.LINE_AA
                    )

        # Squat Logic
        if TypeOfExercise.set_counter <= sets:
            if TypeOfExercise.rep_counter < reps:
                if hip_angle[0] < 85 and knee_angle[0] < 90:
                    TypeOfExercise.stage = "down"
                if hip_angle[0] > 170 and knee_angle[0] > 170 and TypeOfExercise.stage == "down":
                    TypeOfExercise.stage = "up"
                    TypeOfExercise.rep_counter += 1
                    threading.Thread(target=self.spell_out_rep_counter).start()
            else:
                TypeOfExercise.set_counter += 1
                TypeOfExercise.rep_counter = 0
        else:
            TypeOfExercise.stage = "Completed"

        return [TypeOfExercise.set_counter, TypeOfExercise.rep_counter, TypeOfExercise.stage]

    def biceps(self, image, sets, reps):
        # Calculate angle
        left_angle = self.left_elbow_angle()
        right_angle = self.right_elbow_angle()

        #Visualize angle
        cv2.putText(image, str(round(left_angle[0], 2)),
                    tuple(np.multiply(left_angle[1], [640, 480]).astype(int)),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3, cv2.LINE_AA
                    )
        cv2.putText(image, str(round(right_angle[0], 2)),
                    tuple(np.multiply(right_angle[1], [640, 480]).astype(int)),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3, cv2.LINE_AA
                    )

        #Curl Logic
        if TypeOfExercise.set_counter <= sets:
            if TypeOfExercise.rep_counter < reps:
                if left_angle[0] > 160 and right_angle[0] > 160:
                    TypeOfExercise.stage = "down"
                if left_angle[0] < 30 and right_angle[0] < 30 and TypeOfExercise.stage == "down":
                    TypeOfExercise.stage = "up"
                    TypeOfExercise.rep_counter += 1
                    threading.Thread(target=self.spell_out_rep_counter).start()
            else:
                TypeOfExercise.set_counter += 1
                TypeOfExercise.rep_counter = 0
        else:
            TypeOfExercise.stage = "Completed"

        return [TypeOfExercise.set_counter, TypeOfExercise.rep_counter, TypeOfExercise.stage]

    def plank(self, image, sets, reps):
        # Calculate angle
        elbow_angle = self.left_elbow_angle()
        shoulder_angle = self.left_shoulder_angle()
        hip_angle = self.left_hip_angle()

        #Visualize angle
        cv2.putText(image, str(round(elbow_angle[0], 2)),
                    tuple(np.multiply(elbow_angle[1], [640, 480]).astype(int)),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3, cv2.LINE_AA
                    )

        cv2.putText(image, str(round(shoulder_angle[0], 2)),
                    tuple(np.multiply(shoulder_angle[1], [640, 480]).astype(int)),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3, cv2.LINE_AA
                    )

        cv2.putText(image, str(round(hip_angle[0], 2)),
                    tuple(np.multiply(hip_angle[1], [640, 480]).astype(int)),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3, cv2.LINE_AA
                    )

        # plank counter logic
        if TypeOfExercise.set_counter <= sets:
            if TypeOfExercise.rep_counter < reps:
                if elbow_angle[0] > 75 and shoulder_angle[0] > 75 and hip_angle[0] > 160:
                    TypeOfExercise.stage = "started"
                    TypeOfExercise.threshold += 1
                    if TypeOfExercise.threshold > 35 and TypeOfExercise.stage == "started":
                        TypeOfExercise.threshold = 0
                        TypeOfExercise.rep_counter += 1
                        threading.Thread(target=self.spell_out_rep_counter).start()
                else:
                    TypeOfExercise.stage = "stopped"

            else:
                TypeOfExercise.set_counter += 1
                TypeOfExercise.rep_counter = 0
        else:
            TypeOfExercise.stage = "Completed"

        return [TypeOfExercise.set_counter, TypeOfExercise.rep_counter, TypeOfExercise.stage]

    def jacks(self,image, sets, reps):
        # Calculate angle
        left_shoulder_angle = self.left_shoulder_angle()
        right_shoulder_angle = self.right_shoulder_angle()
        left_hip_angle = self.left_hip_angle()
        right_hip_angle = self.right_hip_angle()

        #VIsualize angle
        cv2.putText(image, str(round(right_shoulder_angle[0], 2)),
                    tuple(np.multiply(right_shoulder_angle[1], [640, 480]).astype(int)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2, cv2.LINE_AA
                    )

        cv2.putText(image, str(round(left_shoulder_angle[0], 2)),
                    tuple(np.multiply(left_shoulder_angle[1], [640, 480]).astype(int)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2, cv2.LINE_AA
                    )

        cv2.putText(image, str(round(right_hip_angle[0], 2)),
                    tuple(np.multiply(right_hip_angle[1], [640, 480]).astype(int)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2, cv2.LINE_AA
                    )

        cv2.putText(image, str(round(left_hip_angle[0], 2)),
                    tuple(np.multiply(left_hip_angle[1], [640, 480]).astype(int)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2, cv2.LINE_AA
                    )

        # Jacks counter logic
        if TypeOfExercise.set_counter <= sets:
            if TypeOfExercise.rep_counter < reps:
                if left_shoulder_angle[0] < 30 and right_shoulder_angle[0] < 30 and \
                        left_hip_angle[0] > 170 and right_hip_angle[0] > 170:
                    TypeOfExercise.stage = "down"
                if left_shoulder_angle[0] > 160 and right_shoulder_angle[0] > 160 and \
                        left_hip_angle[0] < 170 and right_hip_angle[0] < 170 and TypeOfExercise.stage == "down":
                    TypeOfExercise.stage = "up"
                    TypeOfExercise.rep_counter += 1
                    threading.Thread(target=self.spell_out_rep_counter).start()
            else:
                TypeOfExercise.set_counter += 1
                TypeOfExercise.rep_counter = 0
        else:
            TypeOfExercise.stage = "Completed"

        return [TypeOfExercise.set_counter, TypeOfExercise.rep_counter, TypeOfExercise.stage]

    def spell_out_rep_counter(self):
        # Use pyttsx3 to spell out the text
        try:
            engine = pyttsx3.init()
            engine.say(str(TypeOfExercise.rep_counter))
            engine.runAndWait()
        except:
            pass


    def calculate_exercise(self, image, exercise_type, sets,reps):
        #Check the exercise type and redirects to the particular method
        if exercise_type == "pushups":
            return self.push_up(image,sets,reps)
        elif exercise_type == "pullups":
            return self.pull_up(sets, reps)
        elif exercise_type == "squat":
            return self.squat(image,sets,reps)
        elif exercise_type == "biceps":
            return self.biceps(image,sets,reps)
        elif exercise_type == "plank":
            return self.plank(image,sets,reps)
        elif exercise_type == "jacks":
            return self.jacks(image,sets,reps)

