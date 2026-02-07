from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from controllers import auth_controller, promise_controller
from controllers import update_controller, politician_controller

app = FastAPI(title="ระบบติดตามคำสัญญานักการเมือง")

# Add SessionMiddleware for authentication
# TODO: Change this secret key to a secure random string in production!
app.add_middleware(SessionMiddleware, secret_key="1234")

app.mount("/static", StaticFiles(directory=Path(__file__).parent / "static"), name="static")

from fastapi.responses import RedirectResponse

app.include_router(auth_controller.router)
app.include_router(promise_controller.router)
app.include_router(update_controller.router)
app.include_router(politician_controller.router)

@app.get("/")
async def root():
    return RedirectResponse(url="/promises")