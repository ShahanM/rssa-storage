from typing import List, Union
from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, and_, or_, select
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

from ..dbconfig import Base


class Study(Base):
	__tablename__ = 'study'

	id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
	date_created = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))

	name = Column(String, nullable=False)
	description = Column(String, nullable=True)

	enabled = Column(Boolean, nullable=False, default=True)

	steps = relationship('Step', back_populates='study', \
		uselist=True, cascade='all, delete-orphan')
	conditions = relationship('StudyCondition', back_populates='study', \
		uselist=True, cascade='all, delete-orphan')
	
	def __init__(self, name: str, description: Union[str, None] = None):
		self.name = name
		self.description = description

