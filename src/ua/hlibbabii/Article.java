package ua.hlibbabii;

import java.util.List;

/**
 * Created with IntelliJ IDEA.
 * User: gleb23
 * Date: 06.04.13
 * Time: 23:05
 * To change this template use File | Settings | File Templates.
 */
interface Article {
    /**
     * Returns the title of this article, if no article available, returns null
     * @return the title of this article
     */
    public String getTitle();

    /**
     * Returns the text of this article. Normally the abstract is not included here.
     * If this article covers several pages, text is grabbed from all of them.
     * If no text available, returns empty string.
     * @return the text of this article without abstract
     */
    public String getText();

    /**
     * Returns the abstract of this article. If no abstract available, returns null.
     * @return the abstract of this article
     */
    public String getAbstract();

    /**
     * Returns the author(s) of this article. If no author available, returns null.
      * @return the author(s) of this article
     */
    public String getAuthor();

    /**
     * Returns the list of keywords for this article. If there is no keywords, returns empty list.
     * @return the list of keywords for this article
     */
    public List<String> getKeyWords();

    /**
     * Returns the list of links in this article. If there is no links, returns empty list.
     * @return the list of links in this article
     */
    public List<String> getLinks();

    /**
     * returns the date for US location this article was updated last time. If no date available, returns null
     * @return the date for US location this article was updated last time
     */
    public java.util.Date getDateOfPublishing();
}
