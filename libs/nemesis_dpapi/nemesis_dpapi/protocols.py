"""Protocol definitions for DPAPI components."""

from typing import Protocol, runtime_checkable
from uuid import UUID

from .core import Blob, MasterKey, MasterKeyType
from .keys import DomainBackupKey, DpapiSystemCredential
from .repositories import MasterKeyFilter


@runtime_checkable
class DpapiManagerProtocol(Protocol):
    """Protocol defining the interface for DPAPI managers."""

    async def __aenter__(self):
        """Async context manager entry."""
        ...

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        ...

    async def upsert_masterkey(self, masterkey: MasterKey) -> None:
        """Add or update a masterkey (encrypted or plaintext)."""
        ...

    async def upsert_domain_backup_key(self, backup_key: DomainBackupKey) -> None:
        """Add or update a domain backup key."""
        ...

    async def upsert_dpapi_system_credential(self, cred: DpapiSystemCredential) -> None:
        """Add or update a DPAPI system credential."""
        ...

    async def decrypt_blob(self, blob: Blob) -> bytes:
        """Decrypt a DPAPI blob using available masterkeys."""
        ...

    async def get_masterkeys(
        self,
        guid: UUID | None = None,
        filter_by: MasterKeyFilter = MasterKeyFilter.ALL,
        backup_key_guid: UUID | None = None,
        masterkey_type: list[MasterKeyType] | None = None,
    ) -> list[MasterKey]:
        """Retrieve masterkey(s) with optional filtering.

        Args:
            guid: Optional specific masterkey GUID to retrieve. If provided, returns a list with one MasterKey or empty list.
            filter_by: Filter by decryption status (default: ALL). Ignored if guid is provided.
            backup_key_guid: Filter by backup key GUID (default: None for all). Ignored if guid is provided.
            masterkey_type: Filter by user account types (default: None for all). Ignored if guid is provided.

        Returns:
            A list of MasterKeys (empty list if no matches)
        """
        ...

    async def get_system_credentials(self, guid: UUID | None = None) -> list[DpapiSystemCredential]:
        """Retrieve DPAPI system credential(s)."""
        ...

    async def get_backup_keys(self, guid: UUID | None = None) -> list[DomainBackupKey]:
        """Retrieve domain backup key(s)."""
        ...

    async def close(self) -> None:
        """Close the manager and cleanup resources."""
        ...
