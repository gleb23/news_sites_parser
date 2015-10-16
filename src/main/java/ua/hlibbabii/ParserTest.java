package ua.hlibbabii;

import java.io.IOException;
import java.util.List;

/**
 * Created with IntelliJ IDEA.
 * User: gleb23
 * Date: 06.04.13
 * Time: 22:55
 * To change this template use File | Settings | File Templates.
 */
public class ParserTest {
    /**
     *
     * @param args
     * @throws IOException
     * @throws NewsParser.URLNotSpecifiedException
     * @throws NewsParser.URLNotSupportedException
     * @throws NewsParser.ConfigException
     */
    public static void main(String[] args) throws IOException, NewsParser.URLNotSpecifiedException, NewsParser.URLNotSupportedException, NewsParser.ConfigException {
//        Parser parser = new Parser();
//        Article art = parser.parse("http://www.reuters.com/article/2013/06/13/us-egypt-brotherhood-bread-specialreport-idUSBRE95C07P20130613");
//        System.out.println(art.toString());
        NewsParser parser = new NewsParser();
        
        List<String> allLinks = parser.getLinksFromMainPage("http://www.washingtonpost.com", 5);
        for (String link : allLinks) {
            System.out.println(link);            
        }
        for (String link : allLinks) {
            parser = new NewsParser();
            Article art = parser.parse(link);
            System.out.println("--------------------"); 
            System.out.println(art.toString());            
        }
        
        allLinks = parser.getLinksFromMainPage("http://www.reuters.com", 5);
        for (String link : allLinks) {
            System.out.println(link);            
        }
        for (String link : allLinks) {
            parser = new NewsParser();
            Article art = parser.parse(link);
            System.out.println("--------------------"); 
            System.out.println(art.toString());            
        }
        
        allLinks = parser.getLinksFromMainPage("http://www.sciencenews.org", 5);
        for (String link : allLinks) {
            System.out.println(link);            
        }
        for (String link : allLinks) {
            parser = new NewsParser();
            Article art = parser.parse(link);
            System.out.println("--------------------"); 
            System.out.println(art.toString());            
        }
    }
}
