# seed.py
from backend.models import SessionLocal, Base, engine, PC

Base.metadata.create_all(engine)
db = SessionLocal()

pcs = [
    PC(name="ПК #1", ip_address="192.168.0.10", mac_address="AA:BB:CC:DD:EE:01"),
    PC(name="ПК #2", ip_address="192.168.0.11", mac_address="AA:BB:CC:DD:EE:02"),
    PC(name="ПК #3", ip_address="192.168.0.12", mac_address="AA:BB:CC:DD:EE:03"),
]

db.add_all(pcs)
db.commit()
print("Тестовые ПК добавлены ✅")
