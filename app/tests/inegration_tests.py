import pytest
from fastapi import Response
from httpx import AsyncClient


@pytest.mark.parametrize(
    "phone, address,  status_code",
    [
        (89321236111, "address1", 200),
        (89321234241, "", 400),
        (89567865222, "address2", 200),
    ],
)
async def test_chec_addres(phone: int, address: str, status_code: int, ac: AsyncClient):
    response: Response = await ac.get("/check_data", params={"phone": phone})

    assert response.status_code == status_code
    if response.status_code == 200:
        assert response.json() == address


@pytest.mark.parametrize(
    "phone, address,  status_code",
    [
        (89492949195, "address1", 201),
        (89321236111, "address13", 400),
        (42487467885, "address4", 201),
    ],
)
async def test_write_data(phone: int, address: str, status_code: int, ac: AsyncClient):
    response: Response = await ac.post(
        url="/write_data", json={"phone": phone, "address": address}
    )
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "phone, address,  status_code",
    [
        (89321236111, "address111", 200),
        (89768213211, "address13", 400),
        (89567865222, "address4", 200),
    ],
)
async def test_rewrite_data(
    phone: int, address: str, status_code: int, ac: AsyncClient
):
    response: Response = await ac.patch(
        url="/write_data", json={"phone": phone, "address": address}
    )
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "phone, address,  status_code_write, status_code_check",
    [
        (89321236777, "address777", 201, 200),
        (89768213444, "address4", 400, 200),
        (89567865999, "address999", 201, 200),
    ],
)
async def test_write_and_check_addres(
    phone: int,
    address: str,
    status_code_write: int,
    status_code_check: int,
    ac: AsyncClient,
):
    response: Response = await ac.post(
        url="/write_data", json={"phone": phone, "address": address}
    )
    assert response.status_code == status_code_write

    response: Response = await ac.get("/check_data", params={"phone": phone})

    assert response.status_code == status_code_check

    if response.status_code == 200:
        assert response.json() == address
