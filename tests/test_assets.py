from marketsim.assets import normalize_asset_symbol


def test_bitcoin_alias_normalizes_to_btc_usd():
    asset = normalize_asset_symbol("bitcoin")
    assert asset.symbol == "BTC-USD"
    assert asset.asset_type == "crypto"
    assert asset.display_name == "Bitcoin"


def test_btc_alias_normalizes_to_btc_usd():
    asset = normalize_asset_symbol("BTC")
    assert asset.symbol == "BTC-USD"
    assert asset.asset_type == "crypto"


def test_stock_symbol_remains_stock():
    asset = normalize_asset_symbol("CVX")
    assert asset.symbol == "CVX"
    assert asset.asset_type == "stock"
