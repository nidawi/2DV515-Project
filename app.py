import asyncio
import aiohttp
from models.CrawlerSnake import CrawlerSnake
from models.TastyWikiURL import TastyWikiURL
from models.AlreadyEaten import AlreadyEaten
from models.WikiTextSelectorStrategy import WikiTextSelectorStrategy
from models.Chewable import Chewable

ROOT_URL = "https://wikipedia.org/wiki/Computer_programming"
DUMP_DIR = "./pages"
MAX_PAGES = 400
DEBUG = True

async def main():
  chewableStrategy = Chewable(ROOT_URL, "*") # Checks if the root's robots.txt allows us (*) to crawl their pages.
  tastyUrlStrategy = TastyWikiURL() # Checks if the page is a valid Wiki link, /wiki/...
  alreadyEaten = AlreadyEaten() # Verifies that the same page isn't crawled twice (optional since you may not want this)
  textStrategy = WikiTextSelectorStrategy() # Collects and returns words from a wikipedia article

  async with aiohttp.ClientSession() as session:
    snake = await CrawlerSnake(
      ROOT_URL,
      debug=DEBUG,
      dir=DUMP_DIR,
      max=MAX_PAGES,
      session=session,
      link_strats=[tastyUrlStrategy, chewableStrategy],
      selection_strats=[alreadyEaten],
      text_strat=textStrategy
      )
    
    print(f"Crawled pages have been saved to {DUMP_DIR}. A total of {snake.get_total_count()} pages were crawled in {snake.get_completion_time()} seconds.")

if __name__ == "__main__":
  async_loop = asyncio.get_event_loop()
  async_loop.run_until_complete(main())