import cv2
from copy import copy
#show
def showCV(image,title='show'):
    cv2.imshow(title,image)
    cv2.waitKey()
    cv2.destroyAllWindows()

def draw_circles(todraw,all_x_y_r,color,need_center=True,draw_in_copy=False):
    if draw_in_copy:    to_draw=copy(todraw)
    else:   to_draw=todraw
    for i in all_x_y_r:
        #cv2.circle(to_draw,(i[0],i[1]),i[2],color,2) # draw the outer circle
        if need_center:
            cv2.circle(to_draw,(i[0],i[1]),2,color,3) # draw the center of the circle
    return to_draw



