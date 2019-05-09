import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLConnection;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;

public class SimpleNetSpider {

    public static void main(String[] args) {

        try{
            URL u = new URL("http://211.20.129.217/EnvServAQR/query.aspx");
            URLConnection connection = u.openConnection();
            HttpURLConnection htCon = (HttpURLConnection) connection;
            int code = htCon.getResponseCode();
            if (code == HttpURLConnection.HTTP_OK)
            { 
                System.out.println("find the website");
                BufferedReader in=new BufferedReader(new InputStreamReader(htCon.getInputStream()));
                String inputLine;
                while ((inputLine = in.readLine()) != null) 
                        System.out.println(inputLine);
                    in.close();
            }
            else
            {
                System.out.println("Can not access the website");
            }
        }
        catch(MalformedURLException e )
        {  
            System.out.println("Wrong URL");
        }
        catch(IOException e)
        {
            System.out.println("Can not connect");
        }
    }
}