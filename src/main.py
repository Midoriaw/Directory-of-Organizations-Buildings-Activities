from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request
from src.database import get_db
from src import schemas, crud
from src.database import lifespan


app = FastAPI(lifespan=lifespan)

API_KEY = "supersecretkey"

@app.middleware("http")
async def check_api_key(request: Request, call_next):
    # Пути, для которых не нужен ключ (они обязательны для работы /docs)
    if request.url.path in ["/docs", "/redoc", "/openapi.json", "/favicon.ico"]:
        return await call_next(request)

    if request.headers.get("X-API-Key") != API_KEY:
        return JSONResponse(status_code=403, content={"detail": "Forbidden"})
    return await call_next(request)


# Главная
@app.get("/")
async def root():
    return {"mess": "API работает!"}

# Получить все организации
@app.get("/organizations", response_model=list[schemas.OrganizationOut])
async def get_organizations(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_organizations(db)

#Получить все здания
@app.get("/buildings", response_model=list[schemas.BuildingOut])
async def get_buildings(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_buildings(db)


# Получить все виды деятельности
@app.get("/activities", response_model=list[schemas.ActivityOut])
async def get_activities(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_activities(db)


# Добавить организацию
@app.post("/organizations", response_model=schemas.OrganizationOut)
async def create_organization(org: schemas.OrganizationCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_organization(db, org)



@app.get("/organizations/building/{building_id}", response_model=list[schemas.OrganizationOut])
async def by_building(building_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_organizations_by_building(db, building_id)

@app.get("/organizations/by_activity/{activity_id}", response_model=list[schemas.OrganizationOut])
async def by_activity(activity_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_organizations_by_activity(db,activity_id)

@app.get("/organizations/by_activity_tree/{activity_id}", response_model=list[schemas.OrganizationOut])
async def by_activity_tree(activity_id: int,db: AsyncSession = Depends(get_db)):
    return await crud.get_organizations_by_activity_tree(db,activity_id )


@app.get("/organizations/search",response_model=list[schemas.OrganizationOut])
async def search(name:str,db: AsyncSession = Depends(get_db)):
    return await crud.get_organizations_by_name(db ,name)


@app.get("/organizations/by_radius", response_model=list[schemas.OrganizationOut])
async def by_radius(lat: float, lng:float, radius:float, db: AsyncSession = Depends(get_db)):
    return await crud.get_organizations_in_radius(db, lat, lng, radius)


@app.get("/organizations/{org_id}", response_model=schemas.OrganizationOut)
async def get_by_id(org_id: int, db: AsyncSession = Depends(get_db)):
    org = await crud.get_organizations_by_id(db,org_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return org