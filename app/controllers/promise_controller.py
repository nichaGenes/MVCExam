from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from templating import templates
from sqlmodel import Session, select
from pathlib import Path

from database import get_session
from models import Promise, Politician, Campaign, PromiseUpdate

router = APIRouter(tags=["promises"])


@router.get("/promises", response_class=HTMLResponse)
async def list_promises(request: Request, session: Session = Depends(get_session)):
    """แสดงรายการคำสัญญาทั้งหมด เรียงตามวันที่ประกาศ"""
    # Query promises with eager loading of relationships would be efficient, 
    # but SQLModel/SQLAlchemy async + jinja2 usually works by lazy loading in sync context 
    # or we pre-load. Let's select all promises ordered by date.
    statement = select(Promise).order_by(Promise.announced_date.desc())
    promises = session.exec(statement).all()
    
    return templates.TemplateResponse("all_promises.html", {
        "request": request,
        "promises": promises,
    })


@router.get("/promises/{id}", response_class=HTMLResponse)
async def get_promise_detail(request: Request, id: str, session: Session = Depends(get_session)):
    """แสดงรายละเอียดคำสัญญาและประวัติการอัปเดต"""
    promise = session.get(Promise, id)
    if not promise:
        raise HTTPException(status_code=404, detail="Promise not found")
        
    return templates.TemplateResponse("promise_detail.html", {
        "request": request,
        "promise": promise,
    })
