from tkinter import *
from UI_cmd import *
 
root = Tk()
root.title("LMS Player")

root.geometry("320x160")
root.resizable(False, False)

id_e = Entry(root, width = 30)
pw_e = Entry(root, width = 30)
btn = Button(root, text="실행", command = btncmd)
c1var = IntVar()
c1 = Checkbutton(root, text='음소거', variable = c1var)
c1.select()

id_e.insert(0, "학번을 입력하세요")
pw_e.insert(0, "비밀번호를 입력하세요")

id_e.pack()
pw_e.pack()
c1.pack()
btn.pack()

root.mainloop()