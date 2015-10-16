package ua.hlibbabii;

import java.io.IOException;

/**
 * Created with IntelliJ IDEA.
 * User: gleb23
 * Date: 06.04.13
 * Time: 22:55
 * To change this template use File | Settings | File Templates.
 */
public class ParserTest {
    public static void main(String[] args) throws IOException, Parser.URLNotSpecifiedException, Parser.URLNotSupportedException {
        Parser parser = new Parser("http://www.nytimes.com/2013/04/17/us/politics/toxic-ricin-detected-on-mail-sent-to-senator.html?ref=politics");
        Article art = parser.parse();
        System.out.println(art.toString());
    }
}
