from tkinter import*
from PIL import Image,ImageTk

from record import CCTV  # Imports the CCTV class from record.py

window=Tk()
window.title("OMEGA CCTV CAMERA By Robert Osei Bonsu")
window.iconphoto(False, PhotoImage(file='mn.png'))
window.geometry('1080x600')

mainFrame = Frame(window,bd=2)

label_title = Label(mainFrame,text="Omega CCTV By Robert",font=('Arial',40,'bold'))
label_title.grid(pady=(10,10),column=1)

icon_1=Image.open("logo.jpg")
icon_1=icon_1.resize((80,80), Image.LANCZOS)
icon_1=ImageTk.PhotoImage(icon_1)
label_icon_1=Label(mainFrame,image=icon_1)
label_icon_1.grid(row=0,pady=(5,10),column=0)

icon_cam=Image.open("cam1.png")
icon_cam=icon_cam.resize((190,190), Image.LANCZOS)
icon_cam=ImageTk.PhotoImage(icon_cam)
label_icon_cam=Label(mainFrame,image=icon_cam)
label_icon_cam.grid(row=1,pady=(5,10),column=1)

btn_icon=Image.open("record.png")
btn_icon=btn_icon.resize((50,50), Image.LANCZOS)
btn_icon=ImageTk.PhotoImage(btn_icon)

video_source_entry = Entry(mainFrame)  # Create a text input field for the video source
video_source_entry.insert(0, "Enter video source, 0 for webcam")  # Add default text
video_source_entry.grid(row=2, pady=(20,10), column=1)

def start_recording():
    video_source = video_source_entry.get()  # Get the video source from the text input field
    if not video_source:
        print("Please enter a valid video source")
        return
    try:
        if video_source.isdigit():
            video_source = int(video_source)
        record = CCTV(video_source)  # Create an instance of the CCTV class
        record.start()  # Start the CCTV feed when the button is clicked
    except ValueError as e:
        print(f"Error: {e}. Unable to open video source.")
        
btn=Button(mainFrame,text="VideoRecord",font=('Arial',25,'bold'),height=90,width=270,fg='blue',image=btn_icon,compound='left', command=start_recording)
btn.grid(row=3,pady=(20,10),column=1)

ebtn_icon=Image.open("exit.png")
ebtn_icon=ebtn_icon.resize((50,50), Image.LANCZOS)
ebtn_icon=ImageTk.PhotoImage(ebtn_icon)

ebtn=Button(mainFrame,text="Exit",font=('Arial',25,'bold'),height=90,width=270,fg='blue',image=ebtn_icon,compound='left', command=window.quit)
ebtn.grid(row=4,pady=(20,10),column=1)

mainFrame.pack()

window.mainloop()