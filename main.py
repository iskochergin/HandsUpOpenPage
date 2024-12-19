import cv2
import mediapipe as mp
import webbrowser

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()


def is_hand_up(landmarks, threshold=0.1):
    left_wrist_index = mp_pose.PoseLandmark.LEFT_WRIST.value
    right_wrist_index = mp_pose.PoseLandmark.RIGHT_WRIST.value
    left_shoulder_index = mp_pose.PoseLandmark.LEFT_SHOULDER.value
    right_shoulder_index = mp_pose.PoseLandmark.RIGHT_SHOULDER.value

    left_wrist_y = landmarks[left_wrist_index].y
    right_wrist_y = landmarks[right_wrist_index].y
    shoulder_left_y = landmarks[left_shoulder_index].y
    shoulder_right_y = landmarks[right_shoulder_index].y

    return left_wrist_y < shoulder_left_y - threshold and right_wrist_y < shoulder_right_y - threshold


cap = cv2.VideoCapture(0)

try:
    while True:
        success, frame = cap.read()
        if not success:
            continue

        frame.flags.writeable = False
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(frame)

        if results.pose_landmarks:
            landmarks = [landmark for landmark in results.pose_landmarks.landmark]
            if is_hand_up(landmarks):
                webbrowser.open_new('https://canvas.letovo.ru')
                exit(0)

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    cap.release()
