import tkinter as tk
from PIL import ImageTk, Image

'''
window = tk.Tk()

canvas = tk.Canvas(window, width=1200,height=699,bd=0, highlightthickness=0)
imgpath = 'graph.jpg'
img = Image.open(imgpath)
photo = ImageTk.PhotoImage(img)
 
canvas.create_image(500, 500, image=photo)
canvas.pack()
entry=tk.Entry(window,insertbackground='blue', highlightthickness =2)
entry.pack()
 
canvas.create_window(30, 20, width=100, height=20, window=entry)
 
window.mainloop()
'''
'''
root = tk.Tk()
imgpath = 'graph.jpg'
img = Image.open(imgpath)
photo = ImageTk.PhotoImage(img)
theLabel = tk.Label(root, justify=tk.LEFT, image=photo, compound = tk.CENTER)
#label = tk.Label(theLabel, text = "123")

#label.pack()
theLabel.pack()

 

tk.mainloop()
 '''
root = tk.Tk()
root.title("Title")
root.geometry("600x600")
root.configure(background="white")
root.wm_attributes('-transparentcolor','black')
imgpath = 'graph.jpg'
img = Image.open(imgpath)
background_image = ImageTk.PhotoImage(img)

background = tk.Label(root, image=background_image, bd=0)
label1 = tk.Label(root,text = "13")
label2 = tk.Label(root,text = "13")
label3 = tk.Label(root,text = "13")
label4 = tk.Label(root,text = "13")
#label5 = tk.Label(root,text = "13")
label1.pack()
label2.pack()
label3.pack()
label4.pack()
#abel5.pack()
background.pack(pady = 10)

root.mainloop()