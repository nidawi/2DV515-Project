from urllib import robotparser, parse
from models.Tastebuds import Tastebuds

storedPermissions = {}

class Chewable(Tastebuds):
  """
  Determines whether the provided target url is chewable (crawlable).

  Looks at the source's Robots.txt.

  @todo : Handle non-existent robots.txt
  """
  def __init__(self, root_url: str, user_agent: str):
    self.__parser = robotparser.RobotFileParser()

    # Parse the URL
    url_parse = parse.urlparse(root_url)
    robotsPath = "%s://%s/robots.txt" % (url_parse.scheme, url_parse.netloc)
    
    self.__parser.set_url(robotsPath)
    self.__user_agent = user_agent
    self.__parser.read()

  def is_tasty(self, page_url: str, **kwargs) -> bool:
    if page_url in storedPermissions:
      return storedPermissions[page_url]
    else:
      result = self.__parser.can_fetch(self.__user_agent, page_url)
      storedPermissions[page_url] = result
      return result