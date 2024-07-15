import asyncio
import json
from typing import Literal, Sequence

import httpx

from .utils import get_max_items_from_list

class AsyncTavilyClient:
    """
    Async Tavily API client class.
    """


    def __init__(self, api_key: str, company_info_tags: Sequence[str] = ("news", "general", "finance")):
        self._base_data = {
            "api_key": api_key,
        }
        self._client_creator = lambda: httpx.AsyncClient(
            headers={
                "Content-Type": "application/json",
            },
            base_url="https://api.tavily.com",
            timeout=180,
        )
        self._company_info_tags = company_info_tags

    async def _search(
        self,
        query: str,
        search_depth: Literal["basic", "advanced"] = "basic",
        topic: str = "general",
        days: int = 2,
        max_results: int = 5,
        include_domains: Sequence[str] = None,
        exclude_domains: Sequence[str] = None,
        include_answer: bool = False,
        include_raw_content: bool = False,
        include_images: bool = False,
        use_cache: bool = True,
    ) -> dict:
        """
        Internal search method to send the request to the API.
        """
        data = {
            **self._base_data,
            "query": query,
            "search_depth": search_depth,
            "topic": topic,
            "days": days,
            "include_answer": include_answer,
            "include_raw_content": include_raw_content,
            "max_results": max_results,
            "include_domains": include_domains,
            "exclude_domains": exclude_domains,
            "include_images": include_images,
            "use_cache": use_cache,
        }
        async with self._client_creator() as client:
            response = await client.post("/search", content=json.dumps(data))

        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()  # Raises a HTTPError if the HTTP request returned an unsuccessful status code

    async def search(self,
                query: str,
                search_depth: Literal["basic", "advanced"] = "basic",
                topic: Literal["general", "news"] = "general",
                max_results: int = 5,
                include_domains: Sequence[str] = None,
                exclude_domains: Sequence[str] = None,
                include_answer: bool = False,
                include_raw_content: bool = False,
                include_images: bool = False,
                use_cache: bool = True,
                ) -> dict:
        """
        Combined search method. Set search_depth to either "basic" or "advanced".
        """
        response_dict = await self._search(query,
                                  search_depth=search_depth,
                                  topic=topic,
                                  max_results=max_results,
                                  include_domains=include_domains,
                                  exclude_domains=exclude_domains,
                                  include_answer=include_answer,
                                  include_raw_content=include_raw_content,
                                  include_images=include_images,
                                  use_cache=use_cache,
                                  )
        
        tavily_results = response_dict.get("results", [])

        response_dict["results"] = tavily_results

        return response_dict

    async def get_search_context(self,
                                query: str,
                                search_depth: Literal["basic", "advanced"] = "basic",
                                topic: Literal["general", "news"] = "general",
                                max_results: int = 5,
                                include_domains: Sequence[str] = None,
                                exclude_domains: Sequence[str] = None,
                                use_cache: bool = True,
                                max_tokens: int = 4000,
                                ) -> str:
        """
        Get the search context for a query. Useful for getting only related content from retrieved websites
        without having to deal with context extraction and limitation yourself.

        max_tokens: The maximum number of tokens to return (based on openai token compute). Defaults to 4000.

        Returns a string of JSON containing the search context up to context limit.
        """
        response_dict = await self._search(query,
                            search_depth=search_depth,
                            topic=topic,
                            max_results=max_results,
                            include_domains=include_domains,
                            exclude_domains=exclude_domains,
                            include_answer=False,
                            include_raw_content=False,
                            include_images=False,
                            use_cache=use_cache,
                            )
        sources = response_dict.get("results", [])
        context = [{"url": source["url"], "content": source["content"]} for source in sources]
        return json.dumps(get_max_items_from_list(context, max_tokens))

    async def qna_search(self,
                query: str,
                search_depth: Literal["basic", "advanced"] = "advanced",
                topic: Literal["general", "news"] = "general",
                max_results: int = 5,
                include_domains: Sequence[str] = None,
                exclude_domains: Sequence[str] = None,
                use_cache: bool = True,
                ) -> str:
        """
        Q&A search method. Search depth is advanced by default to get the best answer.
        """
        response_dict = await self._search(query,
                    search_depth=search_depth,
                    topic=topic,
                    max_results=max_results,
                    include_domains=include_domains,
                    exclude_domains=exclude_domains,
                    include_raw_content=False,
                    include_images=False,
                    include_answer=True,
                    use_cache=use_cache,
                    )
        return response_dict.get("answer", "")

    async def get_company_info(self,
                query: str,
                search_depth: Literal["basic", "advanced"] = "advanced",
                max_results: int = 5,
                ) -> Sequence[dict]:
        """ Company information search method. Search depth is advanced by default to get the best answer. """

        async def _perform_search(topic: str):
            return await self._search(query,
                                search_depth=search_depth,
                                topic=topic,
                                max_results=max_results,
                                include_answer=False,)

        all_results = []
        for data in await asyncio.gather(*[_perform_search(topic) for topic in self._company_info_tags]):
            if "results" in data:
                all_results.extend(data["results"])

        # Sort all the results by score in descending order and take the top 'max_results' items
        sorted_results = sorted(all_results, key=lambda x: x["score"], reverse=True)[:max_results]

        return sorted_results
