# -*- coding: utf-8 -*-
"""
프로젝트 1 · Day 1 — 김치 프리미엄 첫 계산 (2026-07-30)

같은 BTC가 업비트(원화)와 바이낸스(달러)에서 얼마나 다르게 거래되는지 확인한다.

    김프(%) = 업비트 KRW 가격 / (바이낸스 USDT 가격 × 원달러 환율) - 1

파생 렌즈: 같은 기초자산이 두 시장에서 다른 가격 → 현물 베이시스.
보너스로 무기한선물 펀딩비도 같이 찍는다 (베이시스 수렴 메커니즘).
"""

import requests

UPBIT_TICKER = "https://api.upbit.com/v1/ticker"
BINANCE_SPOT = "https://api.binance.com/api/v3/ticker/price"
BINANCE_PERP = "https://fapi.binance.com/fapi/v1/premiumIndex"
FX_RATE = "https://api.frankfurter.app/latest"  # ECB 고시 환율, 키 불필요


def upbit_price(market: str = "KRW-BTC") -> float:
    """업비트 현재가. 응답은 리스트 — 여러 마켓을 한 번에 물어볼 수 있어서."""
    r = requests.get(UPBIT_TICKER, params={"markets": market}, timeout=10)
    r.raise_for_status()
    return float(r.json()[0]["trade_price"])


def binance_price(symbol: str = "BTCUSDT") -> float:
    """바이낸스 현물 현재가."""
    r = requests.get(BINANCE_SPOT, params={"symbol": symbol}, timeout=10)
    r.raise_for_status()
    return float(r.json()["price"])


def binance_funding(symbol: str = "BTCUSDT") -> float:
    """바이낸스 무기한선물의 최근 펀딩비 (8시간당, 소수)."""
    r = requests.get(BINANCE_PERP, params={"symbol": symbol}, timeout=10)
    r.raise_for_status()
    return float(r.json()["lastFundingRate"])


def usd_krw() -> float:
    """원달러 환율 (ECB 고시가 — 실시간 호가는 아니지만 김프 감 잡기엔 충분)."""
    r = requests.get(FX_RATE, params={"from": "USD", "to": "KRW"}, timeout=10)
    r.raise_for_status()
    return float(r.json()["rates"]["KRW"])


def main() -> None:
    krw = upbit_price()          # 업비트 BTC/KRW
    usd = binance_price()        # 바이낸스 BTC/USDT
    fx = usd_krw()               # USD/KRW
    funding = binance_funding()  # 펀딩비 (8h)

    binance_in_krw = usd * fx
    kimp = krw / binance_in_krw - 1
    funding_apr = funding * 3 * 365  # 하루 3번 × 365일 = 연환산

    print(f"업비트   BTC/KRW  : {krw:>15,.0f}")
    print(f"바이낸스 BTC/USDT : {usd:>15,.2f}")
    print(f"환율     USD/KRW  : {fx:>15,.2f}")
    print("-" * 36)
    print(f"바이낸스 원화 환산 : {binance_in_krw:>14,.0f}")
    print(f"김치 프리미엄      : {kimp:>+14.2%}")
    print(f"펀딩비 (8h)        : {funding:>+14.4%}  (연환산 {funding_apr:+.1%})")


if __name__ == "__main__":
    main()
