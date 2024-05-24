from pydantic import BaseModel


class PhoneAddressScheme(BaseModel):
    phone: int
    address: str
