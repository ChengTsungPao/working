import java.util.*;
import java.net.*;
import java.io.*;

import java.util.regex.*;
import java.net.URL;
import java.util.Iterator;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

public class JsoupCrawlerUT{
    public static void main(String[] args)  throws Exception{
        URL url = new URL("http://tw.stock.yahoo.com/q/q?s=2002");     
        Document doc = Jsoup.parse(url, 3000);      
        Elements tables = doc.select("center>table");       
        Iterator iterator;   
        for(Element table : tables){
            
            iterator = table.select("td").iterator();           
           
            while(iterator.hasNext())
            {               
                System.out.println("data" + ": " + iterator.next().text().trim());
            }          
        }                
        System.out.println("--------------------------------------------------");        
        Element  table;
        table = tables.get(1).select("table").get(0);        
        iterator = table.select("th").iterator();       
        while(iterator.hasNext())
        {               
            System.out.println("data" + ": " + iterator.next().text().trim());
        } 
        
        System.out.println("--------------------------------------------------");  

        table = tables.get(1).select("table").get(1);
        iterator = table.select("td").iterator();       
        while(iterator.hasNext()){               
            System.out.println(iterator.next().text().trim());
        }
    }
}