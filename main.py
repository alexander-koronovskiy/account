import requests
import sys


def main():
    base_url = 'https://opt.euroauto.ru'
    login = base_url + '/user/auth'

    # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/User-Agent
    # для ваших запросов используйте такую форму:
    #  User-Agent: <название-продукта> / <версия продукта> <комментарий>
    user_agent = 'nameless-project / 0.0.1 (Python {0})'.format(sys.version[:5])

    # открытие сессии
    session = requests.Session()

    # обновление headers сессии
    session.headers.update({'User-Agent': user_agent})

    # авторизация
    resp = session.post(login, {
        'login': '<логин>',
        'passw': '<пароль>',
        'recaptcha': '<результат-после-успешного-прохождения-капчи>'})

    # запись ответа в файл
    with open('success_login.txt', 'w', encoding='utf-8') as f:
        f.write(str(resp.json()))


if __name__ == "__main__":
    main()
