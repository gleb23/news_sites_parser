package ua.hlibbabii;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

import java.io.IOException;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.*;

/**
 * Created with IntelliJ IDEA.
 * User: gleb23
 * Date: 06.04.13
 * Time: 22:22
 * To change this template use File | Settings | File Templates.
 */
public class Parser {

    private String url;

    public static class URLNotSpecifiedException extends Throwable {
    }
    public static class URLNotSupportedException extends Throwable {
    }

    private class XPaths {
        XPaths(String title, String text, String theAbstract, String nextPage, String links, String keyWords,
               String author, String date, String dateFormat) {
            this.title = title;
            this.text = text;
            this.theAbstract = theAbstract;
            this.nextPage = nextPage;
            this.links = links;
            this.keyWords = keyWords;
            this.author = author;
            this.date = date;
            this.dateFormat = dateFormat;
        }
        public String title;
        public String text;
        public String theAbstract;
        public String nextPage;
        public String links;
        public String keyWords;
        public String author;
        public String date;
        public String dateFormat;
    }
    XPaths xPaths;

    public Parser(String url) {
        this.url = url;
        xPaths = findXPaths(url);
    }

    private XPaths findXPaths(String url) {
        Map<String, XPaths> siteXPath = new TreeMap<String, XPaths>();

        // known sites

        siteXPath.put("http://www.washingtonpost.com",    //   ok, but date
                new XPaths(
                        ".entry-title"            // title
                        , "article"               // text
                        , ""                  // abstract
                        , "a.next-page"           // next page
                        , ""                        // links      // ссылки на левые сайты
                        , ""                  // key words
                        , "span[class=author vcard]>span.fn"                  // author
                        , "div[class=module byline]>h3>span[class=timestamp updated processed]"  // date
                        , "'Published: 'MMMMM d"                  // date format
                ));
        siteXPath.put("http://www.nytimes.com",
                new XPaths(
                        "nyt_headline"                                              // title
                        , "div.articleBody>nyt_text>p, div.articleBody>p"           // text
                        , ""                                                    // abstract
                        , "div#pageLinks>a.next"                                    // next page
                        , ""                                                        // links
                        , ""                                                    // key words
                        , "nyt_byline>h6.byline>span>span, nyt_byline>h6.byline>span>a>span"    // author
                        , "h6.dateline"                                             // date
                        , "'Published: 'MMMMM d, yyyy"                              // date format
                ));
        siteXPath.put("http://www.sciencenews.org",       // text - ?
                new XPaths(
                        "div.article_page>div.article_title"           // title
                        , "div.content_content>p"                      // text  // ?
                        , "div[class=article_sub_title print-no]"      // abstract
                        ,  ""                                      // next page
                        , "div.side_txt>p>a, div.content_content>p>em>a"         // links
                        , ""                                       // key words
                        , "p[class=print-no article_author]>a[class=anonymous print]"      // author
                        , "p[class=print-no article_date]"             // date
                        , "'Web edition: 'MMMMM dd, yyyy"              // date format
                ));
        // XXX
        siteXPath.put("http://www.reuters.com",       // ok
                new XPaths(
                        "h1"                                                // title
                        , "span#articleText>p"                              // text
                        , "span.focusParagraph>p"                                            // abstract
                        , ""        // next page
                        , ""                                                // links
                        , "div.relatedTopicButtons>div.actionButton"                        // key words
                        , "div#articleInfo>p.byline"                                            // author
                        , "div#articleInfo>p>span.timestamp"                                            // date
                        , "EEE MMM d, yyyy h:mma z"                         // date format
                ));;

        // find the site within our list
        for (String str : siteXPath.keySet()) {
            if (url.startsWith(str)) {
                return siteXPath.get(str);
            }
        }
        return null;
    }

    public String getUrl() {
        return url;
    }

    public void setUrl(String url) {
        this.url = url;
    }

    /**
     * returns <code>org.jsoup.nodes.Document</code> object for current URL
     * @return <code>org.jsoup.nodes.Document</code> object for current URL
     * @throws IOException
     */
    public Document getDocument() throws IOException {
        return Jsoup.connect(url).get();
    }

    /**
     * returns <code>org.jsoup.nodes.Document</code> object for the next page of the article
     * relating to the page represented by <code>doc</code>
     * @param doc - <code>Document</code> that contains the page of the article relating to which
     *            the next one is going to be retrieved
     * @return
     * @throws IOException
     */
    public Document getNextPageDocument(Document doc) throws IOException {
        if (xPaths.nextPage.equals("")) {
            return null;
        }
        Element nextPageElement = doc.select(xPaths.nextPage).first();
        if (nextPageElement == null) {
            // there is no next page : doc - document for the last page of the article
            return null;
        } else {
            String nextPageUrl = nextPageElement.attr("abs:href");
            return Jsoup.connect(nextPageUrl).get();
        }
    }

    public Date parseDate(Document doc){
        if (xPaths.date.equals("")) {
            return null;
        }
        Element date = doc.select(xPaths.date).first();
        if (date != null) {
            Date parsedDate = null;
            String dateString = date.text().trim();
            try {
                parsedDate = new SimpleDateFormat(xPaths.dateFormat, Locale.US).parse(dateString);
                //System.out.println(parsedDate);
            } catch (ParseException e) {}
            return parsedDate;
        } else {
            return null;
        }
    }

    /**
     * returns title from the page represented by <code>currentDocument</code>
     * @param doc
     * @return title from the page represented by <code>currentDocument</code>
     */
    public String parseTitle(Document doc) {
        if (xPaths.title.equals("")) {
            return null;
        }
        Element title = doc.select(xPaths.title).first();
        return title != null ? title.text() : null;
    }

    private String parseAbstract(Document doc) {
        if (xPaths.theAbstract.equals("")) {
            return null;
        }
        Element theAbstract = doc.select(xPaths.theAbstract).first();
        return theAbstract != null ? theAbstract.text() : null;
    }

    /**
     * returns author from the page represented by <code>currentDocument</code>
     * @param currentDocument
     * @return author from the page represented by <code>currentDocument</code>
     */
    public String parseAuthor(Document currentDocument) {
        if (xPaths.author.equals("")) {
            return null;
        }
        Element elm = currentDocument.select(xPaths.author).first();
        return elm != null ? elm.text() : null;
    }

    /**
     * returns text from previous pages + text of the article from the page represented by <code>currentDocument</code>
     * @param currentDocument
     * @param currentText text already grabbed from this article
     * @return text from previous pages + text of the article from the page represented by <code>currentDocument</code>
     */
    void parseArticleContentsFromPage(Document currentDocument,
                                                      StringBuilder currentText, List<String> currentLinksList) {
        Elements textParts = currentDocument.select(xPaths.text);
        for (Element textPart : textParts) {
            currentText.append(textPart.text());
        }
        // get links by adding <a> tag to xpaths
        String[] listTextXPaths = xPaths.text.split(",");
        String linksXPaths = new String();
        for (String s : listTextXPaths) {
            linksXPaths += (s.trim() + ">a, ");
        }
        linksXPaths = linksXPaths.substring(0, linksXPaths.length() - 2);

        Elements links = currentDocument.select(linksXPaths);
        for (Element link : links) {
            currentLinksList.add(link.attr("abs:href"));
        }
    }

    private List<String> parseLinks(Document currentDocument) {
        List<String> linksList = new ArrayList<String>();
        if (xPaths.links.equals("")) {
            return linksList;
        }
        Elements links = currentDocument.select(xPaths.links);
        for (Element link : links) {
            linksList.add(link.attr("abs:href"));
        }

        return linksList;
    }
    /**
     * returns key words from current page represented by <code>currentDocument</code>
     * @param currentDocument
     * @return key words from current page represented by <code>currentDocument</code>
     */
    public List<String> parseKeyWords(Document currentDocument) {
        List<String> keyWordsList = new ArrayList<String>();
        if (xPaths.keyWords.equals("")) {
            return keyWordsList;
        }
        Elements keyWords = currentDocument.select(xPaths.keyWords);
        for (Element keyWord : keyWords) {
            keyWordsList.add(keyWord.text());
        }
        return keyWordsList;
    }

    /**
     *
     * @return
     * @throws ua.hlibbabii.Parser.URLNotSpecifiedException
     * @throws IOException
     */
    public Article parse() throws URLNotSpecifiedException, IOException, URLNotSupportedException {
        if (url == null) {
            throw new URLNotSpecifiedException();
        }
        if (xPaths == null) {
            throw new URLNotSupportedException();
        }
        Document currentPage = getDocument();
        ArticleImpl article = new ArticleImpl();

        article.setTitle(this.parseTitle(currentPage));
        article.setTheAbstract(this.parseAbstract(currentPage));
        article.setKeyWords(this.parseKeyWords(currentPage));
        article.setAuthor(this.parseAuthor(currentPage));
        article.setDateOfPublishing(this.parseDate(currentPage));

        List<String> links = this.parseLinks(currentPage);
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
}
