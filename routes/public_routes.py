from flask import Blueprint, render_template, request

from database import get_db_connection


public_bp = Blueprint("public", __name__)


@public_bp.route("/")
def home():
    return render_template("index.html")


@public_bp.route("/search-product", methods=["POST"])
def search_product():

    product_id = request.form.get("product_id")

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)


    # READ PRODUCT DETAILS

    product_query = """
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
    """

    cursor.execute(product_query, (product_id,))
    product = cursor.fetchone()


    # READ SERVICE HISTORY

    service_query = """
        SELECT
            sh.ServiceID,
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
    """

    cursor.execute(service_query, (product_id,))
    service_history = cursor.fetchall()


    cursor.close()
    connection.close()

    # PRODUCT NOT FOUND

    if not product:

        return render_template(
            "index.html",
            error="Product not found."
        )



    # DISPLAY PRODUCT + SERVICE HISTORY

    return render_template(
        "product.html",
        product=product,
        service_history=service_history
    )