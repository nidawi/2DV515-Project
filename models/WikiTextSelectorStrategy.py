import re
from bs4 import BeautifulSoup
from models.TextSelectorStrategy import TextSelectorStrategy

class WikiTextSelectorStrategy(TextSelectorStrategy):
  def get_text(self, soup: BeautifulSoup) -> str:
    # Wikipedia article text is contained in div with id: "mw-content-text"
    # and then each paragraph is its own separate <p>-tag.
    article_div = "mw-content-text"
    paragraph_elem = "p"

    div = soup.find(id=article_div)
    paragraphs = list(map(lambda x : x.get_text().lower(), div.find_all(paragraph_elem)))
    paragraphs_text = list(map(lambda x : re.sub(r"[^a-zA-Z0-9 ]", "", x), paragraphs)) # still do not deal with cites, eg. [25] and there's some awkward spacing?
    only_text = "".join(para for para in paragraphs_text)

    return only_text