import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from dotenv import load_dotenv
import os
import signal


# 商品一覧URL(例: 'http://www.bro-bra.jp/products/list.php?category_id=xxx')
GOODS_LIST_URL = 'http://www.bro-bra.jp/products/list.php?category_id=5'

# カート画面URL
CART_URL = 'http://www.bro-bra.jp/cart/'

# 購入したい商品の情報を辞書に格納
# key: ID(string)
# value: 購入したい数(int)
WANTED_GOODS_DICT = {
    '1726': 3,
    '1725': 4,
}

# .envファイルの内容を読み込む
load_dotenv()

# Chrome の起動オプションを設定する
options = webdriver.ChromeOptions()

# 商品をカートに入れる
def add_to_cart(driver):
    for id, wanted_num in WANTED_GOODS_DICT.items():
        goods_id = 'cart' + id
        driver.find_element(By.ID, goods_id).click()
        for i in range(wanted_num - 1):
            driver.find_element(By.XPATH, "//div[@class='quantity_level']/a[1]").click()
        driver.find_element(By.XPATH, "//div[@class='btn_area']/ul/li[@class='prev']/a[1]").click()


# 個人情報入力
def input_personal_information(driver):
    # 姓
    driver.find_element(By.XPATH, "//input[@name='order_name01']").send_keys(os.environ['LAST_NAME'])
    # 名
    driver.find_element(By.XPATH, "//input[@name='order_name02']").send_keys(os.environ['FIRST_NAME'])
    # セイ
    driver.find_element(By.XPATH, "//input[@name='order_kana01']").send_keys(os.environ['LAST_NAME_KANA'])
    # メイ
    driver.find_element(By.XPATH, "//input[@name='order_kana02']").send_keys(os.environ['FIRST_NAME_KANA'])
    # 郵便番号(xxx-xxxx)
    driver.find_element(By.XPATH, "//input[@name='order_zip01']").send_keys(os.environ['POST_CODE_1'])
    driver.find_element(By.XPATH, "//input[@name='order_zip02']").send_keys(os.environ['POST_CODE_2'])
    # 都道府県
    dropdown = driver.find_element(By.XPATH, "//select[@name='order_pref']")
    select = Select(dropdown)
    select.select_by_visible_text(os.environ['PREFECTURES_KANJI'])
    # 住所：市区町村
    driver.find_element(By.XPATH, "//input[@name='order_addr01']").send_keys(os.environ['ADDRESS_1'])
    # 住所：番地、ビル名
    driver.find_element(By.XPATH, "//input[@name='order_addr02']").send_keys(os.environ['ADDRESS_2'])
    # 電話番号(xxx-xxxx-xxxx)
    driver.find_element(By.XPATH, "//input[@name='order_tel01']").send_keys(os.environ['PHONE_NUMBER_1'])
    driver.find_element(By.XPATH, "//input[@name='order_tel02']").send_keys(os.environ['PHONE_NUMBER_2'])
    driver.find_element(By.XPATH, "//input[@name='order_tel03']").send_keys(os.environ['PHONE_NUMBER_3'])
    # メールアドレス(２回入力)
    driver.find_element(By.XPATH, "//input[@name='order_email']").send_keys(os.environ['EMAIL'])
    driver.find_element(By.XPATH, "//input[@name='order_email02']").send_keys(os.environ['EMAIL'])
    # お届け先指定(チェックすると上で入力した住所を届け先に指定するはずだが、なぜか反映されないので、同じ情報をもう一度入力)
    driver.find_element(By.ID, "deliv_label").click()
    # 姓
    driver.find_element(By.XPATH, "//input[@name='shipping_name01']").send_keys(os.environ['LAST_NAME'])
    # 名
    driver.find_element(By.XPATH, "//input[@name='shipping_name02']").send_keys(os.environ['FIRST_NAME'])
    # セイ
    driver.find_element(By.XPATH, "//input[@name='shipping_kana01']").send_keys(os.environ['LAST_NAME_KANA'])
    # メイ
    driver.find_element(By.XPATH, "//input[@name='shipping_kana02']").send_keys(os.environ['FIRST_NAME_KANA'])
    # 郵便番号(xxx-xxxx)
    driver.find_element(By.XPATH, "//input[@name='shipping_zip01']").send_keys(os.environ['POST_CODE_1'])
    driver.find_element(By.XPATH, "//input[@name='shipping_zip02']").send_keys(os.environ['POST_CODE_2'])
    # 都道府県
    dropdown = driver.find_element(By.XPATH, "//select[@name='shipping_pref']")
    select = Select(dropdown)
    select.select_by_visible_text(os.environ['PREFECTURES_KANJI'])
    # 住所：市区町村
    driver.find_element(By.XPATH, "//input[@name='shipping_addr01']").send_keys(os.environ['ADDRESS_1'])
    # 住所：番地、ビル名
    driver.find_element(By.XPATH, "//input[@name='shipping_addr02']").send_keys(os.environ['ADDRESS_2'])
    # 電話番号(xxx-xxxx-xxxx)
    driver.find_element(By.XPATH, "//input[@name='shipping_tel01']").send_keys(os.environ['PHONE_NUMBER_1'])
    driver.find_element(By.XPATH, "//input[@name='shipping_tel02']").send_keys(os.environ['PHONE_NUMBER_2'])
    driver.find_element(By.XPATH, "//input[@name='shipping_tel03']").send_keys(os.environ['PHONE_NUMBER_3'])


try:
    # ブラウザの新規ウィンドウを開く
    driver = webdriver.Chrome(options=options)

    # 1. 対象サイト にアクセスする (ログインはしない)
    driver.get(GOODS_LIST_URL)

    # 2. 欲しい商品をカートに入れる
    if (len(WANTED_GOODS_DICT) < 1):
        raise Exception
    else:
        add_to_cart(driver)

    # 3.カート画面にアクセス
    driver.get(CART_URL)

    # 4. レジに進む
    driver.find_element(By.XPATH, "//input[@name='confirm']").click()

    # 5. 会員登録するかどうか画面, 今回は会員登録をせずに購入手続きへと進む
    driver.find_element(By.ID, 'buystep').click()

    # 6. お客様情報入力ページ
    input_personal_information(driver)

    # 次へボタン
    driver.find_element(By.ID, 'singular').click()


except:
    print('エラー発生')
    driver.quit()


else:
    os.kill(driver.service.process.pid,signal.SIGTERM)

