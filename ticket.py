from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
import json
import sys

from lib import setupDriver, setupMode, access, stopUntilLoading, stopUntilSpinnerLoading
from loginModule import loginSection
from notification import notifySystem
import sectionTicket

loginCompleted = False
waitingCompleted = False
isAllCompleted = False

mode = setupMode()
driver = setupDriver()
while not isAllCompleted:
  try:
    ### ログインセクション ###

    if(not loginCompleted):
      loginCompleted = loginSection(driver)

    if(mode == 'step'):
      onEndLoginSection = input('LoginSection completed. Are you ready to start next step?: (y or n)')
      if (onEndLoginSection != 'y'):
        break

    while(True):

      #### 待機セクション ####
      if(not waitingCompleted):
        waitingCompleted = sectionTicket.waitingSection(driver)

      #### 購入セクション ####
      isAllCompleted = sectionTicket.reservationSection(driver)
      onEndReservationSection = input('onEndReservationSection completed. Do you want to retry from wating section?: (y or n)')
      if (onEndReservationSection == 'y'):
        waitingCompleted = False
        isAllCompleted = False
        continue
      else:
        break
  except:
    print('Error retrying...')
    time.sleep(5)

time.sleep(1000)