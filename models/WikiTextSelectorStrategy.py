import re
from bs4 import BeautifulSoup
from models.TextSelectorStrategy import TextSelectorStrategy

class WikiTextSelectorStrategy(TextSelectorStrategy):
  """
  A TextSelectionStrategy that extracts text from a wikipedia article.
  """
  def get_text(self, soup: BeautifulSoup) -> str:
    """
    Extracts text from a wikipedia article.
    """
    # Wikipedia article text is contained in div with id: "mw-content-text"
    # and then each paragraph is its own separate <p>-tag.
    article_div = "mw-content-text"
    paragraph_elem = "p"

    # todo: does not deal properly with elements nested within p-tags such as:
    # <sup class="noprint Inline-Template Template-Fact" style="white-space:nowrap;">&#91;<i><a href="/wiki/Wikipedia:Citation_needed" title="Wikipedia:Citation needed"><span title="This claim needs references to reliable sources. (January 2019)">citation needed</span>

    div = soup.find(id=article_div) # extract div
    paragraphs = list(map(lambda x : x.get_text().lower(), div.find_all(paragraph_elem))) # extract text from all p-elements
    paragraphs_text = list(map(lambda x : re.sub(r"(\[\d+\]|[^a-z0-9åäö \-])", "", x), paragraphs)) # replace all invalid characters (preserves åäö)
    only_text = " ".join(para for para in paragraphs_text) # join the paragraphs into a single text
    fixed_text = re.sub(r" {2,}", " ", only_text) # remove all double spaces

    return fixed_text