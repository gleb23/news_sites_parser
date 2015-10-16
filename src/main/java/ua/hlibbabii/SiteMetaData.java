/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package ua.hlibbabii;

/**
 * Meta-data of site to be parsed
 * 
 * @author gleb23
 */
public class SiteMetaData {
        public SiteMetaData(String titleXPath, String textXPath, String abstractXPath, String nextPageXPath, String linksXPath, String keyWordsXPath,
               String authorXPath, String dateXPath, String dateFormat, PageToGetLinks[] newsPages) {
            this.titleXPath = titleXPath;
            this.textXPath = textXPath;
            this.abstractXPath = abstractXPath;
            this.nextPageXPath = nextPageXPath;
            this.linksXPath = linksXPath;
            this.keyWordsXPath = keyWordsXPath;
            this.authorXPath = authorXPath;
            this.dateXPath = dateXPath;
            this.dateFormat = dateFormat;
            this.newsPages = newsPages;
        }
        /**
         * xPath for the title of the article
         */
        public String titleXPath;
        
        /**
         * xPath for the text of the article 
         */
        public String textXPath;
        
        /**
         * xPath for the abstract of the article
         */
        public String abstractXPath;
        
        /**
         * xPath for the link to the next page
         */
        public String nextPageXPath;
        
        /**
         * xPath for the links in the article's text
         */
        public String linksXPath;
        
        /**
         * xPath for the key words of the article
         */
        public String keyWordsXPath;
        
        /**
         * xPath for the author of the article
         */
        public String authorXPath;
        
        /**
         * xPath for the date when the article was published
         */
        public String dateXPath;
        
        /**
         * date format which date for this article written in
         */
        public String dateFormat;
        
        /**
         * array of <code>PageToGetLinks</code> objects
         * @see PageToGetLinks
         */
        public PageToGetLinks[] newsPages;

        /**
         * Structure that contains meta-data to extract links to articles from
         * the site
         */
        public static class PageToGetLinks {
            /**
             * URL to get links from
             */
            public String url;
            
            /**
             * xPath to links on this page
             */
            public String linkXPath;
            
            /**
             * xPath to link to next page with links
             */
            public String nextPageXPath;

            public PageToGetLinks(String url, String linkXPath, String nextPageXPath) {
                this.url = url;
                this.linkXPath = linkXPath;
                this.nextPageXPath = nextPageXPath;
            }
        }
}
