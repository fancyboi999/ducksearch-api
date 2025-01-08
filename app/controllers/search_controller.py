from fastapi import APIRouter, Query, Form
from typing import Optional
import logging
from ..services.search_service import SearchService
from config import Config

logger = logging.getLogger(__name__)
router = APIRouter()
search_service = SearchService(max_workers=Config.MAX_WORKERS)

@router.get("/search")
async def search(
    q: str = Query(..., description="搜索关键词"),
    max_results: Optional[int] = Query(Config.DEFAULT_MAX_RESULTS, description="最大结果数")
):
    logger.info(f"Received search request for: {q}")
    try:
        results = await search_service.search_text(q, max_results)
        return {"results": results}
    except Exception as e:
        logger.error(f"Error during search: {str(e)}")
        return {"error": str(e)}, 500

@router.get("/searchAnswers")
async def search_answers(
    q: str = Query(..., description="搜索关键词")
):
    try:
        results = await search_service.search_answers(q)
        return {"results": results}
    except Exception as e:
        logger.error(f"Error during answer search: {str(e)}")
        return {"error": str(e)}, 500

@router.get("/searchImages")
async def search_images(
    q: str = Query(..., description="搜索关键词"),
    max_results: Optional[int] = Query(Config.DEFAULT_MAX_RESULTS, description="最大结果数")
):
    try:
        results = search_service.search_images(q, max_results)
        return {"results": results}
    except Exception as e:
        logger.error(f"Error during image search: {str(e)}")
        return {"error": str(e)}, 500

@router.get("/searchVideos")
async def search_videos(
    q: str = Query(..., description="搜索关键词"),
    max_results: Optional[int] = Query(Config.DEFAULT_MAX_RESULTS, description="最大结果数")
):
    try:
        results = search_service.search_videos(q, max_results)
        return {"results": results}
    except Exception as e:
        logger.error(f"Error during video search: {str(e)}")
        return {"error": str(e)}, 500

# POST 路由
@router.post("/search")
async def search_post(
    q: str = Form(...),
    max_results: Optional[int] = Form(Config.DEFAULT_MAX_RESULTS)
):
    return await search(q, max_results)

@router.post("/searchAnswers")
async def search_answers_post(
    q: str = Form(...)
):
    return await search_answers(q)

@router.post("/searchImages")
async def search_images_post(
    q: str = Form(...),
    max_results: Optional[int] = Form(Config.DEFAULT_MAX_RESULTS)
):
    return await search_images(q, max_results)

@router.post("/searchVideos")
async def search_videos_post(
    q: str = Form(...),
    max_results: Optional[int] = Form(Config.DEFAULT_MAX_RESULTS)
):
    return await search_videos(q, max_results) 