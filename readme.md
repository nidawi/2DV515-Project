## Assignment Checklist
> Note: I have made no changes to the search engine that I developed for Assignment 3 as it already fulfilled the requirements for A and this fulfills the requirements of A-B for this assignment.

### E
1. ~~Scrape and store raw HTML for at least 200 pages~~
### C-D
1. ~~Parse the raw HTML files to generate a dataset similar to the Wikipedia dataset from Assignment 3~~
2. ~~For each article, the dataset shall contain a file with all words in the article and another file with all outgoing links in the article~~
### A-B
1. ~~Use the dataset with your search engine from Assignment 3~~
2. ~~Use both content-based ranking and PageRank to rank search results~~

### GUI Appearance & Execution Examples
> No changes were made to the client. Results are stored in /pages with respective subfolders /links and /words.

> I started at /wiki/Computer_Programming and crawled 500 pages.
> I then started at /wiki/Cat and crawled another 100 pages.
> Finally, I started at /wiki/Animal and crawled another 100 pages.

> Note: there may still be some imperfections in the text extraction process.

#### Crawling result (final 14 lines; 500 pages @ Computer_Programming)
![Crawling result (final 14 lines; 500 pages @ Computer_Programming)](https://i.gyazo.com/6b8344da9d33f8641f162c3784676411.png)

#### Crawling result (final 14 lines; 100 pages @ Cat)
![Crawling result (final 14 lines; 100 pages @ Cat)](https://i.gyazo.com/ddefd9d0aad0f949c7b14bc0fff38bc1.png)

#### Crawling result (final 14 lines; 100 pages @ Animal)
![Crawling result (final 14 lines; 100 pages @ Animal)](https://i.gyazo.com/621856956343628725669e8f7648aa54.png)

#### Links example (in folder /pages/links)
![Links example (in folder /pages/links)](https://i.gyazo.com/c320580cde65a678132e431a1d8770e5.png)

#### Words example (in folder /pages/words)
![Words example (in folder /pages/words)](https://i.gyazo.com/7ec69a2fe0a968560fc77f56e6fcfea8.png)

#### Example search for "coffee"
![Example search for "coffee"](https://i.gyazo.com/bf368eaaf73de717ffb655b88c34c85d.png)