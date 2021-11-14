from bs4 import BeautifulSoup
import requests


form_data={'Email': 'you@gmail.com', 'Passwd': 'your_password'}
post = "https://accounts.google.com/signin/challenge/sl/password"

with requests.Session() as s:
    soup = BeautifulSoup(s.get("https://mail.google.com").text, 'lxml')
    for inp in soup.select("#gaia_loginform input[name]"):
        if inp["name"] not in form_data:
            form_data[inp["name"]] = inp["value"]
    s.post(post, form_data)
    html = s.get("https://mail.google.com/mail/u/0/#inbox").content

    # запись ответа в файл
    with open('success_login.txt', 'w', encoding='utf-8') as f:
        f.write(str(html))
