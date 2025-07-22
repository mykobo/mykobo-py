from mykobo_py.business.compliance import countries

def test_whitelisted_countries():
    assert len(countries.WHITELISTED_COUNTRIES) == 35