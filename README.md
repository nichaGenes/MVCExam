# ระบบติดตามคำสัญญานักการเมืองช่วงหาเสียงเลือกตั้ง

## Political Campaign Promise Tracker

ระบบบันทึกและติดตามคำสัญญาของนักการเมืองในช่วงหาเสียงเลือกตั้ง พัฒนาด้วยแนวคิด **MVC (Model-View-Controller)** โดยแยกความรับผิดชอบของแต่ละส่วนอย่างชัดเจน

> ⚠️ ระบบมีหน้าที่บันทึกคำสัญญา แต่ไม่รับประกันว่าจะมีการทำตามจริง

---

## Tech Stack

| Layer       | Technology                          |
| ----------- | ----------------------------------- |
| Backend     | Python + FastAPI                    |
| Template    | Jinja2 (Server-Side Rendering)     |
| Database    | JSON Files                          |
| Validation  | Pydantic v2                         |
| Auth        | Session-based (Starlette Middleware) |
| Frontend    | HTML + CSS                          |

---

## Project Structure

```
project/
├── main.py                          # FastAPI entry point + middleware
│
├── controllers/                     # Controller Layer
│   ├── auth_controller.py           #   - Login / Logout
│   ├── promise_controller.py        #   - คำสัญญา (ดูรวม / รายละเอียด)
│   ├── update_controller.py         #   - อัปเดตความคืบหน้า
│   └── politician_controller.py     #   - ข้อมูลนักการเมือง
│
├── models/                          # Model Layer
│   ├── politician.py                #   - Pydantic model + CRUD
│   ├── campaign.py                  #   - Pydantic model + CRUD
│   ├── promise.py                   #   - Pydantic model + CRUD + Business Rules
│   ├── promise_update.py            #   - Pydantic model + CRUD
│   └── user.py                      #   - Pydantic model + Authentication
│
├── views/                           # View Layer (Jinja2 Templates)
│   ├── layout.html                  #   - Base template
│   ├── login.html                   #   - หน้า Login
│   ├── all_promises.html            #   - หน้ารวมคำสัญญาทั้งหมด
│   ├── promise_detail.html          #   - หน้ารายละเอียดคำสัญญา
│   ├── update_progress.html         #   - หน้าอัปเดตความคืบหน้า
│   └── politician.html              #   - หน้านักการเมือง
│
├── data/                            # JSON Database
│   ├── politicians.json
│   ├── campaigns.json
│   ├── promises.json
│   ├── promise_updates.json
│   └── users.json
│
├── static/
│   └── style.css
│
└── requirements.txt
```

---

## Database Schema

### ER Diagram

```
┌──────────────────┐       ┌──────────────────────┐
│   Politicians     │       │     Campaigns         │
├──────────────────┤       ├──────────────────────┤
│ PK id (8 หลัก)    │──┐    │ PK id                │
│    name           │  │    │    year               │
│    party          │  │    │    district            │
└──────────────────┘  │    └──────────┬───────────┘
                      │               │
                      │    ┌──────────▼───────────┐
                      └───>│      Promises         │
                           ├──────────────────────┤
                           │ PK id                │
                           │ FK politician_id      │
                           │ FK campaign_id        │
                           │    description        │
                           │    announced_date     │
                           │    status             │
                           └──────────┬───────────┘
                                      │ 1:N
                           ┌──────────▼───────────┐
                           │   PromiseUpdates      │
                           ├──────────────────────┤
                           │ PK id                │
                           │ FK promise_id         │
                           │    update_date        │
                           │    detail             │
                           └──────────────────────┘

┌──────────────────┐
│      Users        │
├──────────────────┤
│ PK id             │
│    username        │
│    password        │
│    role            │
└──────────────────┘
```

### ตารางข้อมูล

#### Politicians (นักการเมือง)

| Field | Type   | Description                                |
| ----- | ------ | ------------------------------------------ |
| id    | string | รหัส 8 หลัก ตัวแรกไม่ขึ้นต้นด้วย 0 (เช่น `10000001`) |
| name  | string | ชื่อนักการเมือง                                 |
| party | string | พรรคการเมือง                                   |

#### Campaigns (การหาเสียง)

| Field    | Type   | Description  |
| -------- | ------ | ------------ |
| id       | string | รหัสการหาเสียง   |
| year     | int    | ปีการเลือกตั้ง    |
| district | string | เขตเลือกตั้ง     |

#### Promises (คำสัญญา)

| Field          | Type   | Description                                  |
| -------------- | ------ | -------------------------------------------- |
| id             | string | รหัสคำสัญญา                                      |
| politician_id  | string | FK → Politicians                             |
| campaign_id    | string | FK → Campaigns                               |
| description    | string | รายละเอียดคำสัญญา                                  |
| announced_date | date   | วันที่ประกาศ (YYYY-MM-DD)                        |
| status         | enum   | `ยังไม่เริ่ม` / `กำลังดำเนินการ` / `เงียบหาย` |

#### PromiseUpdates (ความคืบหน้า)

| Field       | Type   | Description           |
| ----------- | ------ | --------------------- |
| id          | string | รหัสการอัปเดต             |
| promise_id  | string | FK → Promises         |
| update_date | date   | วันที่อัปเดต (YYYY-MM-DD) |
| detail      | string | รายละเอียดความคืบหน้า        |

#### Users (ผู้ใช้งาน)

| Field    | Type   | Description          |
| -------- | ------ | -------------------- |
| id       | string | รหัสผู้ใช้                |
| username | string | ชื่อผู้ใช้                |
| password | string | รหัสผ่าน (plain text)  |
| role     | enum   | `admin` / `user`     |

---

## Routes

| Method | Path                       | View                | สิทธิ์    | Description              |
| ------ | -------------------------- | ------------------- | -------- | ------------------------ |
| GET    | `/login`                   | login.html          | ทุกคน     | หน้า Login                |
| POST   | `/login`                   | — (redirect)        | ทุกคน     | ตรวจสอบ username/password |
| GET    | `/logout`                  | — (redirect)        | ทุกคน     | ล้าง session              |
| GET    | `/promises`                | all_promises.html   | ทุกคน     | หน้ารวมคำสัญญาทั้งหมด         |
| GET    | `/promises/{id}`           | promise_detail.html | ทุกคน     | หน้ารายละเอียดคำสัญญา         |
| GET    | `/promises/{id}/update`    | update_progress.html| **admin** | ฟอร์มเพิ่มความคืบหน้า         |
| POST   | `/promises/{id}/update`    | — (redirect)        | **admin** | บันทึกความคืบหน้า            |
| GET    | `/politicians/{id}`        | politician.html     | ทุกคน     | คำสัญญาของนักการเมืองแต่ละคน   |

---

## Business Rules

| Rule                                           | จุดตรวจสอบ            |
| ---------------------------------------------- | -------------------- |
| รหัสนักการเมืองต้องเป็นเลข 8 หลัก ขึ้นต้นด้วย 1-9       | Model (Pydantic)     |
| สถานะคำสัญญาต้องเป็น 1 ใน 3 ค่าเท่านั้น              | Model (Enum)         |
| คำสัญญาที่สถานะ **"เงียบหาย"** ห้ามอัปเดตเพิ่มเติม     | Controller + Model   |
| คำสัญญา 1 รายการสามารถมีการอัปเดตได้หลายครั้ง         | Model (1:N relation) |
| เมื่ออัปเดตสำเร็จต้อง redirect กลับหน้ารายละเอียดคำสัญญา | Controller           |
| เฉพาะ admin เท่านั้นที่อัปเดตความคืบหน้าได้            | Controller (session) |

---

## MVC Separation

### Model — ข้อมูลและ Business Logic

- Pydantic models สำหรับ validation (ID format, enum status, date format)
- ฟังก์ชัน CRUD อ่าน/เขียน JSON files
- Business rule: ตรวจสอบสถานะก่อนอนุญาตให้อัปเดต

### View — การแสดงผล

แต่ละหน้าจอแยกเป็นไฟล์ Jinja2 template แยกกันอย่างชัดเจน

| View File              | หน้าที่                                    |
| ---------------------- | ----------------------------------------- |
| `login.html`           | ฟอร์ม login + แสดง error                    |
| `all_promises.html`    | แสดงคำสัญญาทั้งหมดเรียงตามวันที่ประกาศ            |
| `promise_detail.html`  | แสดงรายละเอียดคำสัญญา + ประวัติการอัปเดตทั้งหมด    |
| `update_progress.html` | ฟอร์มเพิ่มความคืบหน้าของคำสัญญา                 |
| `politician.html`      | แสดงข้อมูลนักการเมือง + คำสัญญาทั้งหมดของนักการเมือง |

### Controller — ตัวกลางระหว่าง Model กับ View

- รับ HTTP request จาก client
- เรียก Model เพื่อดึง/บันทึกข้อมูล
- ตรวจสอบสิทธิ์ (admin/user) ผ่าน session
- ส่งข้อมูลไปแสดงผลที่ View หรือ redirect

---

## Authentication

ระบบ login แบบง่ายผ่าน session:

| Role    | สิทธิ์                                  |
| ------- | -------------------------------------- |
| `user`  | ดูคำสัญญาทั้งหมด, ดูรายละเอียด, ดูนักการเมือง |
| `admin` | ทุกอย่างของ user + อัปเดตความคืบหน้าคำสัญญา  |

ใช้ `SessionMiddleware` ของ Starlette เก็บ `user_id` และ `role` ไว้ใน session cookie

---

## Sample Data

### นักการเมือง (5 คน)

| ID       | ชื่อ          | พรรค              |
| -------- | ------------ | ----------------- |
| 10000001 | สมชาย ใจดี      | พรรคอนาคตสดใส        |
| 20000002 | สมหญิง รักไทย    | พรรคประชาชนก้าวหน้า    |
| 30000003 | วิชัย มั่นคง      | พรรคพลังแผ่นดิน       |
| 40000004 | นภา สว่างฟ้า     | พรรคอนาคตสดใส        |
| 50000005 | ธนกร เศรษฐี     | พรรคเศรษฐกิจมั่นคง     |

### คำสัญญา (10 รายการ — ครบทุกสถานะ)

| รหัส | นักการเมือง   | คำสัญญา                  | สถานะ        |
| ---- | ----------- | ----------------------- | ------------ |
| P001 | สมชาย ใจดี    | ค่าแรงขั้นต่ำ 600 บาท        | กำลังดำเนินการ   |
| P002 | สมชาย ใจดี    | รถไฟฟ้า 20 บาทตลอดสาย     | เงียบหาย       |
| P003 | สมหญิง รักไทย  | เรียนฟรีถึงปริญญาตรี         | ยังไม่เริ่ม       |
| P004 | สมหญิง รักไทย  | Wi-Fi ฟรีทั่วประเทศ         | เงียบหาย       |
| P005 | วิชัย มั่นคง    | ลดภาษีรถยนต์ 50%          | กำลังดำเนินการ   |
| P006 | วิชัย มั่นคง    | สร้างสนามกีฬาทุกตำบล        | ยังไม่เริ่ม       |
| P007 | นภา สว่างฟ้า   | พลังงานแสงอาทิตย์ฟรีทุกหลังคา | กำลังดำเนินการ   |
| P008 | นภา สว่างฟ้า   | ลดค่าไฟ 50%             | ยังไม่เริ่ม       |
| P009 | ธนกร เศรษฐี   | แจกเงินดิจิทัล 10,000 บาท   | เงียบหาย       |
| P010 | ธนกร เศรษฐี   | สร้างรถไฟความเร็วสูง         | กำลังดำเนินการ   |

---

## Installation & Run

```bash
# 1. Clone project
git clone <repository-url>
cd project

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run server
uvicorn main:app --reload --port 8000

# 4. Open browser
# http://localhost:8000/login
```

### requirements.txt

```
fastapi
uvicorn[standard]
jinja2
python-multipart
itsdangerous
```

---

## User Accounts (สำหรับทดสอบ)

| Username | Password  | Role  |
| -------- | --------- | ----- |
| admin    | admin123  | admin |
| user1    | user123   | user  |
