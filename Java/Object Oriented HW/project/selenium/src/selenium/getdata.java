package selenium;

import java.util.List;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
//import org.openqa.selenium.htmlunit.HtmlUnitDriver;

public class getdata {
	
	public String immediate_data="", history_data="";
	public int line;
	
	public void Immediate_data() {
		WebDriver driver = new ChromeDriver();
		driver.get("http://211.20.129.217/EnvServAQR/notice.aspx"); 
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
		//System.out.println(immediate_data);	
		driver.close();
	}
	
	public void History_data(String[] day) {
		WebDriver driver = new ChromeDriver();
		driver.get("http://211.20.129.217/EnvServAQR/notice.aspx");
        driver.findElement(By.id("Button1")).click();
        driver.findElement(By.id("Button2")).click();     
        for(int i=0;i<day.length;i++) {
            driver.findElement(By.name("TextBox1")).clear();
    		driver.findElement(By.name("TextBox1")).sendKeys(day[i]);
    		driver.findElement(By.id("Button1")).click();
    		driver.findElement(By.id("Button1")).click();
            List<WebElement> itemList = driver.findElements(By.tagName("td")); 
            line=0;
    		for(WebElement e : itemList) {	
    			//System.out.println("line="+line);
    			if(line++==40) {
    				history_data+=e.getText();
        			if(i<day.length-1) {
        				history_data+="nextdata";
        			}
    			}
    			//System.out.println(e.getText());
    		}
        }
		//System.out.println(history_data);
		driver.close();
	}
	
	public String total = "";
	public String[] parameter = new String[15];;
	public double[] number = new double[15];;
	public String[] unit = new String[15];
	
	public int count;
	public String[] tmp;
	public void Immediate_data_process() {
		tmp = immediate_data.split(": |:|    \n|   \n|  \n| \n|\n| ");
		count=0;
		for(int i=0;i<tmp.length;i++) {
			//System.out.printf("%d %s\n",i,tmp[i]);
			if(tmp[i].toCharArray()[0]=='(' && tmp[i].toCharArray()[tmp[i].length()-1]==')') {
				//System.out.printf("%s %s %s\n",tmp[i],tmp[i+1],tmp[i+2]);
				parameter[count] = tmp[i];
				try {
					number[count] = Double.parseDouble(tmp[i+1]);					
				}catch(Exception e) {
					number[count] = -1;
				}				
				unit[count++] = tmp[i+2];	
				total=total+tmp[i]+" "+tmp[i+1]+" "+tmp[i+2]+"\n";
			}			

		}
		
	}
	
	public double[][] all_data;
	public void History_data_process() {
		String[] lin;
		tmp = history_data.split("nextdata|\n");
		all_data = new double[16][24*history_data.split("nextdata").length];
		for(int i=0;i<history_data.split("nextdata").length;i++) {
			for(int j=1;j<17;j++) {				
				lin = tmp[18*i+j].split(" ");
				System.out.printf("%d %s\n",18*i+j,tmp[18*i+j]);
				count=0;
				if(j==10 || j==11) count=1;
				for(int k=0;k<24;k++) {	
					try {
						all_data[j-1][k+24*i] = Double.parseDouble(lin[k+2+count]);					
					}catch(Exception e) {
						all_data[j-1][k+24*i] = -1;
					}
					
				}
			}
		}

	}

}

