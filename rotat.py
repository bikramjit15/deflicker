import cv2
import numpy as np
import imutils

class ExtractImageWidget:
    def __init__(self, im2):
        self.original_image = im2
        height, width, channels = self.original_image.shape
        #print(height, width)
        # Resize image, remove if you want raw image size
        self.original_image = cv2.resize(self.original_image, (int(width/2), int(height/2)))
        height, width, channels = self.original_image.shape
        #print(height, width)
        self.clone = self.original_image.copy()

        cv2.namedWindow('image')
        cv2.setMouseCallback('image', self.extract_coordinates)

        # Bounding box reference points and boolean if we are extracting coordinates
        self.image_coordinates = []
        self.angle = 0
        self.extract = False
        self.selected_ROI = False

    def extract_coordinates(self, event, x, y, flags, parameters):
        # Record starting (x,y) coordinates on left mouse button click
        if event == cv2.EVENT_LBUTTONDOWN:
            self.image_coordinates = [(x,y)]
            self.extract = True

        # Record ending (x,y) coordintes on left mouse bottom release
        elif event == cv2.EVENT_LBUTTONUP:
            self.image_coordinates.append((x,y))
            self.extract = False

            self.selected_ROI = True
            self.crop_ROI()

            # Draw rectangle around ROI
            cv2.rectangle(self.clone, self.image_coordinates[0], self.image_coordinates[1], (0,255,0), 2)
            cv2.imshow("image", self.clone) 

        # Clear drawing boxes on right mouse button click and reset angle
        elif event == cv2.EVENT_RBUTTONDOWN:
            self.clone = self.original_image.copy()
            self.angle = 0
            self.selected_ROI = False
            cv2.destroyWindow(cropped_image)
            
    def show_image(self):
        h, w, channels = self.clone.shape
        max = int(h/45)
        for i in range(1,max):
                self.clone = cv2.line(self.clone, (0,int(i*h/max)), (w,int(i*h/max)), (0,255,0), (1))
                self.clone = cv2.line(self.clone, (int(i*w/max),0), (int(i*w/max),h), (255,0,0), (1))
        
        
        
        font=cv2.FONT_ITALIC
        self.clone =cv2.putText(self.clone,"Use keys r and e to rotate; left click + drag to crop", (200,50), font, 1, (0,0,255), 1, cv2.LINE_AA)
        self.clone =cv2.putText(self.clone,"press s to preview; c to complete; right click to reset", (200,150), font, 1, (0,0,255), 1, cv2.LINE_AA)
        return self.clone

    def rotate_image(self, angle):
        # Grab the dimensions of the image and then determine the center
     
        self.clone = imutils.rotate(self.original_image, angle=angle)
        self.selected_ROI = False

    def crop_ROI(self):
        if self.selected_ROI:
            self.cropped_image = self.clone.copy()

            x1 = self.image_coordinates[0][0]
            y1 = self.image_coordinates[0][1]
            x2 = self.image_coordinates[1][0]
            y2 = self.image_coordinates[1][1]
            #print(y1,y2,x1,x2)
           # self.clone.line(im2, (0,int(h/2)), (w,int(h/2)), (0,0,0), (5))
            self.cropped_image = self.cropped_image[y1:y2, x1:x2]
            #return(y1,y2,x1,x2)
            #print('Cropped image: {} {}'.format((self.image_coordinates[0]), self.image_coordinates[1]))
        else:
            print('Select ROI to crop before cropping')

    def show_cropped_ROI(self):
        if self.selected_ROI:
            cv2.imshow('cropped_image', self.cropped_image)
        else:
            print('Select ROI to crop before cropping')
        
        
        
        

def ro(im2):
    h, w, channels = im2.shape
    #font=cv2.FONT_ITALIC
    #im2 =cv2.putText(im2,"Use keys r and e to rotate; left click + drag to crop", (500,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
   # im2 =cv2.putText(im2,"s to preview; c to complete; right click to reset", (500,150), font, 2, (0,0,255), 3, cv2.LINE_AA)
   # im2 =cv2.putText(im2,"s to preview; c to complete", (1500,400), font, 2, (0,255,0), 3, cv2.LINE_AA)
   # im2 =cv2.putText(im2,"right click to reset", (1500,500), font, 2, (0,255,0), 3, cv2.LINE_AA)
    rangle = 0
    #im2 = cv2.imread('plane.Bmp')
    extract_image_widget = ExtractImageWidget(im2)
    while True:
        cv2.imshow('image', extract_image_widget.show_image())
        key = cv2.waitKey(1)

        # Rotate clockwise 1 degrees
        if key == ord('r'):
            rangle+=0.5
            extract_image_widget.rotate_image(rangle)
        # Rotate counter clockwise 1 degrees
        if key == ord('e'):
            rangle+=-0.5
            extract_image_widget.rotate_image(rangle)
     
            
        # Close program with keyboard 'q'
        if key == ord('q'):
            cv2.destroyAllWindows()
            exit(1)
        
        if key == ord('s'):
            #cv2.destroyAllWindows()
            extract_image_widget.show_cropped_ROI()
            
        # Crop image
        if key == ord('c'):
            #extract_image_widget.show_cropped_ROI()
            x1 = 2*extract_image_widget.image_coordinates[0][0]
            y1 = 2*extract_image_widget.image_coordinates[0][1]
            x2 = 2*extract_image_widget.image_coordinates[1][0]
            y2 = 2*extract_image_widget.image_coordinates[1][1]
            
            cv2.destroyAllWindows()
            return(y1,y2,x1,x2,rangle)
            #print('Angle of rotation:',rangle)
            #rangle=0