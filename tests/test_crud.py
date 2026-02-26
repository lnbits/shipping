from uuid import uuid4

import pytest

from shipping.crud import (  # type: ignore[import]
    create_regions,
    delete_regions,
    get_regions,
    get_regions_by_id,
    get_regions_ids_by_user,
    get_regions_paginated,
    update_regions,
)
from shipping.models import (  # type: ignore[import]
    CreateRegions,
    Regions,
)


@pytest.mark.asyncio
async def test_create_and_get_regions():
    user_id = uuid4().hex

    data = CreateRegions(
        name="name_27Pt9bgojxiTHFcXoXb4dR",
        regions=["Europe", "Asia"],
        price=100,
        weight_threshold=82,
        price_per_g=88.45226127098425,
    )
    regions_one = await create_regions(user_id, data)
    assert regions_one.id is not None
    assert regions_one.user_id == user_id

    regions_one = await get_regions(user_id, regions_one.id)
    assert regions_one.id is not None
    assert regions_one.user_id == user_id
    assert regions_one.name == data.name
    assert regions_one.regions == data.regions
    assert regions_one.price == data.price
    assert regions_one.weight_threshold == data.weight_threshold
    assert regions_one.price_per_g == data.price_per_g

    data = CreateRegions(
        name="name_27Pt9bgojxiTHFcXoXb4dR",
        regions=["Europe", "Asia"],
        price=100,
        weight_threshold=82,
        price_per_g=88.45226127098425,
    )
    regions_two = await create_regions(user_id, data)
    assert regions_two.id is not None
    assert regions_two.user_id == user_id

    regions_list = await get_regions_ids_by_user(user_id=user_id)
    assert len(regions_list) == 2

    regions_page = await get_regions_paginated(user_id=user_id)
    assert regions_page.total == 2
    assert len(regions_page.data) == 2

    await delete_regions(user_id, regions_one.id)
    regions_list = await get_regions_ids_by_user(user_id=user_id)
    assert len(regions_list) == 1

    regions_page = await get_regions_paginated(user_id=user_id)
    assert regions_page.total == 1
    assert len(regions_page.data) == 1


@pytest.mark.asyncio
async def test_update_regions():
    user_id = uuid4().hex

    data = CreateRegions(
        name="name_27Pt9bgojxiTHFcXoXb4dR",
        regions=["Europe", "Asia"],
        price=100,
        weight_threshold=82,
        price_per_g=88.45226127098425,
    )
    regions_one = await create_regions(user_id, data)
    assert regions_one.id is not None
    assert regions_one.user_id == user_id

    regions_one = await get_regions(user_id, regions_one.id)
    assert regions_one.id is not None
    assert regions_one.user_id == user_id
    assert regions_one.name == data.name
    assert regions_one.regions == data.regions
    assert regions_one.price == data.price
    assert regions_one.weight_threshold == data.weight_threshold
    assert regions_one.price_per_g == data.price_per_g

    data_updated = CreateRegions(
        name="name_27Pt9bgojxiTHFcXoXb4dR",
        regions=["Europe", "Asia"],
        price=100,
        weight_threshold=82,
        price_per_g=88.45226127098425,
    )
    regions_updated = Regions(**{**regions_one.dict(), **data_updated.dict()})

    await update_regions(regions_updated)
    regions_one = await get_regions_by_id(regions_one.id)
    assert regions_one.name == regions_updated.name
    assert regions_one.regions == regions_updated.regions
    assert regions_one.price == regions_updated.price
    assert regions_one.weight_threshold == regions_updated.weight_threshold
    assert regions_one.price_per_g == regions_updated.price_per_g
