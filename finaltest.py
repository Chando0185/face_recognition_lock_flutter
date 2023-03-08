import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mess
import tkinter.simpledialog as tsd
import cv2,os
import csv
from datetime import date
import numpy as np
from PIL import Image
import pandas as pd
import datetime
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

from controller import doorAutomate, ledControll,handSantizer
from win32com.client import Dispatch
import cv2
import numpy as np
import cv2
import pyrebase

firebaseConfig = {
  "apiKey": "AIzaSyBPAV-vUnJ6i6KWDAr3jeL1CHE3UU9hErE",
  "databaseURL": "https://facerecognitionapps-default-rtdb.firebaseio.com/",
  "authDomain" : "facerecognitionapps.firebaseapp.com",
  "projectId": "facerecognitionapps",
  "storageBucket": "facerecognitionapps.appspot.com",
  "messagingSenderId": "275907536240",
  "appId": "1:275907536240:web:391c700ed9a5f02c919bb5",
  "measurementId": "G-48Z528Q2CS"
}



import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("myservice.json")
firebase_admin.initialize_app(cred)

db1=firestore.client()



firebase= pyrebase.initialize_app(firebaseConfig)

db=firebase.database()

storage = firebase.storage()

auth=firebase.auth()

email="facerecognition502@gmail.com"
password="face123456"

user = auth.sign_in_with_email_and_password(email,password)

cam = cv2.VideoCapture(0)


from datetime import datetime

def speak(str1):
    speak=Dispatch(("SAPI.SpVoice"))
    speak.Speak(str1)




def faceBox(faceNet,frame):
    frameHeight=frame.shape[0]
    frameWidth=frame.shape[1]
    blob=cv2.dnn.blobFromImage(frame, 1.0, (300,300), [104,117,123], swapRB=False)
    faceNet.setInput(blob)
    detection=faceNet.forward()
    bboxs=[]
    for i in range(detection.shape[2]):
        confidence=detection[0,0,i,2]
        if confidence>0.7:
            x1=int(detection[0,0,i,3]*frameWidth)
            y1=int(detection[0,0,i,4]*frameHeight)
            x2=int(detection[0,0,i,5]*frameWidth)
            y2=int(detection[0,0,i,6]*frameHeight)
            bboxs.append([x1,y1,x2,y2])
    return frame, bboxs


faceProto = "opencv_face_detector.pbtxt"
faceModel = "opencv_face_detector_uint8.pb"

genderProto = "gender_deploy.prototxt"
genderModel = "gender_net.caffemodel"



faceNet=cv2.dnn.readNet(faceModel, faceProto)

genderNet=cv2.dnn.readNet(genderModel,genderProto)

MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
genderList = ['Male', 'Female']

global key
global date1
key = ''

ts = time.time()
date1 = datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
day,month,year=date1.split("-")



def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)


def tick():
    time_string = time.strftime('%H:%M:%S')
    clock.config(text=time_string)
    clock.after(200,tick)




def check_haarcascadefile():
    exists = os.path.isfile("haarcascade_frontalface_default.xml")
    if exists:
        pass
    else:
        mess._show(title='Some file missing', message='Please Check Your Folder')
        window.destroy()

###################################################################################

def clear():
    txt.delete(0, 'end')
    res = "1)Take Images  >>>  2)Save Profile"
    message1.configure(text=res)


def clear2():
    txt2.delete(0, 'end')
    res = "1)Take Images  >>>  2)Save Profile"
    message1.configure(text=res)


def TakeImages():
    check_haarcascadefile()
    columns = ['SERIAL NO.', '', 'ID', '', 'NAME']
    assure_path_exists("StudentDetails/")
    assure_path_exists("TrainingImage/")
    serial = 0
    exists = os.path.isfile("StudentDetails\StudentDetails.csv")
    if exists:
        with open("StudentDetails\StudentDetails.csv", 'r') as csvFile1:
            reader1 = csv.reader(csvFile1)
            for l in reader1:
                serial = serial + 1
        serial = (serial // 2)
        csvFile1.close()
    else:
        with open("StudentDetails\StudentDetails.csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(columns)
            serial = 1
        csvFile1.close()
    Id = (txt.get())
    name = (txt2.get())
    if ((name.isalpha()) or (' ' in name)):
        cam = cv2.VideoCapture(0)
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(harcascadePath)
        sampleNum = 0
        while (True):
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            cv2.rectangle(img, (0,100), (640, 0), (255,0,0), -2)
            cv2.putText(img, "Please Wait", (20,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255,255,255), 2, cv2.LINE_AA)
            cv2.putText(img, "When taking images, you can move your face", (20,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255,255,255), 2, cv2.LINE_AA)
            cv2.putText(img, "to ensure that the data is accurate.", (20,70), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255,255,255), 2, cv2.LINE_AA)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 1)

                sampleNum = sampleNum + 1
       
                cv2.imwrite("TrainingImage\ " + name + "." + str(serial) + "." + Id + '.' + str(sampleNum) + ".jpg",
                            gray[y:y + h, x:x + w])
          
                cv2.imshow('Taking Images', img)
     
            if cv2.waitKey(1) == ord('q'):
                break
            elif sampleNum > 400:
                break
        cam.release()
        cv2.destroyAllWindows()
        res = "Images Taken for ID : " + Id
        row = [serial, '', Id, '', name]
        with open('StudentDetails\StudentDetails.csv', 'a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
        message1.configure(text=res)
    else:
        if (name.isalpha() == False):
            res = "Enter Correct name"
            message.configure(text=res)


def TrainImages():
    check_haarcascadefile()
    assure_path_exists("TrainingImageLabel/")
    recognizer = cv2.face_LBPHFaceRecognizer.create()
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(harcascadePath)
    faces, ID = getImagesAndLabels("TrainingImage/")
    try:
        recognizer.train(faces, np.array(ID))
    except:
        mess._show(title='No Registrations', message='Please Register someone first!!!')
        return
    recognizer.save("TrainingImageLabel\Trainner.yml")
    res = "Profile Saved Successfully"
    message1.configure(text=res)


def getImagesAndLabels(path):

    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]

    faces = []

    Ids = []

    for imagePath in imagePaths:

        pilImage = Image.open(imagePath).convert('L')

        imageNp = np.array(pilImage)

        ID = int(os.path.split(imagePath)[-1].split(".")[1])
    
        faces.append(imageNp)
        Ids.append(ID)
    return faces, Ids


def TrackImages():
    check_haarcascadefile()
    assure_path_exists("Attendance/")
    assure_path_exists("StudentDetails/")
    for k in tv.get_children():
        tv.delete(k)
    msg = ''
    i = 0
    j = 0
    recognizer = cv2.face.LBPHFaceRecognizer_create()  
    exists3 = os.path.isfile("TrainingImageLabel\Trainner.yml")
    if exists3:
        recognizer.read("TrainingImageLabel\Trainner.yml")
    else:
        mess._show(title='Data Missing', message='Please click on Save Profile to reset data!!')
        return
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath)

    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names = ['Id', '', 'Name', '', 'Date', '', 'Time', '', 'Gender']
    exists1 = os.path.isfile("StudentDetails\StudentDetails.csv")
    if exists1:
        df = pd.read_csv("StudentDetails\StudentDetails.csv")
    else:
        mess._show(title='Details Missing', message='Students details are missing, please check!')
        cam.release()
        cv2.destroyAllWindows()
        window.destroy()
    while True:
        ret, im = cam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)
        now = datetime.now()

        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        cv2.rectangle(im, (0,0), (640, 40), (255,0,0), -2)
        cv2.putText(im, "Time : {} ".format(dt_string), (20,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255,255,255), 2, cv2.LINE_AA)
        cv2.rectangle(im, (0,40), (640, 80), (255,0,0), -2)
        cv2.putText(im, "Please Look At The Camera Don't Move", (20,60), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255,255,255), 2, cv2.LINE_AA)
        cv2.rectangle(im, (0, 80),(200, 140), (255,0,0),-2)
        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (225, 0, 0), 2)
            serial, conf = recognizer.predict(gray[y:y + h, x:x + w])
            if (conf < 50):
                ts = time.time()
                date = datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                timeStamp = datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                aa = df.loc[df['SERIAL NO.'] == serial]['NAME'].values
                ID = df.loc[df['SERIAL NO.'] == serial]['ID'].values
                ID = str(ID)
                ID = ID[1:-1]
                bb = str(aa)
                bb = bb[2:-2]
                global attendance
                
                padding=20
                frame,bboxs=faceBox(faceNet,im)
                for bbox in bboxs:
                # face=frame[bbox[1]:bbox[3], bbox[0]:bbox[2]]
                    face = im[max(0,bbox[1]-padding):min(bbox[3]+padding,im.shape[0]-1),max(0,bbox[0]-padding):min(bbox[2]+padding, im.shape[1]-1)]
                    blob=cv2.dnn.blobFromImage(face, 1.0, (227,227), MODEL_MEAN_VALUES, swapRB=False)
                    genderNet.setInput(blob)
                    genderPred=genderNet.forward()
                    gender=genderList[genderPred[0].argmax()]
                attendance = [str(ID), '', bb, '', str(date), '', str(timeStamp), '',str(gender)]
                cv2.rectangle(im,(x,y),(x+w,y+h),(0,255,0),2)
                cv2.rectangle(im, (x,y-40),(x+w, y), (0,255,0),-2)
                cv2.putText(im, str(bb.upper()),(x,y-10), font, 1, (255,255,255), 2, cv2.LINE_AA)
                cv2.putText(im, "Name: {}".format(bb),(20,100), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,50,255), 2, cv2.LINE_AA)
                cv2.putText(im, "Gender: {}".format(gender),(20,130), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,50,255), 2, cv2.LINE_AA)

            else:
                Id = 'Unknown'
                bb = str(Id)
                padding=20
                
                attendance = ["UNKNOWN", '', "UNKNOWN", '', "UNKNOWN", '', "UNKNOWN", '',"UNKNOWN"]
                frame,bboxs=faceBox(faceNet,im)
                for bbox in bboxs:
                    face = im[max(0,bbox[1]-padding):min(bbox[3]+padding,im.shape[0]-1),max(0,bbox[0]-padding):min(bbox[2]+padding, im.shape[1]-1)]
                    blob=cv2.dnn.blobFromImage(face, 1.0, (227,227), MODEL_MEAN_VALUES, swapRB=False)
                    genderNet.setInput(blob)
                    genderPred=genderNet.forward()
                    gender=genderList[genderPred[0].argmax()]
                cv2.rectangle(im,(x,y),(x+w,y+h),(50,50,255),2)
                cv2.rectangle(im, (x,y-40),(x+w, y), (50,50,255),-2)
                cv2.putText(im, str(bb),(x,y-10), font, 1, (255,255,255), 2, cv2.LINE_AA)
            if bb!='Unknown' and cv2.waitKey(1)==ord('o'):

                time.sleep(5)
                doorAutomate(0)
                ledControll(0)
                time.sleep(5)
                doorAutomate(1)
                ledControll(1)  
                speak("Attendence Taken")
                ts = time.time()
                date = datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                exists = os.path.isfile("Attendance\Attendance_" + date + ".csv")
                if exists:
                    with open("Attendance\Attendance_" + date + ".csv", 'a+') as csvFile1:
                        writer = csv.writer(csvFile1)
                        writer.writerow(attendance)
                    csvFile1.close()
                else:
                    with open("Attendance\Attendance_" + date + ".csv", 'a+') as csvFile1:
                        writer = csv.writer(csvFile1)
                        writer.writerow(col_names)
                        writer.writerow(attendance)
                    csvFile1.close()
                with open("Attendance\Attendance_" + date + ".csv", 'r') as csvFile1:
                    reader1 = csv.reader(csvFile1)
                    for lines in reader1:
                        i = i + 1
                        if (i > 1):
                            if (i % 2 != 0):
                                iidd = str(lines[0]) + '   '
                                tv.insert('', 0, text=iidd, values=(str(lines[2]), str(lines[4]), str(lines[6]), str(lines[8])))
                csvFile1.close()
                current_time = now.strftime("%H:%M:%S")
                db1.collection('attendence_data').add({'name': bb,'time': current_time, 'date': date1, 'showSearch': [date1]})
        cv2.imshow('Taking Attendance', im) 
        if cv2.waitKey(1)== ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()


   



print("Attendance\Attendance_" + date1 + ".csv")

mont={'01':'January',
      '02':'February',
      '03':'March',
      '04':'April',
      '05':'May',
      '06':'June',
      '07':'July',
      '08':'August',
      '09':'September',
      '10':'October',
      '11':'November',
      '12':'December'
      }

def send_mail():
    email_user = ''
    email_password = ''
    email_send = ''

    subject = 'subject'

    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = email_send
    msg['Subject'] = subject

    body = 'Hi there, sending this email from Python! Attendence For Face Recognition System'
    msg.attach(MIMEText(body,'plain'))

    filename="Attendance\Attendance_" + date + ".csv"
    attachment  =open(filename,'rb')

    part = MIMEBase('application','octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition',"attachment; filename= "+filename)

    msg.attach(part)
    text = msg.as_string()
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login(email_user,email_password)
    print("Email Send")
    server.sendmail(email_user,email_send,text)
    server.quit()



window = tk.Tk()
window.geometry("1280x720")
window.resizable(True,False)
window.title("Attendance System")
window.configure(background='#262523')

frame1 = tk.Frame(window, bg="#FF5733")
frame1.place(relx=0.11, rely=0.17, relwidth=0.39, relheight=0.80)

frame2 = tk.Frame(window, bg="#FF5733")
frame2.place(relx=0.51, rely=0.17, relwidth=0.38, relheight=0.80)

message3 = tk.Label(window, text="Face Recognition Based Student Attendance System" ,fg="white",bg="#262523" ,width=55 ,height=1,font=('times', 29, ' bold '))
message3.place(x=10, y=10)

frame3 = tk.Frame(window, bg="#FF5733")
frame3.place(relx=0.52, rely=0.09, relwidth=0.09, relheight=0.07)

frame4 = tk.Frame(window, bg="#FF5733")
frame4.place(relx=0.36, rely=0.09, relwidth=0.16, relheight=0.07)

datef = tk.Label(frame4, text = day+"-"+mont[month]+"-"+year+"  |  ", fg="orange",bg="#262523" ,width=55 ,height=1,font=('times', 22, ' bold '))
datef.pack(fill='both',expand=1)

clock = tk.Label(frame3,fg="orange",bg="#262523" ,width=55 ,height=1,font=('times', 22, ' bold '))
clock.pack(fill='both',expand=1)
tick()

head2 = tk.Label(frame2, text="                       For New Registrations                       ", fg="black",bg="#3ece48" ,font=('times', 17, ' bold ') )
head2.grid(row=0,column=0)

head1 = tk.Label(frame1, text="                       For Already Registered                       ", fg="black",bg="#3ece48" ,font=('times', 17, ' bold ') )
head1.place(x=0,y=0)

lbl = tk.Label(frame2, text="Enter ID",width=20  ,height=1  ,fg="black"  ,bg="#FF5733" ,font=('times', 17, ' bold ') )
lbl.place(x=80, y=55)

txt = tk.Entry(frame2,width=32 ,fg="black",font=('times', 15, ' bold '))
txt.place(x=30, y=88)

lbl2 = tk.Label(frame2, text="Enter Name",width=20  ,fg="black"  ,bg="#FF5733" ,font=('times', 17, ' bold '))
lbl2.place(x=80, y=140)

txt2 = tk.Entry(frame2,width=32 ,fg="black",font=('times', 15, ' bold ')  )
txt2.place(x=30, y=173)

message1 = tk.Label(frame2, text="1)Take Images  >>>  2)Save Profile" ,bg="#FF5733" ,fg="black"  ,width=39 ,height=1, activebackground = "yellow" ,font=('times', 15, ' bold '))
message1.place(x=7, y=230)

message = tk.Label(frame2, text="" ,bg="#FF5733" ,fg="black"  ,width=39,height=1, activebackground = "yellow" ,font=('times', 16, ' bold '))
message.place(x=7, y=450)

lbl3 = tk.Label(frame1, text="Attendance",width=20  ,fg="black"  ,bg="#FF5733"  ,height=1 ,font=('times', 17, ' bold '))
lbl3.place(x=100, y=115)

res=0
exists = os.path.isfile("StudentDetails\StudentDetails.csv")
if exists:
    with open("StudentDetails\StudentDetails.csv", 'r') as csvFile1:
        reader1 = csv.reader(csvFile1)
        for l in reader1:
            res = res + 1
    res = (res // 2) - 1
    csvFile1.close()
else:
    res = 0
message.configure(text='Total Registrations till now  : '+str(res))



menubar = tk.Menu(window,relief='ridge')
filemenu = tk.Menu(menubar,tearoff=0)

filemenu.add_command(label='Exit',command = window.destroy)
menubar.add_cascade(label='Help',font=('times', 29, ' bold '),menu=filemenu)



tv= ttk.Treeview(frame1,height =13,columns = ('name','date','time','gender'))
tv.column('#0',width=82)
tv.column('name',width=90)
tv.column('date',width=90)
tv.column('time',width=90)
tv.column('gender',width=90)
tv.grid(row=2,column=0,padx=(0,0),pady=(150,0),columnspan=4)
tv.heading('#0',text ='ID')
tv.heading('name',text ='NAME')
tv.heading('date',text ='DATE')
tv.heading('time',text ='TIME')
tv.heading('gender',text ='GENDER')


scroll=ttk.Scrollbar(frame1,orient='vertical',command=tv.yview)
scroll.grid(row=2,column=4,padx=(0,100),pady=(150,0),sticky='ns')
tv.configure(yscrollcommand=scroll.set)



clearButton = tk.Button(frame2, text="Clear", command=clear  ,fg="black"  ,bg="#ea2a2a"  ,width=11 ,activebackground = "white" ,font=('times', 11, ' bold '))
clearButton.place(x=335, y=86)
clearButton2 = tk.Button(frame2, text="Clear", command=clear2  ,fg="black"  ,bg="#ea2a2a"  ,width=11 , activebackground = "white" ,font=('times', 11, ' bold '))
clearButton2.place(x=335, y=172)    
takeImg = tk.Button(frame2, text="Take Images", command=TakeImages  ,fg="white"  ,bg="blue"  ,width=34  ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))
takeImg.place(x=30, y=300)
trainImg = tk.Button(frame2, text="Save Profile", command=TrainImages ,fg="white"  ,bg="blue"  ,width=34  ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))
trainImg.place(x=30, y=380)
trackImg = tk.Button(frame1, text="Take Attendance", command=TrackImages  ,fg="black"  ,bg="yellow"  ,width=35  ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))
trackImg.place(x=30,y=50)

quitWindow = tk.Button(frame1, text="Send Mail", command=send_mail  ,fg="black"  ,bg="red"  ,width=35 ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))
quitWindow.place(x=30, y=450)

quitWindow = tk.Button(frame1, text="Quit", command=window.destroy  ,fg="black"  ,bg="red"  ,width=35 ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))
quitWindow.place(x=30, y=500)

window.configure(menu=menubar)
window.mainloop()

