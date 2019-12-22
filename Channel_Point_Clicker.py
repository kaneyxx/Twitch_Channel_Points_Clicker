from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
import msvcrt

def getpass(prompt='Twitch password: '):
    count = 0
    chars = []
    for x in prompt:
        msvcrt.putch(bytes(x, 'utf8'))
    while True:
        new_char = msvcrt.getch()
        if new_char in b'\r\n':
            break
        elif new_char == b'\0x3':  # ctrl + c
            raise KeyboardInterrupt
        elif new_char == b'\b':
            if chars and count >= 0:
                count -= 1
                chars = chars[:-1]
                msvcrt.putch(b'\b')
                msvcrt.putch(b'\x20')  # space
                msvcrt.putch(b'\b')
        else:
            if count < 0:
                count = 0
            count += 1
            chars.append(new_char.decode('utf8'))
            msvcrt.putch(b'*')
    return ''.join(chars)

channel_name = input("Enter channel name: ")
user_name = input("Twitch account: ")
user_pwd = getpass()

browser = webdriver.Chrome()
browser.get("https://twitch.tv/" + channel_name)
WebDriverWait(browser, 10).until(lambda browser: browser.find_element_by_xpath("//div[3]/div/div/div/button/div/div")).click()
WebDriverWait(browser, 10).until(lambda browser: browser.find_element_by_xpath("//div[2]/input")).send_keys(user_name)
WebDriverWait(browser, 10).until(lambda browser: browser.find_element_by_xpath("//div[2]/div/input")).send_keys(user_pwd)
browser.find_element_by_xpath("//form/div/div[3]/button").click()

while True:
    try:
        WebDriverWait(browser, 9999).until(lambda browser: browser.find_element_by_css_selector(".claimable-bonus__icon path")).click()
        time.sleep(1)
    except:
        continue

browser.close()