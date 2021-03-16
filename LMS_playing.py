from tkinter import *
from selenium import webdriver
from bs4 import BeautifulSoup as BS
import chromedriver_autoinstaller
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import datetime
import time
 

def btncmd():
  lms_id = id_e.get()
  lms_pw = pw_e.get()

  URL = "https://myclass.ssu.ac.kr/login.php"

  chrome_options = webdriver.ChromeOptions()
  if(c1var.get() == 1):
    chrome_options.add_argument("--mute-audio")

  path = chromedriver_autoinstaller.install(cwd=True)
  browser = webdriver.Chrome(executable_path = path, chrome_options=chrome_options)
  browser.get(URL)

  def login(lms_id, lms_pw):
    ID = lms_id
    PW = lms_pw

    IDinput = browser.find_element_by_xpath('//*[@id="input-username"]')
    PWinput = browser.find_element_by_xpath('//*[@id="input-password"]')
    loginBtn = browser.find_element_by_xpath('//*[@id="region-main"]/div/div/div/div[3]/div[1]/div[2]/form/div[2]/input')

    IDinput.send_keys(ID)
    PWinput.send_keys(PW)
    loginBtn.click()

  def get_cource_id_list():
    cource_soup = BS(browser.page_source, "html.parser")
    cources = cource_soup.find_all('a',{'class':'course_link'})

    cource_id_list = []
    for cource in cources:
      cource_id_list.append(cource['href'][-5:])

    return cource_id_list

  def isin(name, ctt_list):
    for ctt in ctt_list:
      if(ctt == name):
        return True
    
    return False

  def get_start_time():
    time.sleep(10)
    try:
      alert = browser.switch_to.alert
      start_time = alert.text[14:19]
      start_second = int(start_time[:2])*60 + int(start_time[-2:])
      alert.accept()
      return start_second
    except:
      return 0

  def write_log(content, link):
    f = open("재생 기록.txt",'at',encoding='utf8')
    now = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    data = f"{now} : {content}가 매크로에 의해 재생되었습니다.\n\t {content} 링크 : {link}\n"
    f.write(data)
    f.close()

  
  login(lms_id, lms_pw)
  cource_id_list = get_cource_id_list()

  todo_list = []

  for cource_id in cource_id_list:
    time.sleep(1)
    att_url = "http://myclass.ssu.ac.kr/report/ubcompletion/user_progress_a.php?id="
    browser.get(att_url + cource_id)
    att_soup = BS(browser.page_source, "html.parser")
    att_body = att_soup.find_all("tbody")[1]
    att_tr = att_body.find_all("tr")

    att_list = []

    for tr in att_tr: # 각 강의 출석부에서 미출석 수업 뽑아내기
      att_td = tr.find_all("td")
      if(len(att_td) == 6):
        if(att_td[4].text == 'X'):
          att_list.append(att_td[1].text.strip()) # 재생할 강의 제목 저장
      elif(len(att_td) == 4):
        if(att_td[3].text == 'X'):
          att_list.append(att_td[0].text.strip()) # 재생할 강의 제목 저장

    # print(att_list)
    time.sleep(1)
    ctt_url = 'http://myclass.ssu.ac.kr/mod/xncommons/index.php?id=' + cource_id
    browser.get(ctt_url)
    
    ctt_soup = BS(browser.page_source, "html.parser")
    ctt_body = ctt_soup.find("tbody")

    if(ctt_body):
      ctt_tr = ctt_body.find_all('tr')
      for tr in ctt_tr:
        td = tr.find_all('td')
        if(len(td) > 2):
          if(isin(td[1].text.strip(), att_list)):
            todo_list.append(td[1].find('a')['href'][-6:])

  for video_id in todo_list:
    video_url_format = "http://myclass.ssu.ac.kr/mod/xncommons/viewer.php?id="
    video_url = video_url_format  + video_id
    browser.execute_script(f"window.open('{video_url}');")
    video_tab = browser.window_handles[-1]
    browser.switch_to.window(video_tab)
    playtime = 0
    accept_time = browser.find_element_by_xpath("//*[@id='vod_header']/h1/span").text
    video_name = browser.find_element_by_xpath('//*[@id="vod_header"]/h1').text
    try:
      iframe1 = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'iframe')))
      browser.switch_to.frame(iframe1)
      iframe2 = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'iframe')))
      browser.switch_to.frame(iframe2)
      playbtn = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="front-screen"]/div/div[2]/div[1]/div')))
      playbtn.click()
      start_time = get_start_time()
      
      if(len(accept_time) == 8):
        playtime = int(accept_time[:2])*60*60 + int(accept_time[3:5])*60 + int(accept_time[-2:])
        video_name = video_name[:-9]
      elif(len(accept_time) == 5):
        playtime = int(accept_time[:2])*60 + int(accept_time[-2:])
        video_name = video_name[:-6]

      delay = playtime - start_time
      time.sleep(delay+20)

      browser.switch_to.window(video_tab)
      browser.close()
      write_log(video_name, video_url)
      browser.switch_to.window(browser.window_handles[0])
    except:
      num_tap = len(browser.window_handles)

      if(num_tap > 1):
        for i in reversed(range(num_tap)):
          browser.switch_to.window(browser.window_handles[i])
          if(video_url_format in browser.current_url):
            browser.close()
           

  browser.quit()


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