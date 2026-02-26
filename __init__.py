import asyncio

from fastapi import APIRouter
from lnbits.tasks import create_permanent_unique_task
from loguru import logger

from .crud import db
from .tasks import wait_for_paid_invoices
from .views import shipping_generic_router
from .views_api import shipping_api_router

shipping_ext: APIRouter = APIRouter(prefix="/shipping", tags=["Shipping"])
shipping_ext.include_router(shipping_generic_router)
shipping_ext.include_router(shipping_api_router)


shipping_static_files = [
    {
        "path": "/shipping/static",
        "name": "shipping_static",
    }
]

scheduled_tasks: list[asyncio.Task] = []


def shipping_stop():
    for task in scheduled_tasks:
        try:
            task.cancel()
        except Exception as ex:
            logger.warning(ex)


def shipping_start():
    task = create_permanent_unique_task("ext_shipping", wait_for_paid_invoices)
    scheduled_tasks.append(task)


__all__ = [
    "db",
    "shipping_ext",
    "shipping_start",
    "shipping_static_files",
    "shipping_stop",
]
