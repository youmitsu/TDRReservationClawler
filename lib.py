from selenium import webdriver
import time
import os
import json
import sys

def setupMode(argNum = 2):
  args = sys.argv
  mode = args[argNum]
  if(mode == 'step'):
    mode = 'step'
  else:
    mode = 'default'
  return mode

def setupDriver():
  args = sys.argv
  profileId = args[1]
  ## WebDriver初期化
  options = webdriver.ChromeOptions()
  options.add_argument('--user-data-dir=/Users/sanhorihiroshi/own_dev/disney_crawler/Chrome/Default' + profileId)
  options.add_argument('--profile-directory=Profile ' + profileId)
  driver = webdriver.Chrome(options=options)
  return driver

def _isLoading(driver):
  print('isLoading Start')
  try:
    driver.find_element_by_css_selector('#modalDialog > .loading04')
    print('isLoading Now')
    return True
  except:
    print('is not loading')
    time.sleep(3)
    return False

def stopUntilLoading(driver):
  print('stopUntilLoading...')
  while(_isLoading(driver)):
    time.sleep(1)

def isSpinnerLoading(driver):
  print('isSpinnerLoading Start')
  try:
    targetDateIconStatusPath = '//*[@id="js-vacancyModal"]/section[2]/section/div[3]/div[2]/div[1]/div/table/tbody/tr[7]/td[7]/a/dl/dd/span/img'
    vacancy_status_element = driver.find_element_by_xpath(targetDateIconStatusPath)
    icon_image_url = vacancy_status_element.get_attribute("src")
    print('isSpinnerLoading Now')
    if ('spinner' in icon_image_url):
      return True
    else:
      return False
  except:
    print('Unexcepted Error')
    time.sleep(3)
    return False

def stopUntilSpinnerLoading(driver, loadingActionCount):
  print('stopUntilLoading...')
  while(isSpinnerLoading(driver) and loadingActionCount < 100):
    loadingActionCount = loadingActionCount + 1
    time.sleep(1)

def isLoggedIn(driver):
  try:
    signin_element = driver.find_element_by_css_selector('a[href="/fli/signin/"]')
    return True
  except:
    return False

def access_denied(driver):
  try:
    if ('Denied' in driver.find_element_by_css_selector('body > h1').text):
      print('access denied')
      return True
    return False
  except:
    return False

def is_unavailable(driver):
  try:
    if ('アクセスが集中しており' in driver.find_element_by_css_selector('p.textalign').text):
      print('network is crowded')
      return True
    return False
  except:
    return False

def access(driver, url):
  driver.get(url)
  time.sleep(3)
  if(is_unavailable(driver) or access_denied(driver)):
    print('access failure')
    raise Exception('Website is not available')
