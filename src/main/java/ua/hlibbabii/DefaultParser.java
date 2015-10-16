/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package ua.hlibbabii;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

import java.io.IOException;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.Locale;

/**
 * Default implementation of news parser. 
 * Site meta-data must be specified for every site. 
 * Method <code>getSiteMetaData()</code> must be overridden.
 * If necessary, other methods can be also overridden
 * 
 * @author gleb23
 */
public abstract class DefaultParser {
    
    /**
     * Returns meta-data for site to be parsed. 
     * Must be overridden in subclasses.
     * @return meta-data for site to be parsed
     */
    abstract public SiteMetaData getSiteMetaData();
    
     /**
     * Parses the current page or the next ones as well if the article is on
     * several pages and returns the article as <code>Article</code>
     * object
     * @param url URL of the page that contains the first page of the article 
     * to be parsed
     * @return the article as <code>Article</code> object
     * @throws IOException on error
     */
    public Article parse(String url) throws IOException{
        Document currentPage = getDocument(url);
        ArticleImpl article = new ArticleImpl();

        article.setTitle(parseTitle(currentPage));
        article.setTheAbstract(parseAbstract(currentPage));
        article.setKeyWords(parseKeyWords(currentPage));
        article.setAuthor(parseAuthor(currentPage));
        article.setDateOfPublishing(parseDate(currentPage));

        //List<String> links = this.parseLinks(currentPage);
        List<String> links = new ArrayList<>();
        StringBuilder text = new StringBuilder();
        // until we have read all the pages
        while (currentPage != null) {
            parseArticleContentsFromPage(currentPage, text, links);
            currentPage = getNextPageDocument(currentPage);
        }
        article.setText(text.toString());
        article.setLinks(links);

        return article;
    }
    
    /**
     * Returns links to pages with articles
     * @param <code>nLinks</code> the number of links to return 
     * @return links to pages with articles
     * @throws IOException on error
     */
    public List<String> getLinksFromMainPage(int nLinks) 
            throws IOException {
        List<String> allLinks = new ArrayList<>();
        boolean stopRetrieving;
        if (nLinks == 0) {
            stopRetrieving = true;
        } else {
            stopRetrieving = false;            
        }
        for (SiteMetaData.PageToGetLinks page : getSiteMetaData().newsPages) {
            if (stopRetrieving) {
                break;
            }
            int pageNumber = 1;
            String url = String.format(page.url, pageNumber);
            Document currentPage = getDocument(url);
            Elements linksOnCurrentPage = currentPage.select(page.linkXPath);
            while (!linksOnCurrentPage.isEmpty() && !stopRetrieving) {
                for (Element linkOnCurrentPage : linksOnCurrentPage ) {
                    allLinks.add(linkOnCurrentPage.attr("abs:href"));
                    if (allLinks.size() >= nLinks) {
                        stopRetrieving = true;
                        break;
                    }
                }
                url = String.format(page.url, ++pageNumber);
                currentPage = getDocument(url);
                linksOnCurrentPage = currentPage.select(page.linkXPath);
            }
        }
        return allLinks;
    }
        
    /**
     * returns <code>org.jsoup.nodes.Document</code> object for current URL
     * @param url URL to get Document from
     * @return <code>org.jsoup.nodes.Document</code> object for current URL
     * @throws IOException on error
     */
    protected Document getDocument(String url) throws IOException{
        return Jsoup.connect(url).timeout(0).get();
    }

    /**
     * returns <code>org.jsoup.nodes.Document</code> object for the next page 
     * of the article relating to the page represented by <code>doc</code>
     * @param doc - <code>org.jsoup.nodes.Document</code> 
     * that represents the current page
     * @return <code>org.jsoup.nodes.Document</code> object for the next page 
     * of the article
     * @throws IOException on error
     */
    protected Document getNextPageDocument(Document doc) throws IOException {
        if (getSiteMetaData().nextPageXPath == null) {
            return null;
        }
        Element nextPageElement = doc.select(getSiteMetaData().nextPageXPath).first();
        if (nextPageElement == null) {
            // there is no next page : doc - document for the last page of the article
            return null;
        } else {
            String nextPageUrl = nextPageElement.attr("abs:href");
            return Jsoup.connect(nextPageUrl).get();
        }
    }

    /**
     * Returns the date when the article was published.
     * @param doc <code>org.jsoup.nodes.Document</code> 
     * that represents the current page
     * @return the date when the article was published
     */
    protected Date parseDate(Document doc){
        if (getSiteMetaData().dateXPath == null) {
            return null;
        }
        Element date = doc.select(getSiteMetaData().dateXPath).first();
        if (date != null) {
            Date parsedDate = null;
            String dateString = date.text().trim();
            try {
                parsedDate = new SimpleDateFormat(getSiteMetaData().dateFormat, Locale.US).parse(dateString);
            } catch (ParseException e) {}
            return parsedDate;
        } else {
            return null;
        }
    }

    /**
     * returns the title of the article
     * @param doc <code>org.jsoup.nodes.Document</code> 
     * that represents the current page
     * @return the title of the article
     */
    protected String parseTitle(Document doc) {
        if (getSiteMetaData().titleXPath == null) {
            return null;
        }
        Element title = doc.select(getSiteMetaData().titleXPath).first();
        return title != null ? title.text() : null;
    }

    /**
     * Returns the abstract of the article or paragraph that is set off
     * somehow and refers neither to title, nor to text
     * @param doc <code>org.jsoup.nodes.Document</code> 
     * that represents the current page
     * @return the abstract of the article
     */
    protected String parseAbstract(Document doc) {
        if (getSiteMetaData().abstractXPath  == null) {
            return null;
        }
        Element theAbstract = doc.select(getSiteMetaData().abstractXPath).first();
        return theAbstract != null ? theAbstract.text() : null;
    }

    /**
     * returns the author of the article
     * @param currentDocument <code>org.jsoup.nodes.Document</code> 
     * that represents the current page
     * @return the author of the article
     */
    protected String parseAuthor(Document currentDocument) {
        if (getSiteMetaData().authorXPath == null) {
            return null;
        }
        Element elm = currentDocument.select(getSiteMetaData().authorXPath).first();
        return elm != null ? elm.text() : null;
    }


    /**
     * Gets text and links from the current page of the article represented
     * by <code>currentDocument</code> and adds them to <code>currentText</code>
     * and to <code>currentLinksList</code> respectively.
     * @param currentDocument <code>org.jsoup.nodes.Document</code> 
     * that represents the current page
     * @param currentText container where gathered text is added 
     * @param currentLinksList container where gathered links is added
     */
    protected void parseArticleContentsFromPage(Document currentDocument,
                                                      StringBuilder currentText, List<String> currentLinksList) {
        Elements textParts = currentDocument.select(getSiteMetaData().textXPath);
        for (Element textPart : textParts) {
            currentText.append(textPart.text());
        }

        Elements links = currentDocument.select(getSiteMetaData().linksXPath);
        for (Element link : links) {
            currentLinksList.add(link.attr("abs:href"));
        }
    }

    /**
     * returns key all links from the article on the current page represented by
     * <code>currentDocument</code>
     * @param currentDocument <code>org.jsoup.nodes.Document</code> 
     * that represents the current page
     * @return key all links from the article on the current page represented by
     * <code>currentDocument</code>
     */
    protected List<String> parseLinks(Document currentDocument) {
        List<String> linksList = new ArrayList<>();
        if (getSiteMetaData().linksXPath == null) {
            return linksList;
        }
        Elements links = currentDocument.select(getSiteMetaData().linksXPath);
        for (Element link : links) {
            linksList.add(link.attr("abs:href"));
        }

        return linksList;
    }
    
    /**
     * returns key words to the article
     * @param currentDocument <code>org.jsoup.nodes.Document</code> 
     * that represents the current page
     * @return key words to the article
     */
    protected List<String> parseKeyWords(Document currentDocument) {
        List<String> keyWordsList = new ArrayList<>();
        if (getSiteMetaData().keyWordsXPath == null) {
            return keyWordsList;
        }
        Elements keyWords = currentDocument.select(getSiteMetaData().keyWordsXPath);
        for (Element keyWord : keyWords) {
            keyWordsList.add(keyWord.text());
        }
        return keyWordsList;
    }    
}
