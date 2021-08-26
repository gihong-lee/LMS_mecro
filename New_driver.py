import time
import datetime
from bs4 import BeautifulSoup as BS
from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Driver:
	def __init__(self, options:dict, todo_list:list = []):
		self.todo_list = todo_list
		self.is_running = True

		path = chromedriver_autoinstaller.install(cwd=True)
		chrome_options = webdriver.ChromeOptions()
		chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

		if options["is_mute"]:
			chrome_options.add_argument("--mute-audio")

		self.driver = webdriver.Chrome(executable_path = path, chrome_options=chrome_options)

	def revive_driver(self):
		path = chromedriver_autoinstaller.install(cwd=True)
		self.driver = webdriver.Chrome(executable_path = path)

	def write_log(self, content, link):
		f = open("재생 기록.txt",'at',encoding='utf8')
		now = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
		data = f"{now} : {content}가 매크로에 의해 재생되었습니다.\n\t {content} 링크 : {link}\n"
		f.write(data)
		f.close()

	# def accept_alert(self):
	# 	try:
	# 		WebDriverWait(self.driver, 10).until(EC.alert_is_present())
	# 		alert = self.driver.switch_to.alert
	# 		alert.accept()
	# 	except:
	# 		return 

	def login(self, id : str, pw : str):
		try:
			login_url = "https://smartid.ssu.ac.kr/Symtra_sso/smln.asp?apiReturnUrl=https%3A%2F%2Fclass.ssu.ac.kr%2Fxn-sso%2Fgw-cb.php"

			self.driver.get(login_url)

			IDinput = self.driver.find_element_by_xpath('//*[@id="userid"]')
			PWinput = self.driver.find_element_by_xpath('//*[@id="pwd"]')

			IDinput.send_keys(id)
			PWinput.send_keys(pw)
			self.driver.execute_script("LoginInfoSend('LoginInfo')")
		except:
			print("login 실패")
			self.is_running = False
			self.driver.quit()

	def get_cource_wrap(self) -> list:
		self.driver.get("https://class.ssu.ac.kr/mypage")

		cource_iframe = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'iframe')))
		self.driver.switch_to.frame(cource_iframe)

		self.sleep(0.5)
		cource_soup = BS(self.driver.page_source, "html.parser")
		cource_wraps = cource_soup.find_all('div', {'class':'xn-course-container'})
		
		return cource_wraps

	def get_cource_id(self) -> list:
		cource_wraps = self.get_cource_wrap()
		cource_id_list = []

		for cource_wrap in cource_wraps:
			cource_link = cource_wrap.find('a',{'class':'xnch-link'})
			cource_id_list.append(cource_link['href'].rsplit('/', maxsplit = 1)[-1])

		return cource_id_list

	# def get_none_atd(self, cources):
	# 	try:
	# 		for cource_id in cources:
	# 			atd_list = self.get_undone_video_names(cource_id)
	# 			self.get_video_id(cource_id, atd_list)
	# 			self.sleep(0.5)
	# 	except:
	# 		self.is_running = False

	def get_week_num(self) ->int:
		now_week = datetime.datetime.now().isocalendar()[1]
		st_week = datetime.date(2021,9,1).isocalendar()[1]

		return now_week - st_week + 1 

	def cheak_week(self, atd_td) -> bool:
		this_week = self.get_week_num()
		week = int (atd_td[0].find("span",{"class":"section-title-wrap"}).find_all("span")[-1].text[:-2])

		if week == this_week:
			return True
		else:
			return False

	def get_undone_video_names(self, cource_id: str) -> list:
		atd_list = []
		
		atd_url = f"https://canvas.ssu.ac.kr/courses/{cource_id}/external_tools/6"
		self.driver.get(atd_url)

		atd_iframe = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="tool_content"]')))
		self.driver.switch_to.frame(atd_iframe)
		WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="xn-learn-status"]/div/div/div[2]/table/tbody')))

		atd_soup = BS(self.driver.page_source, "html.parser")
		atd_body = atd_soup.find("tbody",{'class':'xnlsmpb-table'})
		
		is_on = False

		if atd_body:
			atd_tr = atd_body.find_all("tr")
	
			for tr in atd_tr:
				atd_td = tr.find_all("td")

				if (len(atd_td) == 7):
					is_on = self.cheak_week(atd_td)
				
				if is_on:
					if (len(atd_td) == 7):
						if(atd_td[3].text == "동영상" and atd_td[5].text != 'O'):
							atd_list.append(atd_td[2].text.strip())
					elif(len(atd_td) == 5):
						if(atd_td[1].text == "동영상" and atd_td[3].text != 'O'):
							atd_list.append(atd_td[0].text.strip())

		return atd_list

	# def get_video_id(self, cource_id:str, undone_video_names:list):
	# 	if undone_video_names:
	# 		videos_url = 'http://myclass.ssu.ac.kr/mod/xncommons/index.php?id=' + cource_id
	# 		self.driver.get(videos_url)

	# 		videos_soup = BS(self.driver.page_source, "html.parser")
	# 		videos_body = videos_soup.find("tbody")

	# 		if(videos_body):
	# 			videos_tr = videos_body.find_all('tr')

	# 			for tr in videos_tr:
	# 				td = tr.find_all('td')

	# 				if(len(td) > 2):
	# 					word = td[1].text.strip()
						
	# 					if word in undone_video_names:
	# 						self.todo_list.append(td[1].find('a')['href'][-6:])

	# def pp(self, percent:int):
	# 	video_list = self.todo_list.copy()

	# 	for video_id in video_list:
	# 		try:
	# 			self.play_video(video_id, percent)
	# 			if self.is_running:
	# 				self.todo_list.remove(video_id)
	# 				print(video_id,"삭제됨")	
	# 		except:
	# 			# 에러 로그 작성
	# 			print("오류")
	# 			video_tab = self.driver.window_handles[-1]
	# 			self.driver.switch_to.window(video_tab)

	# 			self.driver.close()
	# 			self.accept_alert()
	# 			continue

	# 	self.is_running = False
	# 	self.driver.quit()
		
	# def get_start_time(self) -> int:
	# 	try:
	# 		WebDriverWait(self.driver, 10).until(EC.alert_is_present())
	# 		alert = self.driver.switch_to.alert

	# 		start_time = alert.text[14:19]
	# 		start_second = int(start_time[:2])*60 + int(start_time[-2:])
	# 		alert.accept()

	# 		return start_second
	# 	except:
	# 		return 0

	# def play_video(self ,v_id: str, percent:int):
	# 	self.is_running = True

	# 	video_base_url = "http://myclass.ssu.ac.kr/mod/xncommons/viewer.php?id="
	# 	self.driver.execute_script(f"window.open('{video_base_url + v_id}');")
	# 	video_tab = self.driver.window_handles[-1]
	# 	self.driver.switch_to.window(video_tab)
	
	# 	self.enter_to_frame()
	# 	self.press_playbtn()
		
	# 	video_info = self.get_video_info()
	# 	playtime = self.get_playtime(video_info["playtime"], percent)

	# 	self.sleep(playtime)
	# 	self.close_video_tab(video_tab)
		

	# def get_playtime(self,playtime: int ,percent:int) -> int:
	# 	start_time = self.get_start_time()
	# 	sleep_time = int(playtime * (percent /90)  - float(start_time))
	# 	print(sleep_time)
	# 	return sleep_time

	# def press_playbtn(self):
	# 	playbtn = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="front-screen"]/div/div[2]/div[1]/div')))
	# 	playbtn.click()
	# 	self.driver.switch_to.default_content()
  
	# def close_video_tab(self, video_tab):
	# 	self.driver.switch_to.window(video_tab)
	# 	self.driver.close()
	# 	self.driver.switch_to.window(self.driver.window_handles[0])

	# def enter_to_frame(self):
	# 	iframe1 = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'iframe')))
	# 	self.driver.switch_to.frame(iframe1)

	# 	iframe2 = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'iframe')))
	# 	self.driver.switch_to.frame(iframe2)

	def sleep(self, second:float):
		currtime = 0

		while currtime <= second:
			if self.is_driver_alive():
				time.sleep(0.5)
				currtime += 0.5
			else:
				print("비정상적 종료")
				self.is_running = False
				return 
  
	def is_driver_alive(self):
		try:
			self.driver.current_url	
			# or driver.title
			return True
		except:
			return False

	# def get_video_info(self) -> dict:
	# 	video_info  = {}
	# 	accept_time = self.driver.find_element_by_xpath("//*[@id='vod_header']/h1/span").text
	# 	# video_name = self.driver.find_element_by_xpath('//*[@id="vod_header"]/h1').text
		
	# 	# * (percentage / 90)
	# 	if(len(accept_time) == 8):
	# 		video_info["playtime"] = (int(accept_time[:2])*60*60 + int(accept_time[3:5])*60 + int(accept_time[-2:]))
	# 		# video_info["video_name"] = video_name[:-9]
	# 	elif(len(accept_time) == 5):
	# 		video_info["playtime"] = (int(accept_time[:2])*60 + int(accept_time[-2:]))
	# 		# video_info["video_name"] = video_name[:-6]
    
	# 	print(video_info)
	# 	return video_info
	
	def	quit(self):
		self.driver.quit()


if __name__ =="__main__":
	options = {"is_mute": False}
	driver = Driver(options)
	driver.login('20170617', 'jmir4mlife!')
	cources = driver.get_cource_id()
	driver.get_undone_video_names(cources[1])
	# driver.get_none_atd(cources)
	# driver.pp(95)