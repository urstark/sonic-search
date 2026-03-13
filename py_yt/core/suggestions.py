import json
from typing import Union
from urllib.parse import urlencode

from py_yt.core.constants import ResultMode
from py_yt.core.requests import RequestCore


class SuggestionsCore(RequestCore):
    """Gets search suggestions for the given query.

    Args:
        language (str, optional): Sets the suggestion language. Defaults to 'en'.
        region (str, optional): Sets the suggestion region. Defaults to 'US'.

    Examples:
        Calling `result` method gives the search result.

        >>> suggestions = Suggestions(language = 'en', region = 'US').get('Harry Styles', mode = ResultMode.json)
        >>> print(suggestions)
        {
            'result': [
                'harry styles',
                'harry styles treat people with kindness',
                'harry styles golden music video',
                'harry styles interview',
                'harry styles adore you',
                'harry styles watermelon sugar',
                'harry styles snl',
                'harry styles falling',
                'harry styles tpwk',
                'harry styles sign of the times',
                'harry styles jingle ball 2020',
                'harry styles christmas',
                'harry styles live',
                'harry styles juice'
            ]
        }
    """

    def __init__(self, language: str = "en", region: str = "US", timeout: int = None):
        super().__init__()
        self.language = language
        self.region = region
        self.timeout = timeout

    def _post_request_processing(self, mode):
        searchSuggestions = []

        self.__parseSource()
        for element in self.responseSource:
            if type(element) is list:
                for searchSuggestionElement in element:
                    searchSuggestions.append(searchSuggestionElement[0])
                break
        if mode == ResultMode.dict:
            return {"result": searchSuggestions}
        elif mode == ResultMode.json:
            return json.dumps({"result": searchSuggestions}, indent=4)

    async def _get_autocomplete(self, query: str, mode: int) -> Union[dict, str]:
        self.url = (
            "https://clients1.google.com/complete/search"
            + "?"
            + urlencode(
                {
                    "hl": self.language,
                    "gl": self.region,
                    "q": query,
                    "client": "youtube",
                    "gs_ri": "youtube",
                    "ds": "yt",
                }
            )
        )
        await self.__makeAsyncRequest()
        return self._post_request_processing(mode)

    async def _getAsync(
        self, query: str, mode: int = ResultMode.dict
    ) -> Union[dict, str]:
        # Fix: User wants *actual* related suggestions for a query, 
        # not just string completions like "query remix", "query lofi".
        # So we first search to get a video ID, then get related tracks via v1/next.
        searchSuggestions = []
        try:
            from py_yt.search import VideosSearch
            search = VideosSearch(query, limit=1, language=self.language, region=self.region)
            results = await search.next()
            
            video_id = None
            if results and results.get("result"):
                video_id = results["result"][0].get("id")
                
            if video_id:
                from py_yt.core.constants import searchKey
                self.url = f"https://www.youtube.com/youtubei/v1/next?key={searchKey}"
                self.data = {
                    "context": {
                        "client": {
                            "clientName": "WEB",
                            "clientVersion": "2.20240726.00.00",
                            "hl": self.language,
                            "gl": self.region,
                        }
                    },
                    "videoId": video_id
                }
                # Since SuggestionsCore extends RequestCore, we can use asyncPostRequest
                response = await self.asyncPostRequest(client_name="WEB")
                if response and response.status_code == 200:
                    d = response.json()
                    
                    from py_yt.core.componenthandler import getValue
                    
                    # YouTube's standard path for related videos
                    items = getValue(d, ["contents", "twoColumnWatchNextResults", "secondaryResults", "secondaryResults", "results"])
                    
                    if not items:
                        # Sometimes it's nested differently (e.g., mobile web)
                        items = getValue(d, ["contents", "singleColumnWatchNextResults", "results", "results", "contents"])
                        
                        if items:
                            # The mobile web wraps videos in itemSectionRenderer
                            new_items = []
                            for section in items:
                                contents = getValue(section, ["itemSectionRenderer", "contents"])
                                if contents:
                                    new_items.extend([c for c in contents if "compactVideoRenderer" in c])
                            items = new_items

                    if items:
                        for item in items:
                            comp = item.get("compactVideoRenderer")
                            if comp:
                                title = getValue(comp, ["title", "simpleText"])
                                if not title:
                                    title = getValue(comp, ["title", "runs", 0, "text"])
                                if title:
                                    searchSuggestions.append(title)
        except Exception as e:
            import logging
            logging.error(f"Failed to fetch related suggestions for '{query}': {e}")
            
        # If we successfully got related items, return them
        if searchSuggestions:
            # removing duplicates while preserving order
            seen = set()
            unique_suggestions = []
            for s in searchSuggestions:
                if s not in seen:
                    unique_suggestions.append(s)
                    seen.add(s)
            
            if mode == ResultMode.dict:
                return {"result": unique_suggestions}
            elif mode == ResultMode.json:
                return json.dumps({"result": unique_suggestions}, indent=4)
                
        # Fallback to the old autocomplete mechanism if getting related videos fails
        return await self._get_autocomplete(query, mode)

    def __parseSource(self) -> None:
        try:
            start_index = self.response.index("([") + 1
            end_index = self.response.rindex("])") + 1
            self.responseSource = json.loads(self.response[start_index:end_index])
        except (ValueError, json.JSONDecodeError) as e:
            import logging
            logging.error("ERROR: Could not parse YouTube response. Raw response: %r", getattr(self, "response", ""))
            raise Exception("ERROR: Could not parse YouTube response.") from e

    async def __makeAsyncRequest(self) -> None:
        request = await self.asyncGetRequest()
        self.response = request.text
