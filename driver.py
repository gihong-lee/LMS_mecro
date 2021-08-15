import time
import socket
import datetime
from tkinter import *
from bs4 import BeautifulSoup
import http.client as httplib
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.command import Command
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller

class driver:
	def __init__(self):
		path = chromedriver_autoinstaller.install(cwd=True)
		self.driver = webdriver.Chrome(executable_path = path)
		self.todo_list = []

	def is_running(self) -> bool:
		try:
			self.driver.execute(Command.STATUS)
			return True
		except:
			return False

	def isin(self, name, ctt_list):
		for ctt in ctt_list:
			if(ctt == name):
				return True

	def get_start_time(self) -> int:
		time.sleep(10)
		try:
			alert = self.driver.switch_to.alert
			start_time = alert.text[14:19]
			start_second = int(start_time[:2])*60 + int(start_time[-2:])
			alert.accept()
			return start_second, start_time
		except:
			return 0

	def write_log(self, content, link):
		f = open("재생 기록.txt",'at',encoding='utf8')
		now = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
		data = f"{now} : {content}가 매크로에 의해 재생되었습니다.\n\t {content} 링크 : {link}\n"
		f.write(data)
		f.close()

	def login(self, m_id, m_pw):
		login_url = "https://smartid.ssu.ac.kr/Symtra_sso/smln.asp?apiReturnUrl=https://myclass.ssu.ac.kr/sso/login.php"

		self.driver.get(login_url)

		id_elem = self.driver.find_element_by_id("userid")
		pw_elem = self.driver.find_element_by_id("pwd")

		id_elem.send_keys(m_id)
		pw_elem.send_keys(m_pw)

		self.driver.find_element_by_class_name('btn_login').click()
		time.sleep(2)

	def t_get_cource_id(self) -> list:
		self.driver.get("http://myclass.ssu.ac.kr/local/ubion/user/?year=2021&semester=10")
		cource_soup = BeautifulSoup(self.driver.page_source, "html.parser")
		cource_list = cource_soup.find_all('a',{'class':'coursefullname'})

		cources = []
		for cource in cource_list:
			cources.append(cource['href'][-5:])

		print(cources)
		return cources

	# def t_get_cource_id(self) -> list:
	# 	self.driver.get("http://myclass.ssu.ac.kr/local/ubion/user/?year=2021&semester=10")
	# 	time.sleep(1)

	# 	cources = []
	# 	crt_url = ""

	# 	for i in range(9): # 범위 설정
	# 		self.driver.find_elements_by_css_selector('.coursefullname')[i].click()
	# 		time.sleep(1)
	# 		crt_url = self.driver.current_url
	# 		cources.append(crt_url[-5:])
	# 		self.driver.back()
	# 	return cources

	def get_none_atd(self, cources):		
		for cource_id in cources:
			self.jud_atd(cource_id)
			self.get_video_id(cource_id)

	def jud_atd(self, cource_id: str) -> list:
		att_list = []
		
		att_url = "http://myclass.ssu.ac.kr/report/ubcompletion/user_progress_a.php?id="
		self.driver.get(att_url + cource_id)
		att_soup = BeautifulSoup(self.driver.page_source, "html.parser")
		att_body = att_soup.find_all("tbody")[1]
		att_tr = att_body.find_all("tr")

		for tr in att_tr:
			att_td = tr.find_all("td")
			if(len(att_td) == 6):
				if(att_td[4].text == 'X'):
					att_list.append(att_td[1].text.strip())
			elif(len(att_td) == 4):
				if(att_td[3].text == 'X'):
					att_list.append(att_td[0].text.strip())
		return att_list

	def get_video_id(self, cource_id:str, att_list:list):
		ctt_url = 'http://myclass.ssu.ac.kr/mod/xncommons/index.php?id=' + cource_id
		self.driver.get(ctt_url)

		ctt_soup = BeautifulSoup(self.driver.page_source, "html.parser")
		ctt_body = ctt_soup.find("tbody")

		if(ctt_body):
			ctt_tr = ctt_body.find_all('tr')
			for tr in ctt_tr:
				td = tr.find_all('td')
				if(len(td) > 2):
					if(self.isin(td[1].text.strip(), att_list)):
						self.todo_list.append(td[1].find('a')['href'][-6:])

	def play_video(self):
		for id in self.todo_list:
			self.open_tap_for_video(id)
			self.play_for_time()
		self.driver.quit()

	def open_tap_for_video(self, video_id: str): # 분할
		video_url_format = "http://myclass.ssu.ac.kr/mod/xncommons/viewer.php?id="
		video_url = video_url_format  + video_id
		self.driver.execute_script(f"window.open('{video_url}');")
		video_tab = self.driver.window_handles[-1]
		self.driver.switch_to.window(video_tab)

		return video_tab, video_url, video_url_format

	def get_time(self, video_name):
		playtime = 0
		accept_time = self.driver.find_element_by_xpath("//*[@id='vod_header']/h1/span").text
		video_name = self.driver.find_element_by_xpath('//*[@id="vod_header"]/h1').text
		if(len(accept_time) == 8):
			playtime = int(accept_time[:2])*60*60 + int(accept_time[3:5])*60 + int(accept_time[-2:])
			video_name = video_name[:-9]
		elif(len(accept_time) == 5):
			playtime = int(accept_time[:2])*60 + int(accept_time[-2:])
			video_name = video_name[:-6]
		return video_name, playtime

	def press_play_btn(self):
		iframe1 = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'iframe')))
		self.driver.switch_to.frame(iframe1)
		iframe2 = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'iframe')))
		self.driver.switch_to.frame(iframe2)
		playbtn = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="front-screen"]/div/div[2]/div[1]/div')))
		playbtn.click()
		start_time = self.get_start_time()
		return start_time

	def play_for_time(self, video_url, video_tab, playtime, video_name, start_time, video_url_format):
		try:
			self.get_time()
			self.press_play_btn()
			delay = playtime - start_time
			time.sleep(delay+20)
			self.driver.switch_to.window(video_tab)
			self.driver.close()
			self.write_log(video_name, video_url)
			self.driver.switch_to.window(self.driver.window_handles[0])
		except:
			num_tap = len(self.driver.window_handles)
			if(num_tap > 1):
				for i in reversed(range(num_tap)):
					self.driver.switch_to.window(self.driver.window_handles[i])
					if(video_url_format in self.driver.current_url):
						self.driver.close()

	def	quit(self):
		self.driver.quit()


if __name__ =="__main__":
	driver = driver()
	driver.login('20170619', 'lsh2055855!')
	driver.t_get_cource_id()
	driver.get_none_atd()
	driver.play_video()

	driver.quit()
