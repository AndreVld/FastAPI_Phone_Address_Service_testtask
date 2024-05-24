from typing import Annotated

from fastapi import APIRouter, Body, Depends, status

from app.api.schemas import PhoneAddressScheme
from app.api.service import Service
from app.exceptions import KeyAlreadyExists, KeynotFound, ServerErrorException

router = APIRouter()


@router.post("/write_data", status_code=status.HTTP_201_CREATED)
async def write_data(
    body: Annotated[PhoneAddressScheme, Body()], service: Annotated[Service, Depends()]
):
    res = await service.write_address(body.phone, body.address)
    if res == "exists":
        raise KeyAlreadyExists
    elif res == "error":
        raise ServerErrorException


@router.patch("/write_data", status_code=status.HTTP_200_OK)
async def rewrite(
    body: Annotated[PhoneAddressScheme, Body()], service: Annotated[Service, Depends()]
):
    if await service.exists(body.phone):
        if not await service.rewrite_address(body.phone, body.address):
            raise ServerErrorException
    else:
        raise KeynotFound


@router.get("/check_data", status_code=status.HTTP_200_OK)
async def check_data(phone: int, service: Annotated[Service, Depends()]) -> str:
    if addres := await service.get_address_by_phone(phone):
        return addres
    raise KeynotFound
