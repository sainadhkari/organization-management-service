# app/org/org_controller.py
from fastapi import APIRouter, HTTPException, Depends
from app.schemas.org_schema import OrgCreate, OrgOut, OrgUpdate
from app.schemas.admin_schema import AdminLogin, TokenOut
from app.org.org_service import OrgService
from app.auth.auth_service import AuthService
from app.utils.jwt_handler import oauth2_scheme, get_current_admin

router = APIRouter()
service = OrgService()
auth = AuthService()

@router.post("/org/create", response_model=OrgOut)
def create_org(payload: OrgCreate):
    res = service.create_organization(payload.organization_name, payload.email, payload.password)
    if not res:
        raise HTTPException(status_code=400, detail="Organization already exists")
    return OrgOut(organization_name=res["organization_name"], collection_name=res["collection_name"], admin_id=res["admin_id"])

@router.get("/org/get")
def get_org(organization_name: str):
    org = service.get_organization(organization_name)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    org["org_id"] = str(org.get("_id"))
    return org

@router.put("/org/update")
def update_org(payload: OrgUpdate, token: str = Depends(oauth2_scheme)):
    admin = get_current_admin(token)
    if not admin:
        raise HTTPException(status_code=401, detail="Invalid token")
    res = service.update_organization(payload.old_name, payload.new_name)
    if not res:
        raise HTTPException(status_code=400, detail="Update failed or new name already exists")
    return res

@router.delete("/org/delete")
def delete_org(organization_name: str, token: str = Depends(oauth2_scheme)):
    admin = get_current_admin(token)
    if not admin:
        raise HTTPException(status_code=401, detail="Invalid token")
    ok = service.delete_organization(organization_name)
    if not ok:
        raise HTTPException(status_code=404, detail="Organization not found or delete failed")
    return {"success": True}

@router.post("/admin/login", response_model=TokenOut)
def admin_login(payload: AdminLogin):
    admin = service.admin_login(payload.email, payload.password)
    if not admin:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = auth.create_access_token({"admin_id": str(admin.get("_id")), "org_id": admin.get("org_id"), "email": admin.get("email")})
    return TokenOut(access_token=token)
