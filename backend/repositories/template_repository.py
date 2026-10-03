from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from models.lab_template import LabTemplate


class TemplateRepository:

    def __init__(self, db: Session):
        self.db = db

    # ==========================================================
    # Create Template
    # ==========================================================

    def create(
        self,
        template: LabTemplate,
    ) -> LabTemplate:

        self.db.add(template)

        self.db.commit()

        self.db.refresh(template)

        return template

    # ==========================================================
    # Get Template By Test Code
    # ==========================================================

    def get_by_code(
        self,
        test_code: str,
    ) -> LabTemplate | None:

        result = self.db.execute(

            select(LabTemplate)
            .options(
                selectinload(LabTemplate.parameters)
            )
            .where(
                LabTemplate.test_code == test_code
            )

        )

        return result.scalar_one_or_none()

    # ==========================================================
    # Get All Templates
    # ==========================================================

    def get_all(
        self,
    ) -> list[LabTemplate]:

        result = self.db.execute(

            select(LabTemplate)
            .options(
                selectinload(LabTemplate.parameters)
            )
            .order_by(
                LabTemplate.test_name
            )

        )

        return result.scalars().all()

    # ==========================================================
    # Update Template
    # ==========================================================

    def update(
        self,
        template: LabTemplate,
    ) -> LabTemplate:

        self.db.commit()

        self.db.refresh(template)

        return template

    # ==========================================================
    # Delete Template
    # ==========================================================

    def delete(
        self,
        template: LabTemplate,
    ) -> None:

        self.db.delete(template)

        self.db.commit()