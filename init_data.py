import sys
import os
from datetime import date
from sqlmodel import Session, select

# Ensure app modules can be imported
sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), "app"))

from database import engine, create_db_and_tables
from models import Politician, Campaign, Promise, PromiseStatus, User, UserRole

def init_data():
    create_db_and_tables()
    
    with Session(engine) as session:
        # Check if data already exists to avoid duplicates
        if session.exec(select(Politician)).first():
            print("Data already initialized. Skipping.")
            return

        print("Initializing data...")

        #1. Users
        user1 = User(username="admin", password="admin123", role=UserRole.ADMIN)
        user2 = User(username="user1", password="user123", role=UserRole.USER)
        session.add(user1)
        session.add(user2)

        # 2. Politicians
        pol1 = Politician(id="10000001", name="สมชาย ใจดี", party="พรรคอนาคตสดใส")
        pol2 = Politician(id="20000002", name="สมหญิง รักไทย", party="พรรคประชาชนก้าวหน้า")
        pol3 = Politician(id="30000003", name="วิชัย มั่นคง", party="พรรคพลังแผ่นดิน")
        pol4 = Politician(id="40000004", name="นภา สว่างฟ้า", party="พรรคอนาคตสดใส")
        pol5 = Politician(id="50000005", name="ธนกร เศรษฐี", party="พรรคเศรษฐกิจมั่นคง")
        
        session.add(pol1)
        session.add(pol2)
        session.add(pol3)
        session.add(pol4)
        session.add(pol5)

        # 3. Campaigns
        camp1 = Campaign(id="C2566", year=2566, district="ทั่วประเทศ")
        session.add(camp1)

        # 4. Promises
        promises = [
            Promise(id="P001", politician_id="10000001", campaign_id="C2566", description="ค่าแรงขั้นต่ำ 600 บาท", announced_date=date(2023, 1, 1), status=PromiseStatus.IN_PROGRESS),
            Promise(id="P002", politician_id="10000001", campaign_id="C2566", description="รถไฟฟ้า 20 บาทตลอดสาย", announced_date=date(2023, 1, 15), status=PromiseStatus.DISAPPEARED),
            Promise(id="P003", politician_id="20000002", campaign_id="C2566", description="เรียนฟรีถึงปริญญาตรี", announced_date=date(2023, 2, 1), status=PromiseStatus.NOT_STARTED),
            Promise(id="P004", politician_id="20000002", campaign_id="C2566", description="Wi-Fi ฟรีทั่วประเทศ", announced_date=date(2023, 2, 10), status=PromiseStatus.DISAPPEARED),
            Promise(id="P005", politician_id="30000003", campaign_id="C2566", description="ลดภาษีรถยนต์ 50%", announced_date=date(2023, 2, 20), status=PromiseStatus.IN_PROGRESS),
            Promise(id="P006", politician_id="30000003", campaign_id="C2566", description="สร้างสนามกีฬาทุกตำบล", announced_date=date(2023, 3, 1), status=PromiseStatus.NOT_STARTED),
            Promise(id="P007", politician_id="40000004", campaign_id="C2566", description="พลังงานแสงอาทิตย์ฟรีทุกหลังคา", announced_date=date(2023, 3, 10), status=PromiseStatus.IN_PROGRESS),
            Promise(id="P008", politician_id="40000004", campaign_id="C2566", description="ลดค่าไฟ 50%", announced_date=date(2023, 3, 15), status=PromiseStatus.NOT_STARTED),
            Promise(id="P009", politician_id="50000005", campaign_id="C2566", description="แจกเงินดิจิทัล 10,000 บาท", announced_date=date(2023, 4, 1), status=PromiseStatus.DISAPPEARED),
            Promise(id="P010", politician_id="50000005", campaign_id="C2566", description="สร้างรถไฟความเร็วสูง", announced_date=date(2023, 4, 10), status=PromiseStatus.IN_PROGRESS),
        ]

        for p in promises:
            session.add(p)

        session.commit()
        print("Data initialized successfully!")

if __name__ == "__main__":
    init_data()
