from fastapi import Depends,FastAPI
from database import session
import database_model
import database
from models import Product
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI()

app.add_middleware(CORSMiddleware,
                   allow_credentials=True,
                   allow_methods=["DELETE", "GET", "POST", "PUT", "OPTIONS"],
                   allow_origins=["*"],
                   allow_headers=["*"],)

database_model.Base.metadata.create_all(bind=database.engine)

products=[
    Product(id=1,name="i phone 14",description="This is i phone 14",price=1000.00,quantity=10),
    Product(id=2,name="i phone 14 pro",description="This is i phone 14 pro",price=1200.00,quantity=5)
    
]

def get_db():
    db=session()
    try:
        yield db
    finally:
        db.close()

def initdb():
    db=session()
    
    for product in products:
        db.add(database_model.Product(**product.model_dump()))
    
    db.commit()
    
    
@app.get("/products")
def get_Allproducts(db:Session=Depends(get_db)):
    productsdata=db.query(database_model.Product).all()
    return productsdata
    
@app.get("/products/{id}")
def get_product_by_id(id:int,db:Session=Depends(get_db)):
    productiddata=db.query(database_model.Product).filter(database_model.Product.id==id).first()
    if not productiddata:
        return {"message":"Product not found"}
    return productiddata

@app.post("/add")
def create_product(product:Product,db:Session=Depends(get_db)):
    new_product=database_model.Product(**product.model_dump())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@app.put("/update/{id}")
def update_product(id:int,product:Product,db:Session=Depends(get_db)):
    productiddata=db.query(database_model.Product).filter(database_model.Product.id==id).first()
    if not productiddata:
        return {"message":"Product not found"}  
    for key,value in product.model_dump().items():
        setattr(productiddata,key,value)
    db.commit()
    db.refresh(productiddata)
    return {"message":"Product updated successfully"}  

@app.delete("/delete/{id}")
def delete_product(id:int,db:Session=Depends(get_db)):
    productiddata=db.query(database_model.Product).filter(database_model.Product.id==id).first()
    if not productiddata:
        return {"message":"Product not found"}
    db.delete(productiddata)
    db.commit()
    return {"message":"Product deleted successfully"} 
