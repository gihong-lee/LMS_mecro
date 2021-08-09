from tkinter import *
from selenium import webdriver

class main:
  def __init__(self):
    self.set_window()
    self.set_user_info_frame()
    self.set_options_frame()

    btn = Button(self.root, text="실행", command = self.btncmd)
    btn.pack()
    
    self.root.mainloop()
  
  def set_window(self):
    self.root = Tk()
    self.root.title("LMS Player")

    self.root.geometry("320x160")
    self.root.resizable(False, False)
    
  def set_user_info_frame(self):
    user_info_frame = Frame(self.root)

    id_label = Label(user_info_frame, text = "아이디")
    pw_label = Label(user_info_frame, text = "비밀번호")

    self.id_e = Entry(user_info_frame, width = 30)
    self.pw_e = Entry(user_info_frame, width = 30)

    self.id_e.insert(0, "학번을 입력하세요")
    self.pw_e.insert(0, "비밀번호를 입력하세요")

    id_label.grid(row=0, column=0, pady=(20,5))
    pw_label.grid(row=1, column=0)
    self.id_e.grid(row=0, column=1, pady=(20,5))
    self.pw_e.grid(row=1, column=1)
    
    self.id_e.bind("<1>", self.handle_click)
    self.pw_e.bind("<1>", self.handle_click)

    user_info_frame.pack()

  def set_options_frame(self):
    options_frame = Frame(self.root)
    check_option_frame = Frame(options_frame)
    radio_option_frame = Frame(options_frame)

    self.id_save_var = BooleanVar()
    self.mute_var = BooleanVar()
    self.p_var = IntVar()

    id_save_ckbtn = Checkbutton(check_option_frame, text='아이디 저장', variable = self.id_save_var)
    mute_ckbtn = Checkbutton(check_option_frame, text='음소거', variable = self.mute_var)
    p_btn1 = Radiobutton(radio_option_frame, text='90 %', value = 90, variable = self.p_var)
    p_btn2 = Radiobutton(radio_option_frame, text='95 %', value = 95, variable = self.p_var)
    p_btn3 = Radiobutton(radio_option_frame, text='100 %', value = 100, variable = self.p_var)

    id_save_ckbtn.pack(side=LEFT)
    mute_ckbtn.pack(side=LEFT)
    p_btn1.pack(side=LEFT)
    p_btn2.pack(side=LEFT)
    p_btn3.pack(side=LEFT)

    check_option_frame.pack(side=TOP)
    radio_option_frame.pack(side=TOP)
    options_frame.pack()

  def handle_click(self, event):
    event.widget.delete(0, "end")

  def btncmd(self):
    option = {}

    option["ismute"] = self.mute_var.get()
    option["playing_percent"] = self.p_var.get()

    print(self.mute_var.get())
    print(self.p_var.get())
  


if __name__ == "__main__":
  v_id_list = []
  main()