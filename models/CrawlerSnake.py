import asyncio
import aiohttp
import aiofile
import re
import itertools
from timeit import default_timer as timer
from typing import Set, List, Tuple
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from models.DepthObserver import DepthObserver

ORIGIN_ID = "origin"
SESSION_ID = "session"
LINK_SELECTION_STRATS_ID = "link_strats"
CRAWL_SELECTION_STRATS_ID = "selection_strats"
TEXT_STRAT_ID = "text_strat"
OBSERVER_ID = "observer"
DIR_ID = "dir"
MAX_ID = "max"
DEBUG_ID = "debug"

LINKS_FOLDER_NAME = "Links"
WORDS_FOLDER_NAME = "Words"

# Experimental recursive web crawler
class CrawlerSnake(DepthObserver, object):
  """
  Is a happy snake.
  """
  async def __new__(cls, *args, **kwargs):
    # Now this is an interesting way to do things!
    # From my understanding:
    # async def X is considered different from def X (maybe because async def is converted into a task?)
    # since def __init__ is not defined, Python does not call async def __init__ in its place
    # which is why we have to call it manually here while still avoiding double __init__ calls
    # which you would suffer from if you did this with normal def __new__ and __init__.
    instance = super().__new__(cls)
    await instance.__init__(*args, **kwargs)
    return instance

  async def __init__(self, url: str, **kwargs):
    super().__init__()

    # Create variables
    self.__current_depth = 1

    # Construct crawl url
    origin = kwargs[ORIGIN_ID] if ORIGIN_ID in kwargs else None
    self.__page_url, self.__partial_url, self.__name = self.__parse_url(origin, url)

    # Extract kwargs
    # todo: some of these do not need to be instance variables
    self.__session = kwargs[SESSION_ID] if SESSION_ID in kwargs else aiohttp.ClientSession()
    self.__link_selection_strategies = kwargs[LINK_SELECTION_STRATS_ID] if LINK_SELECTION_STRATS_ID in kwargs else []
    self.__crawl_selection_strategies = kwargs[CRAWL_SELECTION_STRATS_ID] if CRAWL_SELECTION_STRATS_ID in kwargs else []
    self.__text_strategy = kwargs[TEXT_STRAT_ID] if TEXT_STRAT_ID in kwargs else None
    self.__depth_observer = kwargs[OBSERVER_ID] if OBSERVER_ID in kwargs else self
    self.__dir = kwargs[DIR_ID] if DIR_ID in kwargs else None
    self.__max = kwargs[MAX_ID] if MAX_ID in kwargs else 0
    self.__debug_enabled = kwargs[DEBUG_ID] if DEBUG_ID in kwargs else False

    # Start timer + debug
    self.__time = timer()
    self.__debug("Crawling job started for %s!" % self.__name)

    # Crawl the given url
    self.__html = await self.__crawl()

    # Perform work on the current page
    self.__raw_links = self.__get_links()
    self.__raw_text = self.__get_text()

    # If dir has been specified, dump links and text
    if self.__dir:
      await self.__dump_page_contents()

    # Crawl all links contained on the page using asyncio wait/gather
    links_to_crawl = self.__get_links_to_crawl()

    # Then we recursively crawl whatever links remain
    self.__links = await asyncio.gather(
      *[CrawlerSnake(
        link,
        debug=self.__debug_enabled,
        session=self.__session,
        origin=origin if origin is not None else self.__page_url,
        observer=self.__depth_observer,
        max=self.__max,
        dir=self.__dir,
        link_strats=self.__link_selection_strategies,
        selection_strats=self.__crawl_selection_strategies,
        text_strat=self.__text_strategy
        ) for link in links_to_crawl]
    )

    self.__time = round(timer() - self.__time, 2)
    self.__debug("Finished crawling job for %s after %s seconds (%s links out of %s total)." % (self.__name, self.__time, len(self.__links), len(self.__raw_links)))

  def get_completion_time(self) -> float:
    return self.__time

  def get_total_count(self) -> int:
    return self.__current_depth

  def get_links(self) -> List["CrawlerSnake"]:
    return self.__links

  def get_name(self) -> str:
    return self.__name

  def get_path(self) -> str:
    return self.__partial_url

  async def __crawl(self) -> BeautifulSoup:
    """
    Crawls the provided page and returns a BeautifulSoup object describing the result.
    """
    response = await self.__session.get(self.__page_url)
    raw_text = await response.text()
    return BeautifulSoup(raw_text, "html.parser")

  def __parse_url(self, origin: str, page_url: str) -> Tuple[str, str, str]:
    """
    Parses the provided url and returns a tuple representing:

    >>> (actual_url: str, path: str, name: str)
    """
    origin_parse = urlparse(origin)
    path_parse = urlparse(page_url)

    actual_url = "%s://%s%s" % (origin_parse.scheme, origin_parse.netloc, page_url) if origin else page_url
    path = page_url if origin else path_parse.path
    name = path_parse.path.rpartition("/")[-1]

    return (actual_url, path, name)

  def __get_links(self) -> Set[str]:
    """
      Returns a set of all links contained in the page as strings.

      This method uses the link selection strategies.
    """
    # I think the performance is pretty bad here.
    links = self.__html.find_all("a")
    hrefs = map(lambda x : x.get("href"), links)
    basic_filter = filter(lambda x : x is not None, hrefs)
    # Check the potential link with all strategies.
    valid = filter(lambda x : all(strat.is_tasty(x) for strat in self.__link_selection_strategies),
      basic_filter)
    # Perform final validations: not self + not duplicate
    not_self = filter(lambda x : x != self.__partial_url, valid)
    not_duplicate = { link.casefold() : link for link in not_self }

    return set(not_duplicate.values())

  def __get_links_to_crawl(self) -> List[str]:
    """
    Returns a list of links to crawl as strings.

    This method uses the crawl selection strategies.
    """
    # First, we ask for the current depth
    depth = self.__depth_observer._get_current_depth()
    # We use our strategies to select links of interest
    links_of_interest = list(filter(lambda x : all(strat.is_tasty(x) for strat in self.__crawl_selection_strategies),
      list(self.__raw_links)))
    # We select an appropriate amount of links to crawl based on depth
    links_to_crawl = links_of_interest[0:self.__max - depth]
    # Then we update the depth based on our links
    crawl_count = len(links_to_crawl)
    self.__depth_observer._update_depth(crawl_count)

    self.__debug(f"{self.__name} selected {crawl_count} out of {len(links_of_interest)} potential links ({len(self.__raw_links)} total). Current depth: {depth}; new depth: {self.__depth_observer._get_current_depth()}")

    return links_to_crawl

  def __get_text(self) -> str:
    """
    Extracts text from the page based on element type.
    """
    raw_text = self.__html.body
    text = self.__text_strategy.get_text(raw_text) if self.__text_strategy else raw_text.get_text()

    return text

  async def __dump_page_contents(self) -> None:
    await asyncio.gather(
      self.__dump_links(),
      self.__dump_text()
    )

  async def  __dump_links(self) -> None:
    # We need to dump links into /links
    links_dir = f"{self.__dir}/{LINKS_FOLDER_NAME}/{self.__name}"
    async with aiofile.AIOFile(links_dir, "w+") as file:
      writer = aiofile.Writer(file)
      output = "\n".join(self.__raw_links)
      await writer(output)

  async def __dump_text(self) -> None:
    # and words into /words
    words_dir = f"{self.__dir}/{WORDS_FOLDER_NAME}/{self.__name}"
    async with aiofile.AIOFile(words_dir, "w+") as file:
      writer = aiofile.Writer(file)
      await writer(self.__raw_text)

  def __debug(self, message: str) -> None:
    if self.__debug_enabled:
      print(message)

  # Depth Observer (recursive)
  def _get_current_depth(self) -> None:
    return min(self.__current_depth, self.__max)

  def _update_depth(self, amount: int) -> None:
    self.__current_depth += amount