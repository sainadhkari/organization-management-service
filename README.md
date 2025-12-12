# Backend Intern Assignment – Organization Management Service

## Objective

Build a backend service using a backend framework (preferably a Python framework like **FastAPI** or **Django**) that supports creating and managing organizations in a **multi-tenant** architecture using **MongoDB**.

The system must:

- Maintain a **Master Database** for global metadata.  
- Dynamically create **per-organization collections** in MongoDB (e.g. `org_<organization_name>`).  
- Expose REST APIs and an authentication flow for admin users.

***

## Functional Requirements

### 1. Create Organization

**Endpoint:** `POST /org/create`  

**Input:**

- `organization_name`  
- `email` (admin email)  
- `password` (admin password)  

**Expected Behavior:**

- Validate that the organization name does **not** already exist.  
- Dynamically create a new MongoDB collection for the organization (pattern: `org_<organization_name>`).  
- Create an admin user associated with this organization.  
- Store in the Master Database:
  - Organization name  
  - Organization collection name  
  - Connection details (if required)  
  - Admin user reference  
- Return a success response with basic organization metadata.

***

### 2. Get Organization by Name

**Endpoint:** `GET /org/get`  

**Input:**

- `organization_name`  

**Expected Behavior:**

- Fetch and return organization details stored in the Master Database.  
- If the organization does not exist, return an appropriate error.

***

### 3. Update Organization

**Endpoint:** `PUT /org/update`  

**Input:**

- `organization_name`  
- `email` (admin email)  
- `password` (admin password)  

**Expected Behavior:**

- Validate that the **new** organization name does not already exist.  
- Handle creation/rename of the new collection for the organization and **sync existing data** to the new collection.  
- Update the Master Database with the new metadata.

***

### 4. Delete Organization

**Endpoint:** `DELETE /org/delete`  

**Input:**

- `organization_name`  

**Expected Behavior:**

- Allow deletion **only** for the respective authenticated admin user.  
- Delete the relevant MongoDB collection(s) for this organization.  
- Remove organization metadata from the Master Database.

***

### 5. Admin Login

**Endpoint:** `POST /admin/login`  

**Input:**

- `email`  
- `password`  

**Expected Behavior:**

- Validate admin credentials.  
- On success, return a **JWT** token containing:
  - Admin identification  
  - Organization identifier / ID  
- On failure, return an unauthorized error.

***

## Technical Requirements

### A. Master Database

The Master Database should store:

- Organization metadata  
- Connection details for each dynamic database / collection  
- Admin user credentials (passwords stored securely hashed)

### B. Dynamic Collection Creation

When an organization is created:

- Programmatically create a new MongoDB collection dedicated to that organization.  
- The collection may be:
  - Initially empty, or  
  - Initialized with a basic schema / seed data (optional but good to have).

### C. Authentication

- Implement admin login using **JWT**.  
- Passwords **must be hashed** (e.g. using `bcrypt`).

***

## Project Design & Trade-offs

This architecture is designed to be **multi-tenant** and reasonably scalable:

- **Pros:**
  - Clear separation of data between organizations via per-org collections.  
  - Flexible schema using MongoDB.  

- **Trade-offs:**
  - Many collections can increase operational complexity (indexing, backups, migrations).  
  - MongoDB + per-org collections vs. single-collection-with-`org_id` is a design choice:
    - Per-org collections: better isolation, simpler queries per tenant.  
    - Single shared collection: easier global analytics, fewer collections, but needs strict filtering by `org_id`.

Alternative designs might use:

- A relational DB with a shared schema and `org_id` on each row.  
- Separate databases per tenant instead of collections.  

These come with different scaling, cost, and operational trade-offs depending on expected tenant count and data volume.

***

## How to Run the Application

1. **Clone the repository**

```bash
git clone https://github.com/sainadhkari/organization-management-service.git
cd organization-management-service
```

2. **Set up environment variables**

Copy example file and edit:

```bash
cp .env.example .env
```

Configure MongoDB, JWT secret, etc.

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Run the server (FastAPI example)**

```bash
uvicorn app.main:app --reload
```

5. **Explore API docs**

- Swagger UI: `http://127.0.0.1:8000/docs`  
- ReDoc: `http://127.0.0.1:8000/redoc`

***

## Deliverables (as per assignment)

- GitHub repository link.  
- Modular and clean design (preferably class-based).  
- Clear instructions to run the application in `README.md`.  
- A **high-level diagram** of the project architecture (included as `diagram.png.png` in this repo).  
- Brief notes explaining design choices and trade-offs (this README section).


