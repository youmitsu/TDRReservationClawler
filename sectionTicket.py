from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
import json
import sys

from lib import setupDriver, setupMode, access, stopUntilLoading, stopUntilSpinnerLoading
from loginModule import loginSection
from notification import notifySystem

def isDisplayedErrorDialog(driver):
  try:
    text = driver.find_element_by_css_selector('p.pgh-main.text-center.mt00').text
    driver.find_element_by_xpath('/html/body/div[14]/div/div/button').click()
    return text == 'エラーが発生しました'
  except:
    return False

def waitingSection(driver):
  nextMonthArrowBtnSelector = '#searchCalendar > .module-calendar > .switch-cal-wrap > .slider--cal > button.slick-next'

  status = False
  while(True):
    try:
      access(driver, 'https://reserve.tokyodisneyresort.jp/ticket/search/')
    except:
      time.sleep(2)
      status = False
      continue
    try:
      time.sleep(3)
      driver.find_element_by_css_selector(nextMonthArrowBtnSelector).click()
      status = True
      break
    except:
      status = False
      continue
  return status

def canPurchaceTicket(driver):
  try:
    cautionText = driver.find_element_by_xpath('//*[@id="searchResultList"]/ul/li[2]/div/p[3]').text
    print(cautionText)
    return cautionText != '現在、販売していません'
  except Exception as e:
    print(e)
    return True

def reservationSection(driver):
  status = False
  calendarDateBtnSelector = 'a[data-daynumbercount="60"]' #60
  calendarDummyDateBtnSelector = 'a[data-daynumbercount="53"]'
  searchEticketBtnSelector = 'button#searchEticket.button'

  while(True):
    try:
      time.sleep(1)
      driver.find_element_by_css_selector(calendarDateBtnSelector).click()
      time.sleep(2)
      driver.find_element_by_css_selector(searchEticketBtnSelector).click()
      if(isDisplayedErrorDialog(driver)):
        dialog_result = input('Would you like to retry?: (y or n)')
        if (dialog_result == 'y'):
          driver.find_element_by_css_selector(calendarDummyDateBtnSelector).click()
          time.sleep(2)
          continue
      stopUntilLoading(driver)
      time.sleep(1)
      if(canPurchaceTicket(driver)):
        driver.find_element_by_css_selector('div[data-parkticketgroupcd="053"]').click()
        stopUntilLoading(driver)
        time.sleep(1)
        driver.find_element_by_css_selector('ul.list_button > li > button[value="02"]').click()
        time.sleep(2)
        driver.find_element_by_css_selector('dl.search-adult > dd > ul > li:nth-child(3)').click()
        driver.find_element_by_css_selector('dl.search-adult > dd > ul > li:nth-child(3)').click()
        time.sleep(1)
        driver.find_element_by_css_selector('button.search-purchase-button').click()
        status = True
        notifySystem()
        break
      else:
        driver.find_element_by_css_selector(calendarDummyDateBtnSelector).click()
        time.sleep(2)
        continue
    except:
      break
  return status