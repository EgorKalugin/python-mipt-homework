import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, Field, field_serializer, field_validator
from typing import List, Optional
from datetime import date, datetime
import re


class ContactRequest(BaseModel):
    last_name: str = Field(
        ...,
        description="Фамилия с заглавной буквы, содержит только кириллицу",
        examples=["Иванов"],
    )
    first_name: str = Field(
        ...,
        description="Имя с заглавной буквы, содержит только кириллицу",
        examples=["Иван"],
    )
    birth_date: date = Field(..., description="Дата рождения", examples=["2000-01-01"])
    phone_number: str = Field(
        ..., description="Номер телефона", examples=["+78005553535"]
    )
    email: EmailStr = Field(..., description="E-mail", examples=["user@email.com"])
    reasons: Optional[List[str]] = Field(None, description="Причины обращения")
    problem_datetime: Optional[datetime] = Field(
        None, description="Дата и время обнаружения проблемы"
    )

    @field_validator("last_name", "first_name")
    def validate_name(cls, v: str) -> str:
        if not re.match(r"^[А-ЯЁ][а-яё]+$", v):
            raise ValueError(
                "Должно начинаться с заглавной буквы и содержать только кириллицу"
            )
        return v

    @field_validator("phone_number")
    def validate_phone_number(cls, v: str) -> str:
        if not re.match(r"^\+?\d{10,15}$", v):
            raise ValueError("Неверный формат номера телефона")
        return v

    @field_serializer("birth_date", mode="plain")
    def serialize_birth_date(self, v: date) -> str:
        return v.strftime("%Y-%m-%d")

    @field_serializer("problem_datetime")
    def serialize_problem_datetime(self, v: Optional[datetime]) -> Optional[str]:
        return v.strftime("%Y-%m-%d %H:%M:%S") if v else None


app = FastAPI()


@app.post("/contact_request/")
async def create_contact_request(request: ContactRequest):
    try:
        with open(f"contact_requests_{uuid.uuid4()}.json", "a", encoding="utf-8") as f:
            f.write(request.model_dump_json())
        return {"message": "Обращение принято к рассмотрению."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
