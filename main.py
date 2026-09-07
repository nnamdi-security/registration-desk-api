from typing import Annotated, Optional

from fastapi import Cookie, FastAPI, Header, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI()



class UnionHeaders(BaseModel):
    x_union_pass: str  
    x_client_version: str = "1.0" 


class StaffBase(BaseModel):
    username: str
    full_name: Optional[str] = None
    station: str


class StaffIn(StaffBase):
    password: str = Field(min_length=8)

    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "username": "amaka.eze",
                    "full_name": "Amaka Eze",
                    "password": "unionpass2026",
                    "station": "VIP Front Desk",
                }
            ]
        }
    }


class StaffOut(StaffBase):
    pass 

@app.post(
    "/staff",
    response_model=StaffOut, 
    status_code=status.HTTP_201_CREATED,  
    summary="Register a VIP staff member",
)
async def register_staff(
    staff: StaffIn,
    headers: Annotated[UnionHeaders, Header()],
) -> StaffIn:
   
    if headers.x_union_pass != "UNION-2026-VIP":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong pass.")

    return staff


class VisitorCookies(BaseModel):
    session_id: str  
    language: str = "en" 


GREETINGS = {
    "en": "Welcome back!",
    "pidgin": "How far, you don come again!",
}


@app.get("/desk/greeting", summary="Greet a returning visitor by their cookies")
async def greet_visitor(
    cookies: Annotated[VisitorCookies, Cookie()],
) -> dict[str, str]:
    
    greeting = GREETINGS.get(cookies.language, "Welcome!")
    return {"session_id": cookies.session_id, "greeting": greeting}
