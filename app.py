from flask import Flask, request, jsonify, render_template, redirect, url_for
from models import db, Customer, Employee, Product, Sale
from datetime import datetime
import uuid

app = Flask(__name__)

# configure the database URI
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql+psycopg2://testuser:123@localhost:5432/412_group_project"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# init the database
db.init_app(app)


# dummy home page, we can add frontend
@app.route("/")
def home():
    return render_template("layout.html")


# get all customers, all fields
@app.route("/customers", methods=["GET"])
def get_customers():
    customers = Customer.query.all()  # Fetch all customers from the database
    return jsonify(
        [
            {
                "customerid": customer.customerid,
                "firstname": customer.firstname,
                "middleinitial": customer.middleinitial,
                "lastname": customer.lastname,
                "cityid": customer.cityid,
                "address": customer.address,
            }
            for customer in customers
        ]
    )


# get all employees
@app.route("/employees", methods=["GET"])
def get_employees():
    employees = Employee.query.all()
    return jsonify(
        [
            {
                "employeeid": employee.employeeid,
                "firstname": employee.firstname,
                "middleinitial": employee.middleinitial,
                "lastname": employee.lastname,
                "birthdate": employee.birthdate,
                "gender": employee.gender,
                "cityid": employee.cityid,
                "hiredate": employee.hiredate,
            }
            for employee in employees
        ]
    )


# get all products
@app.route("/products", methods=["GET"])
def get_products():
    products = Product.query.all()

    return jsonify(
        [
            {
                "productid": product.productid,
                "productname": product.productname,
                "price": product.price,
                "categoryid": product.categoryid,
                "class": product.class_,
                "modifydate": product.modifydate,
                "resistant": product.resistant,
                "isallergic": product.isallergic,
                "vitalitydays": product.vitalitydays,
            }
            for product in products
        ]
    )


# get all sales
@app.route("/sales", methods=["GET"])
def get_sales():
    # sales = Sale.query.all()
    sales = Sale.query.limit(50).all()
    return render_template("sales.html", sales=sales)

    # return jsonify(
    #     [
    #         {
    #             "salesid": sale.salesid,
    #             "salespersonid": sale.salespersonid,
    #             "customerid": sale.customerid,
    #             "productid": sale.productid,
    #             "quantity": sale.quantity,
    #             "discount": sale.discount,
    #             "totalprice": sale.totalprice,
    #             "salesdate": sale.salesdate,
    #             "transactionnum": sale.transactionnum,
    #         }
    #         for sale in sales
    #     ]
    # )

# Insert Sale
@app.route("/sales", methods=["POST"])
def insert_sale():
    random_uuid = uuid.uuid4()
    txnID= str(random_uuid).replace('-','')[:25]
    try:
        new_sale = Sale(
            salespersonid=request.form['salesperson'],
            customerid=request.form['customer'],
            productid=request.form['product'],
            quantity=request.form['quantity'],
            discount=request.form['discount'],
            totalprice=request.form['totalprice'],
            salesdate=datetime.strptime(request.form['salesDate'], "%Y-%m-%dT%H:%M"),
            transactionnum=txnID
        )
        db.session.add(new_sale)
        db.session.commit()
        return redirect(url_for("get_sales"))
    except Exception as e:
        db.session.rollback()
        return f"Error Adding Sale: {str(e)}", 400
    
if __name__ == "__main__":
    app.run(debug=True, use_reloader=True, port="4000")
