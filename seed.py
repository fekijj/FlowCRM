from backend.models import Base, engine, PC, get_session

Base.metadata.create_all(engine)

with get_session() as db:
    if db.query(PC).count() == 0:
        pcs = [
            PC(name="ПК #1", ip_address="192.168.0.10", mac_address="AA:BB:CC:DD:EE:01"),
            PC(name="ПК #2", ip_address="192.168.0.11", mac_address="AA:BB:CC:DD:EE:02"),
            PC(name="ПК #3", ip_address="192.168.0.12", mac_address="AA:BB:CC:DD:EE:03"),
        ]
        db.add_all(pcs)
        print("✅ Тестовые ПК добавлены")
    else:
        print("⚠️ ПК уже есть в базе")
