# graph/persistence.py

from contextlib import asynccontextmanager

from psycopg_pool import AsyncConnectionPool
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver


@asynccontextmanager
async def checkpointer_context(database_url: str):

    async with AsyncConnectionPool(
        conninfo=database_url,
        kwargs={
            "autocommit": True,
            "prepare_threshold": None,
        },
    ) as pool:

        checkpointer = AsyncPostgresSaver(pool)

        await checkpointer.setup()

        yield checkpointer