
from sqlalchemy import select, delete, update
from sqlalchemy.orm import Session

from database import Base, engine
from schema import TaskSchema
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

    def create_task(self, task: TaskSchema) -> int:
        task_model = Tasks(
            name=task.name,
            date=task.date,
            time=task.time,
            comment=task.comment,
            category_id=task.category_id
        )

        with self.db_session() as session:
            session.add(task_model)
            session.commit()
            return task_model.id

    def update_task_name(self, task_id: int, name: str) -> Tasks:
        with self.db_session() as session:
            query = (
                update(Tasks)
                .where(Tasks.id == task_id)
                .values(name=name)
            ).returning(Tasks.id)
            task_id: int = session.execute(query).scalar_one_or_none()
            session.commit()
            return self.get_task(task_id)

    def delete_task(self, task_id) -> str:
        with self.db_session() as session:
            query = delete(Tasks).where(Tasks.id == task_id).returning(Tasks.name)
            delete_task = session.execute(query)
            session.commit()
            return delete_task

    def get_task_by_category_name(self, category_name: str) -> list[Tasks]:
        query = (select(Tasks)
                 .join(Categories, Tasks.category_id == Categories.id)
                 .whrere(Categories.name == category_name))
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

        task_1 = Tasks(
            name="пробежать 10 км",
            date="2024-09-20",
            time="10:00",
            comment="лучше в первой половине дня",
            category_id=1,
        )
        task_2 = Tasks(
            name="дописать API",
            date="2024-09-05",
            time="до конца дня",
            comment="полюбому нужно доделать, иначе я задержусь на этом пути",
            category_id=3,
        )
        task_3 = Tasks(
            name="сходить в баню",
            date="2024-09-06",
            time="вечером",
            comment="сгонять с серегой в баню",
            category_id=2,
        )
        # with self.db_session() as session:
        #     Base.metadata.drop_all(engine)
        #     Base.metadata.create_all(engine)
        #     session.commit()
        with self.db_session() as session:
            session.add(category_1)
            session.add(category_2)
            session.add(category_3)
            session.add(task_1)
            session.add(task_2)
            session.add(task_3)
            session.commit()

    def drop_all_table(self):
        with self.db_session() as session:
            Base.metadata.drop_all(engine)

            session.commit()
