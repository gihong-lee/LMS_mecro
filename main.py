import pickle
import os
from UI import Ui

def read_file(path: str):
  data_file = open(path,"rb")
  data = pickle.load(data_file)
  data_file.close()

  return data

def get_setting():
  setting = ''
  path = "./setting/setting"
  
  try:
    setting = read_file(path)
  except:
    setting = {"id_set": None, "is_mute_set":None, "percent_set": None}
    if not os.path.isdir("./setting"):
      os.mkdir("./setting")

  return setting

def main():
  setting = get_setting()

  ui = Ui(setting)
  ui.run()

if __name__ == "__main__":
  main()