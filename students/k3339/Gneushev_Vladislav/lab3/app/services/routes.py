from app.domain.entities.routes import Route
from app.infrastructure.database.repositories.routes import RouteRepository
from app.services.exceptions import EntityNotFound


class RouteService:
    def __init__(self, route_repo: RouteRepository):
        self.route_repo = route_repo

    async def get_routes(self) -> list[Route]:
        return await self.route_repo.get_routes()

    async def add_route(self, route: Route) -> Route:
        return await self.route_repo.add_route(route)

    async def delete_route(self, route_id: int) -> None:
        route = await self.route_repo.get_route_by_id(route_id)
        if not route:
            raise EntityNotFound(
                entity=Route,
                field_name='id',
                value=route_id
            )
        await self.route_repo.delete_route(route_id)
