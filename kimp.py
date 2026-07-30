# -*- coding: utf-8 -*-
# 미션 1 — 김프 계산기
# 로직 설계: 사용자 · 구현: Claude (2026-07-30)
#
# 공식(사용자 설계):
#   김프(%) = ( 업비트 KRW가격 / (바이낸스 USDT가격 × 원달러환율) - 1 ) × 100
#
# 알고 있는 단순화 두 가지:
#   ① USDT = 1 USD로 취급 (평소 ±0.1%, 위기 시 더 벌어질 수 있음)
#   ② 환율은 ECB 고시(하루 1회 갱신) — 장중 환율 변동은 미반영

import requests

# 1단계 — 업비트: BTC 원화 가격
# 응답 구조: [ {...26개 필드} ] → [0]으로 꺼내서 trade_price(최근 체결가)만
r = requests.get("https://api.upbit.com/v1/ticker", params={"markets": "KRW-BTC"})
upbit_krw = r.json()[0]["trade_price"]

# 2단계 — 바이낸스: BTC 달러(USDT) 가격
# 응답 구조: {"symbol": ..., "price": "64003.78"} — 딕셔너리 바로, 가격이 문자열이라 float() 필수
r = requests.get("https://api.binance.com/api/v3/ticker/price", params={"symbol": "BTCUSDT"})
binance_usdt = float(r.json()["price"])

# 3단계 — 환율: USD/KRW (Frankfurter = ECB 고시, 무료·무인증)
# 주의: 업비트 KRW-USDT 가격을 환율로 쓰면 안 됨 — 거기엔 이미 김프가 끼어 있어서 상쇄됨
r = requests.get("https://api.frankfurter.app/latest", params={"from": "USD", "to": "KRW"})
usd_krw = r.json()["rates"]["KRW"]

# 4단계 — 조립: 사용자 공식 그대로
binance_krw = binance_usdt * usd_krw           # 바이낸스 가격을 원화로 환산 (달러 × 원/달러 = 원)
kimp = (upbit_krw / binance_krw - 1) * 100     # 비율 - 1 → ×100 → % 프리미엄

print(f"업비트   BTC/KRW  : {upbit_krw:>15,.0f} 원")
print(f"바이낸스 BTC/USDT : {binance_usdt:>15,.2f} 달러")
print(f"환율     USD/KRW  : {usd_krw:>15,.2f} 원")
print("-" * 40)
print(f"바이낸스 원화 환산 : {binance_krw:>14,.0f} 원")
print(f"김치 프리미엄      : {kimp:>+14.2f} %")
