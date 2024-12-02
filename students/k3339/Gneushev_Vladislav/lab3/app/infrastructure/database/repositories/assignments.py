from sqlalchemy import select, delete

from app.domain.entities.assignments import DriverAssignment
from app.infrastructure.database.converters.assignments import from_assignment_dm_to_db, from_assignment_db_to_dm
from app.infrastructure.database.models import DriverAssignmentDB
from app.infrastructure.database.repositories.base import BaseRepository


class AssignmentRepository(BaseRepository):
    async def get_assignments(self, active: bool | None = None) -> list[DriverAssignment]:
        q = select(DriverAssignmentDB)
        if active is not None:
            q = q.where(
                DriverAssignmentDB.to_date.is_(None)
                if active
                else DriverAssignmentDB.to_date.isnot(None)
            )
        result = await self.session.execute(q)
        assignments = result.unique().scalars().all()
        return [
            from_assignment_db_to_dm(assignment)
            for assignment in assignments
         ]

    async def get_driver_active_assignments(self, driver_id: int) -> list[DriverAssignment]:
        q = select(DriverAssignmentDB).where(DriverAssignmentDB.driver_id == driver_id).where(DriverAssignmentDB.to_date.is_(None))
        result = await self.session.execute(q)
        assignments = result.unique().scalars().all()
        return [
            from_assignment_db_to_dm(assignment)
            for assignment in assignments
        ]

    async def add_assignment(self, assignment: DriverAssignment) -> DriverAssignment:
        assignment_db = from_assignment_dm_to_db(assignment)
        self.session.add(assignment_db)
        await self.session.commit()
        await self.session.refresh(assignment_db)
        return from_assignment_db_to_dm(assignment_db)

    async def get_assignment_by_id(self, assignment_id: int) -> DriverAssignment | None:
        q = select(DriverAssignmentDB).where(DriverAssignmentDB.id == assignment_id)
        result = await self.session.execute(q)
        assignment = result.scalars().first()
        if assignment:
            return from_assignment_db_to_dm(assignment)

    async def delete_assignment(self, assignment_id: int) -> None:
        q = delete(DriverAssignmentDB).where(DriverAssignmentDB.id == assignment_id)
        await self.session.execute(q)
        await self.session.commit()
