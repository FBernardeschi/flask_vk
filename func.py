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

USER_AGENT = 'Mozilla/5.0 (iPad; CPU OS 9_0 like Mac OS X) AppleWebKit/601.1.40 (KHTML, like Gecko) Version/9.0 Mobile/13A304 Safari/E7FBAF'

city_id = {1: 'Москва', 2: 'Санкт-Петербург', 10: 'Волгоград', 49: 'Екатеринбург', 37: 'Владивосток'}

def change_info(lst, **par):
    log = []
    session = requests.Session()
    session.headers.update({'User-agent': USER_AGENT})
    # print(session.get('https://ipinfo.io/json', proxies=proxy).text)
    params = {i: j for i, j in par.items() if j != ''}
    print(params)
    for account in lst:
        print(account)
        login, password = account.split(':')
        print(login, password)
        try:
            vk_session = VkApi(login, password)
            print(vk_session.auth(reauth=True), "Авторизация")
            time.sleep(1.5)
            # random_city = random.choice(list(city_id))
            print('До')
            response = vk_session.method('account.saveProfileInfo', params)
            print(response)
            print('После')
            print(response.get('name_request', False) == False)
            if response.get('name_request', False) and response['name_request'].get('lang', False):
                log.append(f'{login} - {response["name_request"]["lang"]}')
            else:
                log.append({"vk_account": {'login': login}})
        except:
            log.append(f'{login} - Неверный пароль или непредвиденная ошибка авторизации')
    return log


def fun_clean_wall(account):
    session = requests.Session()
    session.headers.update({'User-agent': USER_AGENT})
    print(account)
    print(":" in account)
    if ":" in account:
        login, password = account.split(":")
        try:
            vk_session = VkApi(login, password)
            print(vk_session.auth(), "Авторизация")
            time.sleep(1.5)
            posts = vk_session.method('wall.get', {'count': 10})
            print(posts)
            if posts['count'] == 0:
                return "Стена уже очищена"
            else:
                owner_id = posts["items"][0]['owner_id']
                print(owner_id)
                while (posts['count'] != 0):
                    for i in posts['items']:
                        print(i['id'])
                        print(vk_session.method('wall.delete', {"owner_id": owner_id, 'post_id': i['id']}))
                        time.sleep(0.5)
                    posts = vk_session.method('wall.get', {'count': 30})
                return "Стена успешно очищена"
        except:
            return "Ошибка авторизации"
    else:
        return "Необходим разделитель : "