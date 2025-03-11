import cv2
import mediapipe as mp

cam = cv2.VideoCapture(0)
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)

while True:
    _, frame = cam.read()
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = face_mesh.process(rgb_frame)
    landmark_points = output.multi_face_landmarks
    
    # Get the current window size and resize the frame accordingly
    window_name = 'Eye Controlled Mouse'
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    window_size = cv2.getWindowImageRect(window_name)
    frame_h, frame_w, _ = frame.shape
    
    if window_size[2] != 0 and window_size[3] != 0:  # Ensure window has a valid size
        frame = cv2.resize(frame, (window_size[2], window_size[3]))

    new_frame_h, new_frame_w, _ = frame.shape
    
    if landmark_points:
        landmarks = landmark_points[0].landmark
        for idx, landmark in enumerate(landmarks):
            x = int(landmark.x * new_frame_w)
            y = int(landmark.y * new_frame_h)
            cv2.putText(frame, str(idx), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 
                        0.2, (0, 255, 0), 1, cv2.LINE_AA)
    
    cv2.imshow(window_name, frame)
    if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit
        break

cam.release()
cv2.destroyAllWindows()