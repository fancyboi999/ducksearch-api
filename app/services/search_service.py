import logging
import asyncio
import aiohttp
from itertools import islice
from duckduckgo_search import DDGS
from concurrent.futures import ThreadPoolExecutor
from ..utils.html_processor import HTMLProcessor

logger = logging.getLogger(__name__)

class SearchService:
    def __init__(self, max_workers=5):
        self.thread_pool = ThreadPoolExecutor(max_workers=max_workers)
        
    async def fetch_and_parse_url(self, session, url):
        try:
            async with session.get(url, timeout=10) as response:
                html = await response.text()
                return await asyncio.get_event_loop().run_in_executor(
                    self.thread_pool, 
                    HTMLProcessor.process_html,
                    html
                )
        except Exception as e:
            logger.error(f"Error fetching {url}: {str(e)}")
            return None

    async def search_text(self, keywords, max_results=10):
        try:
            results = []
            with DDGS() as ddgs:
                ddgs_gen = ddgs.text(keywords, safesearch='Off', timelimit='y', backend="lite")
                search_results = list(islice(ddgs_gen, max_results))
                
                async with aiohttp.ClientSession() as session:
                    tasks = [
                        self.fetch_and_parse_url(session, r['href']) 
                        for r in search_results
                    ]
                    contents = await asyncio.gather(*tasks)
                    
                    for r, content in zip(search_results, contents):
                        if content:
                            r['full_content'] = content
                        results.append(r)
                        
            logger.info(f"Search completed successfully with {len(results)} results")
            return results
        except Exception as e:
            logger.error(f"Error during search: {str(e)}")
            raise

    async def search_answers(self, keywords):
        try:
            with DDGS() as ddgs:
                logger.info(f"Searching answers for: {keywords}")
                response = ddgs.chat(
                    keywords,
                    model="gpt-4o-mini"
                )
                results = [{
                    'answer': response,
                    'query': keywords
                }]
                
            logger.info(f"Got answer with length: {len(response)}")
            return results
        except Exception as e:
            logger.error(f"Error during answer search: {str(e)}")
            raise

    def search_images(self, keywords, max_results=10):
        results = []
        with DDGS() as ddgs:
            ddgs_gen = ddgs.images(keywords, safesearch='Off', timelimit=None)
            for r in islice(ddgs_gen, max_results):
                results.append(r)
        return results

    def search_videos(self, keywords, max_results=10):
        results = []
        with DDGS() as ddgs:
            ddgs_gen = ddgs.videos(keywords, safesearch='Off', timelimit=None, resolution="high")
            for r in islice(ddgs_gen, max_results):
                results.append(r)
        return results 