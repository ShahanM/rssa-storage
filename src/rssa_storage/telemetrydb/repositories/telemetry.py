from rssa_storage.shared.base_repo import BaseRepository
from rssa_storage.telemetrydb.models.telemetry import ParticipantTelemetry


class TelemetryRepo(BaseRepository[ParticipantTelemetry]):
    pass
