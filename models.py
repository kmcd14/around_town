from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db_conn import Base

class Category(Base):
    __tablename__ = 'categories'  # Table name in the database
    category_id = Column('category_id', Integer, primary_key=True)
    category = Column('category', String, nullable=False)

    def __repr__(self):
        return f"<Category(id={self.category_id}, name='{self.category}')>"

class Group(Base):
    __tablename__ = 'groups'  # Table name in the database
    group_id = Column('group_id', Integer, primary_key=True)
    name = Column('name', String(75))
    description = Column('description', String)
    website = Column('website', String(255))
    phone = Column('phone', String(50))
    email = Column('email', String(100))
    address = Column('address', String)
    area = Column('area', String(100))
    age_group = Column('age_group', String(50))
    category_id = Column('category_id', Integer, ForeignKey('categories.category_id'))  # Foreign key
    category = relationship('Category', backref='groups')  # SQLAlchemy relationship

    def __repr__(self):
        return f"<Group(id={self.group_id}, name='{self.name}', age_group='{self.age_group}')>"
