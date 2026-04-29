from sqlalchemy import (
    create_engine, Column, Integer, String,
    Numeric, Boolean, ForeignKey, func
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

engine = create_engine("sqlite:///:memory:", echo=False)

Base = declarative_base()


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255))

    products = relationship("Product", back_populates="category")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    price = Column(Numeric(10, 2))
    in_stock = Column(Boolean, default=True)

    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("Category", back_populates="products")


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

# ЗАДАЧА 1 — НАПОЛНЕНИЕ ДАННЫМИ
# =========================================
with Session() as session:

    electronics = Category(name="Электроника", description="Гаджеты и устройства.")
    books = Category(name="Книги", description="Печатные книги и электронные книги.")
    clothes = Category(name="Одежда", description="Одежда для мужчин и женщин.")

    session.add_all([electronics, books, clothes])
    session.flush()

    products = [
        Product(name="Смартфон", price=299.99, in_stock=True, category=electronics),
        Product(name="Ноутбук", price=499.99, in_stock=True, category=electronics),
        Product(name="Научно-фантастический роман", price=15.99, in_stock=True, category=books),
        Product(name="Джинсы", price=40.50, in_stock=True, category=clothes),
        Product(name="Футболка", price=20.00, in_stock=True, category=clothes),
    ]

    session.add_all(products)
    session.commit()


# ЗАДАЧА 2 — ЧТЕНИЕ ДАННЫХ
# =========================================
with Session() as session:
    data = session.query(Category, Product).join(Product).all()
    for category, product in data:
        print(f"Категория: {category.name} | Продукт: {product.name}: {product.price}")


# ЗАДАЧА 3 — ОБНОВЛЕНИЕ ДАННЫХ
# =========================================
with Session() as session:
    product = session.query(Product).filter_by(name="Смартфон").first()

    if product:
        product.price = 349.99
        session.commit()

    print(f"Обновленная цена для {product.name} - {session.query(Product.price).filter_by(name='Смартфон').scalar()}")
    
    
# ЗАДАЧА 4 — АГРЕГАЦИЯ И ГРУППИРОВКА
# =========================================
with Session() as session:
    result = (
        session.query(Category.name, func.count(Product.id))
        .join(Product)
        .group_by(Category.name)
        .all()
    )

    for name, count in result:
        print(f"{name}: {count} товаров")


# ЗАДАЧА 5 — ГРУППИРОВКА С ФИЛЬТРАЦИЕЙ
# =========================================
with Session() as session:
    result = (
        session.query(Category.name, func.count(Product.id).label("total"))
        .join(Product)
        .group_by(Category.id)
        .having(func.count(Product.id) > 1)
        .all()
    )

    for name, count in result:
        print(f"{name}: {count} товаров (>1)")