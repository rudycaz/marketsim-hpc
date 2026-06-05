from dataclasses import dataclass


@dataclass(frozen=True)
class AssetInfo:
    input_symbol: str
    symbol: str
    asset_type: str
    display_name: str
    currency: str


CRYPTO_ALIASES = {
    "BTC": "BTC-USD",
    "BITCOIN": "BTC-USD",
    "XBT": "BTC-USD",
    "ETH": "ETH-USD",
    "ETHEREUM": "ETH-USD",
    "SOL": "SOL-USD",
    "SOLANA": "SOL-USD",
    "DOGE": "DOGE-USD",
    "DOGECOIN": "DOGE-USD",
    "XRP": "XRP-USD",
    "ADA": "ADA-USD",
    "CARDANO": "ADA-USD",
    "AVAX": "AVAX-USD",
    "LINK": "LINK-USD",
    "CHAINLINK": "LINK-USD",
    "LTC": "LTC-USD",
    "LITECOIN": "LTC-USD",
}


CRYPTO_DISPLAY_NAMES = {
    "BTC-USD": "Bitcoin",
    "ETH-USD": "Ethereum",
    "SOL-USD": "Solana",
    "DOGE-USD": "Dogecoin",
    "XRP-USD": "XRP",
    "ADA-USD": "Cardano",
    "AVAX-USD": "Avalanche",
    "LINK-USD": "Chainlink",
    "LTC-USD": "Litecoin",
}


def normalize_asset_symbol(symbol: str) -> AssetInfo:
    raw = symbol.strip()
    key = raw.upper().replace(" ", "")

    normalized = CRYPTO_ALIASES.get(key, key)

    if normalized.endswith("-USD") and normalized in CRYPTO_DISPLAY_NAMES:
        return AssetInfo(
            input_symbol=raw,
            symbol=normalized,
            asset_type="crypto",
            display_name=CRYPTO_DISPLAY_NAMES[normalized],
            currency="USD",
        )

    return AssetInfo(
        input_symbol=raw,
        symbol=key,
        asset_type="stock",
        display_name=key,
        currency="USD",
    )


def is_crypto_symbol(symbol: str) -> bool:
    return normalize_asset_symbol(symbol).asset_type == "crypto"
