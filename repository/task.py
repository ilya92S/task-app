
from sqlalchemy import select, delete, update
from sqlalchemy.orm import Session

from database import Base, engine
from schema import TaskSchema, TaskCreateSchema
from models import Tasks, Categories


class TaskRepository:

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_all_tasks(self) -> list[Tasks]:
        query = select(Tasks)
        with self.db_session() as session:
            task: list[Tasks] = session.execute(query).scalars().all()
        return task

    def get_task(self, task_id) -> Tasks | None:
        with self.db_session() as session:
            task: Tasks = session.execute(
                select(Tasks)
                .where(Tasks.id == task_id)
            ).scalar_one_or_none()
        return task

    def create_task(self, task: TaskCreateSchema, user_id) -> int:
        task_model = Tasks(
            name=task.name,
            date=task.date,
            time=task.time,
            comment=task.comment,
            user_id=user_id,
            category_id=task.category_id
        )

        with self.db_session() as session:
            session.add(task_model)
            session.commit()
            return task_model.id


    def get_user_task(self, task_id: int, user_id: int) -> Tasks | None:
        with self.db_session() as session:
            query = (
                select(Tasks)
                .where(
                    Tasks.id == task_id,
                    Tasks.user_id == user_id
                )
            )
            result = session.execute(query)
            return result.scalar_one_or_none()


    def update_task_name(self, task_id: int, name: str) -> Tasks:
        with self.db_session() as session:
            query = (
                update(Tasks)
                .where(
                    Tasks.id == task_id
                )
                .values(name=name)
            ).returning(Tasks.id)
            task_id: int = session.execute(query).scalar_one_or_none()
            session.commit()
            return self.get_task(task_id)

    def delete_task(self, task_id: int, user_id: int) -> str:
        with self.db_session() as session:
            query = (
                delete(Tasks)
                .where(
                    Tasks.id == task_id,
                    Tasks.user_id == user_id
                )
                .returning(Tasks.name)
            )
            task_name = session.execute(query).scalar_one_or_none()
            session.commit()
            return task_name

    def get_task_by_category_name(self, category_name: str) -> list[Tasks]:
        query = (select(Tasks)
                 .join(Categories, Tasks.category_id == Categories.id)
                 .where(Categories.name == category_name))
        with self.db_session() as session:
            tasks: list[Tasks] = session.execute(query)
        return tasks

    def create_tasks_and_category(self):
        category_1 = Categories(
            name="спорт"
        )
        category_2 = Categories(
            name="отдых"
        )
        category_3 = Categories(
            name="работа"
        )


        with self.db_session() as session:
            session.add(category_1)
            session.add(category_2)
            session.add(category_3)
            session.commit()

    def drop_all_table(self):
        with self.db_session() as session:
            Base.metadata.drop_all(engine)

            session.commit()
