from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter
from starlette import status

from app.domain.entities.routes import Route
from app.presentation.api.decorators.only_admin import only_admin
from app.presentation.api.routes.routes.schemas import GetRouteSchema, AddRouteSchema
from app.services.routes import RouteService

router = APIRouter(
    prefix="/routes",
    tags=["Маршруты"],
    route_class=DishkaRoute
)


@router.get(
    "",
    summary="Получить список маршрутов",
    response_model=list[GetRouteSchema],
    status_code=status.HTTP_200_OK
)
async def get_routes(
        route_service: FromDishka[RouteService],
):
    routes = await route_service.get_routes()
    return [
        GetRouteSchema.model_validate(route, from_attributes=True)
        for route in routes
    ]


@router.post(
    "",
    summary="Добавить маршрут",
    response_model=GetRouteSchema,
    status_code=status.HTTP_201_CREATED
)
@only_admin
async def add_route(
        route: AddRouteSchema,
        route_service: FromDishka[RouteService]
):
    route = await route_service.add_route(
        Route(
            id=None,
            name=route.name,
            start_point_name=route.start_point_name,
            end_point_name=route.end_point_name,
            start_time=route.start_time,
            end_time=route.end_time,
            interval_seconds=route.interval_seconds,
            duration_seconds=route.duration_seconds
        )
    )
    return GetRouteSchema.model_validate(route, from_attributes=True)


@router.delete(
    "/{route_id}",
    summary="Удалить маршрут",
    status_code=status.HTTP_204_NO_CONTENT
)
@only_admin
async def delete_route(
        route_id: int,
        route_service: FromDishka[RouteService]
):
    await route_service.delete_route(route_id)
