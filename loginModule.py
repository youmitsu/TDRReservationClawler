from lib import isLoggedIn, access, stopUntilLoading
import os

## ログイン処理
def loginSection(driver):
  status = False
  while(True):
    try:
      access(driver, "https://reserve.tokyodisneyresort.jp")
    except:
      continue
    while(isLoggedIn(driver)):
      try:
        access(driver, "https://reserve.tokyodisneyresort.jp/fli/signin/")
        driver.find_element_by_css_selector('#_userId').send_keys(os.environ['DISNEY_USERNAME'])
        driver.find_element_by_css_selector('#_password').send_keys(os.environ['DISNEY_PASSWORD'])
        driver.find_element_by_css_selector('form.loginform > p.btn > a').click()
        stopUntilLoading(driver)
        status = True
        break
      except:
        print('UnExpectedError in loginSection.')
        status = False
        break
    if(status):
      break
    else:
      continue
  return status