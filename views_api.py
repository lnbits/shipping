# Description: This file contains the extensions API endpoints.
from http import HTTPStatus

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from lnbits.core.models import SimpleStatus, User
from lnbits.core.models.users import AccountId
from lnbits.db import Filters, Page
from lnbits.decorators import (
    check_account_exists,
    check_account_id_exists,
    parse_filters,
)
from lnbits.helpers import generate_filter_params_openapi

from .crud import (
    create_method,
    create_regions,
    delete_method,
    delete_regions,
    get_method_by_id,
    get_methods_paginated,
    get_regions,
    get_regions_by_user,
    get_regions_paginated,
    update_method,
    update_regions,
)
from .models import (
    AvailableRegionsResponse,
    CalculatePriceRequest,
    CalculatePriceResponse,
    CreateMethod,
    CreateRegions,
    ExtensionSettings,  #
    Method,
    MethodFilters,
    Regions,
    RegionsFilters,
)
from .services import (
    calculate_price_for_request,
    get_available_regions_with_methods,
    get_settings,  #
    update_settings,  #
)

regions_filters = parse_filters(RegionsFilters)
method_filters = parse_filters(MethodFilters)

shipping_api_router = APIRouter()


############################# Regions #############################
@shipping_api_router.post("/api/v1/regions", status_code=HTTPStatus.CREATED)
async def api_create_regions(
    data: CreateRegions,
    account_id: AccountId = Depends(check_account_id_exists),
) -> Regions:
    existing = await get_regions_by_user(account_id.id)
    for row in existing:
        if set(row.regions) & set(data.regions):
            raise HTTPException(HTTPStatus.BAD_REQUEST, "Region already assigned.")
    regions = await create_regions(account_id.id, data)
    return regions


@shipping_api_router.put("/api/v1/regions/{regions_id}", status_code=HTTPStatus.CREATED)
async def api_update_regions(
    regions_id: str,
    data: CreateRegions,
    account_id: AccountId = Depends(check_account_id_exists),
) -> Regions:
    regions = await get_regions(account_id.id, regions_id)
    if not regions:
        raise HTTPException(HTTPStatus.NOT_FOUND, "Regions not found.")
    if regions.user_id != account_id.id:
        raise HTTPException(HTTPStatus.FORBIDDEN, "You do not own this regions.")
    existing = await get_regions_by_user(account_id.id)
    for row in existing:
        if row.id == regions_id:
            continue
        if set(row.regions) & set(data.regions):
            raise HTTPException(HTTPStatus.BAD_REQUEST, "Region already assigned.")
    regions = await update_regions(Regions(**{**regions.dict(), **data.dict()}))
    return regions


@shipping_api_router.get(
    "/api/v1/regions/paginated",
    name="Regions List",
    summary="get paginated list of regions",
    response_description="list of regions",
    openapi_extra=generate_filter_params_openapi(RegionsFilters),
    response_model=Page[Regions],
)
async def api_get_regions_paginated(
    account_id: AccountId = Depends(check_account_id_exists),
    filters: Filters = Depends(regions_filters),
) -> Page[Regions]:

    return await get_regions_paginated(
        user_id=account_id.id,
        filters=filters,
    )


@shipping_api_router.get(
    "/api/v1/regions/{regions_id}",
    name="Get Regions",
    summary="Get the regions with this id.",
    response_description="An regions or 404 if not found",
    response_model=Regions,
)
async def api_get_regions(
    regions_id: str,
    account_id: AccountId = Depends(check_account_id_exists),
) -> Regions:

    regions = await get_regions(account_id.id, regions_id)
    if not regions:
        raise HTTPException(HTTPStatus.NOT_FOUND, "Regions not found.")

    return regions


@shipping_api_router.delete(
    "/api/v1/regions/{regions_id}",
    name="Delete Regions",
    summary="Delete the regions.",
    response_description="The status of the deletion.",
    response_model=SimpleStatus,
)
async def api_delete_regions(
    regions_id: str,
    account_id: AccountId = Depends(check_account_id_exists),
) -> SimpleStatus:

    await delete_regions(account_id.id, regions_id)
    return SimpleStatus(success=True, message="Regions Deleted")


############################# Methods #############################
@shipping_api_router.post(
    "/api/v1/methods",
    name="Create Method",
    summary="Create new shipping method.",
    response_description="The created method.",
    response_model=Method,
    status_code=HTTPStatus.CREATED,
)
async def api_create_method(
    data: CreateMethod,
    account_id: AccountId = Depends(check_account_id_exists),
) -> Method:
    regions_list = await get_regions_by_user(account_id.id)
    valid_region_ids = {region.id for region in regions_list}
    invalid = [region_id for region_id in data.regions if region_id not in valid_region_ids]
    if invalid:
        raise HTTPException(HTTPStatus.BAD_REQUEST, "Invalid region.")
    return await create_method(account_id.id, data)


@shipping_api_router.put(
    "/api/v1/methods/{method_id}",
    name="Update Method",
    summary="Update the method with this id.",
    response_description="The updated method.",
    response_model=Method,
)
async def api_update_method(
    method_id: str,
    data: CreateMethod,
    account_id: AccountId = Depends(check_account_id_exists),
) -> Method:
    method = await get_method_by_id(method_id)
    if not method:
        raise HTTPException(HTTPStatus.NOT_FOUND, "Method not found.")
    if method.user_id != account_id.id:
        raise HTTPException(HTTPStatus.FORBIDDEN, "You do not own this method.")
    regions_list = await get_regions_by_user(account_id.id)
    valid_region_ids = {region.id for region in regions_list}
    invalid = [region_id for region_id in data.regions if region_id not in valid_region_ids]
    if invalid:
        raise HTTPException(HTTPStatus.BAD_REQUEST, "Invalid region.")

    method = await update_method(Method(**{**method.dict(), **data.dict()}))
    return method


@shipping_api_router.get(
    "/api/v1/methods/paginated",
    name="Methods List",
    summary="get paginated list of methods",
    response_description="list of methods",
    openapi_extra=generate_filter_params_openapi(MethodFilters),
    response_model=Page[Method],
)
async def api_get_methods_paginated(
    account_id: AccountId = Depends(check_account_id_exists),
    filters: Filters = Depends(method_filters),
) -> Page[Method]:
    return await get_methods_paginated(
        user_id=account_id.id,
        filters=filters,
    )


@shipping_api_router.get(
    "/api/v1/methods/{method_id}",
    name="Get Method",
    summary="Get the method with this id.",
    response_description="A method or 404 if not found",
    response_model=Method,
)
async def api_get_method(
    method_id: str,
    account_id: AccountId = Depends(check_account_id_exists),
) -> Method:
    method = await get_method_by_id(method_id)
    if not method:
        raise HTTPException(HTTPStatus.NOT_FOUND, "Method not found.")
    if method.user_id != account_id.id:
        raise HTTPException(HTTPStatus.FORBIDDEN, "You do not own this method.")
    return method


@shipping_api_router.delete(
    "/api/v1/methods/{method_id}",
    name="Delete Method",
    summary="Delete the method",
    response_description="The status of the deletion.",
    response_model=SimpleStatus,
)
async def api_delete_method(
    method_id: str,
    account_id: AccountId = Depends(check_account_id_exists),
) -> SimpleStatus:
    method = await get_method_by_id(method_id)
    if not method:
        raise HTTPException(HTTPStatus.NOT_FOUND, "Method not found.")
    if method.user_id != account_id.id:
        raise HTTPException(HTTPStatus.FORBIDDEN, "You do not own this method.")

    await delete_method(account_id.id, method_id)
    return SimpleStatus(success=True, message="Method Deleted")


############################# Public Data #############################
@shipping_api_router.get(
    "/api/v1/get_regions",
    name="Get Available Regions",
    summary="Get available regions and methods for this user.",
    response_description="Available regions and methods",
    response_model=AvailableRegionsResponse,
)
async def api_get_available_regions(
    account_id: AccountId = Depends(check_account_id_exists),
) -> AvailableRegionsResponse:
    available_regions, methods, regions = await get_available_regions_with_methods(account_id.id)
    return AvailableRegionsResponse(available_regions=available_regions, methods=methods, regions=regions)


@shipping_api_router.post(
    "/api/v1/calculate_price",
    name="Calculate Shipping Price",
    summary="Calculate shipping price for a region, weight and method.",
    response_description="Calculated shipping price",
    response_model=CalculatePriceResponse,
)
async def api_calculate_price(
    data: CalculatePriceRequest,
    account_id: AccountId = Depends(check_account_id_exists),
) -> CalculatePriceResponse:
    try:
        result = await calculate_price_for_request(
            account_id.id,
            data.region,
            data.weight,
            data.method,
        )
    except ValueError as exc:
        raise HTTPException(HTTPStatus.BAD_REQUEST, str(exc)) from exc
    return CalculatePriceResponse(**result)


############################ Settings #############################
@shipping_api_router.get(
    "/api/v1/settings",
    name="Get Settings",
    summary="Get the settings for the current user.",
    response_description="The settings or 404 if not found",
    response_model=ExtensionSettings,
)
async def api_get_settings(
    account_id: AccountId = Depends(check_account_id_exists),
) -> ExtensionSettings:
    user_id = "admin" if ExtensionSettings.is_admin_only() else account_id.id
    return await get_settings(user_id)


@shipping_api_router.put(
    "/api/v1/settings",
    name="Update Settings",
    summary="Update the settings for the current user.",
    response_description="The updated settings.",
    response_model=ExtensionSettings,
)
async def api_update_extension_settings(
    data: ExtensionSettings,
    account: User = Depends(check_account_exists),
) -> ExtensionSettings:
    if ExtensionSettings.is_admin_only() and not account.admin:
        raise HTTPException(
            HTTPStatus.FORBIDDEN,
            "Only admins can update settings.",
        )
    user_id = "admin" if ExtensionSettings.is_admin_only() else account.id
    return await update_settings(user_id, data)
