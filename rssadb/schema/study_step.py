from typing import List, Union
from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, and_, or_, select
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

from ..dbconfig import Base


class Step(Base):
	__tablename__ = 'study_step'

	id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
	study_id = Column(UUID(as_uuid=True), ForeignKey('study.id'), nullable=False)
	
	order_position = Column(Integer, nullable=False)
	name = Column(String, nullable=False)
	description = Column(String, nullable=True)
	date_created = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))
	enabled = Column(Boolean, nullable=False, default=True)

	study = relationship('Study', back_populates='steps')
	pages = relationship('Page', back_populates='step', \
		uselist=True, cascade='all, delete-orphan')

	def __init__(self, study_id: UUID, order_position: int, name: str, description: Union[str, None] = None):
		self.study_id = study_id
		self.order_position = order_position
		self.name = name
		self.description = description


