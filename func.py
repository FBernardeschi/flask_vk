from vk_api import VkApi
import time
import random
import requests

proxy = {
    'https': 'https://178.66.182.76:3128',
    'https': 'https//195.211.219.147:5555',
    'http': 'http//194.67.91.153:80',
    'https': 'https//77.236.238.33:1256',
    'https': 'https//5.16.1.17:8080',
    'https': 'https//77.236.238.33:1256'
}

USER_AGENT = 'Mozilla/5.0 (iPad; CPU OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12F69 Safari/600.1.4'

city_id = {1: 'Москва', 2: 'Санкт-Петербург', 10: 'Волгоград', 49: 'Екатеринбург', 37: 'Владивосток'}

def change_info(lst, first_name=None, last_name=None,
                city=None, countre=None, relation=None,
                sex=None, status=None):
    log = []
    session = requests.Session()
    session.headers.update({'User-agent': USER_AGENT})
    # print(session.get('https://ipinfo.io/json', proxies=proxy).text)
    for account in lst:
        print(account)
        login, password = account.split(':')
        print(login, password)
        try:
            vk_session = VkApi(login, password)
            print(vk_session.auth(reauth=True), "авторизация")
            time.sleep(1.5)
            random_city = random.choice(list(city_id))
            response = vk_session.method('account.saveProfileInfo', {'first_name': first_name, 'last_name': last_name,
                                                                     'city_id': random_city, 'country_id': 0,
                                                                     'status': status})
            print(response['name_request']['lang'])
            if response['name_request']['lang']:
                log.append(f'{login} - {response["name_request"]["lang"]}')
            else:
                log.append({"vk_account": {'login': login, 'name': first_name, 'last_name': last_name, 'city': city_id[random_city]}})
        except:
            log.append(f'{login} - Неверный пароль или непредвиденная ошибка авторизации')
    return log
