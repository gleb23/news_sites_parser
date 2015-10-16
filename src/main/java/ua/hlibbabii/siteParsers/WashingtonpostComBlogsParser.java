/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package ua.hlibbabii.siteParsers;

import ua.hlibbabii.SiteMetaData;

/**
 *
 * @author gleb23
 */
public class WashingtonpostComBlogsParser extends SciencenewsOrgParser{
    private static final SiteMetaData siteMetaData = new SiteMetaData(
        ".entry-title"                                      // title
        , "div[class=entry-content]>p"                      // text
        , null                                              // abstract
        , "a.next-page"                                     // next page
        , "div[class=entry-content]>p>a"                    // linksXPath
        , "p[class=left tag-link-normal]>a"                 // key words
        , "p.wp-byline>a"                                   // authorXPath
        , "div[class=module byline]>h3>span[class=timestamp updated processed]"  // dateXPath
        , "'Published: 'MMMMM d"                                                 // dateXPath format
        , new SiteMetaData.PageToGetLinks[] {

            new SiteMetaData.PageToGetLinks(
                "http://www.washingtonpost.com/newssearch/search.html"
                ,"ol#search-results>li>h3>a"
                ,""
            )

        }
    ); 
    
    @Override
    public SiteMetaData getSiteMetaData() {
        return siteMetaData;
    }    
}
