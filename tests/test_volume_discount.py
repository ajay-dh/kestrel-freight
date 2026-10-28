from kestrel.quote import quote


def test_big_shipments_get_a_discount():
    # 1,000 kg should be cheaper than 999 kg on the same lane
    assert quote(1000, 100) < quote(999, 100)
