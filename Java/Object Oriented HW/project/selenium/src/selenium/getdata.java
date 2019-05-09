package selenium;

import java.util.List;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
//import org.openqa.selenium.htmlunit.HtmlUnitDriver;

public class getdata {
	
	public String immediate_data, history_data;
	public int line;
	
	public void Immediate_data() {
		WebDriver driver = new ChromeDriver();
		driver.get("http://211.20.129.217/EnvServAQR/query.aspx"); 
        driver.findElement(By.id("Button1")).click(); 
        List<WebElement> itemList = driver.findElements(By.tagName("td")); 
        line=0;
		for(WebElement e : itemList) {
			//System.out.println("line="+line);
			if(line++==9) {
				immediate_data=e.getText();
			}
			//System.out.println(e.getText());
		}
		System.out.println(immediate_data);	
		//driver.close();
	}
	
	public void History_data(String day) {
		WebDriver driver = new ChromeDriver();
		driver.get("http://211.20.129.217/EnvServAQR/query.aspx");
        driver.findElement(By.id("Button1")).click();
        driver.findElement(By.id("Button2")).click();         
        driver.findElement(By.name("TextBox1")).clear();
		driver.findElement(By.name("TextBox1")).sendKeys(day);
		driver.findElement(By.id("Button1")).click();
		driver.findElement(By.id("Button1")).click();
        List<WebElement> itemList = driver.findElements(By.tagName("td")); 
        line=0;
		for(WebElement e : itemList) {	
			//System.out.println("line="+line);
			if(line++==40) {
				history_data=e.getText();
			}
			//System.out.println(e.getText());
		}
		System.out.println(history_data);
		//driver.close();
	}

}

