from src.auto_break import BreakRcp
from src.objects import BasePayload


def main():
    ob = BasePayload.set_instance({'email': 'email', 'password': 'pass', 'request_verification_token': None})
    a = BreakRcp(browser_type='google chrome', user_auth=ob)
    a.add_break()


if __name__ == '__main__':
    main()
