from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    ForeignKey,
    Text,
    UniqueConstraint,
    insert,
)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm.session import sessionmaker

Base = declarative_base()


class Project(Base):
    __tablename__ = "project"
    id = Column(Integer, primary_key=True)
    tasks = relationship("Task", backref="project", passive_deletes=True)


class Task(Base):
    __tablename__ = "task"
    __table_args__ = (UniqueConstraint("name"),)

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    project_id = Column(
        Integer, ForeignKey("project.id", ondelete="CASCADE"), nullable=False
    )


engine = create_engine("postgresql://dev:dev@localhost:5435/playground")
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Here's an example of not using the session.begin() "context manager".
# We're also triggering an integrity error by violating the uniqueness constraint
# on the task name.
project = Project(tasks=[Task(name="mike"), Task(name="mike")])
session.add(project)
try:
    session.commit()
except IntegrityError:
    print("integrity error happened!")
    session.rollback()

project = Project(tasks=[Task(name="mike"), Task(name="mary"), Task(name="charles")])
session.add(project)
try:
    session.commit()
except IntegrityError:
    print("integrity error happened!")

# Here's another way of executing statements:
result = session.execute(insert(Project), [{"id": 1}, {"id": 6}])
_ = session.execute(
    insert(Task),
    [
        {"name": "karen", "project_id": 1},
        {"name": "richard", "project_id": 2},
    ],
)

# For Task, ondelete="CASCADE" means that tasks will get deleted when a parent
# Project is deleted. This is handled by the DB (thanks to passive_deletes).
project = Project(tasks=[Task(name="william"), Task(name="donna")])
session.add(project)
session.commit()
session.refresh(project)
session.delete(project)
session.commit()
print("done")
