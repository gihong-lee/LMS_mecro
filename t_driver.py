import datetime
import time
from bs4 import BeautifulSoup as BS
from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class driver:
#   def_생성자(id, pw, video_id_list ) :
# 		m_id = id, m_pw = pw, 스캠_url
  def __init__(self, v_list : list):
    path = chromedriver_autoinstaller.install(cwd=True)
    self.driver = webdriver.Chrome(executable_path = path)
    self.v_list = v_list

    URL = "https://smartid.ssu.ac.kr/Symtra_sso/smln.asp?apiReturnUrl=https://myclass.ssu.ac.kr/sso/login.php"
    self.driver.get(URL)

# 	def_로그인(self,) :
# 		아이디 창 객체 저장
# 		비번 창 객체 저장
# 		로그인 버튼 객체 저장
#  //
# 		아이디창에 m_id 넣기
# 		비번창에 m_pw 넣기
# 		로그인버튼 누르기  -> 오류뜸 고쳐야함
  def login(self, id : str, pw : str): 
    IDinput = self.driver.find_element_by_xpath('//*[@id="userid"]')
    PWinput = self.driver.find_element_by_xpath('//*[@id="pwd"]')

    IDinput.send_keys(id)
    PWinput.send_keys(pw)
    self.driver.execute_script("LoginInfoSend('LoginInfo')")


# 	def_할일 체크:
# 		if ( video 리스트 객체 ) {
#        동영상 재생
#      } else {
# 		    출석부 읽기
#      }
  def check_todo(self):
    if not(self.v_list):
      self.get_atd_list()

    self.pp()
    


# def_출석부 읽기:
# cource_id_list = 강의 ID 추출()
# //
# 		each cource_id in cource_id_list  {
# 		  	출석부 url + cource_id 접근
#         미출석 video 추출()
#         video_id 추출()
# 			}
  def get_atd_list(self):
    cource_id_list = self.get_cource_id()

    for cource_id in cource_id_list:
      undone_video_names = self.get_undone_video_names(cource_id)
      self.get_video_id(cource_id, undone_video_names)


# 	def_강의 ID 추출:
# soup = smart_camp의 첫 페이지의 html

# links = find all of ( class == cource_link ) in soup 

# each link in links {
# 	list <= 5 character in link 
# }
  def get_cource_id(self) -> list:
    self.driver.get("http://myclass.ssu.ac.kr/")
    cource_soup = BS(self.driver.page_source, "html.parser")
    cources = cource_soup.find_all('a',{'class':'course_link'})

    cource_id_list = []
    for cource in cources:
      cource_id_list.append(cource['href'][-5:])

    return cource_id_list


# def_주차 알아내기 : 
# 	return  ( week of present ) - ( week of 2021.09.01 )
  def get_week_num(self) -> int:
    y = datetime.datetime(2021,9,1)
    x = datetime.datetime.now()

    return int(x.strftime("%U")) - int(y.strftime("%U"))


# def_ video_id 추출 : 
# 		week_num = 주차알아내기()
# 		soup = 출석부의 html
# 		attendance_list = find all of ( tagname = “tr” ) in ( tagname = “tbody” )
# //
# 		each attendance in attendance_list {
# 		       if ( week of attendance == week_num & 미출석video 판단(attendance) ) {
# 				video_id_list <= video_id in attendance 
# 		       }

  def get_undone_video_names(self, cource_id: str) -> list:
    atd_base_url = "http://myclass.ssu.ac.kr/report/ubcompletion/user_progress_a.php?id="
    atd_url = atd_base_url + cource_id
    # week_num = self.get_week_num()
    atd_list = []

    self.sleep(0.5)
    self.driver.get(atd_url)

    atd_soup = BS(self.driver.page_source, "html.parser")
    atd_body = atd_soup.find_all("tbody")

    if len(atd_body) > 1:
      atd_tr = atd_body.find_all("tr")

      for tr in atd_tr: # 각 강의 출석부에서 미출석 수업 뽑아내기
        atd_td = tr.find_all("td")
        
        if(len(atd_td) == 6):
          if(atd_td[4].text != 'O'):
            atd_list.append(atd_td[1].text.strip()) # 재생할 강의 제목 저장
        elif(len(atd_td) == 4):
          if(atd_td[3].text != 'O'):
            atd_list.append(atd_td[0].text.strip()) # 재생할 강의 제목 저장

      return atd_list
    else:
      return


  def get_video_id(self, cource_id: str, undone_video_names: list):
    if undone_video_names:
      videos_base_url = "http://myclass.ssu.ac.kr/mod/xncommons/index.php?id="
      videos_url = videos_base_url + cource_id

      self.driver.get(videos_url)
      videos_soup = BS(self.driver.page_source, "html.parser")
      videos_body = videos_soup.find("tbody")

      if(videos_body):
        videos_tr = videos_body.find_all('tr')

        for tr in videos_tr:
          td = tr.find_all('td')

          if(len(td) > 2):
            word = td[1].text.strip()

            if word in undone_video_names:
              self.v_list.append(td[1].find('a')['href'][-6:])

# def_동영상재생 :
# 	구현방법 논의 할 것
# 현재 : 수강시간 계산후 그 만큼 sleep
# 방안1 : 현재 동영상 재생시간을 받아 계산시간 보다 크면 success
  def pp(self):
    self.sleep(0.5)

    video_base_url = "http://myclass.ssu.ac.kr/mod/xncommons/viewer.php?id="
    video_id_list = self.v_list.copy()

    for v_id in video_id_list:
      self.driver.execute_script(f"window.open('{video_base_url + v_id}');")
      video_tab = self.driver.window_handles[-1]
      self.driver.switch_to.window(video_tab)

      self.enter_to_frame()
      self.play_video()

      start_time = self.get_start_time()
      video_info = self.get_video_info()

      print(video_info, start_time)
      self.sleep(video_info["playtime"] - start_time)
      # self.sleep(10)
      self.close_video_tab(video_tab)
      self.v_list.remove(v_id)

# def_시작시간 받아오기:
# 	alert_win_obj = alert window of driver
# //
# 	if ( exit alert_win_obj ) {
# 			start_time = start time of alert_win_obj
# 		return start_time
# 	}
# 	else return 0
  def get_start_time(self):
    try:
      WebDriverWait(self.driver, 10).until(EC.alert_is_present())
      alert = self.driver.switch_to.alert
    
      start_time = alert.text[14:19]
      start_second = int(start_time[:2])*60 + int(start_time[-2:])
      alert.accept()

      return start_second
    except:
      return 0

# def_수강시간만큼 동영상 재생:
# 	동영상재생 함수에 따라 바뀜
  def play_video(self):
    playbtn = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="front-screen"]/div/div[2]/div[1]/div')))
    playbtn.click()
    self.driver.switch_to.default_content()
  
  def close_video_tab(self, video_tab):
    self.driver.switch_to.window(video_tab)
    self.driver.close()
    self.driver.switch_to.window(self.driver.window_handles[0])

  def enter_to_frame(self):
    iframe1 = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'iframe')))
    self.driver.switch_to.frame(iframe1)

    iframe2 = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'iframe')))
    self.driver.switch_to.frame(iframe2)

  def sleep(self, second:float):
    currtime = 0

    while currtime <= second:
      if self.is_driver_alive():
        time.sleep(0.5)
        currtime += 0.5
      else:
        self.driver.quit()
        print("비정상적 종료")
  
  def is_driver_alive(self):
   try:
      self.driver.current_url
      # or driver.title
      return True
   except:
      return False

  
  def get_video_info(self) -> dict:
    video_info  = {}
    accept_time = self.driver.find_element_by_xpath("//*[@id='vod_header']/h1/span").text
    # video_name = self.driver.find_element_by_xpath('//*[@id="vod_header"]/h1').text
    
    # * (percentage / 90)
    if(len(accept_time) == 8):
      video_info["playtime"] = (int(accept_time[:2])*60*60 + int(accept_time[3:5])*60 + int(accept_time[-2:]))
      # video_info["video_name"] = video_name[:-9]
    elif(len(accept_time) == 5):
      video_info["playtime"] = (int(accept_time[:2])*60 + int(accept_time[-2:]))
      # video_info["video_name"] = video_name[:-6]
    
    return video_info
     
if __name__ == "__main__":
  v = ["623694"]

  driver = driver(v)

  driver.login("20170617", "jmir4mlife@")
  driver.check_todo()