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
    sup_tag = "sup"

    div = soup.find(id=article_div) # extract div
    p_elems = div.find_all(paragraph_elem) # extract p elements

    # get rid of wikipedia-specific nested tags that disrupt text results
    for p in p_elems:
      for sup in p.find_all(sup_tag):
        sup.decompose()

    paragraphs = list(map(lambda x : x.get_text().lower(), p_elems)) # extract text from all p-elements
    paragraphs_text = list(map(lambda x : re.sub(r"(\[\d+\]|[^a-z0-9åäö \-])", "", x), paragraphs)) # replace all invalid characters (preserves åäö)
    only_text = " ".join(para for para in paragraphs_text) # join the paragraphs into a single text
    fixed_text = re.sub(r" {2,}", " ", only_text).strip() # remove all double spaces + trailing / preceding spaces

    return fixed_text