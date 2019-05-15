package testselenium;

import java.util.List;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.support.ui.Select;

public class main {
	public static void main(String[] args) {
		WebDriver driver = new ChromeDriver();
		driver.get("https://taqm.epa.gov.tw/taqm/tw/HourlyData.aspx"); 
		//driver.findElement(By.name("·s¥_¥«-´I¶Q¨¤")).click();
		WebElement select = driver.findElement(By.id("ctl05_lbSite"));
		//select.click();
		Select dropDown = new Select(select);           
		String selected = dropDown.getFirstSelectedOption().getText();
		System.out.println(selected);
		List<WebElement> Options = dropDown.getOptions();
		Options.get(2).getText();
		Options.get(0).click();
		Options.get(2).click();
		driver.findElement(By.id("ctl05_btnQuery")).click();
        List<WebElement> itemList = driver.findElements(By.tagName("td")); 
        //List<WebElement> itemList = driver.findElements(By.xpath(".//table[class='TABLE_G']")); 
        int line=0;
		for(WebElement e : itemList) {
			
			System.out.println("line:"+(line++)+"  "+e.getText());
			if(line>30) break;
		}
		
	}


}