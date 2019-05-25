package FinalProject;

import java.lang.InterruptedException;
import java.util.Date; 
import java.text.SimpleDateFormat;
import java.util.List;
import org.openqa.selenium.Keys;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import java.io.FileWriter;
import java.io.IOException;
import org.openqa.selenium.support.ui.Select;

public class getdata {
	
	public int[] wait = {5,10};
	public String immediate_data="", history_data="",location;
	public int line,key=5,flag;
	public String[] tmp;
	public String[][] air = new String[12][3];
	public String[][] all_air = {{"SO2","SO2 (ppb)","SO2"},{"CO","CO (ppm)","CO"},{"O3","O3 (ppb)","O3"},
			{"PM10","PM10 (μg/m3)","PM10"},{"NOx","NOx (ppb)","NOx"},{"NO","NO (ppb)","NO"},
			{"NO2","NO2 (ppb)","NO2"},{"Tetrahydrocannabinol","THC (ppm)","THC"},{"Non-Methane Hydrocarbon","NMHC (ppm)","NMHC"},
			{"Air Tempature","AT (℃)","AT"},{"CH4","CH4 (ppm)","CH4"},{"Relative Humidity","RH (%)","RH"}};
	
	public void Immediate_data(String wh) {
		
		SimpleDateFormat sdFormat = new SimpleDateFormat("MM/dd");
		Date date = new Date();
		String strDate = sdFormat.format(date);		
		
		where(wh);
		ChromeOptions options = new ChromeOptions();
		options.addArguments("--headless");		
		WebDriver driver = new ChromeDriver(options);
		driver.get("https://taqm.epa.gov.tw/taqm/tw/HourlyData.aspx");
		
		WebElement select1 = driver.findElement(By.id("ctl05_lbSite"));
		Select dropDown1 = new Select(select1); 
		List<WebElement> Options1 = dropDown1.getOptions();			
		Options1.get(0).click();
		Options1.get(key).click();
		
		WebElement select2 = driver.findElement(By.id("ctl05_lbParam"));
		Select dropDown2 = new Select(select2);
		List<WebElement> Options2 = dropDown2.getOptions();		
        String a;
		for(int i=0;i<Options2.size();i++) {	
			a = Options2.get(i).getText();			
			if(a.equals("NO") ||
			   a.equals("AMB_TEMP") ||
			   a.equals("NO2") ||
			   a.equals("NOx") ||
			   a.equals("SO2") ||
			   a.equals("CO") ||
			   a.equals("CH4") ||
			   a.equals("THC") ||
			   a.equals("NMHC") ||
		       a.equals("O3") ||
			   a.equals("PM10") ||
			   a.equals("RH") ) {				
				if(i>0) {
					Options2.get(i).click();
				}				
			}
		}
		
		
        try {
            Thread.sleep(wait[0]*1000);        	
        } catch (InterruptedException n) {
            n.printStackTrace(); 
        }		
		driver.findElement(By.id("ctl05_btnQuery")).click();
		
		
        try {
            Thread.sleep(wait[1]*1000);        	
        } catch (InterruptedException n) {
            n.printStackTrace(); 
        }		
        List<WebElement> itemList = driver.findElements(By.tagName("td")); 
        
        
        line=0;
        int index=0;
        String airname;
        String[] temp;
		for(WebElement e : itemList) {
			if(line++==28) {
				tmp=e.getText().split("\n");
				flag=0;				
				for(int i=0;i<tmp.length;i++) {					
					if(tmp[i].split(" ")[0].equals(strDate)) {
						immediate_data=immediate_data+" "+tmp[i]+"\n";
						temp = tmp[i-2].split("：|（");						
						airname = temp[temp.length-2];						
						if(airname.equals("AMB_TEMP")) airname = "AT";
						for(int j=0;j<all_air.length;j++) {
							if(airname.equals(all_air[j][2])) {
								air[index++] = all_air[j];
							}
						}					
						flag=1;						
					}
				}
				if(flag==0) {
					immediate_data=immediate_data+" None"+"\n";
				}			
			}
		}
		driver.close();
		System.out.println(immediate_data);
	}	

	
	public void History_data(String[] day,String wh,int find) {
		
		where(wh);		
		if(day.length==1) {
			
			ChromeOptions options = new ChromeOptions();
			options.addArguments("--headless");		
			WebDriver driver = new ChromeDriver(options);
			driver.get("https://taqm.epa.gov.tw/taqm/tw/HourlyData.aspx"); 
			
			WebElement select1 = driver.findElement(By.id("ctl05_lbSite"));
			Select dropDown1 = new Select(select1); 
			List<WebElement> Options1 = dropDown1.getOptions();			
			Options1.get(0).click();
			Options1.get(key).click();
			
			WebElement select2 = driver.findElement(By.id("ctl05_lbParam"));
			Select dropDown2 = new Select(select2);
			List<WebElement> Options2 = dropDown2.getOptions();
			
	        String a;
			for(int i=0;i<Options2.size();i++) {	
				a = Options2.get(i).getText();			
				if(a.equals("NO") ||
				   a.equals("AMB_TEMP") ||
				   a.equals("NO2") ||
				   a.equals("NOx") ||
				   a.equals("SO2") ||
				   a.equals("CO") ||
				   a.equals("CH4") ||
				   a.equals("THC") ||
				   a.equals("NMHC") ||
			       a.equals("O3") ||
				   a.equals("PM10") ||
				   a.equals("RH") ) {
					if(i>0) {
						Options2.get(i).click();
					}
					
				}
			}
			
			
	        driver.findElement(By.id("ctl05_txtDateS")).clear();
			driver.findElement(By.id("ctl05_txtDateS")).sendKeys(day[0]);			
	        driver.findElement(By.id("ctl05_txtDateE")).clear();
			driver.findElement(By.id("ctl05_txtDateE")).sendKeys(day[0]);
			driver.findElement(By.id("ctl05_txtDateE")).sendKeys(Keys.ENTER); 
			
			
	        try {
	            Thread.sleep(wait[0]*1000);	        	
	        } catch (InterruptedException n) {
	            n.printStackTrace(); 
	        }			
			driver.findElement(By.id("ctl05_btnQuery")).click();
			
			
	        try {
	            Thread.sleep(wait[1]*1000);	        	
	        } catch (InterruptedException n) {
	            n.printStackTrace(); 
	        }			
	        List<WebElement> itemList = driver.findElements(By.tagName("td")); 
	        
	        
	        line=0;	 
	        int index=0;
	        String airname;
	        String[] temp;
			for(WebElement e : itemList) {
				if(line++==28) {			        
					tmp=e.getText().split("\n");
					flag=0;					
					for(int i=0;i<tmp.length;i++) {
				        try {
							if(Integer.parseInt(tmp[i].split(" ")[0].split("/")[0])==Integer.parseInt(day[0].split("/")[1]) &&
									   Integer.parseInt(tmp[i].split(" ")[0].split("/")[1])==Integer.parseInt(day[0].split("/")[2])) {
										history_data=history_data+tmp[i]+"\n";
										temp = tmp[i-2].split("：|（");
										airname = temp[temp.length-2];										
										if(airname.equals("AMB_TEMP")) airname = "AT";
										for(int j=0;j<all_air.length;j++) {
											if(airname.equals(all_air[j][2])) {
												air[index++] = all_air[j];
											}
										}	
										flag=1;								
									}
				        } catch (NumberFormatException n) {				            
				        	System.out.print("");
				        }
					}
					if(flag==0) {
						history_data=history_data+"None"+"\n";
					}
					break;
				}
			}
			driver.close();
			System.out.println(history_data);		
			
		}else {
			
			ChromeOptions options = new ChromeOptions();
			options.addArguments("--headless");		
			WebDriver driver = new ChromeDriver(options);
			driver.get("https://taqm.epa.gov.tw/taqm/tw/HourlyData.aspx"); 
    		
			WebElement select1 = driver.findElement(By.id("ctl05_lbSite"));
			Select dropDown1 = new Select(select1); 
			List<WebElement> Options1 = dropDown1.getOptions();
			Options1.get(0).click();
			Options1.get(key).click();
			
			WebElement select2 = driver.findElement(By.id("ctl05_lbParam"));
			Select dropDown2 = new Select(select2);
			List<WebElement> Options2 = dropDown2.getOptions();			
			Options2.get(0).click();
			Options2.get(find).click();	         
	        
            driver.findElement(By.id("ctl05_txtDateS")).clear();
    		driver.findElement(By.id("ctl05_txtDateS")).sendKeys(day[0]);    		
            driver.findElement(By.id("ctl05_txtDateE")).clear();
    		driver.findElement(By.id("ctl05_txtDateE")).sendKeys(day[1]);
    		driver.findElement(By.id("ctl05_txtDateE")).sendKeys(Keys.ENTER); 
    		
			
	        try {
	            Thread.sleep(wait[0]*1000);
	        } catch (InterruptedException n) {
	            n.printStackTrace(); 
	        }
			driver.findElement(By.id("ctl05_btnQuery")).click();
			
			
	        try {
	            Thread.sleep(wait[1]*1000);
	        } catch (InterruptedException n) {
	            n.printStackTrace(); 
	        }
	        List<WebElement> itemList = driver.findElements(By.tagName("td")); 
	        
	        
	        String tmp = "";
	        line = 0;
	        for(WebElement e : itemList) {
	        	if(line++==28) {
	        		tmp=e.getText();	        		
	        		break;
	        	}
	        
	        }
	        String[] tmp1 = tmp.split("\n");
	        for(int i=0;i<tmp1.length;i++) {	        	
		        try {
		        	if(Integer.parseInt(tmp1[i].split(" ")[0].split("/")[0])==Integer.parseInt(day[0].split("/")[1]) &&
		 	        	   Integer.parseInt(tmp1[i].split(" ")[0].split("/")[1])==Integer.parseInt(day[0].split("/")[2])) {
		 	        		for(;i<tmp1.length;i++) {
		 	        			history_data = history_data+tmp1[i]+"\n";	        			
		 	        		}	
		 	        	}
		        } catch (NumberFormatException n) {		            
		        	System.out.print("");
		        }
	        }   
	        driver.close();
	        System.out.println(history_data);	        
		}		
	}
	
	public int count;
	
	public double[][] all_data1;
	public double[] all_data2;
	
	public void Immediate_data_process() {
		String tmp="";
		SimpleDateFormat sdFormat = new SimpleDateFormat("yyyy/MM/dd HH:mm");
		Date date = new Date();
		String strDate = sdFormat.format(date);
		for(int i=0;i<immediate_data.split("\n").length;i++) {	
			tmp = tmp + air[i][1] + " " + immediate_data.split("\n")[i].split(" ")[Integer.parseInt(strDate.split(" ")[1].split(":")[0])] + "\n";
		}
		immediate_data=tmp;		
	}
	
	public void History_data_process(String[] day) {
		String[] data2,data1 = history_data.split("\n");
		if(day.length==1) {
			all_data1 = new double[data1.length][24];
			for(int kind=0;kind<data1.length;kind++) {
				data2 = data1[kind].split(" ");
				for(int num=1;num<data2.length;num++) {					
					try {
						all_data1[kind][num-1] = Double.parseDouble(data2[num]);					
					}catch(Exception e) {
						all_data1[kind][num-1] = -1;
					}
				}
			}			
		}else {
			all_data2 = new double[data1.length*24];
			for(int date=0;date<data1.length;date++) {
				data2 = data1[date].split(" ");
				for(int num=1;num<data2.length;num++) {					
					try {						
						all_data2[date*(data2.length-1)+num-1] = Double.parseDouble(data2[num]);					
					}catch(Exception e) {
						all_data2[date*(data2.length-1)+num-1] = -1;
					}
				}
			}
		}		
	}	
	
	public void File_immediate(){
		try {
			SimpleDateFormat sdFormat = new SimpleDateFormat("yyyy/MM/dd hh:mm");
			Date date = new Date();
			String strDate = sdFormat.format(date);			
			FileWriter f = new FileWriter("./mydata/Instant.txt",true);				
			for(int i=0;i<immediate_data.split("\n").length;i++) {
				f.write(location+"\r\n");
				f.write(air[i][1]+"\r\n");
				f.write(strDate.split("/| ")[1]+"/"+strDate.split("/| ")[2]+" "+immediate_data.split("\n")[i].split(" ")[2]+"\r\n");
			}					
			f.close();
		}
	    catch(IOException ie) {
	        ie.printStackTrace();
	    }
	}
	
	public void File_History(String[] day,String label) {
		try {
			String[] tmp = history_data.split("\n");
			if(day.length==1) {
				FileWriter f = new FileWriter("./mydata/History.txt",true);
				for(int i=0;i<tmp.length;i++) {					
					f.write(location+"\r\n");
					f.write(air[i][1]+"\r\n");
					f.write(tmp[i]+"\r\n");
				}
				f.close();
			}else {
				FileWriter f = new FileWriter("./mydata/History.txt",true);	
				for(int i=0;i<tmp.length;i++) {
					f.write(location+"\r\n");
					f.write(label+"\r\n");
					f.write(tmp[i]+"\r\n");
				}
				f.close();
			}
		}
	    catch(IOException ie) {
	        ie.printStackTrace();
	    }
	}
	
	public void where(String wh) {
		location=wh;
		if(wh.equals("台北")) {
			key = 5;
		}else if(wh.equals("新北")) {
			key = 6;
		}else if(wh.equals("桃園")) {
			key = 20;
		}else if(wh.equals("新竹")) {
			key = 27;
		}else if(wh.equals("苗栗")) {
			key = 30;
		}else if(wh.equals("台中")) {
			key = 35;
		}else if(wh.equals("彰化")) {
			key = 38;
		}else if(wh.equals("雲林")) {
			key = 46;
		}else if(wh.equals("嘉義")) {
			key = 49;
		}else if(wh.equals("台南")) {
			key = 53;
		}else if(wh.equals("高雄")) {
			key = 64;
		}else if(wh.equals("屏東")) {
			key = 66;
		}else if(wh.equals("台東")) {
			key = 73;
		}else if(wh.equals("花蓮")) {
			key = 71;
		}else if(wh.equals("宜蘭")) {
			key = 69;
		}else if(wh.equals("澎湖")) {
			key = 76;
		}else if(wh.equals("基隆")) {
			key = 4;
		}else if(wh.equals("南投")) {
			key = 41;
		}		
		
	}

}



