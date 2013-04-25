package ua.hlibbabii;

import java.util.ArrayList;
import java.util.Date;
import java.util.List;

/**
 * Created with IntelliJ IDEA.
 * User: gleb23
 * Date: 06.04.13
 * Time: 21:48
 * To change this template use File | Settings | File Templates.
 */
public class ArticleImpl implements Article {

    private String title = null;
    private String text = null;
    private String theAbstract = null;
    private String author = null;
    private List<String> keyWords = new ArrayList<String>();
    private List<String> links = new ArrayList<String>();
    private Date dateOfPublishing = null;

    @Override
    public String getTitle() {
        return this.title;
    }

    @Override
    public String getText() {
        return this.text;
    }

    @Override
    public String getAbstract() {
        return theAbstract;  //To change body of implemented methods use File | Settings | File Templates.
    }

    @Override
    public String getAuthor() {
        return author;
    }

    @Override
    public List<String> getKeyWords() {
        return this.keyWords;
    }

    @Override
    public List<String> getLinks() {
        return links;  //To change body of implemented methods use File | Settings | File Templates.
    }

    @Override
    public Date getDateOfPublishing() {
        return this.dateOfPublishing;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public void setText(String text) {
        this.text = text;
    }

    public void setAuthor(String author) {
        this.author = author;
    }

    public void setLinks(List<String> links) {
        this.links = links;
    }

    public void addLink(String link) {
        this.links.add(link);
    }

    public void setTheAbstract(String theAbstract) {
        this.theAbstract = theAbstract;
    }

    public void setKeyWords(List<String> keyWords) {
        this.keyWords = keyWords;
    }

    public void addKeyWord(String word) {
        this.keyWords.add(word);
    }

    public void setDateOfPublishing(Date dateOfPublishing) {
        this.dateOfPublishing = dateOfPublishing;
    }

    /**
     * returns string representation of this <code>ArticleImpl</code> object
     * @return
     */
    @Override
    public String toString() {
        StringBuilder summary = new StringBuilder();

        if (title != null) {
            summary.append("=" + title + "=");
        } else {
            summary.append("No title");
        }
        summary.append("\n");

        if (theAbstract != null) {
            summary.append("Abstract: " + theAbstract);
        } else {
            summary.append("No abstract");
        }
        summary.append("\n");

        if (text != null) {
            summary.append("Text: " + text);
        } else {
            summary.append("No text");
        }
        summary.append("\n");

        if (author != null) {
            summary.append("author=" + author);
        } else {
            summary.append("No author");
        }
        summary.append("\n");

        if (dateOfPublishing != null) {
            summary.append(dateOfPublishing);
        } else {
            summary.append("No date of publishing");
        }
        summary.append("\n");

        if (links.isEmpty()) {
            summary.append("No links: ");
        } else {
            summary.append("Links: ");
            for (String link : links) {
                summary.append(link + "   ");
            }
        }
        summary.append("\n");

        if (keyWords.isEmpty()) {
            summary.append("No key words");
        } else {
            summary.append("Key words: ");
            for (String keyWord : keyWords) {
                summary.append(keyWord + "   ");
            }
        }

        return summary.toString();
    }
}
