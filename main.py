import requests
import sys


def main():
    base_url = 'https://bg.alfabank.ru'
    login = base_url + '/auth/realms/farzoom-prod/account'

    # User-Agent Forms: <название-продукта> / <версия продукта> <комментарий>
    user_agent = 'nameless-project / 0.0.1 (Python {0})'.format(sys.version[:5])

    # session open
    session = requests.Session()

    # session headers
    session.headers.update({'User-Agent': user_agent})

    # auth
    resp = session.post(login, {
        'login': '',
        'password': ''})

    # res
    with open('success_login.txt', 'w', encoding='utf-8') as f:
        f.write(str(resp.text))
    print(resp)


if __name__ == "__main__":
    main()
