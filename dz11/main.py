from contextlib import asynccontextmanager
from typing import Annotated, Any

from redis import asyncio as aioredis
import uvicorn
from fastapi import Depends, FastAPI, Query
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from dz9.main import StudentRepo, engine
from dz11.auth import UserSchema, auth_router, get_current_user


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    redis = aioredis.from_url(
        "redis://localhost", encoding="utf8", decode_responses=False
    )
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield


app = FastAPI(lifespan=app_lifespan)

app.include_router(auth_router)


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
@cache(expire=60)
def get_students(
    student: Annotated[StudentFilters, Query()],
    student_repo: StudentRepoDepends,
    current_user: Annotated[UserSchema, Depends(get_current_user)],
) -> list[StudentSchema]:
    res = student_repo.select_users(student.to_filters_dict())
    return [StudentSchema.model_validate(el) for el in res]


@app.post("/")
@cache(expire=60)
def create_student(
    student: StudentBaseSchema,
    student_repo: StudentRepoDepends,
    current_user: Annotated[UserSchema, Depends(get_current_user)],
) -> StudentSchema:
    res = student_repo.insert_user(student.model_dump())
    return StudentSchema.model_validate(res)


@app.put("/")
@cache(expire=60)
def update_student(
    student: StudentSchema,
    student_repo: StudentRepoDepends,
    current_user: Annotated[UserSchema, Depends(get_current_user)],
):
    student_repo.update_user(student.id, student.model_dump())
    return student


@app.delete("/{id}")
@cache(expire=60)
def delete_student(
    id: int,
    student_repo: StudentRepoDepends,
    current_user: Annotated[UserSchema, Depends(get_current_user)],
):
    student_repo.delete_user(id)


if __name__ == "__main__":
    uvicorn.run(app)
