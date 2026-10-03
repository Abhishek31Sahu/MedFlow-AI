from sqlalchemy.orm import Session

from repositories.template_repository import TemplateRepository

from models.lab_template import LabTemplate
from models.lab_parameter import LabParameter

from schemas.lab_template import (
    CreateTemplateRequest,
    UpdateTemplateRequest,
)


class TemplateService:

    def __init__(self, db: Session):
        self.repo = TemplateRepository(db)

    # =====================================================
    # Create Template
    # =====================================================

    def create_template(
        self,
        request: CreateTemplateRequest,
    ):

        # Check duplicate test code
        existing = self.repo.get_by_code(
            request.test_code
        )

        if existing:
            raise ValueError(
                "Template already exists."
            )

        template = LabTemplate(

            test_code=request.test_code,

            test_name=request.test_name,

            category=request.category,

            description=request.description,

        )

        # Add Parameters
        for index, parameter in enumerate(
            request.parameters,
            start=1,
        ):

            template.parameters.append(

                LabParameter(

                    code=parameter.code,

                    name=parameter.name,

                    unit=parameter.unit,

                    value_type=parameter.value_type,

                    reference_low=parameter.reference_low,

                    reference_high=parameter.reference_high,

                    required=parameter.required,

                    display_order=index,

                )

            )

        return self.repo.create(template)

    # =====================================================
    # Get Template
    # =====================================================

    def get_template(
        self,
        test_code: str,
    ):

        template = self.repo.get_by_code(
            test_code
        )

        if template is None:
            raise ValueError(
                "Template not found."
            )

        return template

    # =====================================================
    # Get All Templates
    # =====================================================

    def get_all_templates(self):

        return self.repo.get_all()

    # =====================================================
    # Delete Template
    # =====================================================

    def delete_template(
        self,
        test_code: str,
    ):

        template = self.repo.get_by_code(
            test_code
        )

        if template is None:
            raise ValueError(
                "Template not found."
            )

        self.repo.delete(template)

        return {
            "message": "Template deleted successfully."
        }

    # =====================================================
    # Update Template
    # =====================================================

    def update_template(
        self,
        test_code: str,
        request: UpdateTemplateRequest,
    ):

        template = self.repo.get_by_code(
            test_code
        )

        if template is None:
            raise ValueError(
                "Template not found."
            )

        template.test_name = request.test_name
        template.category = request.category
        template.description = request.description

        # Remove old parameters
        template.parameters.clear()

        # Add new parameters
        for index, parameter in enumerate(
            request.parameters,
            start=1,
        ):

            template.parameters.append(

                LabParameter(

                    code=parameter.code,

                    name=parameter.name,

                    unit=parameter.unit,

                    value_type=parameter.value_type,

                    reference_low=parameter.reference_low,

                    reference_high=parameter.reference_high,

                    required=parameter.required,

                    display_order=index,

                )

            )

        return self.repo.update(template)