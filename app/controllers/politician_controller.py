from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select
from pathlib import Path

from database import get_session
from models import Politician, Promise

router = APIRouter(tags=["politicians"])
templates = Jinja2Templates(directory=Path(__file__).parent.parent / "views")


@router.get("/politicians/{id}", response_class=HTMLResponse)
async def get_politician_detail(request: Request, id: str, session: Session = Depends(get_session)):
    """แสดงข้อมูลนักการเมืองและคำสัญญาทั้งหมด"""
    politician = session.get(Politician, id)
    if not politician:
        raise HTTPException(status_code=404, detail="Politician not found")
        
    # Get promises for this politician
    statement = select(Promise).where(Promise.politician_id == id).order_by(Promise.announced_date.desc())
    promises = session.exec(statement).all()

    return templates.TemplateResponse("politician.html", {
        "request": request,
        "politician": politician,
        "promises": promises,
    })
