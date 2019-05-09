package project1;

import java.util.List;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;


//import org.openqa.selenium.htmlunit.HtmlUnitDriver;

public class Main {

    public static void main(String[] args) {
    	//System.setProperty("webdriver.chrome.driver", "D:\\program\\vscode_workspace\\private\\working\\Java\\Object Oriented HW\\test\\selenium\\chromedriver.exe");
    	WebDriver driver = new ChromeDriver();
        WebDriver driver1 = new ChromeDriver();
        driver.get("https://www.google.com.tw/");
        driver1.get("http://211.20.129.217/EnvServAQR/query.aspx");
        WebElement submitButton = driver1.findElement(By.id("Button1")); 
        submitButton.click(); 
        
        
        WebElement element = driver.findElement(By.name("q"));
        List<WebElement> itemList = driver1.findElements(By.tagName("td"));
        
        int i=0;
        String data="0";
		for(WebElement e : itemList) {
			System.out.println(i++);
			if(i==10) {
				data=e.getText();
			}
			//System.out.println(e.getText());
		}


		element.clear();
        element.sendKeys("mysql excel 2013"); 
        element.submit();

        String title = driver.getTitle();
        System.out.printf(title);
        System.out.println(data);
 
        driver.close();
        //driver1.close();
        
    }

}
