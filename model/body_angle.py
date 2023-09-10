import mediapipe as mp
import numpy as np

mp_pose = mp.solutions.pose

#To calculate angle
class BodyAngle:
    def __init__(self,landmarks):
        self.landmarks = landmarks

    def left_elbow_angle(self):
        # Calculate angle of left elbow
        left_shoulder = [self.landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                         self.landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        left_elbow = [self.landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                      self.landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
        left_wrist = [self.landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                      self.landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

        left_elbow_angle = self.calculate_angle(left_shoulder, left_elbow, left_wrist)

        return [left_elbow_angle,left_elbow]

    def left_shoulder_angle(self):
        # Calculate angle of left shoulder
        left_elbow = [self.landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                      self.landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
        left_shoulder = [self.landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                         self.landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        left_hip = [self.landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                    self.landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]

        left_shoulder_angle = self.calculate_angle(left_elbow, left_shoulder, left_hip)

        return [left_shoulder_angle,left_shoulder]

    def left_hip_angle(self):
        # Calculate angle of left hip
        left_shoulder = [self.landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                         self.landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        left_hip = [self.landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                    self.landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
        left_knee = [self.landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                     self.landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]

        left_hip_angle = self.calculate_angle(left_shoulder, left_hip, left_knee)

        return [left_hip_angle,left_hip]

    def left_knee_angle(self):
        # Calculate angle of left knee
        left_hip = [self.landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                    self.landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
        left_knee = [self.landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                     self.landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
        left_ankle = [self.landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                      self.landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

        left_knee_angle = self.calculate_angle(left_hip, left_knee, left_ankle)

        return [left_knee_angle,left_knee]

    def right_elbow_angle(self):
        # Calculate angle of right elbow
        right_shoulder = [self.landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                          self.landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
        right_elbow = [self.landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                       self.landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
        right_wrist = [self.landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                       self.landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

        right_elbow_angle = self.calculate_angle(right_shoulder, right_elbow, right_wrist)

        return [right_elbow_angle,right_elbow]

    def right_shoulder_angle(self):
        # Calculate angle of right shoulder
        right_shoulder = [self.landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                          self.landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
        right_hip = [self.landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                     self.landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
        right_wrist = [self.landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                       self.landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

        right_shoulder_angle = self.calculate_angle(right_hip, right_shoulder, right_wrist)

        return [right_shoulder_angle,right_shoulder]

    def right_hip_angle(self):
        # Calculate angle of right hip
        right_shoulder = [self.landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                          self.landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
        right_hip = [self.landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                     self.landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
        right_ankle = [self.landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                       self.landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

        right_hip_angle = self.calculate_angle(right_shoulder, right_hip, right_ankle)

        return [right_hip_angle,right_hip]

    def calculate_angle(self,a ,b ,c):
        # Calculate angle method
        a = np.array(a) # First
        b = np.array(b) # Mid
        c = np.array(c) # End

        radians = np.arctan2(c[1 ] -b[1], c[0 ] -b[0]) - np.arctan2(a[1 ] -b[1], a[0 ] -b[0])
        angle = np.abs(radians *180.0 /np.pi)

        if angle >180.0:
            angle = 360 - angle

        return angle

