from datetime import datetime

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Query, HTTPException
from starlette import status

from app.domain.entities.assignments import EndAssignmentReason
from app.presentation.api.decorators.only_admin import only_admin
from app.presentation.api.routes.assignments.schemas import GetAssignmentSchema, AddAssignmentSchema, \
    EndAssignmentSchema
from app.services.assignments import AssignmentService
from app.services.exceptions import DriverHasActiveAssignment

router = APIRouter(
    prefix="/assignments",
    tags=["Назначения водителей на маршруты"],
    route_class=DishkaRoute
)


@router.get(
    "",
    summary="Получить список назначений",
    response_model=list[GetAssignmentSchema]
)
async def get_assigments(
        assigment_service: FromDishka[AssignmentService],
        active: bool = Query(None, description="Активные назначения")
):
    assigments = await assigment_service.get_assignments(
        active=active
    )
    return [
        GetAssignmentSchema.model_validate(assigment, from_attributes=True)
        for assigment in assigments
    ]


@router.post(
    "",
    summary="Добавить назначение",
    response_model=GetAssignmentSchema,
    status_code=status.HTTP_201_CREATED
)
@only_admin
async def add_assignment(
        assignment: AddAssignmentSchema,
        assignment_service: FromDishka[AssignmentService],
):
    try:
        assignment = await assignment_service.add_assignment(
            from_date=datetime.utcnow(),
            day_of_week=assignment.day_of_week,
            driver_id=assignment.driver_id,
            route_id=assignment.route_id,
            bus_id=assignment.bus_id
        )
    except DriverHasActiveAssignment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Время маршрута пересекается с другим маршрутом водителя в этот день"
        )
    return GetAssignmentSchema.model_validate(assignment, from_attributes=True)


@router.delete(
    "/{assignment_id}",
    summary="Удалить назначение",
    status_code=status.HTTP_204_NO_CONTENT
)
@only_admin
async def delete_assignment(
        assignment_id: int,
        assignment_service: FromDishka[AssignmentService]
):
    await assignment_service.delete_assignment(assignment_id)


@router.post(
    "/{assignment_id}/end",
    summary="Завершить назначение",
    status_code=status.HTTP_200_OK
)
@only_admin
async def end_assignment(
        assignment_id: int,
        body: EndAssignmentSchema,
        assignment_service: FromDishka[AssignmentService]
):
    await assignment_service.end_assignment(
        assignment_id=assignment_id,
        reason=body.reason
    )


@router.get(
    "/end/reasons",
    summary="Получить причины завершения назначения",
    response_model=list[str]
)
async def get_end_assignment_reasons():
    return [
        reason
        for reason in EndAssignmentReason
    ]
