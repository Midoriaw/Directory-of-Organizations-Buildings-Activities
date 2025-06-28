import asyncio
from sqlalchemy import select
from src.database import AsyncSessionLocal
from src import models

async def seed():
    async with AsyncSessionLocal() as session:
        # Проверяем, есть ли уже здания в базе
        result = await session.execute(select(models.Building).limit(1))
        exists = result.scalar_one_or_none()
        if exists:
            print("Данные уже есть, сидирование пропущено")
            return

        # Добавляем данные, вручную вызывая commit
        building1 = models.Building(address="ул. Ленина, 1", latitude=55.7558, longitude=37.6173)
        building2 = models.Building(address="пр. Мира, 10", latitude=55.7600, longitude=37.6200)
        session.add_all([building1, building2])

        activity1 = models.Activity(name="Розничная торговля")
        activity2 = models.Activity(name="Магазины одежды", parent=activity1)
        activity3 = models.Activity(name="Онлайн-продажи", parent=activity1)
        session.add_all([activity1, activity2, activity3])

        org = models.Organization(name="Магазин Одежды", building=building1)
        org.activities = [activity1, activity2]
        session.add(org)

        phone1 = models.PhoneNumber(number="+7 123 456 78 90", organization=org)
        phone2 = models.PhoneNumber(number="+7 987 654 32 10", organization=org)
        session.add_all([phone1, phone2])

        await session.commit()
        print("Сидирование завершено успешно!")

if __name__ == "__main__":
    asyncio.run(seed())
