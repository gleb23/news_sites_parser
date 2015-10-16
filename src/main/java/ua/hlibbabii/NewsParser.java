package ua.hlibbabii;

/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

import org.w3c.dom.Element;
import org.w3c.dom.NodeList;
import org.xml.sax.SAXException;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import java.io.File;
import java.io.IOException;
import java.net.URISyntaxException;
import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 * Parser for articles from news sites. Current version supports
 * parsing from the following sites:
 * <ul>
 * <li>http://www.washingtonpost.com</li> 
 * <li>http://www.nytimes.com </li>
 * <li>http://www.reuters.com </li> 
 * <li>http://www.sciencenews.org </li>
 * <ul>
 * To add support for another site: create class that extends DefaultParser; 
 * specify site meta-data there (see examples for existing parsers); 
 * override method <code>getSiteMetaData()</code>;
 * if necessary override other method; add entry to parsers.xml 
 * 
 * Created with IntelliJ IDEA.
 * User: gleb23
 * Date: 06.04.13
 * Time: 22:22
 * To change this template use File | Settings | File Templates.
 */
public class NewsParser {

    /**
     * default constructor
     */
    public NewsParser() {
    }

    /**
     * Thrown when null appears to be instead of the URL
     */
    public static class URLNotSpecifiedException extends Exception {
    }
    
    /**
     * Thrown when URL is not valid or not supported
     */
    public static class URLNotSupportedException extends Exception {
    }
    
    /**
     * Exception connected with invalid parsers.xml file configuration
     * or errors when parsing it, or parser class is not found
     */
    public static class ConfigException extends Exception {
    }
    
    /** 
     * Parses the current page or the next ones as well if the article is on
     * several pages and returns returns the article as <code>Article</code>
     * object
     * @param url URL of the page that contains the first page of the article 
     * to be parsed
     * @return the article as <code>Article</code> object
     * @throws URLNotSpecifiedException 
     * if <code>null</code> passed as parameter
     * @throws IOException on error
     * @throws URLNotSupportedException
     * if passed URL is either not valid or not supported
     * @throws ConfigException 
     * if errors when parsing parsers.xml file occured
     * or parser class is not found
     */
    public Article parse(String url) throws URLNotSpecifiedException,
            IOException, URLNotSupportedException, ConfigException, URISyntaxException {
        DefaultParser parserForSite = findParserForSite(url);
        return parserForSite.parse(url);
    }
    
    /**
     * Returns links to pages with the most recent articles
     * @param url URL of the main page of the site e.g
     * http://washingtonpost.com, http://nytimes.com,
     * http://reuters.com, http://sciencenews.org
     * @param nLinks the number of links to return 
     * @return links to pages with the most recent articles
     * @throws URLNotSpecifiedException 
     * if <code>null</code> passed as parameter
     * @throws IOException on error
     * @throws URLNotSupportedException
     * if passed URL is either not valid or not supported
     * @throws ConfigException 
     * if errors when parsing parsers.xml file occured 
     * or parser class is not found 
     */
    public List<String> getLinksFromMainPage(String url, int nLinks)
            throws IOException, URLNotSpecifiedException,
            URLNotSupportedException, ConfigException, URISyntaxException {
        DefaultParser parserForSite = findParserForSite(url);
        return parserForSite.getLinksFromMainPage(nLinks);
    }

    /**
     * returns appropriate parser for given URL
     * @param url URL of the main page of the site e.g
     * http://washingtonpost.com, http://nytimes.com,
     * http://reuters.com, http://sciencenews.org to get parser for 
     * @return appropriate parser for given URL
     * @throws URLNotSupportedException
     * if passed URL is either not valid or not supported
     * @throws ConfigException 
     * if errors when parsing parsers.xml file occured 
     * or parser class is not found
     * 
     */
    private DefaultParser findParserForSite(String url) throws URLNotSupportedException, URLNotSpecifiedException, ConfigException, URISyntaxException {
        if (url == null) {
            throw new URLNotSpecifiedException(); 
        }
        // TODO change location of xml!!!
        File fXmlFile = new File(ClassLoader.getSystemResource("parsers.xml").toURI());
	DocumentBuilderFactory dbFactory = DocumentBuilderFactory.newInstance();
	DocumentBuilder dBuilder;
        org.w3c.dom.Document doc;
        try {
            dBuilder = dbFactory.newDocumentBuilder();
            doc = dBuilder.parse(fXmlFile);
            NodeList nList = doc.getElementsByTagName("parser-mapping");
            for (int i = 0; i < nList.getLength(); i++) { 
                Element eElement = (Element) nList.item(i);
                Element elm = (Element) eElement.getElementsByTagName("url").item(0);
                if (url.startsWith(elm.getTextContent())) {
                    String curPackage = getClass().getPackage().getName();
                    String className = eElement.getElementsByTagName("class").item(0)
                            .getTextContent();
                    return ((DefaultParser)Class.forName(curPackage + "." + className).newInstance());
                }
            }
        } catch (SAXException | IOException | ParserConfigurationException | ClassNotFoundException | InstantiationException | IllegalAccessException ex) {
            Logger.getLogger(NewsParser.class.getName()).log(Level.SEVERE, null, ex);
            throw new ConfigException();
        }
        throw new URLNotSupportedException();
    }
}
