from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
import json
import sys

from lib import setupDriver, setupMode, access, stopUntilLoading, stopUntilSpinnerLoading
from loginModule import loginSection
from notification import notifySystem, notifySlackForHotel

def waitingSection(driver):
  status = False
  while(True):
    try:
      access(driver, 'https://reserve.tokyodisneyresort.jp/hotel/list/?showWay=&roomsNum=&adultNum=2&childNum=&stayingDays=1&useDate=&cpListStr=&childAgeBedInform=&searchHotelCD=DHM&searchHotelDiv=&hotelName=&searchHotelName=&searchLayer=&searchRoomName=&hotelSearchDetail=&detailOpenFlg=0&checkPointStr=&hotelChangeFlg=false&removeSessionFlg=true&returnFlg=false&hotelShowFlg=&displayType=hotel-search&reservationStatus=1')
    except:
      time.sleep(2)
      continue
    try:
      ## //*[@id="section_ヴェネツィア・サイド スーペリアルーム"]/div/div[2]/ul/li[2]/a
      ## //*[@id="section_ポルト・パラディーゾ・サイド スーペリアルーム パーシャルビュー"]/div/div[2]/ul/li/a
      ## //*[@id="section_ポルト・パラディーゾ・サイド スーペリアルーム ピアッツァビュー"]/div/div[2]/ul/li[2]/a
      ## //*[@id="section_ポルト・パラディーゾ・サイド スーペリアルーム ピアッツァグランドビュー"]/div/div[2]/ul/li[2]/a
      driver.find_element_by_xpath('//*[@id="section_ポルト・パラディーゾ・サイド スーペリアルーム ピアッツァビュー"]/div/div[2]/ul/li[2]/a').click()
      time.sleep(1)
      driver.find_element_by_xpath('//*[@id="js-vacancyModal"]/section[1]/div/ul/li/a').click()
      time.sleep(3)
      status = True
      break
    except:
      print('Error!')
      status = False
      continue
  return status

def canReservationHotel(driver):
  VACANCY_ICON_URL = 'https://reserve.tokyodisneyresort.jp/cgp/images/jp/pc/ico/ico_state_14.png'
  targetDatePath = '//*[@id="js-vacancyModal"]/section[2]/section/div[3]/div[2]/div[1]/div/table/tbody/tr[7]/td[7]/a/dl/dd'
  targetDateImagePath = targetDatePath + '/span/img'
  ## 残りわずかの場合のチェック
  calendar_image_class = ''
  try:
    calendar_date_element = driver.find_element_by_xpath(targetDatePath)
    calendar_image_class = calendar_date_element.get_attribute('class')
    if('few' in calendar_image_class):
      return True
  except:
    print('no few item')
  ## ×か○かのチェック
  try:
    if('vMiddle' in calendar_image_class):
      vacancy_status_element = driver.find_element_by_xpath(targetDateImagePath)
      icon_image_url = vacancy_status_element.get_attribute("src")
      return icon_image_url != VACANCY_ICON_URL
    else:
      return False
  except:
    return False

def reservationSection(driver):
  status = False
  nextBtnPath = '//*[@id="js-vacancyModal"]/section[2]/section/div[3]/div[2]/div[1]/div/table/tbody/tr[1]/th[3]/ul/li/button'
  prevBtnPath = '//*[@id="js-vacancyModal"]/section[2]/section/div[3]/div[2]/div[1]/div/table/tbody/tr[1]/th[1]/ul/li/button'
  targetDatePath = '//*[@id="js-vacancyModal"]/section[2]/section/div[3]/div[2]/div[1]/div/table/tbody/tr[7]/td[7]/a'
  while(True):
    try:
      driver.find_element_by_xpath(nextBtnPath).click()
      loadingActionCount = 0
      stopUntilSpinnerLoading(driver, loadingActionCount)
      time.sleep(1)
      if(canReservationHotel(driver)):
        driver.find_element_by_xpath(targetDatePath).click()
        time.sleep(1)
        status = True
        notifySystem()
        notifySlackForHotel()
        break
      else:
        driver.find_element_by_xpath(prevBtnPath).click()
        time.sleep(1)
        continue
    except:
      break
  return status