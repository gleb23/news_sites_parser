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
public class ReutersComParser extends DefaultParser {
    private static final SiteMetaData siteMetaData = new SiteMetaData(
        "h1"                                            // title
        , "span#articleText>p"                          // text
        , "span.focusParagraph>p"                       // abstract
        , null                                          // next page
        , "span#articleText>p>a"                        // linksXPath
        , "div.relatedTopicButtons>div.actionButton"    // key words
        , "div#articleInfo>p.byline"                    // authorXPath
        , "div#articleInfo>p>span.timestamp"            // dateXPath
        , "EEE MMM d, yyyy h:mma z"                     // dateXPath format
        , new SiteMetaData.PageToGetLinks[] {
            
            new SiteMetaData.PageToGetLinks(
                "http://www.reuters.com/news/archive/topNews?view=page&page=%d&pageSize=10"
                ,"div.moduleBody>div.feature>h2>a"
                ,""
            )
                
        }
    );
    
    @Override
    public SiteMetaData getSiteMetaData() {
        return siteMetaData;
    }
}
