import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.URL;
import java.net.URLConnection;

public class Main
{
	public static void main(String[] args)
	{

		String url = "http://211.20.129.217/EnvServAQR/query.aspx";
	
		String result = "";

		BufferedReader in = null;
		try
		{
	
			URL realUrl = new URL(url);
	
			URLConnection connection = realUrl.openConnection();
		
			connection.connect();
			
			in = new BufferedReader(new InputStreamReader(connection.getInputStream()));
		
			String line;
			while ((line = in.readLine()) != null)
			{
				result += line + "\n";
			}
		} catch (Exception e)
		{
			System.out.println("gg" + e);
			e.printStackTrace();
		}
		finally
		{
			try
			{
				if (in != null)
				{
					in.close();
				}
			} catch (Exception e2)
			{
				e2.printStackTrace();
			}
		}
		System.out.println(result);
	}
}