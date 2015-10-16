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
public class SciencenewsOrgParser extends DefaultParser {
    private static final SiteMetaData siteMetaData = new SiteMetaData(
        "div.article_page>div.article_title"                 // title
        , "div.content_content>p"                            // text
        , "div[class=article_sub_title print-no]"            // abstract
        ,  null                                              // next page
        , "div.side_txt>p>a, div.content_content>p>em>a"     // linksXPath
        , null                                               // key words
        , "p[class=print-no article_author]>a[class=anonymous print]"      // authorXPath
        , "p[class=print-no article_date]"                                 // dateXPath
        , "'Web edition: 'MMMMM dd, yyyy"                                  // dateXPath format
        , new SiteMetaData.PageToGetLinks[] {
            
            new SiteMetaData.PageToGetLinks(
                    "http://www.sciencenews.org/view/latest/page/%d"
                    ,"li.story_>div.story_title>a"
                    ,""
                )
                
        }    
    );
    
    @Override
    public SiteMetaData getSiteMetaData() {
        return siteMetaData;
    }
}
