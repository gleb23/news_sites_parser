/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package ua.hlibbabii.siteParsers;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;
import ua.hlibbabii.DefaultParser;
import ua.hlibbabii.SiteMetaData;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 *
 * @author gleb23
 */
public class WashingtonpostComParser extends DefaultParser {
    private static final SiteMetaData siteMetaData
        = new SiteMetaData( 
                ".entry-title"                                          // title
                , "div[class=article_body entry-content]>article>p"     // text 
                , null                                              // abstract
                , "a.next-page"                                     // next page
                , "div[class=article_body entry-content]>article>p>a"// linksXPath
                , "p[class=left tag-link-normal]>a"                  // key words
                , "span[class=author vcard]>span.fn"                  // authorXPath
                , "div[class=module byline]>h3>span[class=timestamp updated processed]" // dateXPath
                , "'Published: 'MMMMM d"                                                // dateXPath format
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

    @Override
    public List<String> getLinksFromMainPage(int nLinks) throws IOException {
        List<String> allLinks = new ArrayList<>();
        
        SiteMetaData.PageToGetLinks page = getSiteMetaData().newsPages[0];

        Map<String, String> parameterMap = new HashMap<>();
        parameterMap.put("query", "1");
        parameterMap.put("datefilter", "displaydatetime:[NOW/DAY-1DAY TO NOW/DAY+1DAY]");
        parameterMap.put("filter", "");
        parameterMap.put("sort", "displaydatetime desc");
        parameterMap.put("startat", "0");
        parameterMap.put("offset", new Integer(nLinks).toString());
        parameterMap.put("facets.fields", "contenttype");
        parameterMap.put("useChart", "false");
        
        Document currentPage = Jsoup.connect(page.url).data(parameterMap).post();
        
        Elements linksOnCurrentPage = currentPage.select(page.linkXPath);
        for (Element linkOnCurrentPage : linksOnCurrentPage ) {
            allLinks.add(linkOnCurrentPage.attr("abs:href"));
        }

        return allLinks;
    }
}
