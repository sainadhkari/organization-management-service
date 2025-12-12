# app/org/org_repository.py
from app.database.mongo import master_db
from bson.objectid import ObjectId

class OrgRepository:
    def __init__(self, db=master_db):
        self.db = db
        self.org_coll = self.db["organizations"]
        self.admins = self.db["admins"]

    def find_org_by_name(self, name: str):
        return self.org_coll.find_one({"organization_name": {"$regex": f"^{name}$", "$options": "i"}})

    def create_org(self, org_name: str, collection_name: str, admin_id: str):
        res = self.org_coll.insert_one({
            "organization_name": org_name,
            "collection_name": collection_name,
            "admin_id": admin_id,
            "created_at": __import__("datetime").datetime.utcnow()
        })
        return str(res.inserted_id)

    def create_admin(self, email: str, password_hash: str, org_id: str):
        res = self.admins.insert_one({
            "email": email,
            "password_hash": password_hash,
            "org_id": org_id,
            "created_at": __import__("datetime").datetime.utcnow()
        })
        return str(res.inserted_id)

    def get_admin_by_email(self, email: str):
        return self.admins.find_one({"email": email})

    def update_org_collection(self, org_id: str, new_collection: str):
        return self.org_coll.update_one({"_id": ObjectId(org_id)}, {"$set": {"collection_name": new_collection}})

    def delete_org(self, org_name: str):
        org = self.find_org_by_name(org_name)
        if not org:
            return False
        # drop collection
        coll_name = org.get("collection_name")
        if coll_name:
            self.db.drop_collection(coll_name)
        # delete admins linked to org
        self.admins.delete_many({"org_id": str(org.get("_id"))})
        # delete org record
        self.org_coll.delete_one({"_id": org.get("_id")})
        return True

    def migrate_collection(self, old_name: str, new_name: str):
        old_coll = self.db[old_name]
        new_coll = self.db[new_name]
        cursor = old_coll.find({})
        docs = []
        for d in cursor:
            d.pop("_id", None)
            docs.append(d)
        if docs:
            new_coll.insert_many(docs)
        return True
