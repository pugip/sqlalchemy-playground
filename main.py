from sqlalchemy import create_engine, Column, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm.session import sessionmaker

Base = declarative_base()


class Project(Base):
    __tablename__ = "project"
    id = Column(Integer, primary_key=True)
    tasks = relationship("Task", backref="project")


class Task(Base):
    __tablename__ = "task"
    id = Column(Integer, primary_key=True)
    project_id = Column(
        Integer, ForeignKey("project.id", ondelete="CASCADE"), nullable=True
    )


engine = create_engine("postgresql://dev:dev@localhost:5435/playground")
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

task = Task()
project = Project(tasks=[task, Task()])
session.add(project)
session.commit()
print(project.tasks)
session.delete(task)
print(project.tasks)
session.commit()
print(project.tasks)


task = Task()
project = Project(tasks=[task, Task()])
session.add(project)
session.commit()
print(project.tasks)
session.delete(task)
print(project.tasks)
session.commit()
print(project.tasks)
