from fastapi import FastAPI, Depends
from models import Product
from database import sessionLocal, engine
import database_models
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=["*"]
)
database_models.Base.metadata.create_all(bind = engine) 

@app.get("/")

def greet():
    return ('Welcom Home')

products = [
    Product(id = 1,name ="phone", description ="smart phone", price = 99,quantity=10),
    Product(id = 2,name ="laptop", description ="mac", price = 999,quantity=12),
    Product(id = 3,name ="watch", description ="apple watch", price = 200,quantity=15),
    Product(id = 5,name ="airpods", description ="apple", price = 100,quantity=20),
]


def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    db = sessionLocal()

    count = db.query(database_models.Product).count

    if count ==0:

        for product in products:
            db.add(database_models.Product(**product.model_dump()))

        db.commit()

init_db()

@app.get("/products")

def get_all_products(db: Session = Depends(get_db)):
    #db = sessionLocal()
    #db.query()
    db_products = db.query(database_models.Product).all()
    return products

@app.get("/products/{id}")

def get_products_by_id(id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        return db_product
    else:
        return 'Product not found'

@app.post('/products')
def add_product(product: Product, db: Session = Depends(get_db)):
    db.add(database_models.Product(**product.model_dump()))
    db.commit()
    return product

@app.put('/products/{id}')
def update_product(id: int, product: Product, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db_product.quantity = product.quantity
        db.commit()
        return 'Product updated successfully'

    else:
        return 'Product not found'

@app.delete('/products')
def delete_product(id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
            db.delete(db_product)
            db.commit()
            return 'Product deleted successfully'
    else:
        return 'Product not found'