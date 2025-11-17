from csv import DictReader
from typing import Any

from sqlalchemy import Integer, String, create_engine, func, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

URL = "sqlite:///dz9.db"
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


def insert_user(row: dict[str, Any]):
    with Session(engine) as session:
        new_student = StudentWithMark(**row)
        session.add(new_student)
        session.commit()


def select_users(row: dict[str, Any]) -> list[StudentWithMark]:
    with Session(engine) as session:
        select_query = select(StudentWithMark)
        if id := row.get("id"):
            return list(session.scalars(select_query.where(StudentWithMark.id == id)))

        if first_name := row.get("first_name"):
            select_query = select_query.where(StudentWithMark.first_name == first_name)

        if last_name := row.get("last_name"):
            select_query = select_query.where(StudentWithMark.last_name == last_name)
        if faculty := row.get("faculty"):
            select_query = select_query.where(StudentWithMark.faculty == faculty)
        if course := row.get("course"):
            select_query = select_query.where(StudentWithMark.course == course)
        if mark := row.get("mark"):
            select_query = select_query.where(StudentWithMark.mark == mark)

        return list(session.scalars(select_query))


def get_students_by_faculty(faculty: str) -> list[StudentWithMark]:
    with Session(engine) as session:
        return list(
            session.scalars(
                select(StudentWithMark).where(StudentWithMark.faculty == faculty)
            )
        )


def get_unique_courses() -> set[str]:
    with Session(engine) as session:
        return set(session.query(StudentWithMark.faculty).distinct().all())


def get_average_mark() -> int:
    with Session(engine) as session:
        return session.query(func.avg(StudentWithMark.mark)).scalar()


def get_students_with_low_marks_on_courses(course: str) -> list[StudentWithMark]:
    with Session(engine) as session:
        return list(
            session.scalars(
                select(StudentWithMark).where(
                    StudentWithMark.course == course,
                    StudentWithMark.mark < 30,
                )
            )
        )


def insert_from_csv():
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
        with Session(engine) as session:
            for row in reader:
                row = {header_map[k]: v for k, v in row.items()}
                new_student = StudentWithMark(**row)
                session.add(new_student)
            session.commit()
