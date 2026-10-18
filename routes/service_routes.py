from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session
)

from database import get_db_connection


service_bp = Blueprint(
    "service",
    __name__,
    url_prefix="/service"
)



@service_bp.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(
            url_for(
                "auth.login",
                role="SERVICE_CENTER"
            )
        )

    if session.get("role") != "SERVICE_CENTER":
        return "Access denied."

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT
            ServiceCenterID,
            CenterName,
            LicenseNumber,
            Phone
        FROM ServiceCenter
        WHERE UserID = %s
        """,
        (session["user_id"],)
    )

    service_center = cursor.fetchone()

    cursor.close()
    connection.close()

    if not service_center:
        return "Service center profile not found."

    return render_template(
        "service_dashboard.html",
        service_center=service_center
    )




@service_bp.route(
    "/search-product",
    methods=["GET", "POST"]
)
def search_product():

    if "user_id" not in session:
        return redirect(
            url_for(
                "auth.login",
                role="SERVICE_CENTER"
            )
        )

    if session.get("role") != "SERVICE_CENTER":
        return "Access denied."

    product = None
    error = None

    if request.method == "POST":

        product_id = request.form.get("product_id")

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT
                p.ProductID,
                p.ProductName,
                p.Model,
                p.SerialNumber,
                p.ManufacturingDate,
                p.BatchNumber,
                p.Category,
                p.Status,
                m.CompanyName
            FROM Product p
            JOIN Manufacturer m
                ON p.ManufacturerID = m.ManufacturerID
            WHERE p.ProductID = %s
            """,
            (product_id,)
        )

        product = cursor.fetchone()

        cursor.close()
        connection.close()

        if not product:
            error = "Product not found."

    return render_template(
        "service_search_product.html",
        product=product,
        error=error
    )



@service_bp.route(
    "/add-service",
    methods=["GET", "POST"]
)
def add_service():

    if "user_id" not in session:
        return redirect(
            url_for(
                "auth.login",
                role="SERVICE_CENTER"
            )
        )

    if session.get("role") != "SERVICE_CENTER":
        return "Access denied."

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Find logged-in service center
    cursor.execute(
        """
        SELECT ServiceCenterID, CenterName
        FROM ServiceCenter
        WHERE UserID = %s
        """,
        (session["user_id"],)
    )

    service_center = cursor.fetchone()

    if not service_center:
        cursor.close()
        connection.close()
        return "Service center profile not found."

    if request.method == "POST":

        product_id = request.form.get("product_id")
        service_type = request.form.get("service_type")
        problem_reported = request.form.get("problem_reported")
        diagnosis = request.form.get("diagnosis")
        action_taken = request.form.get("action_taken")
        remarks = request.form.get("remarks")
        service_date = request.form.get("service_date")
        cost = request.form.get("cost")

        # Check product exists
        cursor.execute(
            """
            SELECT ProductID
            FROM Product
            WHERE ProductID = %s
            """,
            (product_id,)
        )

        product = cursor.fetchone()

        if not product:

            cursor.close()
            connection.close()

            return render_template(
                "add_service.html",
                service_center=service_center,
                error="Product ID does not exist."
            )

        try:

            cursor.execute(
                """
                INSERT INTO ServiceHistory
                (
                    ProductID,
                    ServiceCenterID,
                    ServiceType,
                    ProblemReported,
                    Diagnosis,
                    ActionTaken,
                    Remarks,
                    ServiceDate,
                    Cost
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
                    %s
                )
                """,
                (
                    product_id,
                    service_center["ServiceCenterID"],
                    service_type,
                    problem_reported,
                    diagnosis,
                    action_taken,
                    remarks,
                    service_date,
                    cost
                )
            )

            connection.commit()

            service_id = cursor.lastrowid

            cursor.close()
            connection.close()

            return render_template(
                "service_created.html",
                service_id=service_id,
                product_id=product_id
            )

        except Exception as e:

            connection.rollback()

            cursor.close()
            connection.close()

            return render_template(
                "add_service.html",
                service_center=service_center,
                error=f"Error adding service record: {e}"
            )

    cursor.close()
    connection.close()

    return render_template(
        "add_service.html",
        service_center=service_center
    )

# UPDATE SERVICE RECORD

@service_bp.route(
    "/update-service/<int:service_id>",
    methods=["GET", "POST"]
)
def update_service(service_id):

    if "user_id" not in session:
        return redirect(
            url_for(
                "auth.login",
                role="SERVICE_CENTER"
            )
        )

    if session.get("role") != "SERVICE_CENTER":
        return "Access denied."

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Get service center

    cursor.execute(
        """
        SELECT ServiceCenterID, CenterName
        FROM ServiceCenter
        WHERE UserID = %s
        """,
        (session["user_id"],)
    )

    service_center = cursor.fetchone()

    if not service_center:
        cursor.close()
        connection.close()
        return "Service center profile not found."


    # Get existing service record


    cursor.execute(
        """
        SELECT *
        FROM ServiceHistory
        WHERE ServiceID = %s
          AND ServiceCenterID = %s
        """,
        (
            service_id,
            service_center["ServiceCenterID"]
        )
    )

    service = cursor.fetchone()

    if not service:

        cursor.close()
        connection.close()

        return "Service record not found or access denied."

    # UPDATE

    if request.method == "POST":

        service_type = request.form.get("service_type")
        problem_reported = request.form.get("problem_reported")
        diagnosis = request.form.get("diagnosis")
        action_taken = request.form.get("action_taken")
        remarks = request.form.get("remarks")
        service_date = request.form.get("service_date")
        cost = request.form.get("cost")

        try:

            cursor.execute(
                """
                UPDATE ServiceHistory
                SET
                    ServiceType = %s,
                    ProblemReported = %s,
                    Diagnosis = %s,
                    ActionTaken = %s,
                    Remarks = %s,
                    ServiceDate = %s,
                    Cost = %s
                WHERE ServiceID = %s
                  AND ServiceCenterID = %s
                """,
                (
                    service_type,
                    problem_reported,
                    diagnosis,
                    action_taken,
                    remarks,
                    service_date,
                    cost,
                    service_id,
                    service_center["ServiceCenterID"]
                )
            )

            connection.commit()

            cursor.close()
            connection.close()

            return redirect(
                url_for(
                    "service.service_records",
                    product_id=service["ProductID"]
                )
            )

        except Exception as e:

            connection.rollback()

            cursor.close()
            connection.close()

            return render_template(
                "update_service.html",
                service=service,
                error=f"Update failed: {e}"
            )

    cursor.close()
    connection.close()

    return render_template(
        "update_service.html",
        service=service
    )


# READ SERVICE RECORDS

@service_bp.route("/records/<product_id>")
def service_records(product_id):

    if "user_id" not in session:
        return redirect(
            url_for(
                "auth.login",
                role="SERVICE_CENTER"
            )
        )

    if session.get("role") != "SERVICE_CENTER":
        return "Access denied."

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT
            sh.ServiceID,
            sh.ProductID,
            sh.ServiceType,
            sh.ProblemReported,
            sh.Diagnosis,
            sh.ActionTaken,
            sh.Remarks,
            sh.ServiceDate,
            sh.Cost,
            sc.CenterName
        FROM ServiceHistory sh
        JOIN ServiceCenter sc
            ON sh.ServiceCenterID = sc.ServiceCenterID
        WHERE sh.ProductID = %s
        ORDER BY sh.ServiceDate DESC
        """,
        (product_id,)
    )

    records = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "service_records.html",
        records=records,
        product_id=product_id
    )