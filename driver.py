from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
# driver = webdriver.Chrome()
# driver.get("http://www.python.org")
# # assert "Python" in driver.title
# # elem = driver.find_element_by_name("q")
# # elem.clear()
# # elem.send_keys("pycon")
# # elem.send_keys(Keys.RETURN)
# # assert "No results found." not in driver.page_source
# # driver.close()

class driver:
# 	def_생성자(id, pw, video_id_list ) :
# 		m_id = id, m_pw = pw, 스캠_url
	def __init__(self):
		self.driver = webdriver.Chrome()
		

# 	def_로그인(self,) :
# 		아이디 창 객체 저장
# 		비번 창 객체 저장
# 		로그인 버튼 객체 저장

# 		아이디창에 m_id 넣기
# 		비번창에 m_pw 넣기
# 		로그인버튼 누르기  -> 오류뜸 고쳐야함
	def login(self, m_id, m_pw):
		login_url = "https://smartid.ssu.ac.kr/Symtra_sso/smln.asp?apiReturnUrl=https://myclass.ssu.ac.kr/sso/login.php"

		self.driver.get(login_url)

		id_elem = self.driver.find_element_by_id("userid")
		pw_elem = self.driver.find_element_by_id("pwd")

		id_elem.send_keys(m_id)
		pw_elem.send_keys(m_pw)

		self.driver.find_element_by_class_name('btn_login').click()


# def_출석부 읽기:
# cource_id_list = 강의 ID 추출()

# 		each cource_id in cource_id_list  {
# 			출석부 url + cource_id 접근
			
# video_id 추출()
# 			}
	def get_cource_id(self):
		self.driver.get("http://myclass.ssu.ac.kr/local/ubion/user/?year=2021&semester=10")
		time.sleep(1)

		cources = []
		crt_url = ""

		for i in range(9):
			self.driver.find_elements_by_css_selector('.coursefullname')[i].click()
			time.sleep(1)
			crt_url = self.driver.current_url
			cources.append(crt_url[-5:])
			self.driver.back()


# 	def_할일 체크:
# 		if ( video 리스트 객체 ) {
# 동영상 재생
# } else {
# 		출석부 읽기
# }
	def check_atd(self):
		pass

# 	def_강의 ID 추출:
# soup = smart_camp의 첫 페이지의 html

# links = find all of ( class == cource_link ) in soup 

# each link in links {
# 	list <= 5 character in link 
# }
	def get_video_id(self):
		pass


# def_주차 알아내기 : 
# 	return  ( week of present ) - ( week of 2021.09.01 )
	def get_week(self):
		pass

# def_ video_id 추출 : 
# 		week_num = 주차알아내기()
# 		soup = 출석부의 html
# 		attendance_list = find all of ( tagname = “tr” ) in ( tagname = “tbody” )

# 		each attendance in attendance_list {
# 		       if ( week of attendance == week_num & 미출석video 판단(attendance) ) {
# 				video_id_list <= video_id in attendance 
# 		       }
	def get_video_id(self):
		pass

# def_미출석video 판단 :  ->bool
# 	if( 출석 != ‘o’ ) return true
	def jud_atd(self):
		pass

# def_동영상재생 :
# 	구현방법 논의 할 것
# 현재 : 수강시간 계산후 그 만큼 sleep
# 방안1 : 현재 동영상 재생시간을 받아 계산시간 보다 크면 success
	def play_video(self):
		pass

# def_시작시간 받아오기:
# 	alert_win_obj = alert window of driver

# 	if ( exit alert_win_obj ) {
# 			start_time = start time of alert_win_obj
# 		return start_time
# 	}
# 	else return 0
	def prt_time(self):
		pass


# def_수강시간만큼 동영상 재생:
# 	동영상재생 함수에 따라 바뀜
	def play_for_time(self):
		pass

driver()
time.sleep(5)