from flask import Flask, request, jsonify, render_template, redirect, url_for
from models import db, Customer, Employee, Product, Sale
from datetime import datetime
from sqlalchemy import func
import uuid

app = Flask(__name__)

# configure the database URI
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql+psycopg2://testuser:123@localhost:5432/412_group_project"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# init the database
db.init_app(app)

# route to edit tables
@app.route("/")
def home():
    return render_template("layout.html")


# get all customers, all fields
@app.route("/customers", methods=["GET"])
def get_customers():
    customers = Customer.query.order_by(Customer.customerid).limit(100).all()
    return render_template("customers.html", customers=customers)


# get all employees
@app.route("/employees", methods=["GET"])
def get_employees():
    employees = Employee.query.order_by(Employee.employeeid).limit(100).all()
    return render_template("employees.html", employees=employees)


# get all products
@app.route("/products", methods=["GET"])
def get_products():
    products = Product.query.order_by(Product.productid).limit(100).all()
    return render_template("products.html", products=products)


# get all sales
@app.route("/sales", methods=["GET"])
def get_sales():
    # sales = Sale.query.all()
    sales = Sale.query.order_by(Sale.salesid.desc()).limit(100).all()
    return render_template("sales.html", sales=sales)

 
@app.route("/tableEdits")
def table_edits():
    return render_template("tableEdits.html")


# Delete a sale given its product name
@app.route("/delete-product", methods=["POST"])
def delete_product():
    productName = request.form.get("delete_productName")

    sales = Sale.query.join(Product).filter_by(productname=productName).all()
    if sales:
        try:
            for sale in sales:
                db.session.delete(sale)
            db.session.commit()
            delete_status = f"All sales with product '{productName}' successfully deleted"
        except Exception as e:
            db.session.rollback()
            delete_status = f"Deleting exception: {str(e)}"
    else:
        delete_status = f"There are no sales with product '{productName}'"
    return render_template("tableEdits.html", delete_status=delete_status)


# Update a product given its name
@app.route("/update-product", methods=["POST"])
def update_product():
    productName_old = request.form.get("update_oldProductName")
    productName_new = request.form.get("update_newProductName")

    products = Product.query.filter_by(productname=productName_old).all()
    if products:
        try:
            for product in products:
                product.productname = productName_new
            db.session.commit()
            update_status = f"All products named '{productName_old}' successfully updated to '{productName_new}'"
        except Exception as e:
            db.session.rollback()
            update_status = f"Updating exception: {str(e)}"
    else:
        update_status = f"There are no products named '{productName_old}'"
    return render_template("tableEdits.html", update_status=update_status)

# Insert Sale
@app.route("/sales", methods=["POST"])
def insert_sale():
    max_id = db.session.query(func.max(Sale.salesid)).scalar() or 0
    next_id = max_id + 1

    random_uuid = uuid.uuid4()
    txnID= str(random_uuid).replace('-','')[:25]
    try:
        new_sale = Sale(
            salesid=next_id,
            salespersonid=request.form['salesperson'],
            customerid=request.form['customer'],
            productid=request.form['product'],
            quantity=request.form['quantity'],
            discount=request.form['discount'],
            totalprice=0.0,
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
