import cv2
facedetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
id1=input("Enter your id: ")
video = cv2.VideoCapture(0)
count=0;
while True:
	check , frame = video.read()
	gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
	faces = facedetect.detectMultiScale(gray,1.3,5)
	for x,y,h,w in faces:
		count=count+1
		cv2.imwrite("dataSet/User."+str(id1)+"."+str(count)+".jpg",gray[y:y+h,x:x+h])
		cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,255),3)
   
	cv2.imshow("Faces",frame)
	cv2.waitKey(1)
	if count>500:
		break
	

video.release()
cv2.destroyAllWindows()
print("Collecting Sample complete..................")






