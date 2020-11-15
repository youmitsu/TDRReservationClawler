from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
import json
import sys

from lib import setupDriver, setupMode, access, stopUntilLoading, stopUntilSpinnerLoading, access_denied, is_unavailable
from loginModule import loginSection
from notification import notifySystem, notifySlackForHotel, notifySlackForRest

from model import Restaurant

def _getTargetUrl(target):
  if(target == Restaurant.BELLAVISTA_FIRST):
    # return "https://reserve.tokyodisneyresort.jp/restaurant/search/?useDate=20201129&mealDivList=3&adultNum=2&childNum=0&childAgeInform=&restaurantType=2&nameCd=RBVL0&wheelchairCount=0&stretcherCount=0&keyword=&reservationStatus=0"
    return "https://reserve.tokyodisneyresort.jp/restaurant/search/?useDate=20201130&mealDivList=3&adultNum=2&childNum=0&childAgeInform=&restaurantType=4&nameCd=RBBY0&wheelchairCount=0&stretcherCount=0&keyword=&reservationStatus=0"
  elif(target == Restaurant.BELLAVISTA_SECOND):
    return "https://reserve.tokyodisneyresort.jp/restaurant/search/?useDate=20201129&mealDivList=3&adultNum=2&childNum=0&childAgeInform=&restaurantType=2&nameCd=RBVL1&wheelchairCount=0&stretcherCount=0&keyword=&reservationStatus=0"
  elif(target == Restaurant.MAGELLANS_DINNER):
    return "https://reserve.tokyodisneyresort.jp/restaurant/search/?useDate=20201129&mealDivList=3&adultNum=2&childNum=0&childAgeInform=&restaurantType=5&nameCd=RMGL0&wheelchairCount=0&stretcherCount=0&keyword=&reservationStatus=0"
  elif(target == Restaurant.MAGELLANS_LUNCH):
    return "https://reserve.tokyodisneyresort.jp/restaurant/search/?useDate=20201129&mealDivList=2&adultNum=2&childNum=0&childAgeInform=&restaurantType=5&nameCd=RMGL0&wheelchairCount=0&stretcherCount=0&keyword=&reservationStatus=0"
  elif(target == Restaurant.DICANALETTO):
    return "https://reserve.tokyodisneyresort.jp/restaurant/search/?useDate=20201129&mealDivList=2&adultNum=2&childNum=0&childAgeInform=&restaurantType=5&nameCd=RRDC0&wheelchairCount=0&stretcherCount=0&keyword=&reservationStatus=0"
  elif(target == Restaurant.SSCOLOMBIA):
    return "https://reserve.tokyodisneyresort.jp/restaurant/search/?useDate=20201129&mealDivList=2&adultNum=2&childNum=0&childAgeInform=&restaurantType=5&nameCd=RSSD0&wheelchairCount=0&stretcherCount=0&keyword=&reservationStatus=0"
  elif(target == Restaurant.LOOSEBELT):
    return "https://reserve.tokyodisneyresort.jp/restaurant/search/?useDate=20201129&mealDivList=2&adultNum=2&childNum=0&childAgeInform=&restaurantType=5&nameCd=RTRL1&wheelchairCount=0&stretcherCount=0&keyword=&reservationStatus=0"
  else:
    return "https://reserve.tokyodisneyresort.jp/restaurant/search/?useDate=20201118&mealDivList=2&adultNum=2&childNum=0&childAgeInform=&restaurantType=5&nameCd=RHZB1&wheelchairCount=0&stretcherCount=0&keyword=&reservationStatus=0"

def _closeDialogIfDisplayed(driver):
  try:
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="modalDialog"]/p[2]/a/img').click()
    print('dialog closed')
    return True
  except:
    return False

def _isFull(driver):
  try:
    emptyText = driver.find_element_by_css_selector('.empty > p').text
    return '空きはございません' in emptyText
  except Exception as e:
    return False

def _isPreRelease(driver):
  try:
    preReleaseText = driver.find_element_by_css_selector('.preRelease > p').text
    return 'ご予約開始となります' in preReleaseText
  except Exception as e:
    return False

def waitingSection(driver, target):
  status = False
  while(True):
    try:
      access(driver, _getTargetUrl(target))
      _closeDialogIfDisplayed(driver)
      status = True
      break
    except:
      print('Error! on waitingSection')
      status = False
      continue
  return status

def reservationSection(driver):
  searchBtnXpath = '//*[@id="content"]/div[1]/div/div/p/input'
  status = False
  while(True):
    try:
      if (not _isPreRelease(driver) and not _isFull(driver)):
        time.sleep(1)
        status = True
        notifySystem()
        notifySlackForRest()
        break
      else:
        driver.find_element_by_xpath(searchBtnXpath).click()
        stopUntilLoading(driver)
        time.sleep(1)
        if (access_denied(driver) or access_denied(driver)):
          raise Exception('Website is not available')
        continue
    except:
      status = False
      break
  return status