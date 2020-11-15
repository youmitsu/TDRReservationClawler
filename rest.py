from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
import json
import sys

import sectionRest

from lib import setupDriver, setupMode, access, stopUntilLoading, stopUntilSpinnerLoading
from loginModule import loginSection
from notification import notifySystem, notifySlackForHotel
from model import Restaurant

def setupTarget():
  args = sys.argv
  targetArgs = args[2]
  print(targetArgs)
  if(targetArgs == Restaurant.BELLAVISTA_FIRST.value):
    return Restaurant.BELLAVISTA_FIRST
  elif(targetArgs == Restaurant.BELLAVISTA_SECOND.value):
    return Restaurant.BELLAVISTA_SECOND
  elif(targetArgs == Restaurant.MAGELLANS_DINNER.value):
    return Restaurant.MAGELLANS_DINNER
  elif(targetArgs == Restaurant.MAGELLANS_LUNCH.value):
    return Restaurant.MAGELLANS_LUNCH
  elif(targetArgs == Restaurant.DICANALETTO.value):
    return Restaurant.DICANALETTO
  elif(targetArgs == Restaurant.SSCOLOMBIA.value):
    return Restaurant.SSCOLOMBIA
  elif(targetArgs == Restaurant.LOOSEBELT.value):
    return Restaurant.LOOSEBELT
  else:
    return Restaurant.TEST

loginCompleted = False
waitingCompleted = False
isAllCompleted = False

driver = setupDriver()
mode = setupMode(3)
target = setupTarget()
print(mode)
print(target)

while not isAllCompleted:
  try:
    ### ログインセクション ###

    if(not loginCompleted):
      loginCompleted = loginSection(driver)

    while(True):

      #### 待機セクション ####

      if(not waitingCompleted):
        waitingCompleted = sectionRest.waitingSection(driver, target)

      if(mode == 'step'):
        onEndWaitingSection = input('onEndWaitingSection completed. Are you ready to start next step?: (y or n)')
        if (onEndWaitingSection != 'y'):
          break

      #### 購入セクション ####

      isAllCompleted = sectionRest.reservationSection(driver)
      onEndReservationSection = input('onEndReservationSection completed. Do you want to retry from wating section?: (y or n)')
      if (onEndReservationSection == 'y'):
        waitingCompleted = False
        isAllCompleted = False
        continue
      else:
        break
  except:
    print('Error retrying...')
    if(input('Do you want to retry? y or n: ') == 'n'):
      quit()
    time.sleep(5)

time.sleep(1000)