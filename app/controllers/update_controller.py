from datetime import date
from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from templating import templates
from sqlmodel import Session
from pathlib import Path

from database import get_session
from models import Promise, PromiseUpdate, PromiseStatus, User
from controllers.auth_controller import require_admin

router = APIRouter(tags=["updates"])


@router.get("/promises/{id}/update", response_class=HTMLResponse)
async def update_promise_page(
    request: Request, 
    id: str, 
    session: Session = Depends(get_session),
    user: User = Depends(require_admin)
):
    """แสดงฟอร์มเพิ่มความคืบหน้า (Admin only)"""
    promise = session.get(Promise, id)
    if not promise:
        raise HTTPException(status_code=404, detail="Promise not found")
        
    if not promise.can_update():
        raise HTTPException(status_code=400, detail="Cannot update this promise (Status: Disappeared)")
        
    return templates.TemplateResponse("update_progress.html", {
        "request": request,
        "promise": promise,
    })


@router.post("/promises/{id}/update", response_class=HTMLResponse)
async def update_promise(
    request: Request, 
    id: str, 
    detail: str = Form(...),
    session: Session = Depends(get_session),
    user: User = Depends(require_admin)
):
    """บันทึกความคืบหน้า (Admin only)"""
    promise = session.get(Promise, id)
    if not promise:
        raise HTTPException(status_code=404, detail="Promise not found")
    
    if not promise.can_update():
        raise HTTPException(status_code=400, detail="Cannot update this promise (Status: Disappeared)")
        
    if not detail.strip():
        return templates.TemplateResponse("update_progress.html", {
            "request": request,
            "promise": promise,
            "error": "กรุณากรอกรายละเอียดความคืบหน้า"
        })
        
    # Generate ID for update
    # Simple ID generation: P{promise_id_suffix}-U{count+1}
    # Or just use uuid, but requirement says string. Let's try to follow a simple pattern or UUID.
    # The README example IDs are "P001", etc.
    # Let's generate a unique ID using timestamp or simple counter if possible.
    # Given the complexity, let's use a simple timestamp-based ID or just a random string.
    import uuid
    new_id = str(uuid.uuid4())[:20]

    update = PromiseUpdate(
        id=new_id,
        promise_id=id,
        update_date=date.today(),
        detail=detail
    )
    
    session.add(update)
    session.commit()
    
    return RedirectResponse(f"/promises/{id}", status_code=303)
