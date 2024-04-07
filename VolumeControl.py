import cv2
import time
import pyautogui
import mediapipe as mp

wCam, hCam = 700, 500
cap=cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0


mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

while True:
    ret, frame=cap.read()
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(frame, f'FPS: {int(fps)}',(40,50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)
    if not ret:
        break

    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(image_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            index_finger_y = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
            thumb_y = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y

            if index_finger_y < thumb_y:
                hand_gesture = 'pointing up'

            elif index_finger_y > thumb_y:
                hand_gesture = 'pointing down'

            else:
                hand_gesture = 'other'



            if hand_gesture == 'pointing up':
                pyautogui.press('volumeup')

            elif hand_gesture == 'pointing down':
                pyautogui.press('volumedown')

            cv2.imshow("Hand Gesture", frame)

            if cv2.waitKey(1) &0xFF == ord('q'):
                break

cap.release()
cv2.destroyAllWindows()