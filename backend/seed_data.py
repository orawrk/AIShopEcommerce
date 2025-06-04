"""
Database seeding script to populate the database with authentic product data
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from config.database import SessionLocal, engine, Base
from models.product import Product
from models.enums import ProductCategoryEnum

def create_tables():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully")

def seed_products():
    """Seed the database with authentic product data"""
    db = SessionLocal()
    
    try:
        # Check if products already exist
        if db.query(Product).count() > 0:
            print("Products already exist in database")
            return
        
        # Authentic product data
        products = [
            # Electronics
            Product(
                name="iPhone 15 Pro",
                description="Latest Apple smartphone with A17 Pro chip, titanium design, and advanced camera system",
                price=999.99,
                category=ProductCategoryEnum.ELECTRONICS,
                stock_quantity=50,
                rating=4.8,
                sku="IPHONE15PRO",
                image_url="https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/iphone-15-pro-finish-select-202309-6-1inch-naturaltitanium"
            ),
            Product(
                name="MacBook Air M3",
                description="13-inch laptop with M3 chip, 8GB RAM, 256GB SSD, all-day battery life",
                price=1099.00,
                category=ProductCategoryEnum.ELECTRONICS,
                stock_quantity=30,
                rating=4.7,
                sku="MACBOOKAIRM3",
                image_url="https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/macbook-air-midnight-select-20220606"
            ),
            Product(
                name="Sony WH-1000XM5 Headphones",
                description="Industry-leading noise canceling wireless headphones with 30-hour battery life",
                price=399.99,
                category=ProductCategoryEnum.ELECTRONICS,
                stock_quantity=75,
                rating=4.6,
                sku="SONYWH1000XM5",
                image_url="https://m.media-amazon.com/images/I/51QeS0jCZyL._AC_SL1500_.jpg"
            ),
            Product(
                name="Samsung 65\" QLED 4K TV",
                description="65-inch QLED 4K Smart TV with Quantum HDR and built-in streaming apps",
                price=1299.99,
                category=ProductCategoryEnum.ELECTRONICS,
                stock_quantity=20,
                rating=4.5,
                sku="SAMSUNG65QLED",
                image_url="https://images.samsung.com/is/image/samsung/p6pim/us/qn65q70cafxza/gallery/us-qled-4k-q70c-qn65q70cafxza-537899348"
            ),
            Product(
                name="Nintendo Switch OLED",
                description="Gaming console with 7-inch OLED screen, 64GB storage, and enhanced audio",
                price=349.99,
                category=ProductCategoryEnum.ELECTRONICS,
                stock_quantity=45,
                rating=4.8,
                sku="SWITCHOLED",
                image_url="https://assets.nintendo.com/image/upload/c_fill,w_1200/q_auto:best/f_auto/dpr_2.0/ncom/software/switch/70010000000025/7137262b5a64d921e193653f8aa0b722925abc5680380ca0e18a5cfd91697f58"
            ),
            
            # Clothing
            Product(
                name="Levi's 501 Original Jeans",
                description="Classic straight-leg jeans in authentic indigo denim, the original since 1873",
                price=89.50,
                category=ProductCategoryEnum.CLOTHING,
                stock_quantity=100,
                rating=4.4,
                sku="LEVIS501ORIG",
                image_url="https://lsco.scene7.com/is/image/lsco/005010000-front-pdp-lse"
            ),
            Product(
                name="Nike Air Force 1 '07",
                description="Classic white leather sneakers with Nike Air cushioning and timeless basketball design",
                price=110.00,
                category=ProductCategoryEnum.CLOTHING,
                stock_quantity=80,
                rating=4.7,
                sku="NIKEAF107",
                image_url="https://static.nike.com/a/images/t_PDP_1728_v1/f_auto,q_auto:eco/b7d9211c-26e7-431a-ac24-b0540fb3c00f/air-force-1-07-mens-shoes-jBrhbr.png"
            ),
            Product(
                name="Patagonia Houdini Jacket",
                description="Ultra-lightweight windbreaker made from 100% recycled nylon with DWR finish",
                price=129.00,
                category=ProductCategoryEnum.CLOTHING,
                stock_quantity=60,
                rating=4.5,
                sku="PATHOUDINIJKT",
                image_url="https://www.patagonia.com/dw/image/v2/BDJB_PRD/on/demandware.static/-/Sites-patagonia-master/default/dw8c0d8c92/images/hi-res/24142_BLK.jpg"
            ),
            Product(
                name="Uniqlo Heattech Crew Neck T-Shirt",
                description="Ultra-warm crew neck long sleeve made with moisture-wicking Heattech fabric",
                price=19.90,
                category=ProductCategoryEnum.CLOTHING,
                stock_quantity=150,
                rating=4.3,
                sku="UNIQLOHTCRW",
                image_url="https://image.uniqlo.com/UQ/ST3/AsianCommon/imagesgoods/400418/item/goods_09_400418.jpg"
            ),
            
            # Books
            Product(
                name="The Psychology of Money by Morgan Housel",
                description="Timeless lessons on wealth, greed, and happiness exploring the psychology behind financial decisions",
                price=16.99,
                category=ProductCategoryEnum.BOOKS,
                stock_quantity=200,
                rating=4.6,
                sku="PSYCHMONEY",
                image_url="https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1581527774i/41881472.jpg"
            ),
            Product(
                name="Atomic Habits by James Clear",
                description="An easy and proven way to build good habits and break bad ones with practical strategies",
                price=18.00,
                category=ProductCategoryEnum.BOOKS,
                stock_quantity=180,
                rating=4.7,
                sku="ATOMICHABITS",
                image_url="https://jamesclear.com/wp-content/uploads/2018/09/atomic-habits-dots.jpg"
            ),
            Product(
                name="Sapiens by Yuval Noah Harari",
                description="A brief history of humankind exploring how Homo sapiens came to dominate the world",
                price=17.99,
                category=ProductCategoryEnum.BOOKS,
                stock_quantity=120,
                rating=4.5,
                sku="SAPIENS",
                image_url="https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1420585954i/23692271.jpg"
            ),
            
            # Home & Garden
            Product(
                name="Dyson V15 Detect Cordless Vacuum",
                description="Powerful cordless vacuum with laser dust detection and LCD screen displaying particle count",
                price=749.99,
                category=ProductCategoryEnum.HOME_GARDEN,
                stock_quantity=25,
                rating=4.6,
                sku="DYSONV15DET",
                image_url="https://dyson-h.assetsadobe2.com/is/image/content/dam/dyson/products/vacuum-cleaners/stick/dyson-v15-detect/dyson-v15-detect-absolute-nickel-red-1.png"
            ),
            Product(
                name="Instant Pot Duo 7-in-1 Electric Pressure Cooker",
                description="6-quart multi-use programmable cooker: pressure cooker, slow cooker, rice cooker, steamer, saute, yogurt maker, warmer",
                price=99.95,
                category=ProductCategoryEnum.HOME_GARDEN,
                stock_quantity=40,
                rating=4.4,
                sku="INSTANTPOTDUO",
                image_url="https://m.media-amazon.com/images/I/71V8rDQSl8L._AC_SL1500_.jpg"
            ),
            Product(
                name="Philips Hue White and Color Ambiance Starter Kit",
                description="Smart LED light bulbs with bridge, app control, and 16 million colors",
                price=199.99,
                category=ProductCategoryEnum.HOME_GARDEN,
                stock_quantity=35,
                rating=4.5,
                sku="PHILIPSHUESTRT",
                image_url="https://assets.philips.com/is/image/PhilipsConsumer/046677562984_01-IMS-en_US"
            ),
            
            # Sports
            Product(
                name="Hydro Flask 32 oz Wide Mouth Water Bottle",
                description="Insulated stainless steel water bottle that keeps drinks cold for 24 hours, hot for 12 hours",
                price=44.95,
                category=ProductCategoryEnum.SPORTS,
                stock_quantity=90,
                rating=4.7,
                sku="HYDROFLASK32",
                image_url="https://www.hydroflask.com/media/catalog/product/w/3/w32ts001_black_1.jpg"
            ),
            Product(
                name="Yeti Rambler 20 oz Tumbler",
                description="Double-wall vacuum insulated tumbler with MagSlider lid, keeps drinks at temperature for hours",
                price=34.99,
                category=ProductCategoryEnum.SPORTS,
                stock_quantity=75,
                rating=4.6,
                sku="YETIRAMBLER20",
                image_url="https://cdn.shopify.com/s/files/1/0520/1156/4964/products/21071500020_Rambler_20oz_Tumbler_Black_1_a_2x_2x_1024x1024.png"
            ),
            Product(
                name="Theraband Resistance Bands Set",
                description="Professional elastic resistance bands for strength training, physical therapy, and fitness",
                price=29.99,
                category=ProductCategoryEnum.SPORTS,
                stock_quantity=110,
                rating=4.3,
                sku="THERABANDSET",
                image_url="https://www.theraband.com/media/catalog/product/cache/1/image/9df78eab33525d08d6e5fb8d27136e95/2/0/20321_theraband_clx_individual_1.jpg"
            )
        ]
        
        # Add all products to database
        for product in products:
            db.add(product)
        
        db.commit()
        print(f"Successfully seeded {len(products)} products into the database")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("Creating database tables...")
    create_tables()
    
    print("Seeding database with product data...")
    seed_products()
    
    print("Database setup complete!")