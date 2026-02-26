from datetime import datetime, timezone

from lnbits.db import FilterModel
from pydantic import BaseModel, Field

DEFAULT_AVAILABLE_REGIONS = [
    "Africa",
    "Asia",
    "Europe",
    "UK/Ireland",
    "North America",
    "South America",
    "Central America",
    "Caribbean",
    "Oceania",
    "Middle East",
    "Antarctica",
]


########################### Regions ############################
class CreateRegions(BaseModel):
    name: str
    regions: list[str]
    price: float
    weight_threshold: int | None
    price_per_g: float | None
    


class Regions(BaseModel):
    id: str
    user_id: str
    name: str
    regions: list[str]
    price: float
    weight_threshold: int | None
    price_per_g: float | None
    
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))




class RegionsFilters(FilterModel):
    __search_fields__ = [
        "name","regions","price","weight_threshold","price_per_g",
    ]

    __sort_fields__ = [
        "name",
        "regions",
        "price",
        "weight_threshold",
        "price_per_g",
        
        "created_at",
        "updated_at",
    ]

    created_at: datetime | None
    updated_at: datetime | None


################################# Methods ###########################


class CreateMethod(BaseModel):
    title: str
    cost_percentage: float = 0
    regions: list[str] = Field(default_factory=list)


class Method(BaseModel):
    id: str
    user_id: str
    title: str
    cost_percentage: float
    regions: list[str] = Field(default_factory=list)

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class MethodFilters(FilterModel):
    __search_fields__ = [
        "title",
    ]

    __sort_fields__ = [
        "title",
        "cost_percentage",
        "created_at",
        "updated_at",
    ]

    created_at: datetime | None
    updated_at: datetime | None


class AvailableRegionsResponse(BaseModel):
    available_regions: list[str]
    methods: list[Method]
    regions: list[Regions]


class CalculatePriceRequest(BaseModel):
    region: str
    weight: int
    method: str | None = None


class CalculatePriceResponse(BaseModel):
    regions_id: str
    regions_name: str
    region: str
    regions: list[str]
    weight: int
    base_price: float
    cost_percentage: float
    method_fee: float
    final_price: float
    currency: str
    fiat_price: float
    method_id: str | None
    method_title: str | None


############################ Settings #############################
class ExtensionSettings(BaseModel):
    currency: str = "sat"
    available_regions: list[str] = Field(default_factory=lambda: DEFAULT_AVAILABLE_REGIONS.copy())

    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @classmethod
    def is_admin_only(cls) -> bool:
        return bool("False" == "True")


class UserExtensionSettings(ExtensionSettings):
    id: str
