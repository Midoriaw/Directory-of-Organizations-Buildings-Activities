from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src import models, schemas
from sqlalchemy.orm import selectinload



#Получить все организации
async def get_all_organizations(db:AsyncSession):
    result = await db.execute(select(models.Organization).options(selectinload(models.Organization.activities), selectinload(models.Organization.phone_number),selectinload(models.Organization.building)))
    return result.scalars().unique().all()

#Получить все здания
async def get_all_buildings(db: AsyncSession):
    result = await db.execute(select(models.Building))
    return result.scalars().all()


#Получить все виды деятельности
async def get_all_activities(db: AsyncSession):
    result = await db.execute(select(models.Activity))
    return result.scalars().all()

#Создать организацию с номерами телефонов и активностями
async def create_organization(db: AsyncSession, org_data: schemas.OrganizationCreate):
    new_org = models.Organization(name=org_data.name, building_id=org_data.building_id)

    #привязываем активности
    if org_data.activity_ids:
        result = await db.execute(select(models.Activity).where(models.Activity.id.in_(org_data.activity_ids)))
        new_org.activities = result.scalars().all()

    db.add(new_org)
    await db.flush()

    #Добавляем телефоны
    for number in org_data.phone_numbers:
        db.add(models.PhoneNumber(number=number, organization=new_org))

    await db.commit()
    await db.refresh(new_org)
    return new_org

# Получить организации по ID здания
async def get_organizations_by_building(db: AsyncSession, building_id: int):
    result = await db.execute(select(models.Organization).where(models.Organization.building_id == building_id))
    return result.scalars().all()

# Получить организации по ID вида деятельности
async def get_organizations_by_activity(db: AsyncSession, activity_id: int):
    result = await db.execute(select(models.Organization).join(models.Organization.activities).where(models.Activity.id == activity_id))
    return result.scalars().all()

# По дереву деятельности
async def get_organizations_by_activity_tree(db: AsyncSession, activity_id: int):
    result = await db.execute(select(models.Organization).join(models.Organization.activities).where(models.Activity.id == activity_id))
    return result.scalars().all()

# Поиск по имени
async def get_organizations_by_name(db: AsyncSession, name: str):
    result = await db.execute(select(models.Organization).where(models.Organization.name.ilike(f"%{name}%")))
    return result.scalars().all()

# Поиск в радиусе
async def get_organizations_in_radius(db: AsyncSession, lat: float, lng:float, radius:float):
    result = await db.execute(select(models.Organization).join(models.Organization.building).where(
    (models.Building.latitude - lat)*(models.Building.latitude - lat) +
    (models.Building.longitude - lng)*(models.Building.longitude - lng) <= (radius*radius)))

    return  result.scalars().all()

# Получить организацию по ID
async def get_organizations_by_id(db: AsyncSession, org_id: int):
    result = await db.execute(select(models.Organization).where(models.Organization.id == org_id))
    return result.scalars().first()