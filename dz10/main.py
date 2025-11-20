from typing import Annotated, Any

import uvicorn
from fastapi import Depends, FastAPI, Query
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from dz9.main import StudentRepo, engine

app = FastAPI()


class StudentBaseSchema(BaseModel):
    first_name: str
    last_name: str
    faculty: str
    course: str
    mark: int

    model_config = ConfigDict(from_attributes=True)


class StudentSchema(StudentBaseSchema):
    id: int


class StudentFilters(BaseModel):
    id: int | None = None
    first_name: str | None = None
    last_name: str | None = None
    faculty: str | None = None
    course: str | None = None
    mark: int | None = None

    def to_filters_dict(self) -> dict[str, Any]:
        return {key: val for (key, val) in self.model_dump().items() if val is not None}


def student_repo_depends():
    with Session(engine) as session:
        yield StudentRepo(session)


StudentRepoDepends = Annotated[StudentRepo, Depends(student_repo_depends)]


@app.get("/")
def get_students(
    student: Annotated[StudentFilters, Query()],
    student_repo: StudentRepoDepends,
) -> list[StudentSchema]:
    res = student_repo.select_users(student.to_filters_dict())
    return [StudentSchema.model_validate(el) for el in res]


@app.post("/")
def create_student(
    student: StudentBaseSchema,
    student_repo: StudentRepoDepends,
) -> StudentSchema:
    res = student_repo.insert_user(student.model_dump())
    return StudentSchema.model_validate(res)


@app.put("/")
def update_student(
    student: StudentSchema,
    student_repo: StudentRepoDepends,
):
    student_repo.update_user(student.id, student.model_dump())
    return student


@app.delete("/{id}")
def delete_student(
    id: int,
    student_repo: StudentRepoDepends,
):
    student_repo.delete_user(id)


if __name__ == "__main__":
    uvicorn.run(app)
