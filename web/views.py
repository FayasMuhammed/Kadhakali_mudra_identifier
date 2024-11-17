from django.shortcuts import render

# Create your views here.


from django.shortcuts import render
from django.http import StreamingHttpResponse, JsonResponse
from django.views import View
import cv2
import mediapipe as mp
import math
from django.views.generic import TemplateView

# MediaPipe hands model
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands()

# Function to calculate Euclidean distance
def euclidean_distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

# Global variable to control video capture
recording = False

# Home page view
class IndexView(TemplateView):
    template_name="home.html"

class VideoRecordingPageView(TemplateView):
    template_name="feed.html"

# View to start video recording
class StartRecordingView(View):
    def post(self, request):
        global recording
        recording = True
        return JsonResponse({}, status=204)

# View to stop video recording
class StopRecordingView(View):
    def post(self, request):
        global recording
        recording = False
        return JsonResponse({}, status=204)

# Video stream generator
def generate_frames():
    vid = cv2.VideoCapture(0)
    tip_lst = [4, 8, 12, 16, 20]

    while True:
        success, frame = vid.read()
        if not success or not recording:
            if not recording:
                vid.release()
                break   
            continue

        # Convert to RGB for MediaPipe processing
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(frame_rgb)
        landmark_list = []

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                landmarks = []
                for id, lm in enumerate(hand_landmarks.landmark):
                    h, w, c = frame.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    landmarks.append((cx, cy))

                if len(landmarks) == 21:
                    thumb_tip = landmarks[4]
                    index_tip = landmarks[8]
                    middle_tip = landmarks[12]
                    ring_tip = landmarks[16]
                    pinky_tip = landmarks[20]

                    distance_thumb_index = euclidean_distance(thumb_tip, index_tip)

                    if distance_thumb_index < 30:  
                        
                        middle_tip = landmarks[12]
                        ring_tip = landmarks[16]
                        pinky_tip = landmarks[20]

                        middle_knuckle = landmarks[10]
                        ring_knuckle = landmarks[14]
                        pinky_knuckle = landmarks[18]

                        if (middle_tip[1] < middle_knuckle[1] and
                            ring_tip[1] < ring_knuckle[1] and
                            pinky_tip[1] < pinky_knuckle[1] and
                            landmarks[8][1] >landmarks[10][1] and
                            landmarks[8][1]> landmarks[14][1]):
                            if landmarks[6][1]>landmarks[10][1] and middle_tip[1]<ring_tip[1]:
                                print("Mudraakhyam")
                                cv2.putText(frame,'Mudraakhyam ',(25,25),cv2.FONT_HERSHEY_COMPLEX,color=(0,255,0),thickness=2,fontScale=1)
                        elif (landmarks[20][1]< landmarks[18][1] and
                            landmarks[16][1] < landmarks[14][1] and
                            landmarks[12][1]>landmarks[10][1]
                            and landmarks[15][1]<landmarks[20][1]
                            and landmarks[4][1]<landmarks[12][1]):
                            distance_thumb_pinky=euclidean_distance(thumb_tip,pinky_tip)
                            if distance_thumb_pinky>60:
                                print('kattakam')
                                cv2.putText(frame,'kattakam ',(25,25),cv2.FONT_HERSHEY_COMPLEX,color=(0,255,0),thickness=2,fontScale=1)
                                
    
                        elif (ring_tip[1]< ring_knuckle[1] and
                            pinky_tip[1] < pinky_knuckle[1] and
                            landmarks[12][1]<landmarks[4][1] and
                            landmarks[15][1]<landmarks[20][1]): 
                            distance_thumb_pinky=euclidean_distance(thumb_tip,pinky_tip)
                            if distance_thumb_pinky>75:
                                print('hamsasyam')   
                                cv2.putText(frame,'hamsasyam ',(25,25),cv2.FONT_HERSHEY_COMPLEX,color=(0,255,0),thickness=2,fontScale=1)
                    
                        else:


                            
                            print('NOt identifie')
                            cv2.putText(frame,'NOt identifie ',(25,25),cv2.FONT_HERSHEY_COMPLEX,color=(0,0,255),thickness=2,fontScale=1)

                            
                    elif(landmarks[4][1]<landmarks[2][1] and
                        landmarks[8][1]<landmarks[6][1] and
                        landmarks[12][1]<landmarks[10][1] and
                        landmarks[16][1]>landmarks[14][1] and
                        landmarks[20][1]<landmarks[18][1] ):
                        distance_thumb_index = euclidean_distance(thumb_tip, index_tip)
                        if distance_thumb_index>170:
                            print('pathakka')
                            cv2.putText(frame,'pathakka ',(25,25),cv2.FONT_HERSHEY_COMPLEX,color=(0,255,0),thickness=2,fontScale=1)
                    elif(landmarks[4][0]<landmarks[3][0] and
                        landmarks[8][1]>landmarks[5][1] and
                        landmarks[12][1]> landmarks[9][1] and
                        landmarks[16][1]> landmarks[13][1] and
                        landmarks[20][1]> landmarks[17][1]):
                        print('mushti')
                        cv2.putText(frame,'mushti ',(25,25),cv2.FONT_HERSHEY_COMPLEX,color=(0,255,0),thickness=2,fontScale=1)
                    elif (landmarks[4][1]<= landmarks[17][1] and
                        landmarks[8][1]<=landmarks[17][1] and
                        landmarks[12][1]<= landmarks[17][1] and
                        landmarks[16][1]<= landmarks[17][1] and
                        landmarks[20][1]< landmarks[17][1] and
                        landmarks[18][1]<landmarks[14][1] and 
                        landmarks[18][1]<landmarks[10][1] and 
                        landmarks[6][1]>landmarks[18][1]):
                        distance_thumb_index_pin=euclidean_distance(landmarks[4],landmarks[6])
                        distance_thumb_index = euclidean_distance(thumb_tip, index_tip)
                        if distance_thumb_index_pin<40 and distance_thumb_index>50:

                            print('Kartharee Mukham')
                            cv2.putText(frame,'Kartharee Mukham ',(25,25),cv2.FONT_HERSHEY_COMPLEX,color=(0,255,0),thickness=2,fontScale=1)
                    elif(landmarks[4][0]<landmarks[3][0] and
                        landmarks[8][1]>landmarks[6][1] and
                        landmarks[12][1]> landmarks[9][1] and
                        landmarks[16][1]> landmarks[14][1] and
                        landmarks[20][1]> landmarks[17][1]):
                        print('sukathundam')
                        cv2.putText(frame,'sukathundam ',(25,25),cv2.FONT_HERSHEY_COMPLEX,color=(0,255,0),thickness=2,fontScale=1)
                    elif(landmarks[4][0]<landmarks[3][0] and
                        landmarks[8][1]<landmarks[6][1] and
                        landmarks[12][1]< landmarks[10][1] and
                        landmarks[16][1]> landmarks[14][1] and
                        landmarks[20][1]> landmarks[17][1]):
                        distance_index_middel=euclidean_distance(index_tip,middle_tip)

                        if distance_index_middel<50:
                            print('Kapithakam')
                            cv2.putText(frame,'Kapithakam ',(25,25),cv2.FONT_HERSHEY_COMPLEX,color=(0,255,0),thickness=2,fontScale=1)
                        else:
                            print('sikharam')
                            cv2.putText(frame,'sikharam ',(25,25),cv2.FONT_HERSHEY_COMPLEX,color=(0,255,0),thickness=2,fontScale=1)
                    elif(landmarks[4][1]<landmarks[2][1] and
                        landmarks[8][1]<landmarks[6][1] and
                        landmarks[12][1]< landmarks[10][1] and
                        landmarks[16][1]< landmarks[14][1] and
                        landmarks[20][1]< landmarks[18][1]):
                        if  landmarks[4][0]>landmarks[3][0]:
                            if distance_thumb_index>175 :
                                print('Hamsapaksham')
                                cv2.putText(frame,'Hamsapaksham ',(25,25),cv2.FONT_HERSHEY_COMPLEX,color=(0,255,0),thickness=2,fontScale=1)
                            else:
                                distance__thumb_index_pip=euclidean_distance(thumb_tip,landmarks[5])
                                if landmarks[12][1]<landmarks[11][1]:
                                    print('thripathaka')
                                    cv2.putText(frame,'thripathaka ',(25,25),cv2.FONT_HERSHEY_COMPLEX,color=(0,255,0),thickness=2,fontScale=1)
                        else:
                                print('palavam')
                                cv2.putText(frame,'palavam ',(25,25),cv2.FONT_HERSHEY_COMPLEX,color=(0,255,0),thickness=2,fontScale=1)
            

                    elif(
                        landmarks[8][1]>landmarks[6][1] and
                        landmarks[12][1]> landmarks[10][1] and
                        landmarks[16][1]< landmarks[14][1] and
                        landmarks[20][1]< landmarks[18][1]and 
                        landmarks[6][1] <landmarks[14][1] and
                        landmarks[10][1]< landmarks[14][1]):
                        distance_thumb_middel=euclidean_distance(thumb_tip,middle_tip)
                        if distance_thumb_index<30 and distance_thumb_middel<30:
                            print('hamsaasyam')
                            cv2.putText(frame,'hamsaasyam ',(25,25),cv2.FONT_HERSHEY_COMPLEX,color=(0,255,0),thickness=4,fontScale=1)
                    elif (landmarks[4][1]>landmarks[3][1] and
                        landmarks[8][1]<landmarks[7][1] and
                        landmarks[12][1]>landmarks[9][1] and
                        landmarks[16][1]>landmarks[13][1] and
                        landmarks[20][1]> landmarks[17][1]):
                        print('ardhachandhanam')
                        cv2.putText(frame,'ardhachandhanam ',(25,25),cv2.FONT_HERSHEY_COMPLEX,color=(0,255,0),thickness=4,fontScale=1)
                    elif (landmarks[4][1]<landmarks[3][1] and
                        landmarks[8][1]>landmarks[6][1] and
                        landmarks[12][1] <landmarks[11][1] and
                        landmarks[16][1] <landmarks[15][1] and
                        landmarks[20][1] <landmarks[19][1]):
                        distance_thumb_middel = euclidean_distance(thumb_tip, middle_tip)
                        if distance_thumb_middel>110:
                            print('bramaram')
                            cv2.putText(frame,'bramaram ',(25,25),cv2.FONT_HERSHEY_COMPLEX,color=(0,255,0),thickness=2,fontScale=1)
                    elif(landmarks[4][0]<landmarks[3][0] and
                        landmarks[8][1]<landmarks[7][1] and
                        landmarks[12][1]>landmarks[9][1] and
                        landmarks[16][1]>landmarks[13][1] and
                        landmarks[20][1]>landmarks[17][1]):
                        distance_thumb_ring=euclidean_distance(thumb_tip,landmarks[14])
                        if distance_thumb_ring<50:
                            print('soochimukham')
                            cv2.putText(frame,'soochimukham ',(25,25),cv2.FONT_HERSHEY_COMPLEX,color=(0,255,0),thickness=2,fontScale=1)
                    elif(landmarks[20][1]<landmarks[19][1] and
                        landmarks[8][1]<landmarks[7][1] and
                        landmarks[10][1]>landmarks[6][1] and
                        landmarks[14][1]>landmarks[18][1] 
                        ):
                        distance_thumb=euclidean_distance(thumb_tip,index_tip)
                        distance_thumb_middel=euclidean_distance(thumb_tip,middle_tip)
                        if distance_thumb_index<130 and distance_thumb_middel<30:
                        
                            print('mrigashershanam')
                            cv2.putText(frame,'mrigashershanam ',(25,25),cv2.FONT_HERSHEY_COMPLEX,color=(0,255,0),thickness=2,fontScale=1)
                        else:
                            print('mukuram')
                            
                            cv2.putText(frame,'mukuram ',(25,25),cv2.FONT_HERSHEY_COMPLEX,color=(0,255,0),thickness=2,fontScale=1)

                    else:
                        print('NO mudra identified')
                        cv2.putText(frame,'NO mudra identified ',(25,25),cv2.FONT_HERSHEY_COMPLEX,color=(0,0,255),thickness=2,fontScale=1)

                
            

        # Encode the frame to JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    vid.release()


# View to serve the video feed
class VideoFeedView(View):
    def get(self, request):
        return StreamingHttpResponse(generate_frames(), content_type='multipart/x-mixed-replace; boundary=frame')
