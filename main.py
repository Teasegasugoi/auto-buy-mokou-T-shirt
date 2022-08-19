import chromedriver_binary # nopa
from selenium import webdriver

# x. Chrome の起動オプションを設定する
options = webdriver.ChromeOptions()
options.add_argument('--headless')

# x. ブラウザの新規ウィンドウを開く
print('connecting to remote browser...')
driver = webdriver.Chrome(options=options)

# 1. Qiita にアクセスする
driver.get('https://qiita.com')
print(driver.current_url)

# x. ブラウザを終了する
driver.quit()