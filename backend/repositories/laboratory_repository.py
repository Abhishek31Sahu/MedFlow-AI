from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from models.laboratory import LaboratoryOrder
from models.enums import LabOrderStatus


class LaboratoryRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, order: LaboratoryOrder) -> LaboratoryOrder:
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)
        return order

    def get_by_id(
        self,
        order_id: UUID,
    ) -> Optional[LaboratoryOrder]:

        result = self.db.execute(
            select(LaboratoryOrder).where(
                LaboratoryOrder.id == order_id
            )
        )

        return result.scalar_one_or_none()

    def get_by_service_request(
        self,
        service_request_id: str,
    ) -> Optional[LaboratoryOrder]:

        result = self.db.execute(
            select(LaboratoryOrder).where(
                LaboratoryOrder.service_request_id
                == service_request_id
            )
        )

        return result.scalar_one_or_none()

    def get_pending_orders(self) -> List[LaboratoryOrder]:

        result = self.db.execute(
            select(LaboratoryOrder)
            .where(
                LaboratoryOrder.status
                == LabOrderStatus.PENDING
            )
            .order_by(
                LaboratoryOrder.ordered_at
            )
        )

        return list(result.scalars().all())

    def get_patient_orders(
        self,
        patient_id: str,
    ) -> List[LaboratoryOrder]:

        result = self.db.execute(
            select(LaboratoryOrder)
            .where(
                LaboratoryOrder.patient_id
                == patient_id
            )
            .order_by(
                LaboratoryOrder.ordered_at.desc()
            )
        )

        return list(result.scalars().all())

    def get_doctor_orders(
        self,
        practitioner_id: str,
    ) -> List[LaboratoryOrder]:

        result = self.db.execute(
            select(LaboratoryOrder)
            .where(
                LaboratoryOrder.practitioner_id
                == practitioner_id
            )
            .order_by(
                LaboratoryOrder.ordered_at.desc()
            )
        )

        return list(result.scalars().all())

    def get_technician_orders(
        self,
        technician_id: str,
    ) -> List[LaboratoryOrder]:

        result = self.db.execute(
            select(LaboratoryOrder)
            .where(
                LaboratoryOrder.technician_id
                == technician_id
            )
            .order_by(
                LaboratoryOrder.ordered_at.desc()
            )
        )

        return list(result.scalars().all())

    def update(
        self,
        order: LaboratoryOrder,
    ) -> LaboratoryOrder:

        self.db.commit()
        self.db.refresh(order)

        return order

    def delete(
        self,
        order: LaboratoryOrder,
    ) -> None:

        self.db.delete(order)
        self.db.commit()