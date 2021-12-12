from bs4 import BeautifulSoup
from datetime import datetime
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

    def add_break(self):
        with requests.Session() as session:
            session.auth = self.user_auth.auth_tuple()
            headers = self.set_user_agent(self.browser_type)
            landing_page = session.get(URL1, verify=False, headers=headers)
            soup = BeautifulSoup(session.get(URL1).content, 'html.parser')
            try:
                token = soup.find('input', {'name': '__RequestVerificationToken'}).get('value')
            except Exception as e:
                print("Got unhandled exception %s" % str(e))
            self.user_auth.request_verification_token = str(token)
            session.post(landing_page.url, data=self.user_auth.to_dict(), headers=headers)
            first_payload = FirstPayload.set_instance(self.user_auth.__dict__)
            second_page = session.post(URL2, data=first_payload.to_dict(), headers=headers)
            statuses = second_page.json()['statuses']
            for d in statuses:
                if d['Name'] == 'Przerwa':
                    second_payload = SecondPayload().set_instance({
                        'status_id': d['Id'],
                        'qr': second_page.json()['qrCode'],
                        'is_end': d['IsEnd'],
                        'time_local_unix': second_page.json()['timeLocalUnix'],
                        'time_utc_unix': second_page.json()['timeUtcUnix'],
                        'time_zone_id': second_page.json()['timeZoneId']
                    })

            session.post(URL3, data=second_payload.to_dict(), headers=headers)

