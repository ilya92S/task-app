from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from settings import Settings

engine = create_async_engine(
    url=Settings().db_url,
    future=True,
    echo=True,
    pool_pre_ping=True
)
"""
pool_pre_ping нужен для того что бы при создании пула отправился
запрос к БД что бы посмотреть живой пул или нет
нужно для того что бы не было ни каких рандомных багов
"""

AsyncSessionFactory = async_sessionmaker(
    engine,
    autoflush=False,
    expire_on_commit=False
)
"""
async_sessionmaker - это класс который конфигурирует AsyncSession, 
это класс которы в то же время асинхронный контекстный менеджер, 
когда мы откроем контекстный менеджер, он создаст транзакцию, 
войдет в метод транзакции и он начнет соединение и
вернет объект асинхронной сессии
"""


async def get_db_session() -> AsyncSession:
    async with AsyncSessionFactory() as session:
        yield session


"""
AsyncSessionFactory - это объект AsyncSession, который тоже является 
контекстным менеджером, нам нужно его открыть и закрыть, 
когда мы будем выходить и вызовется __aexit__, у нас
вызовется метод close(это корутина, которая закрывает соединение в сессии)

выше мы открываем контекстный менеджер и возвращаем через 
yield экземпляр асинхронной сессии - это сложно, такое поверхностное объяснение
"""
