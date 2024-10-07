from typing import Annotated, Any, Collection

import jinja2
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fasthx import Jinja
from jinja2_fragments.fastapi import Jinja2Blocks
from pydantic import BaseModel, Field
from starlette.responses import HTMLResponse


# Pydantic model of the data the example API is using.
class UserInput(BaseModel):
    first_name: str
    last_name: str


class User(UserInput):
    id: Annotated[int, Field(frozen=True)]


# Create the app.
app = FastAPI()

def unpack_object(obj: Any) -> dict[str, Any] | None:
    # print("unpack_object", obj)
    if obj is None:
        return None
    if isinstance(obj, dict):
        return obj
    if isinstance(obj, BaseModel):
        return obj.model_dump(mode="json")


def unpack_result(*, route_result: Any, route_context: dict[str, Any]) -> dict[str, Any]:
    ctx = {"route": route_context}
    if route_result is not None:
        if isinstance(route_result, Collection):
            ctx["items"] = [unpack_object(o) for o in route_result]
        else:
            ctx["item"] = unpack_object(route_result)
    # print("unpack_result", ctx)
    return ctx

# Create a FastAPI Jinja2Templates instance and use it to create a
# FastHX Jinja instance that will serve as your decorator.
# jinja = Jinja(Jinja2Templates("templates", auto_reload=True, undefined=jinja2.StrictUndefined), make_context=unpack_result)
jinja = Jinja(Jinja2Blocks("templates", auto_reload=True, undefined=jinja2.StrictUndefined), make_context=unpack_result)


USERS = [
    User(id=0, first_name="John", last_name="Lennon"),
    User(id=1, first_name="Paul", last_name="McCartney"),
    User(id=2, first_name="George", last_name="Harrison"),
    User(id=3, first_name="Ringo", last_name="Starr"),
]


@app.get("/", tags=["HTML"], response_class=HTMLResponse)
@jinja.page("index.html")
def index() -> None:
    """
    Home page
    HTML only
    """
    pass


@app.get("/user-list", tags=["HTML", "HTMX", "API"], responses={200: {
        "content": {"text/html": {}},
        "description": "Return the JSON item or an image.",
    }})
@jinja.xh("users.html")
def users() -> list[User]:
    """
    User list
    HTML (full page), HTMX (fragment), or API (JSON)
    """
    return USERS

@app.get("/user/{id}", tags=["HTML", "HTMX", "API"], responses={200: {
        "content": {"text/html": {}},
        "description": "Return the JSON item or an image.",
    }})
@jinja.xh("user.html")
def user(id: int) -> User:
    """
    A single user
    HTML (full page), HTMX (fragment), or API (JSON)
    """
    return USERS[id]
