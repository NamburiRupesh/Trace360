# Trace360 🌐

> **Digital Product Passport (DPP) & Lifecycle Traceability System**

Trace360 is a web-based Digital Product Passport and product lifecycle management platform built with Python, Flask, and MySQL. It enables end-to-end transparency across physical products by maintaining an immutable record of manufacturing metadata, warranty/ownership, and service/maintenance history.

---

## 🌟 Key Features

- **🔍 Public Product Verification**:
  - Anyone can enter a unique Product ID (`TRC-YYYY-XXXXXXXX`) on the home page to inspect product authenticity, manufacturer info, manufacturing date, batch number, and complete service history.

- **🏭 Manufacturer Portal**:
  - Secure registration and login for manufacturers.
  - Register new products with unique serialized passports, models, and batch tracking.
  - Automated unique product identification (`TRC-<YEAR>-<UUID>`).

- **🔧 Service Center Portal**:
  - Authorized service center registration and login.
  - Product lookup prior to repairs/maintenance.
  - Log diagnostic results, problems reported, actions taken, remarks, servicing dates, and repair costs.
  - Update and maintain historical service logs.

- **🛡️ Role-Based Access Control (RBAC)**:
  - Dedicated role schemas supporting `ADMIN`, `MANUFACTURER`, `SUPPLIER`, `SERVICE_CENTER`, and `CUSTOMER`.
  - Session-based authorization guards preventing cross-role access.
  - Password hashing powered by `werkzeug.security`.

---

## 🛠️ Tech Stack

- **Backend**: Python 3, Flask (Modular Blueprints)
- **Database**: MySQL (using `mysql-connector-python`)
- **Security**: Werkzeug (`generate_password_hash`, `check_password_hash`)
- **Frontend**: Jinja2 Templates, Semantic HTML5, Custom CSS

---

## 📁 Project Structure

```
Trace360/
├── app.py                      # Application entry point & blueprint registration
├── database.py                 # MySQL database connection helper
├── trace360.sql                # Complete SQL database schema & initial seed data
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git ignore rules for Python, cache, and IDEs
├── routes/
│   ├── auth_routes.py          # Authentication (login & registration)
│   ├── manufacturer_routes.py  # Manufacturer dashboard & product creation
│   ├── public_routes.py        # Landing page & public product verification
│   └── service_routes.py       # Service center dashboard & maintenance logs
├── templates/                  # Jinja2 HTML views
│   ├── base.html               # Base layout shell
│   ├── index.html              # Landing page with product lookup
│   ├── product.html            # Public product passport & service history
│   ├── login.html              # Multi-role authentication page
│   ├── manufacturer_dashboard.html
│   ├── create_product.html     # Product registration form
│   ├── product_created.html    # Success confirmation with Product ID
│   ├── service_dashboard.html  # Service center control center
│   ├── add_service.html        # Maintenance / repair entry form
│   ├── update_service.html     # Service record editor
│   ├── service_records.html    # Historical service logs view
│   ├── service_search_product.html
│   ├── register_manufacturer.html
│   └── register_service_center.html
└── static/
    └── css/
        └── style.css           # Custom styling for portals and cards
```

---

## 🗄️ Database Schema

The relational schema is configured in [`trace360.sql`](trace360.sql):

- **`Role`**: Predefined platform roles (`ADMIN`, `MANUFACTURER`, `SUPPLIER`, `SERVICE_CENTER`, `CUSTOMER`).
- **`User`**: Account credentials, hashed passwords, role linkage, and status.
- **`Manufacturer`**: Company profiles, GSTIN, and registration details linked to a user.
- **`ServiceCenter`**: Service center details, license numbers, and contact info.
- **`Product`**: Unique `ProductID` primary key, serial number, batch, category, and lifecycle state.
- **`ServiceHistory`**: Audit trail of all repairs, diagnostics, parts replacement, dates, and costs.

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.8+**
- **MySQL Server 8.0+**

### 1. Clone the Repository

```bash
git clone https://github.com/NamburiRupesh/Trace360.git
cd Trace360
```

### 2. Set Up a Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Database Setup

1. Open MySQL and run the migration script:
   ```bash
   mysql -u root -p < trace360.sql
   ```
2. Verify the database credentials in [`database.py`](database.py):
   ```python
   def get_db_connection():
       connection = mysql.connector.connect(
           host="localhost",
           user="root",
           password="your_mysql_password",
           database="trace360_db"
       )
       return connection
   ```

### 5. Run the Application

```bash
python app.py
```

The application will start at: **`http://127.0.0.1:5000`**

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
