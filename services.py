from decimal import ROUND_HALF_UP, Decimal

from lnbits.core.models import Payment
from loguru import logger

from .crud import (
    create_extension_settings,  #
    get_extension_settings,  #
    get_method_by_id,
    get_method_by_title,
    get_methods_by_user,
    get_regions_by_user,
    update_extension_settings,  #
)
from .models import ExtensionSettings, Method, Regions  #


async def payment_received_for_ignore(payment: Payment) -> bool:
    logger.info("Payment receive logic generation is disabled.")
    return True


async def get_settings(user_id: str) -> ExtensionSettings:
    settings = await get_extension_settings(user_id)
    if not settings:
        settings = await create_extension_settings(user_id, ExtensionSettings())
    elif not settings.available_regions:
        settings.available_regions = ExtensionSettings().available_regions
        settings = await update_extension_settings(user_id, settings)
    return settings


async def update_settings(user_id: str, data: ExtensionSettings) -> ExtensionSettings:
    settings = await get_extension_settings(user_id)
    if not settings:
        settings = await create_extension_settings(user_id, data)
    else:
        settings = await update_extension_settings(user_id, data)

    return settings


async def get_available_regions_with_methods(user_id: str) -> tuple[list[str], list, list]:
    settings = await get_settings(user_id)
    methods = await get_methods_by_user(user_id)
    regions = await get_regions_by_user(user_id)
    return settings.available_regions, methods, regions


def _round_price(value: float, currency: str) -> float:
    quant = Decimal("1") if currency in {"sat", "yen", "jpy"} else Decimal("0.01")
    return float(Decimal(str(value)).quantize(quant, rounding=ROUND_HALF_UP))


def _get_priced_region(region: str, regions_list: list[Regions]) -> Regions:
    matching = [item for item in regions_list if region in item.regions]
    if not matching:
        raise ValueError("Region not found for any pricing rule.")
    return sorted(matching, key=lambda item: item.price)[0]


def _compute_base_price(region_record: Regions, weight: int) -> float:
    base_price = float(region_record.price)
    if region_record.weight_threshold is None or region_record.price_per_g is None:
        return base_price
    if weight <= region_record.weight_threshold:
        return base_price
    return base_price + (weight - region_record.weight_threshold) * float(region_record.price_per_g)


async def _get_method_for_request(
    user_id: str,
    region_id: str,
    method: str | None,
) -> Method | None:
    if not method:
        return None
    method_obj = await get_method_by_id(method)
    if not method_obj:
        method_obj = await get_method_by_title(user_id, method)
    if not method_obj:
        raise ValueError("Method not found.")
    if method_obj.user_id != user_id:
        raise ValueError("Method not found.")
    if method_obj.regions and region_id not in method_obj.regions:
        raise ValueError("Method not available for this region.")
    return method_obj


async def calculate_price_for_request(
    user_id: str,
    region: str,
    weight: int,
    method: str | None,
) -> dict:
    if weight < 0:
        raise ValueError("Weight must be zero or greater.")
    settings = await get_settings(user_id)
    if region not in settings.available_regions:
        raise ValueError("Region is not available.")
    regions_list = await get_regions_by_user(user_id=user_id)
    region_record = _get_priced_region(region, regions_list)
    base_price = _compute_base_price(region_record, weight)

    method_obj = await _get_method_for_request(user_id, region_record.id, method)

    cost_percentage = method_obj.cost_percentage if method_obj else 0
    method_fee = base_price * (cost_percentage / 100)
    final_price = base_price + method_fee

    rounded_base = _round_price(base_price, settings.currency)
    rounded_fee = _round_price(method_fee, settings.currency)
    rounded_final = _round_price(final_price, settings.currency)

    return {
        "regions_id": region_record.id,
        "regions_name": region_record.name,
        "region": region,
        "regions": region_record.regions,
        "weight": weight,
        "base_price": rounded_base,
        "cost_percentage": cost_percentage,
        "method_fee": rounded_fee,
        "final_price": rounded_final,
        "currency": settings.currency,
        "fiat_price": rounded_final,
        "method_id": method_obj.id if method_obj else None,
        "method_title": method_obj.title if method_obj else None,
    }
