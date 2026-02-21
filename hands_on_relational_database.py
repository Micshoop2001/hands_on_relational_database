from sqlalchemy import create_engine, Integer, String, ForeignKey, select
from sqlalchemy.orm import Session, DeclarativeBase, Mapped, mapped_column, relationship

engine = create_engine('mysql+mysqlconnector://root:Lima22Alpha#@localhost/mydatabase')

class Base(DeclarativeBase):
    pass

class Orders(Base):
    __tablename__ = "orders"
    user = relationship("User", back_populates="orders")
    product = relationship("Product", back_populates="orders")

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id")) 
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"))
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)

class User(Base):
    __tablename__ = "users"
    orders = relationship("Orders", back_populates="user")

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable = False) 
    
    
class Product(Base):
    __tablename__ = "product"
    orders = relationship("Orders", back_populates="product")
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    

Base.metadata.create_all(engine)                
session = Session(engine)

new_user = [User(name="Peter", email='something@email.com')
                ,User(name="Amon", email='Amon@email.com')
                ,User(name="Zion", email='Zion@email.com')]

new_product = [Product(name="Pen", price=2)
                ,Product(name="Pad", price=4)
                ,Product(name="Stapler", price=6)]

new_orders = [Orders(user_id=1, product_id=2, quantity=4)
                ,Orders(user_id=1, product_id=1, quantity=7)
                ,Orders(user_id=2, product_id=2, quantity=3)
                ,Orders(user_id=3, product_id=3, quantity=1)]

session.add_all([*new_user
                 ,*new_product
                 ,*new_orders])
session.commit()

#Write Python code to:
#Retrieve all users and print their information.
#Retrieve all products and print their name and price.
#Retrieve all orders, showing the user’s name, product name, and quantity.
#Update a product’s price.
#Delete a user by ID.
queryusers = select(User)
queryprod = select(Product.name, Product.price)
queryorder = (select(User.name, Product.name, Orders.quantity)
              .join(Orders, User.id == Orders.user_id)
              .join(Product, Product.id == Orders.product_id))

print(session.execute(queryusers).scalars().all(), '\n')
print(session.execute(queryprod).scalars().all(), '\n')
print(session.execute(queryorder).scalars().all(), '\n')

prodprice = session.get(Product, 2)
prodprice.price = 3
session.commit()

deluser = session.get(User, 3)
session.delete(deluser)
session.commit()
