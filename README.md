# kaikeba_CV_exercise
kaikeba CV course exercise codes

week.c implements a class containing some basic operation for image.

getShape(self): return (rows , cols , channels) of an image.

changeBrightness(self , lighten , factor): lighten==1: image become brighter by factor percents.
                                           lighten==0: image become darker by factor percents.

reverseColor(self): to reverse every pixel , x = 255 - x

equalizeImg(self): to equalize every channel of an imag

rotateImg(self,rad,scale): to rotate the imag around the center with no crap.

persTrans(self,rand,pts1=None,pts2=None):rand=1:to warpPerspective randomly.
                                         rand=0:to warpPerspective using specific points
