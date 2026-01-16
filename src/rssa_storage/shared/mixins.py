import uuid
from typing import Any, Protocol

from sqlalchemy import update


class VersionedModel(Protocol):
    """Protocol for models that support versioning."""

    id: uuid.UUID
    version: int


class VersionedRepositoryMixin:
    """Mixin for repositories handling versioned models with optimistic concurrency control.

    Expected to be used with BaseRepository or similar class that provides `db` and `model` attributes.
    """

    db: Any
    model: type[VersionedModel]

    async def update_response(self, instance_id: uuid.UUID, update_data: dict[str, Any], client_version: int) -> bool:
        """Update a versioned instance with optimistic concurrency control.

        Args:
            instance_id: The UUID of the instance to update.
            update_data: A dictionary of fields to update.
            client_version: The version number provided by the client.

        Returns:
            True if the update was successful, False if there was a version conflict.
        """
        update_fields = {**update_data, 'version': client_version + 1}

        update_stmt = (
            update(self.model)
            .where(self.model.id == instance_id, self.model.version == client_version)
            .values(**update_fields)
        )

        result = await self.db.execute(update_stmt)

        if result.rowcount == 1:
            await self.db.flush()
            return True
        else:
            await self.db.rollback()
            return False
