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

> Note: there are still some imperfections in the text extraction process.

#### Crawling result (final 14 lines; 500 pages @ Computer_Programming)
![Crawling result (final 14 lines; 500 pages @ Computer_Programming)](https://i.gyazo.com/74d523cb93fd143f7200449da251473d.png)

#### Crawling result (final 14 lines; 100 pages @ Cat)
![Crawling result (final 14 lines; 100 pages @ Cat)](https://i.gyazo.com/ba30dd1f052d3fc82ea538e4c6976b8c.png)

#### Crawling result (final 14 lines; 100 pages @ Animal)
![Crawling result (final 14 lines; 100 pages @ Animal)](https://i.gyazo.com/4aceda49195561e6eae6f2caae55cef5.png)

#### Links example (in folder /pages/links)
![Links example (in folder /pages/links)](https://i.gyazo.com/c4f3f1622bd7fa428d0175b259bab00f.png)

#### Words example (in folder /pages/words)
![Words example (in folder /pages/words)](https://i.gyazo.com/21d79339b93c6138e85827fbb256ef25.png)

#### Example search for "coffee"
![Example search for "coffee"](https://i.gyazo.com/1535fe5624fc224875248eed53fb79b0.png)