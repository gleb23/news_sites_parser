/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package ua.hlibbabii.siteParsers;

import ua.hlibbabii.DefaultParser;
import ua.hlibbabii.SiteMetaData;

/**
 *
 * @author gleb23
 */
public class NytimesComParser extends DefaultParser {
    private static final SiteMetaData siteMetaData = new SiteMetaData(
        "nyt_headline"                                              // title
        , "div.articleBody>nyt_text>p, div.articleBody>p"           // text
        , null                                                    // abstract
        , "div#pageLinks>a.next"                                    // next page
        , null                                                        // linksXPath
        , null                                                    // key words
        , "nyt_byline>h6.byline>span>span, nyt_byline>h6.byline>span>a>span"    // authorXPath
        , "h6.dateline"                                             // dateXPath
        , "'Published: 'MMMMM d, yyyy"                              // dateXPath format
        , new SiteMetaData.PageToGetLinks[] {

            new SiteMetaData.PageToGetLinks(
                "http://query.nytimes.com/search/sitesearch/#/*/24hours/articles/%d/allauthors/newest/"
                , "li.story>div.element2>h3>a"
                , ""
            )

        }
    );
    
    @Override
    public SiteMetaData getSiteMetaData() {
        return siteMetaData;
    }
}
