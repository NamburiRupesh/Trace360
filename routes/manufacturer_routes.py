from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session
)

from database import get_db_connection

from datetime import datetime

import uuid


manufacturer_bp = Blueprint(
    "manufacturer",
    __name__,
    url_prefix="/manufacturer"
)



# MANUFACTURER DASHBOARD

@manufacturer_bp.route("/dashboard")
def dashboard():

    # Check login
    if "user_id" not in session:
        return redirect(
            url_for(
                "auth.login",
                role="MANUFACTURER"
            )
        )

    # Check role
    if session.get("role") != "MANUFACTURER":
        return "Access denied."

    return render_template(
        "manufacturer_dashboard.html"
    )



# CREATE PRODUCT

@manufacturer_bp.route(
    "/create-product",
    methods=["GET", "POST"]
)
def create_product():

    # Check login

    if "user_id" not in session:
        return redirect(
            url_for(
                "auth.login",
                role="MANUFACTURER"
            )
        )



    # Check role

    if session.get("role") != "MANUFACTURER":
        return "Access denied."


    connection = get_db_connection()

    cursor = connection.cursor(
        dictionary=True
    )



    # Find manufacturer profile


    cursor.execute(
        """
        SELECT
            ManufacturerID,
            CompanyName
        FROM Manufacturer
        WHERE UserID = %s
        """,
        (session["user_id"],)
    )

    manufacturer = cursor.fetchone()


    if not manufacturer:

        cursor.close()
        connection.close()

        return "Manufacturer profile not found."


    # FORM SUBMISSION

    if request.method == "POST":

        product_name = request.form.get(
            "product_name"
        )

        model = request.form.get(
            "model"
        )

        serial_number = request.form.get(
            "serial_number"
        )

        manufacturing_date = request.form.get(
            "manufacturing_date"
        )

        batch_number = request.form.get(
            "batch_number"
        )

        category = request.form.get(
            "category"
        )


        # Generate unique Product ID

        product_id = (
            f"TRC-{datetime.now().year}-"
            f"{uuid.uuid4().hex[:8].upper()}"
        )


        # INSERT PRODUCT

        query = """
            INSERT INTO Product
            (
                ProductID,
                ProductName,
                Model,
                SerialNumber,
                ManufacturingDate,
                BatchNumber,
                Category,
                ManufacturerID,
                Status
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                'ACTIVE'
            )
        """


        values = (
            product_id,
            product_name,
            model,
            serial_number,
            manufacturing_date,
            batch_number,
            category,
            manufacturer["ManufacturerID"]
        )


        try:

            cursor.execute(
                query,
                values
            )

            connection.commit()


            cursor.close()
            connection.close()


            # Show generated Product ID

            return render_template(
                "product_created.html",
                product_id=product_id,
                product_name=product_name
            )


        except Exception as e:

            connection.rollback()

            cursor.close()
            connection.close()

            return render_template(
                "create_product.html",
                manufacturer=manufacturer,
                error=f"Error creating product: {e}"
            )


    # DISPLAY FORM

    cursor.close()
    connection.close()

    return render_template(
        "create_product.html",
        manufacturer=manufacturer
    )