# app/schemas/org_schema.py
from pydantic import BaseModel, EmailStr

class OrgCreate(BaseModel):
    organization_name: str
    email: EmailStr
    password: str

class OrgOut(BaseModel):
    organization_name: str
    collection_name: str
    admin_id: str

class OrgUpdate(BaseModel):
    old_name: str
    new_name: str
