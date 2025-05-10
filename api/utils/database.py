import os
import logging
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection
from pymongo.errors import ConnectionFailure

logger = logging.getLogger(__name__)
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

class AsyncMongoDB:
    """
    Asynchronous client for working with MongoDB using Motor.

    Methods:
        connect() -> None
        close() -> None
        get_collection(name: str) -> AsyncIOMotorCollection
        get_or_create_collection(
            name: str,
            index_fields: list[tuple[str, int]] = None,
            unique: bool = False
        ) -> AsyncIOMotorCollection
        list_collection_names() -> list[str]
        verify_connection() -> bool
    """

    def __init__(
        self,
        uri: str | None = None,
        db_name: str | None = None,
        server_selection_timeout_ms: int = 3000,
        max_pool_size: int = 100,
    ):
        self._uri = uri or os.getenv("MONGO_URI", "mongodb://localhost:27017")
        self._db_name = db_name or os.getenv("MONGO_DB_NAME", "default_db")
        self._connect_opts = {
            "serverSelectionTimeoutMS": server_selection_timeout_ms,
            "maxPoolSize": max_pool_size,
        }
        self._client: AsyncIOMotorClient | None = None
        self.db: AsyncIOMotorDatabase | None = None

    async def connect(self) -> None:
        """
        Establishes connection to MongoDB, initializes db attribute and verifies connectivity.
        Should be called during application startup.
        """
        try:
            self._client = AsyncIOMotorClient(self._uri, **self._connect_opts)
            self.db = self._client[self._db_name]
            await self._client.admin.command("ping")
            logger.info("Successfully connected and pinged MongoDB database '%s'", self._db_name)
        except ConnectionFailure as e:
            logger.error("Failed to connect or ping MongoDB: %s", e)
            raise

    def close(self) -> None:
        """
        Closes connection to MongoDB. Should be called during application shutdown.
        """
        if self._client:
            self._client.close()
            logger.info("MongoDB connection closed")

    async def get_collection(self, name: str) -> AsyncIOMotorCollection:
        """Returns a collection by name, error if it does not exist."""
        if self.db is None:
            logger.error("Attempted to get collection '%s' before DB initialized", name)
            raise ConnectionFailure("Database not initialized")
        if not name:
            logger.error("Collection name not specified")
            raise ValueError("Collection name must be specified")
        existing = await self.db.list_collection_names()
        if name not in existing:
            logger.error("Collection '%s' does not exist in database '%s'", name, self._db_name)
            raise ValueError(f"Collection '{name}' does not exist")
        return self.db[name]

    async def get_or_create_collection(
        self,
        name: str,
        index_fields: list[tuple[str, int]] = None,
        unique: bool = False
    ) -> AsyncIOMotorCollection:
        """
        Retrieves or creates a collection with optional indexes.
        """
        if self.db is None:
            logger.error("Attempted to get or create collection '%s' before DB initialized", name)
            raise ConnectionFailure("Database not initialized")
        existing = await self.db.list_collection_names()
        if name not in existing:
            await self.db.create_collection(name)
            logger.info("Created new collection '%s'", name)
        coll = self.db[name]
        if index_fields:
            self._client[self._db_name][name].create_index(index_fields, unique=unique)
            logger.info(
                "Created index on collection '%s': %s (unique=%s)",
                name, index_fields, unique
            )
        return coll

    async def list_collection_names(self) -> list[str]:
        """Returns list of collection names in the database."""
        if self.db is None:
            logger.error("Attempted to list collections before DB initialized")
            raise ConnectionFailure("Database not initialized")
        return await self.db.list_collection_names()

    async def verify_connection(self) -> bool:
        """Pings server and attempts reconnect if ping fails."""
        if self._client is None:
            await self.connect()
        try:
            await self._client.admin.command("ping")
            logger.info("MongoDB ping successful")
            return True
        except ConnectionFailure:
            logger.warning("MongoDB ping failed, attempting reconnect")
            try:
                await self.connect()
                return True
            except ConnectionFailure:
                logger.error("MongoDB reconnect failed")
                return False

global mongo_db
mongo_db = AsyncMongoDB()
