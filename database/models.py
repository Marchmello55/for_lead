from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine


# Создаем асинхронный движок
engine = create_async_engine("sqlite+aiosqlite:///database/db.sqlite3", echo=False)
# Настраиваем фабрику сессий
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    tg_id: Mapped[int] = mapped_column(primary_key=True)
    role: Mapped[str] = mapped_column(String(), default="")

class Exexutor(Base):
    __tablename__ = "executor"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(), default="")
    link: Mapped[str] = mapped_column(String(), default="")
    state: Mapped[str] = mapped_column(String(), default="")
    description: Mapped[str] = mapped_column(String(), default="")
    task: Mapped[str] = mapped_column(String(), default="")


class Progects(Base):
    __tablename__ = "progects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(), default="")
    price: Mapped[str] = mapped_column(String(), default="")
    exercise: Mapped[str] = mapped_column(String(), default="")
    customer: Mapped[str] = mapped_column(String(), default="")
    link_to_chat: Mapped[str] = mapped_column(String(), default="")
    executor: Mapped[str] = mapped_column(String(), default="")
    deadline: Mapped[str] = mapped_column(String(), default="")
    reports: Mapped[str] = mapped_column(String(), default="")
    state: Mapped[str] = mapped_column(String(), default="")
    tasks: Mapped[str] = mapped_column(String(), default="")
    paid_month: Mapped[str] = mapped_column(Integer(), default=0)
    paid_year: Mapped[str] = mapped_column(Integer(), default=0)


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)