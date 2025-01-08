import os
from app import create_app
from config import Config

app = create_app(os.getenv('FASTAPI_CONFIG') or 'default')

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host=Config.HOST, port=Config.PORT) 