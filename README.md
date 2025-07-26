# ParkSense AI

## Table of Contents

- [Project Structure](#project-structure)
- [System Diagrams](#system-diagrams)
- [Backend](#backend-fastapi--mongodb)
- [Frontend](#frontend-nextjs--shadcn-ui)
- [Development Notes](#development-notes)
- [API Endpoints](#api-endpoints)

A full-stack solution for smart parking management, featuring a FastAPI backend (with MongoDB) and a modern Next.js frontend.

---

## Project Structure

```
.
├── app/                   # FastAPI backend (Python)
├── parksense-frontend/    # Next.js frontend (TypeScript)
├── requirements.txt       # Backend dependencies
├── .env                   # Backend environment variables (not committed)
└── README.md
```

---

## System Diagrams

### 1. System Architecture

```mermaid
graph TD
    A[User Browser] --> B[Next.js Frontend]
    B --> C[FastAPI Backend]
    C --> D[MongoDB]
    C --> B
    B --> E[ShadCN UI / Tailwind CSS]
    
    %% Styling
    A --> |HTTP JWT Auth| B
    B --> |REST API| C
    C --> |Async Driver| D
```

### 2. Database Entity-Relationship Diagram (ERD)

```mermaid
erDiagram
    USERS {
        string _id PK
        string username
        string email
        string password_hash
        string[] roles
        bool is_deleted
    }
    VEHICLES {
        string _id PK
        string license_plate
        string make
        string model
        string color
        bool is_deleted
    }
    ZONES {
        string _id PK
        string name
        string description
        bool is_deleted
    }
    PARKING_SPACES {
        string _id PK
        string zone_id FK
        string label
        bool is_occupied
        bool is_deleted
    }
    CAMERAS {
        string _id PK
        string zone_id FK
        string location
        bool is_deleted
    }
    VIOLATIONS {
        string _id PK
        string vehicle_id FK
        string parking_space_id FK
        string violation_type
        string timestamp
        bool is_deleted
    }
    
    ZONES ||--o{ PARKING_SPACES : contains
    ZONES ||--o{ CAMERAS : monitored_by
    VEHICLES ||--o{ VIOLATIONS : involved_in
    PARKING_SPACES ||--o{ VIOLATIONS : location_of
```

### 3. API Flow Diagram

```mermaid
sequenceDiagram
    participant U as User Browser
    participant F as Next.js Frontend
    participant A as FastAPI Backend
    participant M as MongoDB

    U->>F: Login/Register form
    F->>A: POST /auth/login or /auth/register
    A->>M: Query/Insert user
    M-->>A: User data
    A-->>F: JWT Token / Error
    F-->>U: Store token, show dashboard

    U->>F: CRUD action (Add Vehicle)
    F->>A: API Request with JWT
    A->>M: DB Operation
    M-->>A: Result
    A-->>F: Response success/error
    F-->>U: Update UI
```

---

## Backend (FastAPI + MongoDB)

### Features
- User authentication & registration (JWT, hashed passwords, role-based access)
- CRUD APIs for users, cameras, zones, parking spaces, vehicles, violations
- Filtering, pagination, sorting, bulk operations, soft delete
- MongoDB Atlas/cloud/local support

### Setup

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```
   MONGO_URI=your_mongodb_uri
   MONGO_DB=parksense
   SECRET_KEY=your_secret_key
   ```

3. **Run MongoDB**
   - Use MongoDB Atlas or run locally and update `MONGO_URI` accordingly.

4. **Start the FastAPI server**
   ```bash
   uvicorn app.main:app --reload
   ```

5. **Test the health endpoint**
   - Visit [http://localhost:8000/health](http://localhost:8000/health)

---

## Frontend (Next.js + ShadCN UI)

### Features
- Modern UI with ShadCN components and Tailwind CSS
- JWT login/logout, AuthContext, admin detection
- Protected dashboard and navigation
- CRUD pages for all entities (users, vehicles, zones, cameras, parking spaces, violations)
- Role-based UI (admin/user), error/loading states

### Setup

1. **Install dependencies**
   ```bash
   cd parksense-frontend
   npm install
   ```

2. **Run the development server**
   ```bash
   npm run dev
   ```

3. **Open [http://localhost:3000](http://localhost:3000) in your browser**

---

## Development Notes

- **.env** and other secrets are not committed. See setup above.
- Both backend and frontend are fully functional and ready for integration.
- CORS is enabled for local development.
- For deployment, see Next.js and FastAPI deployment guides.

---

## API Endpoints

<details>
<summary>Click to expand endpoints</summary>

### Authentication
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `GET /auth/me` - Get current user info

### Users
- `GET /users` - List all users
- `POST /users` - Create new user
- `GET /users/{id}` - Get user by ID
- `PUT /users/{id}` - Update user
- `DELETE /users/{id}` - Delete user

### Vehicles
- `GET /vehicles` - List all vehicles
- `POST /vehicles` - Create new vehicle
- `GET /vehicles/{id}` - Get vehicle by ID
- `PUT /vehicles/{id}` - Update vehicle
- `DELETE /vehicles/{id}` - Delete vehicle

### Zones
- `GET /zones` - List all zones
- `POST /zones` - Create new zone
- `GET /zones/{id}` - Get zone by ID
- `PUT /zones/{id}` - Update zone
- `DELETE /zones/{id}` - Delete zone

### Parking Spaces
- `GET /parking-spaces` - List all parking spaces
- `POST /parking-spaces` - Create new parking space
- `GET /parking-spaces/{id}` - Get parking space by ID
- `PUT /parking-spaces/{id}` - Update parking space
- `DELETE /parking-spaces/{id}` - Delete parking space

### Cameras
- `GET /cameras` - List all cameras
- `POST /cameras` - Create new camera
- `GET /cameras/{id}` - Get camera by ID
- `PUT /cameras/{id}` - Update camera
- `DELETE /cameras/{id}` - Delete camera

### Violations
- `GET /violations` - List all violations
- `POST /violations` - Create new violation
- `GET /violations/{id}` - Get violation by ID
- `PUT /violations/{id}` - Update violation
- `DELETE /violations/{id}` - Delete violation

</details>