from vk_api import VkApi
import time
import random
import requests

user_ag = [
    'Mozilla/5.0 (iPad; CPU OS 15_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/103.0.5060.63 Mobile/15E148 Safari/604.1',
    'AppleCoreMedia/1.0.0.16H62 (iPad; U; CPU OS 12_5_5 like Mac OS X; nl_nl)',
    'Mozilla/5.0 (iPad; CPU OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/103.0.5060.63 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPad; CPU OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6 Mobile/15E148 Safari/604.1'
]

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

def get_token(login, password):
    session = requests.Session()
    session.headers.update({'User-agent': USER_AGENT})
    response = requests.get(
        f'https://oauth.vk.com/token?grant_type=password&client_id=2274003&client_secret=hHbZxrka2uZ6jB1inYsH&username={login}&password={password}&v=5.131&2fa_supported=1')
    print(response.json())
    if 'error_description' in response.json():
        return False
    else:
        token = response.json()['access_token']
        vk_session = VkApi(token=token)
        return vk_session

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
            vk_session.http.headers['User-agent'] = random.choice(user_ag)

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
        login, password = account.split(':')
        try:
            vk_session = VkApi(login, password)
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
                        time.sleep(0.3)
                    posts = vk_session.method('wall.get', {'count': 30})
                return "Стена успешно очищена"
        except:
            return "Ошибка авторизации"
    else:
        return "Необходим разделитель : "

def gift_sender(accounts, id_user, id_gift, anon, message=':3'):
    lst = []
    for acc in accounts:
        print(acc)
        login, password = acc.split(':')
        session = requests.Session()
        session.headers.update({'User-agent': USER_AGENT})
        response = requests.get(f'https://oauth.vk.com/token?grant_type=password&client_id=2274003&client_secret=hHbZxrka2uZ6jB1inYsH&username={login}&password={password}&v=5.131&2fa_supported=1')
        print(response.json())
        if 'error_description' in response.json():
            lst.append(f'{login} - {response.json()["error_description"]}')
        else:
            token = response.json()['access_token']
            try:
                vk_session = VkApi(token=token)
                #vk_session.http.headers['User-agent'] = random.choice(user_ag)
                print(vk_session.auth(reauth=True), "Авторизация")
                print(id_gift, id_user)
                time.sleep(0.5)
                print(vk_session.method('gifts.send', {'user_ids': id_user, 'gift_id': id_gift,
                                                          'guid': 10, 'privacy': anon, 'message': message}))
                lst.append(f'{login} - Подарки отправлены')
            except:
                return 'Неизвестная ошибка'
    return lst

def chat_ids_out(account, chat_id):
    login, password = account.split(':')
    print(login, password)
    vk_session = get_token(login, password)
    if vk_session:
        try:
            users_lst = vk_session.method('messages.getChat', {'chat_id': chat_id, 'fields': ['nickname']})
            users = [i['id'] for i in users_lst['users']]
            print(users)
            return users
        except:
            return f'Неизвестная ошибка, скорее всего беседы под номером {chat_id} не существует'
    else:
        return "Неверный логин или пароль"