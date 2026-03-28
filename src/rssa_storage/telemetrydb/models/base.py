import sqlalchemy as sa

from rssa_storage.shared import DateAuditMixin
from rssa_storage.shared.db_utils import NAMING_CONVENTION, SharedModel


class TelemetryBase(SharedModel, DateAuditMixin):
    __abstract__ = True

    metadata = sa.MetaData(naming_convention=NAMING_CONVENTION)
