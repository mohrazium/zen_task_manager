# from sqlalchemy import create_engine
# from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
#                                     create_async_engine)
# from sqlalchemy.orm import declarative_base, sessionmaker
#
# from src.config.settings.config import settings
#
# # Async engine for async operations
# async_engine = create_async_engine(
#     settings.DATABASE_URL, echo=settings.DEBUG, future=True
# )
#
# # Sync engine for migrations and sync operations
# sync_engine = create_engine(
#     settings.DATABASE_URL_SYNC,
#     echo=settings.DEBUG,
# )
#
# # Session makers
# AsyncSessionLocal = async_sessionmaker(
#     async_engine, class_=AsyncSession, expire_on_commit=False
# )
#
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)
#
# Base = declarative_base()
#
#
# async def get_db() -> AsyncSession:
#     async with AsyncSessionLocal() as session:
#         try:
#             yield session
#         finally:
#             await session.close()
#
#
# async def create_tables():
#     async with async_engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
