from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

from database import get_db_connection


auth_bp = Blueprint("auth", __name__)


# LOGIN


@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    role = request.args.get("role", "MANUFACTURER")

    if role not in ["MANUFACTURER", "SERVICE_CENTER"]:
        role = "MANUFACTURER"

    error = None

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        # Find user and check role
        query = """
            SELECT
                u.UserID,
                u.Username,
                u.Email,
                u.PasswordHash,
                u.Status,
                r.RoleName
            FROM User u
            JOIN Role r
                ON u.RoleID = r.RoleID
            WHERE u.Username = %s
              AND r.RoleName = %s
        """

        cursor.execute(query, (username, role))

        user = cursor.fetchone()

        cursor.close()
        connection.close()

        if user and check_password_hash(
            user["PasswordHash"],
            password
        ):

            # Store login information in session
            session["user_id"] = user["UserID"]
            session["username"] = user["Username"]
            session["role"] = user["RoleName"]

            # Manufacturer
            if role == "MANUFACTURER":
                return redirect(
                    url_for("manufacturer.dashboard")
                )

            # Service Center
            elif role == "SERVICE_CENTER":
                return redirect(
                    url_for("service.dashboard")
                )

        else:

            error = "Invalid username or password."

    return render_template(
        "login.html",
        role=role,
        error=error
    )



# MANUFACTURER REGISTRATION


@auth_bp.route("/register/manufacturer", methods=["GET", "POST"])
def register_manufacturer():

    error = None

    if request.method == "POST":

        
        # Get form data
        

        company_name = request.form.get("company_name")
        registration_number = request.form.get("registration_number")
        gstin = request.form.get("gstin")

        username = request.form.get("username")
        email = request.form.get("email")

        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")


        
        # Validate password
        

        if password != confirm_password:

            return render_template(
                "register_manufacturer.html",
                error="Passwords do not match."
            )


        
        # Connect to database


        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        try:

            # Check username/email already exists

            cursor.execute(
                """
                SELECT UserID
                FROM User
                WHERE Username = %s
                   OR Email = %s
                """,
                (username, email)
            )

            existing_user = cursor.fetchone()

            if existing_user:

                return render_template(
                    "register_manufacturer.html",
                    error="Username or email already exists."
                )


            # Get MANUFACTURER RoleID
            

            cursor.execute(
                """
                SELECT RoleID
                FROM Role
                WHERE RoleName = 'MANUFACTURER'
                """
            )

            role = cursor.fetchone()

            if not role:

                return render_template(
                    "register_manufacturer.html",
                    error="MANUFACTURER role not found."
                )



            password_hash = generate_password_hash(password)



            # Create User

            cursor.execute(
                """
                INSERT INTO User
                (
                    Username,
                    Email,
                    PasswordHash,
                    RoleID,
                    Status
                )
                VALUES
                (
                    %s,
                    %s,
                    %s,
                    %s,
                    'APPROVED'
                )
                """,
                (
                    username,
                    email,
                    password_hash,
                    role["RoleID"]
                )
            )


            # Get newly created UserID
            user_id = cursor.lastrowid


            # Create Manufacturer

            cursor.execute(
                """
                INSERT INTO Manufacturer
                (
                    UserID,
                    CompanyName,
                    RegistrationNumber,
                    GSTIN
                )
                VALUES
                (
                    %s,
                    %s,
                    %s,
                    %s
                )
                """,
                (
                    user_id,
                    company_name,
                    registration_number,
                    gstin
                )
            )


            connection.commit()


            cursor.close()
            connection.close()



            return redirect(
                url_for(
                    "auth.login",
                    role="MANUFACTURER"
                )
            )


        except Exception as e:

            connection.rollback()

            cursor.close()
            connection.close()

            return render_template(
                "register_manufacturer.html",
                error=f"Registration failed: {e}"
            )


    return render_template(
        "register_manufacturer.html",
        error=error
    )


# SERVICE CENTER REGISTRATION


@auth_bp.route("/register/service-center", methods=["GET", "POST"])
def register_service_center():

    if request.method == "POST":

        # Get form data

        center_name = request.form.get("center_name")
        license_number = request.form.get("license_number")
        phone = request.form.get("phone")

        username = request.form.get("username")
        email = request.form.get("email")

        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")


        # Check password

        if password != confirm_password:

            return render_template(
                "register_service_center.html",
                error="Passwords do not match."
            )


        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        try:

            # Check username/email

            cursor.execute(
                """
                SELECT UserID
                FROM User
                WHERE Username = %s
                   OR Email = %s
                """,
                (username, email)
            )

            existing_user = cursor.fetchone()

            if existing_user:

                cursor.close()
                connection.close()

                return render_template(
                    "register_service_center.html",
                    error="Username or email already exists."
                )



            # Get SERVICE_CENTER RoleID

            cursor.execute(
                """
                SELECT RoleID
                FROM Role
                WHERE RoleName = 'SERVICE_CENTER'
                """
            )

            role = cursor.fetchone()

            if not role:

                cursor.close()
                connection.close()

                return render_template(
                    "register_service_center.html",
                    error="SERVICE_CENTER role not found."
                )


            password_hash = generate_password_hash(password)


            
            # Create User

            cursor.execute(
                """
                INSERT INTO User
                (
                    Username,
                    Email,
                    PasswordHash,
                    RoleID,
                    Status
                )
                VALUES
                (
                    %s,
                    %s,
                    %s,
                    %s,
                    'APPROVED'
                )
                """,
                (
                    username,
                    email,
                    password_hash,
                    role["RoleID"]
                )
            )

            user_id = cursor.lastrowid



            # Create Service Center

            cursor.execute(
                """
                INSERT INTO ServiceCenter
                (
                    UserID,
                    CenterName,
                    LicenseNumber,
                    Phone
                )
                VALUES
                (
                    %s,
                    %s,
                    %s,
                    %s
                )
                """,
                (
                    user_id,
                    center_name,
                    license_number,
                    phone
                )
            )



            connection.commit()

            cursor.close()
            connection.close()


            # Go to Service Center Login
           

            return redirect(
                url_for(
                    "auth.login",
                    role="SERVICE_CENTER"
                )
            )


        except Exception as e:

            connection.rollback()

            cursor.close()
            connection.close()

            return render_template(
                "register_service_center.html",
                error=f"Registration failed: {e}"
            )


    # GET request
    return render_template(
        "register_service_center.html"
    )