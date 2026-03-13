from typing import Any, Dict, Optional

from py_yt.core.constants import SearchMode
from py_yt.core.search import SearchCore


class Search(SearchCore):
    """Searches for videos, channels & playlists in YouTube.

    Args:
        query (str): Sets the search query.
        limit (int, optional): Sets limit to the number of results. Defaults to 20.
        language (str, optional): Sets the result language. Defaults to 'en'.
        region (str, optional): Sets the result region. Defaults to 'US'.

    Examples:
        Calling `result` method gives the search result.

        >>> search = Search('Watermelon Sugar', limit = 1)
        >>> result = await search.next()
        >>> print(result)
        {
            "result": [
                {
                    "type": "video",
                    "id": "E07s5ZYygMg",
                    "title": "Harry Styles - Watermelon Sugar (Official Video)",
                    "publishedTime": "6 months ago",
                    "duration": "3:09",
                    "viewCount": {
                        "text": "162,235,006 views",
                        "short": "162M views"
                    },
                    "thumbnails": [
                        {
                            "url": "https://i.ytimg.com/vi/E07s5ZYygMg/hq720.jpg?sqp=-oaymwEjCOgCEMoBSFryq4qpAxUIARUAAAAAGAElAADIQj0AgKJDeAE=&rs=AOn4CLAOWBTE1SDrtrDQ1aWNzpDZ7YiMIw",
                            "width": 360,
                            "height": 202
                        },
                        {
                            "url": "https://i.ytimg.com/vi/E07s5ZYygMg/hq720.jpg?sqp=-oaymwEXCNAFEJQDSFryq4qpAwkIARUAAIhCGAE=&rs=AOn4CLD7U54pGZLPKTuMP-J3kpm4LIDPVg",
                            "width": 720,
                            "height": 404
                        }
                    ],
                    "descriptionSnippet": [
                        {
                            "text": "This video is dedicated to touching. Listen to Harry Styles' new album 'Fine Line' now: https://HStyles.lnk.to/FineLineAY Follow\u00a0..."
                        }
                    ],
                    "channel": {
                        "name": "Harry Styles",
                        "id": "UCZFWPqqPkFlNwIxcpsLOwew",
                        "thumbnails": [
                            {
                                "url": "https://yt3.ggpht.com/a-/AOh14GgNUvHxwlnz4RpHamcGnZF1px13VHj01TPksw=s68-c-k-c0x00ffffff-no-rj-mo",
                                "width": 68,
                                "height": 68
                            }
                        ],
                        "link": "https://www.youtube.com/channel/UCZFWPqqPkFlNwIxcpsLOwew"
                    },
                    "accessibility": {
                        "title": "Harry Styles - Watermelon Sugar (Official Video) by Harry Styles 6 months ago 3 minutes, 9 seconds 162,235,006 views",
                        "duration": "3 minutes, 9 seconds"
                    },
                    "link": "https://www.youtube.com/watch?v=E07s5ZYygMg",
                    "shelfTitle": null
                }
            ]
        }
    """

    def __init__(
        self,
        query: str,
        limit: int = 20,
        language: str = "en",
        region: str = "US",
        timeout: Optional[int] = None,
        with_live: bool = True,
        max_retries: int = 0,
    ):
        self.searchMode = (True, True, True)
        super().__init__(
            query, limit, language, region, None, timeout, with_live=with_live, max_retries=max_retries
        )  # type: ignore

    async def next(self) -> Dict[str, Any]:
        return await self._nextAsync()  # type: ignore


class VideosSearch(SearchCore):
    """Searches for videos in YouTube.

    Args:
        query (str): Sets the search query.
        limit (int, optional): Sets limit to the number of results. Defaults to 20.
        language (str, optional): Sets the result language. Defaults to 'en'.
        region (str, optional): Sets the result region. Defaults to 'US'.

    Examples:
        Calling `result` method gives the search result.

        >>> search = VideosSearch('Watermelon Sugar', limit = 1)
        >>> result = await search.next()
        >>> print(result)
        {
            "result": [
                {
                    "type": "video",
                    "id": "E07s5ZYygMg",
                    "title": "Harry Styles - Watermelon Sugar (Official Video)",
                    "publishedTime": "6 months ago",
                    "duration": "3:09",
                    "viewCount": {
                        "text": "162,235,006 views",
                        "short": "162M views"
                    },
                    "thumbnails": [
                        {
                            "url": "https://i.ytimg.com/vi/E07s5ZYygMg/hq720.jpg?sqp=-oaymwEjCOgCEMoBSFryq4qpAxUIARUAAAAAGAElAADIQj0AgKJDeAE=&rs=AOn4CLAOWBTE1SDrtrDQ1aWNzpDZ7YiMIw",
                            "width": 360,
                            "height": 202
                        },
                        {
                            "url": "https://i.ytimg.com/vi/E07s5ZYygMg/hq720.jpg?sqp=-oaymwEXCNAFEJQDSFryq4qpAwkIARUAAIhCGAE=&rs=AOn4CLD7U54pGZLPKTuMP-J3kpm4LIDPVg",
                            "width": 720,
                            "height": 404
                        }
                    ],
                    "descriptionSnippet": [
                        {
                            "text": "This video is dedicated to touching. Listen to Harry Styles' new album 'Fine Line' now: https://HStyles.lnk.to/FineLineAY Follow\u00a0..."
                        }
                    ],
                    "channel": {
                        "name": "Harry Styles",
                        "id": "UCZFWPqqPkFlNwIxcpsLOwew",
                        "thumbnails": [
                            {
                                "url": "https://yt3.ggpht.com/a-/AOh14GgNUvHxwlnz4RpHamcGnZF1px13VHj01TPksw=s68-c-k-c0x00ffffff-no-rj-mo",
                                "width": 68,
                                "height": 68
                            }
                        ],
                        "link": "https://www.youtube.com/channel/UCZFWPqqPkFlNwIxcpsLOwew"
                    },
                    "accessibility": {
                        "title": "Harry Styles - Watermelon Sugar (Official Video) by Harry Styles 6 months ago 3 minutes, 9 seconds 162,235,006 views",
                        "duration": "3 minutes, 9 seconds"
                    },
                    "link": "https://www.youtube.com/watch?v=E07s5ZYygMg",
                    "shelfTitle": null
                }
            ]
        }
    """

    def __init__(
        self,
        query: str,
        limit: int = 20,
        language: str = "en",
        region: str = "US",
        timeout: Optional[int] = None,
        with_live: bool = True,
        max_retries: int = 0,
    ):
        self.searchMode = (True, False, False)
        super().__init__(
            query,
            limit,
            language,
            region,
            SearchMode.videos,
            timeout,
            with_live=with_live,
            max_retries=max_retries,
        )

    async def next(self) -> Dict[str, Any]:
        return await self._nextAsync()  # type: ignore

class PlaylistsSearch(SearchCore):
    """Searches for playlists in YouTube.

    Args:
        query (str): Sets the search query.
        limit (int, optional): Sets limit to the number of results. Defaults to 20.
        language (str, optional): Sets the result language. Defaults to 'en'.
        region (str, optional): Sets the result region. Defaults to 'US'.

    Examples:
        Calling `result` method gives the search result.

        >>> search = PlaylistsSearch('Harry Styles', limit = 1)
        >>> result = await search.next()
        >>> print(result)
        {
            "result": [
                {
                    "type": "playlist",
                    "id": "PL-Rt4gIwHnyvxpEl-9Le0ePztR7WxGDGV",
                    "title": "fine line harry styles full album lyrics",
                    "videoCount": "12",
                    "channel": {
                        "name": "ourmemoriestonight",
                        "id": "UCZCmb5a8LE9LMxW9I3-BFjA",
                        "link": "https://www.youtube.com/channel/UCZCmb5a8LE9LMxW9I3-BFjA"
                    },
                    "thumbnails": [
                        {
                            "url": "https://i.ytimg.com/vi/raTh8Mu5oyM/hqdefault.jpg?sqp=-oaymwEWCKgBEF5IWvKriqkDCQgBFQAAiEIYAQ==&rs=AOn4CLCdCfOQYMrPImHMObdrMcNimKi1PA",
                            "width": 168,
                            "height": 94
                        },
                        {
                            "url": "https://i.ytimg.com/vi/raTh8Mu5oyM/hqdefault.jpg?sqp=-oaymwEWCMQBEG5IWvKriqkDCQgBFQAAiEIYAQ==&rs=AOn4CLDsKmyGH8bkmt9MzZqIoXI4UaduBw",
                            "width": 196,
                            "height": 110
                        },
                        {
                            "url": "https://i.ytimg.com/vi/raTh8Mu5oyM/hqdefault.jpg?sqp=-oaymwEXCPYBEIoBSFryq4qpAwkIARUAAIhCGAE=&rs=AOn4CLD9v7S0KeHLBLr0bF-LrRjYVycUFA",
                            "width": 246,
                            "height": 138
                        },
                        {
                            "url": "https://i.ytimg.com/vi/raTh8Mu5oyM/hqdefault.jpg?sqp=-oaymwEXCNACELwBSFryq4qpAwkIARUAAIhCGAE=&rs=AOn4CLAIzQIVxZsC0PfvLOt-v9UWJ-109Q",
                            "width": 336,
                            "height": 188
                        }
                    ],
                    "link": "https://www.youtube.com/playlist?list=PL-Rt4gIwHnyvxpEl-9Le0ePztR7WxGDGV"
                }
            ]
        }
    """

    def __init__(
        self,
        query: str,
        limit: int = 20,
        language: str = "en",
        region: str = "US",
        timeout: Optional[int] = None,
        max_retries: int = 0,
    ):
        self.searchMode = (False, False, True)
        super().__init__(query, limit, language, region, SearchMode.playlists, timeout, max_retries=max_retries)  # type: ignore

    async def next(self) -> Dict[str, Any]:
        return await self._nextAsync()  # type: ignore

