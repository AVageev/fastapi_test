import requests
import time
from datetime import datetime

def fetch_spread():
    url = 'https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/securities/SBER/marketdata.json'
    response = requests.get(url)
    data = response.json()
    md = data['marketdata']['data'][0]
    bid = md[2]
    offer = md[4]
    spread = md[6]
    update_time = md[32]
    return bid, offer, spread, update_time

def main():
    while True:
        now = datetime.now().time()
        if now >= datetime.strptime('07:00', '%H:%M').time() and now <= datetime.strptime('23:50', '%H:%M').time():
            try:
                bid, offer, spread, update_time = fetch_spread()
                print(f'{update_time} BID: {bid}, OFFER: {offer}, SPREAD: {spread}')
            except Exception as e:
                print('Ошибка:', e)
        else:
            print('Вне времени сбора данных')
        time.sleep(5)  # пауза 5 секунд

if __name__ == '__main__':
    main()
