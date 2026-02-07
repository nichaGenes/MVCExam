from pathlib import Path
from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from templating import templates
from sqlmodel import Session, select

from database import get_session
from models import User

router = APIRouter(tags=["auth"])


# ============================================
# Dependency: ดึง current user จาก session
# ============================================

def get_current_user(request: Request, session: Session = Depends(get_session)) -> User | None:
    """ดึงข้อมูล user จาก session ถ้า login อยู่"""
    user_id = request.session.get("user_id")
    if user_id is None:
        return None
    return session.get(User, user_id)


def require_admin(request: Request, session: Session = Depends(get_session)) -> User:
    """Dependency สำหรับ route ที่ต้องการสิทธิ์ admin"""
    user = get_current_user(request, session)
    if user is None or not user.is_admin():
        raise HTTPException(status_code=403, detail="ต้องเข้าสู่ระบบในฐานะผู้ดูแลระบบ")
    return user


# ============================================
# Routes
# ============================================

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """แสดงหน้า Login"""
    # ถ้า login อยู่แล้ว redirect ไปหน้าหลัก
    if request.session.get("user_id"):
        return RedirectResponse("/promises", status_code=303)

    return templates.TemplateResponse("login.html", {
        "request": request,
        "error": None,
    })


@router.post("/login", response_class=HTMLResponse)
async def login(request: Request, session: Session = Depends(get_session)):
    """ตรวจสอบ username/password แล้วสร้าง session"""
    form = await request.form()
    username = form.get("username", "").strip()
    password = form.get("password", "").strip()

    # Validate input
    if not username or not password:
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "กรุณากรอกชื่อผู้ใช้และรหัสผ่าน",
        })

    # ค้นหา user ใน database
    statement = select(User).where(User.username == username)
    user = session.exec(statement).first()

    # ตรวจสอบ password (plain text ตาม requirement ไม่ต้องคำนึงถึงความปลอดภัย)
    if user is None or user.password != password:
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง",
        })

    # สร้าง session
    request.session["user_id"] = user.id
    request.session["username"] = user.username
    request.session["role"] = user.role.value

    return RedirectResponse("/promises", status_code=303)


@router.get("/logout")
async def logout(request: Request):
    """ล้าง session แล้ว redirect กลับหน้า login"""
    request.session.clear()
    return RedirectResponse("/login", status_code=303)