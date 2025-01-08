import logging
from fastapi import FastAPI
from config import config

def create_app(config_name='default'):
    app = FastAPI(title="DuckDuckGo API")
    
    # 配置日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # 注册路由
    from .controllers.search_controller import router as search_router
    app.include_router(search_router)
    
    return app 