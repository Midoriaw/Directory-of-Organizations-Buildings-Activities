from pydantic import BaseModel, Field
from typing import List, Optional


class ActivityBase(BaseModel):
    name: str
    parent_id: Optional[int] = None


class ActivityCreate(ActivityBase):
    pass


class ActivityOut(ActivityBase):
    id: int

    class Config:
        from_attributes = True



class BuildingBase(BaseModel):
    address: str
    latitude: float
    longitude: float



class BuildingCreate(BuildingBase):
    pass


class BuildingOut(BuildingBase):
    id: int

    class Config:
        orm_mode = True



class PhoneNumberOut(BaseModel):
    id: int
    number: str

    class Config:
        from_attributes = True



class OrganizationBase(BaseModel):
    name: str
    building_id: int
    activity_ids: List[int] = Field(default_factory=list)
    phone_numbers: List[str] = Field(default_factory=list)


class OrganizationCreate(OrganizationBase):
    pass


class OrganizationOut(BaseModel):
    id: int
    name: str
    building: BuildingOut
    activities: List[ActivityOut]
    phone_numbers: List[PhoneNumberOut]

    class Config:
        from_attributes = True

