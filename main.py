import os
import uvicorn
from dotenv import load_dotenv
from app import app

if __name__ == "__main__":
    load_dotenv()
    env = os.environ.get("ENV")

    if env == "prod":
        uvicorn.run(app.app, host="0.0.0.0")
    uvicorn.run("app.app:app", host="0.0.0.0", reload=True)
