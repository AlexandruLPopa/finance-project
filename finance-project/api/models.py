from pydantic import BaseModel, Field
from uuid import UUID

# DONE add the field with description, aprox half


class UserAdd(BaseModel):
    username: str = Field(
        description="Alphanumeric username between 6 and 20 characters."
    )


class AssetAdd(BaseModel):
    ticker: str = Field(
        description="A ticker is a unique series of letters assigned to a security."
    )


class BaseModelOrmTrue(BaseModel):
    class Config:
        orm_mode = True


class AssetInfoBase(BaseModelOrmTrue):
    ticker: str = Field(description="The stock symbol.")
    name: str = Field(description="The company's full name.")
    country: str = Field(description="The company's headquarters country.")
    sector: str = Field(description="The company's main field of operations.")


class AssetInfoUser(AssetInfoBase):
    units: float = Field(description="The amount of stock units.")


class AssetInfoPrice(AssetInfoBase):
    currency: str = Field(description="The symbol for currency.")
    current_price: float = Field(description="The stock's current price.")
    # DONE homework
    today_low_price: float = Field(
        description="The stock's lowest registered price today."
    )
    today_high_price: float = Field(
        description="The stock's highest registered price today."
    )
    open_price: float = Field(
        description="The stock's latest registered opening price."
    )
    closed_price: float = Field(
        description="The stock's latest registered closing price."
    )
    fifty_day_price: float = Field(
        description="The stock's average price over the last fifty days."
    )
    price_evolution: str = Field(
        description="The stock's price evolution over the last 24 hours."
    )


class UserInfo(BaseModelOrmTrue):
    id: UUID = Field(description="A unique user ID.")
    username: str = Field(
        description="Alphanumeric username between 6 and 20 characters."
    )
    stocks: list[AssetInfoBase] = Field(
        description="A list of stocks associated to the user."
    )
