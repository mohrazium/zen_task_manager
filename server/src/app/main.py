from fastapi import FastAPI

from src.config.database.zen_task_db_handler import ZenTaskDbHandler




app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/new")
async def new():
    return {"mess": "new"}

@app.get("/db")
async def db():
    db = ZenTaskDbHandler.db()
    en= db.getEngine()
    if en:
        return {"message": "Database engine is configured."}
    else:
        return {"message": "Database engine is not configured. Please initialize the database first."}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}