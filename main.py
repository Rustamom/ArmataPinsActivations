try:
    import browser_cookie3
    browsercookieInstalled = True
except:
    browsercookieInstalled = False
from datetime import datetime
from lxml import html
import sys
import requests
import re
import os.path
import colorama
from colorama import Fore
colorama.init()
# Функции
def rewriteFilePins():
    f = open('pins.txt', 'w')
    for item in pins:
        f.write("%s" % item)
    f.close()
def show_exception_and_exit(exc_type, exc_value, exc_traceback):
    rewriteFilePins()
    print(Fore.RED + 'Ошибка "' + str(exc_value) + '" в строке ' + str(exc_traceback.tb_lineno))
    input("Press ENTER to exit.")
    sys.exit(-1)
def checkErrors():
    global cycle_index
    cycle_index += 1
    if len(tree.xpath('//*[@id="mr_block_pin_load"]')) > 0:
        raise Exception(Fore.RED + "Закрыт сайт или куки устарели. Обнови страницу")
    rewriteFilePins()

    messageError = tree.xpath('//*[@class="pin_error"]/span/text()')[0].encode('l1').decode()

    if 'активирован' in messageError:
        global pin
        print(str(cycle_index) + '.Этот пин-код уже активирован' + ': ' + pin)
        pins.pop(0)
        try:
            myData = pins[0].rstrip()
            pin = myData.split(':')[0]
        except:
            pin = ''
    else:
        rewriteFilePins()
        print(Fore.RED + datetime.now().strftime("%H:%M:%S ") + messageError)
sys.tracebacklimit = 0
sys.excepthook = show_exception_and_exit

cookies_dict = {}
while cookies_dict == {}:
    if browsercookieInstalled:
        browser = (input('Введите ваш браузер из списка(chrome, firefox, opera(не GX), operaGX, яндекс, edge, другой)\n')).lower()
    else:
        print('Модуль browser_cookie3 не был установлен. Доступен только ручной ввод куки')
        browser = 'другой'

    if browser == 'другой':
        cookies = input('Вставьте куки\n')
        # Установка кук
        try:
            allCookies = re.findall(r'\S+;?', cookies)
            for cook in allCookies:
                nameCookie = re.findall(r'(\S+)=', cook)[0]
                valueCookie = re.findall(r'=(\S+)', cook)[0]
                cookies_dict[nameCookie] = valueCookie
        except:
            print('Неверно вставил куки')
    elif browser == 'operagx':
        cookies_dict = browser_cookie3.opera(cookie_file=os.path.join(
                    os.getenv('APPDATA', '')) + '\\..\\Roaming\\Opera Software\\Opera GX Stable\\Cookies', key_file=os.path.join(
                    os.getenv('APPDATA', '')) + '\\..\\Roaming\\Opera Software\\Opera GX Stable\\Local State',
                                             domain_name='awru.my.games')
    elif browser == 'яндекс':
        cookies_dict = browser_cookie3.opera(cookie_file=os.path.join(
            os.getenv('APPDATA', '')) + '\\..\\Local\\Yandex\\YandexBrowser\\User Data\\Default\\Cookies', key_file=os.path.join(
            os.getenv('APPDATA', '')) + '\\..\\Local\\Yandex\\YandexBrowser\\User Data\\Local State',
                                             domain_name='awru.my.games')
    elif browser == 'opera':
        cookies_dict = browser_cookie3.opera(domain_name='awru.my.games')
    elif browser == 'chrome':
        cookies_dict = browser_cookie3.chrome(cookie_file=os.path.join(
                    os.getenv('APPDATA', '')) + '\\..\\Local\\Google\\Chrome\\User Data\\Default\\Network\\Cookies',
                                              domain_name='awru.my.games')
    elif browser == 'firefox':
        cookies_dict = browser_cookie3.firefox(domain_name='awru.my.games')
    elif browser == 'edge':
        cookies_dict = browser_cookie3.edge(domain_name='awru.my.games')
pins = []
headers1 = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ru-RU'
}

# Активация пинов
pins = open('pins.txt').readlines()

if not pins or pins[0] == '\n':
    raise Exception(Fore.RED + 'Нет пинов в файле pins.txt')

allCredits = 0
cycle_index = 0

while pins and pins[0] != '\n':
    myData = pins[0].rstrip()
    pin = myData.split(':')[0]
    countCredits = myData.split(':')[1]

    payload = {'pin': pin,
               'activate':'1'}
    r = requests.post("https://awru.my.games/dynamic/pin/?a=activate", headers=headers1, cookies=cookies_dict,
                      data=payload, allow_redirects=False)
    tree = html.fromstring(r.content)
    if len(tree.xpath('//*[@class="pin_ok"]')) == 0:
        checkErrors()
    else:
        pins.pop(0)
        allCredits = allCredits + int(countCredits)
        cycle_index += 1
        print(str(cycle_index) + '.Всего активировано золота: ' + str(allCredits))

rewriteFilePins()
print('Закончил активацию пинов')
input("Нажмите ENTER для выхода.")