from csv import DictReader
from typing import Any

from sqlalchemy import (Integer, String, create_engine, delete, func, select,
                        update)
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

URL = "sqlite:///dz9/dz9.db"
engine = create_engine(URL, echo=True)


class Base(DeclarativeBase): ...


class StudentWithMark(Base):
    __tablename__ = "students_with_marks"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(30))
    last_name: Mapped[str] = mapped_column(String(30))
    faculty: Mapped[str] = mapped_column(String(30))
    course: Mapped[str] = mapped_column(String(30))
    mark: Mapped[int] = mapped_column(Integer())

    def __repr__(self) -> str:
        return f"{self.id=} {self.first_name=} {self.last_name=}"


class StudentRepo:
    def __init__(self, session: Session):
        self.session = session

    def insert_user(self, row: dict[str, Any]) -> StudentWithMark:
        new_student = StudentWithMark(**row)
        self.session.add(new_student)
        self.session.commit()
        return new_student

    def select_users(self, filters: dict[str, Any]) -> list[StudentWithMark]:
        select_query = select(StudentWithMark)
        if filters.get("id") is not None:
            return list(
                self.session.scalars(
                    select_query.where(StudentWithMark.id == filters.get("id"))
                )
            )

        if first_name := filters.get("first_name"):
            select_query = select_query.where(StudentWithMark.first_name == first_name)
        if last_name := filters.get("last_name"):
            select_query = select_query.where(StudentWithMark.last_name == last_name)
        if faculty := filters.get("faculty"):
            select_query = select_query.where(StudentWithMark.faculty == faculty)
        if course := filters.get("course"):
            select_query = select_query.where(StudentWithMark.course == course)
        if mark := filters.get("mark"):
            select_query = select_query.where(StudentWithMark.mark == mark)

        return list(self.session.scalars(select_query))

    def get_students_by_faculty(self, faculty: str) -> list[StudentWithMark]:
        return list(
            self.session.scalars(
                select(StudentWithMark).where(StudentWithMark.faculty == faculty)
            )
        )

    def get_unique_courses(
        self,
    ) -> set[str]:
        return set(self.session.query(StudentWithMark.faculty).distinct().all())

    def get_average_mark(
        self,
    ) -> int:
        return self.session.query(func.avg(StudentWithMark.mark)).scalar()

    def update_user(
        self,
        id: int,
        user: dict[str, Any],
    ):
        del user["id"]
        self.session.execute(
            update(StudentWithMark).where(StudentWithMark.id == id).values(**user)
        )
        self.session.commit()

    def delete_user(
        self,
        id: int,
    ):
        self.session.execute(delete(StudentWithMark).where(StudentWithMark.id == id))
        self.session.commit()

    def delete_users(
        self,
        ids: list[int],
    ):
        self.session.execute(delete(StudentWithMark).where(StudentWithMark.id.in_(ids)))
        self.session.commit()

    def get_students_with_low_marks_on_courses(
        self, course: str
    ) -> list[StudentWithMark]:
        return list(
            self.session.scalars(
                select(StudentWithMark).where(
                    StudentWithMark.course == course,
                    StudentWithMark.mark < 30,
                )
            )
        )

    def insert_from_csv(
        self,
    ):
        csv_name = "students.csv"
        header_map = {
            "Фамилия": "last_name",
            "Имя": "first_name",
            "Факультет": "faculty",
            "Курс": "course",
            "Оценка": "mark",
        }

        with open(csv_name) as f:
            reader = DictReader(f)
            for row in reader:
                row = {header_map[k]: v for k, v in row.items()}
                new_student = StudentWithMark(**row)
                self.session.add(new_student)
            self.session.commit()
