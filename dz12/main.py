from fastapi import APIRouter, BackgroundTasks

from dz10.main import StudentRepoDepends

router = APIRouter(prefix="/background_tasks")


@router.post("/load-from-csv")
def load_students_from_csv(
    student_repo: StudentRepoDepends,
    background_tasks: BackgroundTasks,
):
    background_tasks.add_task(student_repo.insert_from_csv)
    return {"message": "Loading students from csv task sent in the background"}


@router.delete("/delete_by_list")
def delete_students_by_list(
    ids: list[int],
    student_repo: StudentRepoDepends,
    background_tasks: BackgroundTasks,
):
    background_tasks.add_task(student_repo.delete_users, ids)
    return {"message": "Deleting students task sent in the background"}
