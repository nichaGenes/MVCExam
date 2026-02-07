# ระบบติดตามคำสัญญานักการเมือง (MVC Promise Tracker)

ระบบบันทึกและติดตามคำสัญญาของนักการเมืองในช่วงหาเสียงเลือกตั้ง พัฒนาด้วย **Generic MVC Architecture** ที่แยกส่วนการทำงานชัดเจน ง่ายต่อการดูแลรักษาและขยายต่อ

---

## A. โครงสร้าง MVC และการทำงานร่วมกัน

ระบบแบ่งไฟล์ตามหน้าที่ในรูปแบบ Model-View-Controller ดังนี้:

### 1. Model (ข้อมูลและลอจิก)
*หน้าที่:* จัดการโครงสร้างข้อมูล กฎทางธุรกิจ (Business Rules) และการติดต่อฐานข้อมูล

อยู่ภายใต้โฟลเดอร์ `app/models/`:
- **`politician.py`**: กำหนดโครงสร้างข้อมูลนักการเมือง (ID, ชื่อ, พรรค)
- **`promise.py`**: กำหนดโครงสร้างคำสัญญาและจัดการสถานะ (ยังไม่เริ่ม, กำลังดำเนินการ, เงียบหาย)
- **`campaign.py`**: ข้อมูลแคมเปญการหาเสียง
- **`user.py`**: ข้อมูลผู้ใช้และระบบ Authentication

*การทำงานร่วมกัน:* Model ถูกเรียกใช้โดย **Controller** เพื่อดึงหรือบันทึกข้อมูลลงฐานข้อมูล (PostgreSQL ผ่าน SQLModel)

### 2. View (การแสดงผล)
*หน้าที่:* รับข้อมูลจาก Controller และนำมาแสดงผลเป็น HTML ให้ผู้ใช้เห็น

อยู่ภายใต้โฟลเดอร์ `app/views/`:
- **`layout.html`**: แม่แบบหลักของทุกหน้า (Base Template)
- **`all_promises.html`**: แสดงรายการคำสัญญาทั้งหมด
- **`promise_detail.html`**: แสดงรายละเอียดและไทม์ไลน์ความคืบหน้า
- **`politician.html`**: หน้าโปรไฟล์นักการเมืองและคำสัญญาของเขา
- **`update_progress.html`**: แบบฟอร์มสำหรับ Admin กรอกอัปเดตงาน

*การทำงานร่วมกัน:* View รับข้อมูล (Variables) ที่ส่งมาจาก **Controller** แล้วนำไปเรนเดอร์ผ่าน Jinja2 Template Engine

### 3. Controller (ตัวกลางควบคุม)
*หน้าที่:* รับคำสั่งจากผู้ใช้ (Request), ประมวลผล, เรียกใช้ Model, และส่งผลลัพธ์ไปที่ View

อยู่ภายใต้โฟลเดอร์ `app/controllers/`:
- **`promise_controller.py`**:
    - ดึงรายการคำสัญญาทั้งหมดจาก Model → ส่งไปที่ `all_promises.html`
    - ดึงรายละเอียดคำสัญญา → ส่งไปที่ `promise_detail.html`
- **`politician_controller.py`**:
    - ดึงข้อมูลนักการเมืองและคำสัญญาที่เกี่ยวข้อง → ส่งไปที่ `politician.html`
- **`update_controller.py`**:
    - ตรวจสอบสิทธิ์ Admin
    - รับข้อมูลจากฟอร์ม → บันทึกลง Model (PromiseUpdate) → Redirect กลับไปหน้ารายละเอียด
- **`auth_controller.py`**: จัดการการเข้าสู่ระบบ (Login/Logout)

---

## B. สรุป Routes/Actions หลัก

| หน้าที่ | URL Path | HTTP Method | Controller Action | View ที่เกี่ยวข้อง |
| :--- | :--- | :--- | :--- | :--- |
| **หน้าแรก** | `/` | GET | Redirect ไป `/promises` | - |
| **แสดงคำสัญญาทั้งหมด** | `/promises` | GET | `list_promises` | `all_promises.html` |
| **ดูรายละเอียดคำสัญญา** | `/promises/{id}` | GET | `get_promise_detail` | `promise_detail.html` |
| **ดูโปรไฟล์นักการเมือง** | `/politicians/{id}` | GET | `get_politician_detail` | `politician.html` |
| **แสดงฟอร์มอัปเดต** (Admin) | `/promises/{id}/update` | GET | `update_promise_page` | `update_progress.html` |
| **บันทึกการอัปเดต** (Admin) | `/promises/{id}/update` | POST | `update_promise` | - (Redirect) |
| **เข้าสู่ระบบ** | `/login` | GET/POST | `login` | `login.html` |
| **ออกจากระบบ** | `/logout` | GET | `logout` | - (Redirect) |

---

## วิธีการใช้งาน (Installation & Run)

1.  **ติดตั้ง Dependencies**:
    ```bash
    # ทางเลือกที่ 1: ใช้ uv (แนะนำ)
    uv sync
    
    # ทางเลือกที่ 2: ใช้ pip
    pip install -r requirements.txt
    ```

2.  **เริ่มระบบฐานข้อมูล**:
    ```bash
    docker compose up -d
    ```

3.  **เตรียมข้อมูลตัวอย่าง (Initialize Data)**:
    ```bash
    # รันสคริปต์เพื่อเพิ่มข้อมูลจำลอง
    uv run python init_data.py
    ```

4.  **เริ่มเซิร์ฟเวอร์**:
    ```bash
    uv run fastapi dev
    ```
    *เข้าใช้งานได้ที่: http://127.0.0.1:8000*

---

### บัญชีทดสอบ (User Accounts)
- **Admin** (แก้ไขได้): `username: admin`, `password: admin123`
- **User** (ดูได้อย่างเดียว): `username: user1`, `password: user123`
