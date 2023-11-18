
def threh(video,save_video,thres1,area_threh):
 cam = cv2.VideoCapture(video)#打开一个视频
 input_fps = cam.get(cv2.CAP_PROP_FPS)
 ret_val, input_image = cam.read()
 index=[]
 images=[]
 images.append(input_image)
 video_length = int(cam.get(cv2.CAP_PROP_FRAME_COUNT))
 input_image=cv2.resize(input_image,(512,512))
 ending_frame = video_length
 fourcc = cv2.VideoWriter_fourcc(*'XVID')
 out = cv2.VideoWriter(save_video,fourcc, input_fps, (512, 512))
 gray_lwpCV = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)
 gray_lwpCV = cv2.GaussianBlur(gray_lwpCV, (21, 21), 0)
 background=gray_lwpCV

# es = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 4))

 i = 0 # default is 0
 outt=[]
 while(cam.isOpened()) and ret_val == True and i <2999:
  ## if i % 2==1:
  ret_val, input_image = cam.read()
  input_image=cv2.resize(input_image,(512,512))
  gray_lwpCV = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)
  gray_lwpCV = cv2.GaussianBlur(gray_lwpCV, (21, 21), 0)
  diff = cv2.absdiff(background, gray_lwpCV)
  outt.append(diff)
  #跟着图像变换背景
  tem_diff=diff.flatten()
  tem_ds=pd.Series(tem_diff)
  tem_per=1-len(tem_ds[tem_ds==0])/len(tem_ds)
  if (tem_per <0.2 )| (tem_per>0.75):
   background=gray_lwpCV
  else:
   diff = cv2.threshold(diff, thres1, 255, cv2.THRESH_BINARY)[1]
   ret,thresh = cv2.threshold(diff.copy(),150,255,0)
   contours, hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
  #  contours, hierarchy = cv2.findContours(diff.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
   for c in contours:
    if (cv2.contourArea(c) < area_threh) | (cv2.contourArea(c) >int(512*512*0.3) ) :  # 对于矩形区域，只显示大于给定阈值的轮廓（去除微小的变化等噪点）
     continue
    (x, y, w, h) = cv2.boundingRect(c) # 该函数计算矩形的边界框
    cv2.rectangle(input_image, (x, y), (x+w, y+h), (0, 255, 0), 2) 
    index.append(i)
  #  cv2.imshow('contours', input_image)
  #  cv2.imshow('dis', diff)
  out.write(input_image)
  images.append(input_image)
  i = i+1
 out.release()
 cam.release()
 return outt,index,images