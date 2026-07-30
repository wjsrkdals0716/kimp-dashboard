# 김프(%) = (업비트 KRW / (바이낸스 USDT × 원달러환율) - 1) × 100
# 단순화: USDT=1USD, 환율은 ECB 고시(하루 1회 갱신)

import requests

r = requests.get("https://api.upbit.com/v1/ticker", params={"markets": "KRW-BTC"})
upbit_krw = r.json()[0]["trade_price"]

r = requests.get("https://api.binance.com/api/v3/ticker/price", params={"symbol": "BTCUSDT"})
binance_usdt = float(r.json()["price"])  # 가격이 문자열로 옴

# 환율은 크립토 바깥 소스여야 함 — 업비트 KRW-USDT엔 이미 김프가 끼어 있음
r = requests.get("https://api.frankfurter.app/latest", params={"from": "USD", "to": "KRW"})
usd_krw = r.json()["rates"]["KRW"]

binance_krw = binance_usdt * usd_krw
kimp = (upbit_krw / binance_krw - 1) * 100

print(f"업비트   BTC/KRW  : {upbit_krw:>15,.0f} 원")
print(f"바이낸스 BTC/USDT : {binance_usdt:>15,.2f} 달러")
print(f"환율     USD/KRW  : {usd_krw:>15,.2f} 원")
print("-" * 40)
print(f"바이낸스 원화 환산 : {binance_krw:>14,.0f} 원")
print(f"김치 프리미엄      : {kimp:>+14.2f} %")
