from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# datamodel for Customers
class Customer(db.Model):
    __tablename__ = "customers"

    customerid = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    middleinitial = db.Column(db.String(1))
    lastname = db.Column(db.String(50), nullable=False)
    cityid = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"<Customer {self.firstname} {self.lastname}>"


# datamodel for Employees
class Employee(db.Model):
    __tablename__ = "employees"

    employeeid = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    middleinitial = db.Column(db.String(1))
    lastname = db.Column(db.String(50), nullable=False)
    birthdate = db.Column(db.Date)
    gender = db.Column(db.String(1))
    cityid = db.Column(db.Integer, nullable=False)
    hiredate = db.Column(db.Date)

    def __repr__(self):
        return f"<Employee {self.firstname} {self.lastname}>"


# datamodel for Products
class Product(db.Model):
    __tablename__ = "products"

    productid = db.Column(db.Integer, primary_key=True)
    productname = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    categoryid = db.Column(db.Integer)
    class_ = db.Column("class", db.String)
    modifydate = db.Column(db.Date)
    resistant = db.Column(db.String(50))
    isallergic = db.Column(db.Boolean)
    vitalitydays = db.Column(db.Integer)

    def __repr__(self):
        return f"<Product {self.productname}>"


# datamodel for Sales
class Sale(db.Model):
    __tablename__ = "sales"

    salesid = db.Column(db.Integer, primary_key=True)
    salespersonid = db.Column(
        db.Integer, db.ForeignKey("employees.employeeid"), nullable=False
    )
    customerid = db.Column(
        db.Integer, db.ForeignKey("customers.customerid"), nullable=False
    )
    productid = db.Column(
        db.Integer, db.ForeignKey("products.productid"), nullable=False
    )
    quantity = db.Column(db.Integer, nullable=False)
    discount = db.Column(db.Float)
    totalprice = db.Column(db.Float)
    salesdate = db.Column(db.Date)
    transactionnum = db.Column(db.String(50), unique=True, nullable=False)
    
    employee = db.relationship("Employee", backref=db.backref("sales", lazy=True))
    customer = db.relationship("Customer", backref=db.backref("sales", lazy=True))
    product = db.relationship("Product", backref=db.backref("sales", lazy=True))

    def __repr__(self):
        return f"<Sale {self.salesid}>"
