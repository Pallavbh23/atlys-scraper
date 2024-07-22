from app.models import Product
from app.database.database import load_db, save_db

def get_all_products():
    return load_db()

def update_product(product: Product):
    db = load_db()
    updated = False
    for p in db:
        if p["product_title"] == product.get('product_title'):
            print('repeated product found', product)
            if p["product_price"] != product.get('product_price'):
                p.update(product)
                save_db(db)
                updated = True
            return
    db.append(product)
    save_db(db)
    return updated