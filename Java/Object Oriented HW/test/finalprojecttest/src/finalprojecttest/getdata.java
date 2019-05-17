package finalprojecttest;
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
	
	public String immediate_data="", history_data="";
	public int line,key=5,flag;
	
	/*public void Immediate_data(String wh) {
		where(wh);
		ChromeOptions options = new ChromeOptions();
		options.addArguments("--headless");		
		WebDriver driver = new ChromeDriver(options);
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
	}*/
	
	/*public void Immediate_data(String wh) {
		
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
		
		
		System.out.println(key);
		Options1.get(0).click();
		Options1.get(key).click();
		
		WebElement select2 = driver.findElement(By.id("ctl05_lbParam"));
		Select dropDown2 = new Select(select2);
		List<WebElement> Options2 = dropDown2.getOptions();
		

        List<WebElement> itemList; 
        

		
		String a;
		String[] tmp,tmp1;
		int times=0;
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
					Options2.get(0).click();
					Options2.get(i).click();
				}
				
				driver.findElement(By.id("ctl05_btnQuery")).click();
		        try {
		            Thread.sleep(5000);
		        	//driver.wait(5000);
		        } catch (InterruptedException n) {
		            n.printStackTrace(); 
		        }
				
				
		        itemList = driver.findElements(By.tagName("td")); 
		        
		        line=0;
				for(WebElement e : itemList) {
					//System.out.println("line="+line);
					//System.out.println(e.getText());

					//driver.manage().timeouts().implicitlyWait(10, TimeUnit.SECONDS);
					if(line++==28) {
						tmp=e.getText().split("\n");
						flag=0;
						for(String y:tmp) {	
							//System.out.println(y.split(" ")[0]);
							if(y.split(" ")[0].equals(strDate)) {
								immediate_data=immediate_data+a+" "+y+"\n";
								flag=1;
								break;
							}
	
						}
						if(flag==0) {
							immediate_data=immediate_data+a+" None"+"\n";
						}
					
					}
					/*if(line++==28) {
						tmp=e.getText().split("\n");
						if(tmp.length>120) {
							tmp1=tmp[120].split(" ");
							immediate_data=immediate_data+a+" ";
							for(int k=1;k<tmp1.length;k++) {
								immediate_data=immediate_data+" "+tmp1[k];								
							}
							immediate_data=immediate_data+"\n";
							times=0;
						}
						else {
							if(times<1) i--;
							if(times++>=1) {
								immediate_data=immediate_data+a+" None"+"\n";
								times=0;
							}							
						}
						
					}
					if(line>30) break;			
				}
				
				//System.out.println(Options2.get(7).getText());
				driver.close();
				
				
				driver = new ChromeDriver();//options
				driver.get("https://taqm.epa.gov.tw/taqm/tw/HourlyData.aspx"); 
				select1 = driver.findElement(By.id("ctl05_lbSite"));
				dropDown1 = new Select(select1); 
				Options1 = dropDown1.getOptions();
				
				
				System.out.println(key);
				Options1.get(0).click();
				Options1.get(key).click();
				
				select2 = driver.findElement(By.id("ctl05_lbParam"));
				dropDown2 = new Select(select2);
				Options2 = dropDown2.getOptions();
				

			}

			if(line++==28) {
				tmp=e.getText().split("\n");
				flag=0;
				for(String y:tmp) {	
					System.out.println(y.split(" ")[0]);
					if(y.split(" ")[0].equals("05/16")) {
						immediate_data=immediate_data+y+"\n";
						flag=1;
						break;
					}

				}
				if(flag==0) {
					immediate_data=immediate_data+a+" None"+"\n";
				}
				
			}
		

			
			
		}
		System.out.println(immediate_data);	
		//driver.close();
	}*/
	
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
		
		
		System.out.println(key);
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
            Thread.sleep(2000);
        	//driver.wait(5000);
        } catch (InterruptedException n) {
            n.printStackTrace(); 
        }
		
		driver.findElement(By.id("ctl05_btnQuery")).click();
        try {
            Thread.sleep(15000);
        	//driver.wait(5000);
        } catch (InterruptedException n) {
            n.printStackTrace(); 
        }
		
		
        List<WebElement> itemList = driver.findElements(By.tagName("td")); 
        
        line=0;
		for(WebElement e : itemList) {
			//System.out.println("line="+line);
			//System.out.println(e.getText());

			//driver.manage().timeouts().implicitlyWait(10, TimeUnit.SECONDS);
			if(line++==28) {
				tmp=e.getText().split("\n");
				flag=0;
				for(String y:tmp) {	
					//System.out.println(y.split(" ")[0]);
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
	}	
	
	/*public void History_data(String[] day,String wh) {
		where(wh);
		ChromeOptions options = new ChromeOptions();
		options.addArguments("--headless");		
		WebDriver driver = new ChromeDriver(options);
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
	}*/
	
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
			
			
			System.out.println(key);
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
	            Thread.sleep(2000);
	        	//driver.wait(5000);
	        } catch (InterruptedException n) {
	            n.printStackTrace(); 
	        }
			
			driver.findElement(By.id("ctl05_btnQuery")).click();
	        try {
	            Thread.sleep(10000);
	        	//driver.wait(5000);
	        } catch (InterruptedException n) {
	            n.printStackTrace(); 
	        }
			
			
	        List<WebElement> itemList = driver.findElements(By.tagName("td")); 
	        
	        line=0;
	        
			for(WebElement e : itemList) {
				System.out.println("line="+line);
				System.out.println(e.getText());
	
				//driver.manage().timeouts().implicitlyWait(10, TimeUnit.SECONDS);
				if(line++==28) {			        
					tmp=e.getText().split("\n");
					flag=0;
					for(String y:tmp) {	
						System.out.println(y.split(" ")[0]);
				        try {
							if(Integer.parseInt(y.split(" ")[0].split("/")[0])==Integer.parseInt(day[0].split("/")[1]) &&
									   Integer.parseInt(y.split(" ")[0].split("/")[1])==Integer.parseInt(day[0].split("/")[2])) {
										history_data=history_data+y+"\n";
										flag=1;								
									}
				        } catch (NumberFormatException n) {
				            //n.printStackTrace(); 
				        	System.out.print("");
				        }
					}
					if(flag==0) {
						history_data=history_data+"None"+"\n";
					}
					break;
				}
			}
	
			System.out.println(history_data);

		}else {
			
			//ChromeOptions options = new ChromeOptions();
			//options.addArguments("--headless");		
			WebDriver driver = new ChromeDriver();//options
			driver.get("https://taqm.epa.gov.tw/taqm/tw/HourlyData.aspx"); 
			

    		
			WebElement select1 = driver.findElement(By.id("ctl05_lbSite"));
			Select dropDown1 = new Select(select1); 
			List<WebElement> Options1 = dropDown1.getOptions();
			
			
			System.out.println(key);
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
	            Thread.sleep(1000);
	        } catch (InterruptedException n) {
	            n.printStackTrace(); 
	        }
			driver.findElement(By.id("ctl05_btnQuery")).click();
			
	        try {
	            Thread.sleep(5000);
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
	        	//System.out.println(tmp1[i].split(" ")[0].split("/")[0]);
		        try {
		        	if(Integer.parseInt(tmp1[i].split(" ")[0].split("/")[0])==Integer.parseInt(day[0].split("/")[1]) &&
		 	        	   Integer.parseInt(tmp1[i].split(" ")[0].split("/")[1])==Integer.parseInt(day[0].split("/")[2])) {
		 	        		for(;i<tmp1.length;i++) {
		 	        			history_data = history_data+tmp1[i]+"\n";	        			
		 	        		}
		 	        	}
		        } catch (NumberFormatException n) {
		            //n.printStackTrace(); 
		        	System.out.print("");
		        }

	        }
        
	        System.out.println(history_data);
	        
		}
		
	}
	
	public void where(String wh) {
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
	
	public int count;
	public String[] tmp;
	
	/*public String total = "";
	public String[] parameter = new String[15];;
	public double[] number = new double[15];;
	public String[] unit = new String[15];
	

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
		
	}*/
	
	/*public double[][] all_data;
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

	}*/
	
	public void History_data_process(String[] day) {
		
		
	}
	
	
	public void File_immediate(){
		try {
			SimpleDateFormat sdFormat = new SimpleDateFormat("yyyy/MM/dd hh:mm:ss");
			Date date = new Date();
			String strDate = sdFormat.format(date);
			FileWriter f = new FileWriter("./mydata/Instant.txt",true);		
			f.write(strDate);
			f.write(immediate_data);
			f.write("\r\n");
			f.close();
		}
	    catch(IOException ie) {
	        ie.printStackTrace();
	    }
	}
	
	public void File_History(String[] day,String label) {
		try {
			FileWriter f = new FileWriter("./mydata/History.txt",true);	
			f.write(label);
			f.write("\r\n");
			f.write(history_data);
			f.write("\r\n");
			f.close();
		}
	    catch(IOException ie) {
	        ie.printStackTrace();
	    }
	}

}


