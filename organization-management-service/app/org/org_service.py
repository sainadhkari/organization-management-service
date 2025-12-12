# app/org/org_service.py
from app.org.org_repository import OrgRepository
from app.auth.auth_service import AuthService

class OrgService:
    def __init__(self, repo: OrgRepository = None):
        self.repo = repo or OrgRepository()
        self.auth = AuthService()

    def create_organization(self, organization_name: str, email: str, password: str):
        existing = self.repo.find_org_by_name(organization_name)
        if existing:
            return None
        # sanitize
        sanitized = organization_name.strip().lower().replace(" ", "_")
        collection_name = f"org_{sanitized}"
        # create admin (org_id temporarily blank, we update if needed)
        pwd_hash = self.auth.hash_password(password)
        admin_id = self.repo.create_admin(email, pwd_hash, "")
        # create org metadata
        org_id = self.repo.create_org(organization_name, collection_name, admin_id)
        # update admin with org_id
        self.repo.admins.update_one({"_id": __import__("bson").objectid.ObjectId(admin_id)}, {"$set": {"org_id": org_id}})
        # touch collection (create)
        self.repo.db[collection_name].insert_one({"_init": True})
        self.repo.db[collection_name].delete_one({"_init": True})
        return {"organization_name": organization_name, "collection_name": collection_name, "admin_id": admin_id, "org_id": org_id}

    def get_organization(self, organization_name: str):
        return self.repo.find_org_by_name(organization_name)

    def update_organization(self, old_name: str, new_name: str):
        existing_new = self.repo.find_org_by_name(new_name)
        if existing_new:
            return None
        org = self.repo.find_org_by_name(old_name)
        if not org:
            return None
        new_sanitized = new_name.strip().lower().replace(" ", "_")
        new_collection = f"org_{new_sanitized}"
        # migrate data
        self.repo.migrate_collection(org["collection_name"], new_collection)
        # update metadata
        self.repo.update_org_collection(str(org.get("_id")), new_collection)
        self.repo.org_coll.update_one({"_id": org.get("_id")}, {"$set": {"organization_name": new_name}})
        return {"updated_to": new_name, "new_collection": new_collection}

    def delete_organization(self, organization_name: str):
        return self.repo.delete_org(organization_name)

    def admin_login(self, email: str, password: str):
        admin = self.repo.get_admin_by_email(email)
        if not admin:
            return None
        if not self.auth.verify_password(password, admin.get("password_hash")):
            return None
        return admin
