import sys

from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests
from src.objects import BasePayload, FirstPayload, SecondPayload

URL1 = 'https://inewi.pl/kiosk/'
URL2 = 'https://inewi.pl/kiosk/OnlineRcp/LoginByEmailOrPhone'
URL3 = 'https://inewi.pl/kiosk/OnlineRcp/SetStatus'


class BreakRcp:
    def __init__(self, browser_type: str, user_auth: BasePayload):
        self.browser_type = browser_type
        self.user_auth = user_auth

    @staticmethod
    def set_user_agent(browser_type: str):
        ua = UserAgent()
        return {"User-Agent": ua[browser_type]}

    @staticmethod
    def get_verification_token(self, session):
        try:
            page = BeautifulSoup(session.get(URL1).content, 'html.parser')
            token = page.find('input', {'name': '__RequestVerificationToken'}).get('value')
        except requests.ConnectionError as err:
            print("Connection error %s" % str(err))
        except Exception as e:
            print("Got unhandled exception %s" % str(e))
        return token

    def add_break(self):
        with requests.Session() as session:
            session.auth = self.user_auth.auth_tuple()
            headers = self.set_user_agent(self.browser_type)
            try:
                landing_page = session.get(URL1, verify=False, headers=headers, timeout=5)
            except requests.Timeout:
                # possible infinite loop
                self.add_break()
            except requests.ConnectionError as err:
                # add browser pop up
                SystemExit(err)
            self.user_auth.request_verification_token = str(self.get_verification_token(session))
            try:
                session.post(landing_page.url, data=self.user_auth.to_dict(), headers=headers, timeout=5)
            except requests.Timeout:
                # possible infinite loop
                self.add_break()
            except requests.ConnectionError as err:
                # add browser pop up
                SystemExit(err)
            first_payload = FirstPayload.set_instance(self.user_auth.__dict__)
            try:
                second_page = session.post(URL2, data=first_payload.to_dict(), headers=headers, timeout=5)
            except requests.Timeout:
                self.add_break()
            except requests.ConnectionError as err:
                # add browser pop up
                SystemExit(err)
            statuses = second_page.json()['statuses']
            for d in statuses:
                if d['Name'] == 'Przerwa':
                    second_payload = SecondPayload().set_instance({
                        'status_id': d['Id'],
                        'qr': second_page.json()['qrCode'],
                        'is_end': second_page.json()['preferedStatusIsEnd'],  # typo in Inewi ¯\_(ツ)_/¯
                        'time_local_unix': second_page.json()['timeLocalUnix'],
                        'time_utc_unix': second_page.json()['timeUtcUnix'],
                        'time_zone_id': second_page.json()['timeZoneId']
                    })
            try:
                session.post(URL3, data=second_payload.to_dict(), headers=headers)
            except requests.Timeout:
                self.add_break()
            except requests.ConnectionError as err:
                # add browser pop up
                SystemExit(err)
