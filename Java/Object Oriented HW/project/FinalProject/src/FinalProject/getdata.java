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
	
	public String immediate_data="", history_data="",location;
	public int line,key=5,flag;
	public String[] tmp;
	
	public void Immediate_data(String wh) {
		
		SimpleDateFormat sdFormat = new SimpleDateFormat("MM/dd");
		Date date = new Date();
		String strDate = sdFormat.format(date);		
		
		where(wh);
		//ChromeOptions options = new ChromeOptions();
		//options.addArguments("--headless");		
		WebDriver driver = new ChromeDriver();//options
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
            Thread.sleep(5000);        	
        } catch (InterruptedException n) {
            n.printStackTrace(); 
        }		
		driver.findElement(By.id("ctl05_btnQuery")).click();
		
		
        try {
            Thread.sleep(10000);        	
        } catch (InterruptedException n) {
            n.printStackTrace(); 
        }		
        List<WebElement> itemList = driver.findElements(By.tagName("td")); 
        
        
        line=0;
		for(WebElement e : itemList) {
			if(line++==28) {
				tmp=e.getText().split("\n");
				flag=0;
				for(String y:tmp) {	
					System.out.println(y);
					if(y.split(" ")[0].equals(strDate)) {
						immediate_data=immediate_data+" "+y+"\n";
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
			
			//ChromeOptions options = new ChromeOptions();
			//options.addArguments("--headless");		
			WebDriver driver = new ChromeDriver();//options
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
	            Thread.sleep(5000);	        	
	        } catch (InterruptedException n) {
	            n.printStackTrace(); 
	        }			
			driver.findElement(By.id("ctl05_btnQuery")).click();
			
			
	        try {
	            Thread.sleep(10000);	        	
	        } catch (InterruptedException n) {
	            n.printStackTrace(); 
	        }			
	        List<WebElement> itemList = driver.findElements(By.tagName("td")); 
	        
	        
	        line=0;	        
			for(WebElement e : itemList) {
				if(line++==28) {			        
					tmp=e.getText().split("\n");
					flag=0;
					for(String y:tmp) {							
				        try {
							if(Integer.parseInt(y.split(" ")[0].split("/")[0])==Integer.parseInt(day[0].split("/")[1]) &&
									   Integer.parseInt(y.split(" ")[0].split("/")[1])==Integer.parseInt(day[0].split("/")[2])) {
										history_data=history_data+y+"\n";
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
			
			//ChromeOptions options = new ChromeOptions();
			//options.addArguments("--headless");		
			WebDriver driver = new ChromeDriver();//options
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
	            Thread.sleep(5000);
	        } catch (InterruptedException n) {
	            n.printStackTrace(); 
	        }
			driver.findElement(By.id("ctl05_btnQuery")).click();
			
			
	        try {
	            Thread.sleep(10000);
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
		String[] air = {"SO2 (ppb)","CO (ppm)","O3 (ppb)","PM10 (�gg/m3)","NOx (ppb)","NO (ppb)",
				"NO2 (ppb)","THC (ppm)","NMHC (ppm)","AT (�J)","CH4 (ppm)","RH (%)"};
		SimpleDateFormat sdFormat = new SimpleDateFormat("yyyy/MM/dd hh:mm");
		Date date = new Date();
		String strDate = sdFormat.format(date);
		for(int i=0;i<immediate_data.split("\n").length;i++) {			
			tmp = tmp + air[i] + " " + immediate_data.split("\n")[i].split(" ")[Integer.parseInt(strDate.split(" ")[1].split(":")[0])] + "\n";
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
			String[] air = {"SO2 (ppb)","CO (ppm)","O3 (ppb)","PM10 (�gg/m3)","NOx (ppb)","NO (ppb)",
							"NO2 (ppb)","THC (ppm)","NMHC (ppm)","AT (�J)","CH4 (ppm)","RH (%)"};
			SimpleDateFormat sdFormat = new SimpleDateFormat("yyyy/MM/dd hh:mm");
			Date date = new Date();
			String strDate = sdFormat.format(date);			
			FileWriter f = new FileWriter("./mydata/Instant.txt",true);				
			for(int i=0;i<immediate_data.split("\n").length;i++) {
				f.write(location+"\r\n");
				f.write(air[i]+"\r\n");
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
				String[] air = {"SO2 (ppb)","CO (ppm)","O3 (ppb)","PM10 (�gg/m3)","NOx (ppb)","NO (ppb)",
								"NO2 (ppb)","THC (ppm)","NMHC (ppm)","AT (�J)","CH4 (ppm)","RH (%)"};
				FileWriter f = new FileWriter("./mydata/History.txt",true);
				for(int i=0;i<tmp.length;i++) {					
					f.write(location+"\r\n");
					f.write(air[i]+"\r\n");
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
		if(wh.equals("�x�_")) {
			key = 5;
		}else if(wh.equals("�s�_")) {
			key = 6;
		}else if(wh.equals("���")) {
			key = 20;
		}else if(wh.equals("�s��")) {
			key = 27;
		}else if(wh.equals("�]��")) {
			key = 30;
		}else if(wh.equals("�x��")) {
			key = 35;
		}else if(wh.equals("����")) {
			key = 38;
		}else if(wh.equals("���L")) {
			key = 46;
		}else if(wh.equals("�Ÿq")) {
			key = 49;
		}else if(wh.equals("�x�n")) {
			key = 53;
		}else if(wh.equals("����")) {
			key = 64;
		}else if(wh.equals("�̪F")) {
			key = 66;
		}else if(wh.equals("�x�F")) {
			key = 73;
		}else if(wh.equals("�Ὤ")) {
			key = 71;
		}else if(wh.equals("�y��")) {
			key = 69;
		}else if(wh.equals("���")) {
			key = 76;
		}else if(wh.equals("��")) {
			key = 4;
		}else if(wh.equals("�n��")) {
			key = 41;
		}		
		
	}

}



