package testselenium;

import java.util.List;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.support.ui.Select;
import org.openqa.selenium.Keys;

public class main {
	public static void main(String[] args) throws InterruptedException {
		WebDriver driver = new ChromeDriver();
		driver.get("https://taqm.epa.gov.tw/taqm/tw/HourlyData.aspx"); 
		//driver.findElement(By.name("")).click();
		WebElement select = driver.findElement(By.id("ctl05_lbSite"));
		//select.click();
		Select dropDown = new Select(select);           
		String selected = dropDown.getFirstSelectedOption().getText();
		System.out.println(selected);
		List<WebElement> Options = dropDown.getOptions();
		//Options.get(2).getText();
		Options.get(0).click();		
		Options.get(41).click();
		driver.findElement(By.id("ctl05_btnQuery")).click();
		//driver.navigate().refresh();
		//Options = dropDown.getOptions();
		//Options.get(0).click();
		//Options.get(41).click();

		//driver.findElement(By.id("ctl05_txtDateE")).sendKeys(Keys.ENTER);
		//driver.findElement(By.id("ctl05_txtDateE")).sendKeys(Keys.ENTER);
		//driver.findElement(By.id("ctl05_btnQuery")).click();
		Thread.sleep(5000);
        List<WebElement> itemList = driver.findElements(By.tagName("td")); 
        //List<WebElement> itemList = driver.findElements(By.xpath(".//table[class='TABLE_G']")); 
        int line=0;
        String tmp="";
		for(WebElement e : itemList) {
			if(line==28) tmp=e.getText();
			System.out.println("line:"+(line)+"  "+e.getText());
			if(line>30) break;
			line++;
		}
		System.out.println(tmp);
		line=0;
		String ans="";
		for(String x : tmp.split("\n")){
			System.out.println("line:"+(line)+"  "+x);
			line++;
			if(x.split(" ")[0].equals("05/16")) {
				ans=x;
			}
		}
		System.out.println(ans);
	}


}