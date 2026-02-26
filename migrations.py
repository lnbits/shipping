# the migration file is where you build your database tables
# If you create a new release for your extension ,
# remember the migration file is like a blockchain, never edit only add!

empty_dict: dict[str, str] = {}


async def m001_extension_settings(db):
    """
    Initial settings table.
    """

    await db.execute(
        f"""
        CREATE TABLE shipping.extension_settings (
            id TEXT NOT NULL,
            currency TEXT NOT NULL,
            available_regions TEXT NOT NULL DEFAULT '[]',
            updated_at TIMESTAMP NOT NULL DEFAULT {db.timestamp_now}
        );
    """
    )


async def m002_regions(db):
    """
    Regions table.
    """

    await db.execute(
        f"""
        CREATE TABLE shipping.regions (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            name TEXT NOT NULL,
            regions TEXT NOT NULL,
            price REAL NOT NULL,
            weight_threshold INT,
            price_per_g REAL,
            created_at TIMESTAMP NOT NULL DEFAULT {db.timestamp_now},
            updated_at TIMESTAMP NOT NULL DEFAULT {db.timestamp_now}
        );
    """
    )


async def m003_methods(db):
    """
    Methods table.
    """

    await db.execute(
        f"""
        CREATE TABLE shipping.methods (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            title TEXT NOT NULL,
            cost_percentage REAL NOT NULL DEFAULT 0,
            regions TEXT NOT NULL DEFAULT '[]',
            created_at TIMESTAMP NOT NULL DEFAULT {db.timestamp_now},
            updated_at TIMESTAMP NOT NULL DEFAULT {db.timestamp_now}
        );
    """
    )
