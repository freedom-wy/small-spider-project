import requests
import re


class Login(object):
    def __init__(self):
        self.login_session = requests.session()
        self.header = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
        }
        self.city_token = ""


    def handle_city_token(self):
        """
        获取city_token,为登录做准备
        :return:self.city_token
        """
        login_url = "https://github.com/login"
        response = self.login_session.get(url=login_url,headers=self.header)
        city_token_search = re.compile(r'name="authenticity_token"\svalue="(.*?)"\s\/>')
        self.city_token = city_token_search.search(response.text).group(1)

    def handle_login_github(self):
        """
        执行登录
        :return: 登录后匹配的字符串
        """
        login_name = input("请输入用户名:")
        login_password = input("请输入密码:")
        self.handle_city_token()
        #获取登录cookie
        self.login_session.get(url="https://github.com/manifest.json",headers=self.header)
        data = {
            "commit": "Sign in",
            "utf8": "✓",
            "authenticity_token":self.city_token,
            "login": login_name,
            "password": login_password,
            "webauthn-support": "supported",
        }
        session_url = "https://github.com/session"
        self.header['Referer'] = "https://github.com/login"
        # 登录
        self.login_session.post(url=session_url,headers=self.header,data=data)
        self.header.pop('Referer')
        #请求设置页
        response = self.login_session.get(url="https://github.com/settings/profile",headers=self.header)
        search_email = re.compile(login_name)
        # 登陆成功后可以获取到自己的登录名称
        print(search_email.search(response.text).group())
if __name__ == '__main__':
    github = Login()
    github.handle_login_github()
