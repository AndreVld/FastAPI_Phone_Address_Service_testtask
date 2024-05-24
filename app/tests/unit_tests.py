import pytest

from app.api.service import Service


@pytest.mark.parametrize(
    "phone, address, exists",
    [
        (89768213444, "address4", True),
        (89321323232, "", False),
        (89567865222, "address4", True),
    ],
)
async def test_get_addres_by_phone(
    phone: int, address: str, exists: bool, redis_session
):
    serv = Service(redis=redis_session)
    res = await serv.get_address_by_phone(phone)
    if exists:
        assert res == address
    else:
        assert not res


@pytest.mark.parametrize(
    "phone, address, exists",
    [
        (87473235156, "address2134", False),
        (89323213333, "address21123134", True),
        (87471276282, "address213234", False),
    ],
)
async def test_write_addres(phone: int, address: str, exists: bool, redis_session):
    serv = Service(redis=redis_session)
    res = await serv.write_address(phone, address)
    if exists:
        assert res == "exists"
    else:
        assert res is None


@pytest.mark.parametrize(
    "phone, address",
    [
        (89321236111, "address2134"),
        (89567865222, "address21123134"),
        (89323213333, "address213234"),
    ],
)
async def test_rewrite_address(phone: int, address: str, redis_session):
    serv = Service(redis=redis_session)
    res = await serv.rewrite_address(phone, address)
    assert res is True


@pytest.mark.parametrize(
    "phone, exists",
    [
        (89321236111, True),
        (89567899996, False),
        (89567865222, True),
    ],
)
async def test_exists(phone: int, exists: bool, redis_session):
    serv = Service(redis=redis_session)
    res = await serv.exists(phone)
    assert res == exists
