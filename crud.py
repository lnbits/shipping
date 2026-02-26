# Description: This file contains the CRUD operations for talking to the database.


from lnbits.db import Database, Filters, Page
from lnbits.helpers import urlsafe_short_hash

from .models import (
    CreateMethod,
    CreateRegions,
    ExtensionSettings,  #
    Method,
    MethodFilters,
    Regions,
    RegionsFilters,
    UserExtensionSettings,  #
)

db = Database("ext_shipping")


########################### Regions ############################
async def create_regions(user_id: str, data: CreateRegions) -> Regions:
    regions = Regions(**data.dict(), id=urlsafe_short_hash(), user_id=user_id)
    await db.insert("shipping.regions", regions)
    return regions


async def get_regions(
    user_id: str,
    regions_id: str,
) -> Regions | None:
    return await db.fetchone(
        """
            SELECT * FROM shipping.regions
            WHERE id = :id AND user_id = :user_id
        """,
        {"id": regions_id, "user_id": user_id},
        Regions,
    )


async def get_regions_by_id(
    regions_id: str,
) -> Regions | None:
    return await db.fetchone(
        """
            SELECT * FROM shipping.regions
            WHERE id = :id
        """,
        {"id": regions_id},
        Regions,
    )


async def get_regions_ids_by_user(
    user_id: str,
) -> list[str]:
    rows: list[dict] = await db.fetchall(
        """
            SELECT DISTINCT id FROM shipping.regions
            WHERE user_id = :user_id
        """,
        {"user_id": user_id},
    )

    return [row["id"] for row in rows]


async def get_regions_paginated(
    user_id: str | None = None,
    filters: Filters[RegionsFilters] | None = None,
) -> Page[Regions]:
    where = []
    values = {}
    if user_id:
        where.append("user_id = :user_id")
        values["user_id"] = user_id

    return await db.fetch_page(
        "SELECT * FROM shipping.regions",
        where=where,
        values=values,
        filters=filters,
        model=Regions,
    )


async def get_regions_by_user(user_id: str) -> list[Regions]:
    return await db.fetchall(
        """
            SELECT * FROM shipping.regions
            WHERE user_id = :user_id
        """,
        {"user_id": user_id},
        Regions,
    )


async def update_regions(data: Regions) -> Regions:
    await db.update("shipping.regions", data)
    return data


async def delete_regions(user_id: str, regions_id: str) -> None:
    await db.execute(
        """
            DELETE FROM shipping.regions
            WHERE id = :id AND user_id = :user_id
        """,
        {"id": regions_id, "user_id": user_id},
    )


################################# Methods ###########################


async def create_method(user_id: str, data: CreateMethod) -> Method:
    method = Method(**data.dict(), id=urlsafe_short_hash(), user_id=user_id)
    await db.insert("shipping.methods", method)
    return method


async def get_method_by_id(
    method_id: str,
) -> Method | None:
    return await db.fetchone(
        """
            SELECT * FROM shipping.methods
            WHERE id = :id
        """,
        {"id": method_id},
        Method,
    )


async def get_method_by_title(
    user_id: str,
    title: str,
) -> Method | None:
    return await db.fetchone(
        """
            SELECT * FROM shipping.methods
            WHERE user_id = :user_id AND title = :title
        """,
        {"user_id": user_id, "title": title},
        Method,
    )


async def get_methods_by_user(
    user_id: str,
) -> list[Method]:
    return await db.fetchall(
        """
            SELECT * FROM shipping.methods
            WHERE user_id = :user_id
        """,
        {"user_id": user_id},
        Method,
    )


async def get_methods_paginated(
    user_id: str | None = None,
    filters: Filters[MethodFilters] | None = None,
) -> Page[Method]:
    where = []
    values = {}
    if user_id:
        where.append("user_id = :user_id")
        values["user_id"] = user_id

    return await db.fetch_page(
        "SELECT * FROM shipping.methods",
        where=where,
        values=values,
        filters=filters,
        model=Method,
    )


async def update_method(data: Method) -> Method:
    await db.update("shipping.methods", data)
    return data


async def delete_method(user_id: str, method_id: str) -> None:
    await db.execute(
        """
            DELETE FROM shipping.methods
            WHERE id = :id AND user_id = :user_id
        """,
        {"id": method_id, "user_id": user_id},
    )


############################ Settings #############################
async def create_extension_settings(user_id: str, data: ExtensionSettings) -> ExtensionSettings:
    settings = UserExtensionSettings(**data.dict(), id=user_id)
    await db.insert("shipping.extension_settings", settings)
    return settings


async def get_extension_settings(
    user_id: str,
) -> ExtensionSettings | None:
    return await db.fetchone(
        """
            SELECT * FROM shipping.extension_settings
            WHERE id = :user_id
        """,
        {"user_id": user_id},
        ExtensionSettings,
    )


async def update_extension_settings(user_id: str, data: ExtensionSettings) -> ExtensionSettings:
    settings = UserExtensionSettings(**data.dict(), id=user_id)
    await db.update("shipping.extension_settings", settings)
    return settings
