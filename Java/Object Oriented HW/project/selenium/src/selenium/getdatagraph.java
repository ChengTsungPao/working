package selenium;

public class getdatagraph {
	
	public int find;
	public String[] day;
	public String[] legend;
	getdata data = new getdata();
	
	public getdatagraph() {
		day = new String[1];
		legend = new String[4];
		day[0] = "2019/5/1";
		legend[0] = "graph";
		legend[1] = "time";
		legend[2] = "parameter";
		legend[3] = "parameter";		
	}
	
	public getdatagraph(String[] d,String label) {
		day = new String[d.length];
		legend = new String[4];
		for(int i=0;i<d.length;i++) {
			day[i]=d[i];
		}
		choose(label);		
	}
	
	public String instant_button(){
		data.Immediate_data();
		data.Immediate_data_process();
		return data.immediate_data;
	}
	
	public void history_button(){
		data.History_data(day);
		data.History_data_process();
		String[] x = new String[day.length*24];
		for(int i=0;i<x.length;i++) {
			x[i]=String.valueOf(i);
		}
		double[] y = data.all_data[find];
		creategraph line = new creategraph(legend);
		//System.out.printf("%d %d\n",x.length,y.length);
		line.graph(x,y);
		line.show();
	}
	
	public void choose(String a) {
		
		if(a.equals("一氧化氮") || a.equals("NO")) {
			find=0;
			legend[0] = "NO";
			legend[1] = "time (hr)";
			legend[2] = "NO (ppb)";
			legend[3] = "NO";		
			
		}else if(a.equals("大氣溫度") || a.equals("AT")) {
			find=11;
			legend[0] = "Air Tempature";
			legend[1] = "time (hr)";
			legend[2] = "AT (℃)";
			legend[3] = "AT";
			
		}else if(a.equals("二氧化氮") || a.equals("NO2")) {
			find=1;
			legend[0] = "NO2";
			legend[1] = "time (s)";
			legend[2] = "NO2 (ppb)";
			legend[3] = "NO2";
			
		}else if(a.equals("相對溼度") || a.equals("RH")) {
			find=12;
			legend[0] = "Relative Humidity";
			legend[1] = "time (hr)";
			legend[2] = "RH (%)";
			legend[3] = "RH";
			
		}else if(a.equals("氮氧化物") || a.equals("NOx")) {
			find=2;
			legend[0] = "NOx";
			legend[1] = "time (hr)";
			legend[2] = "NOx (ppb)";
			legend[3] = "NOx";
			
		}else if(a.equals("二氧化硫") || a.equals("SO2")) {
			find=3;
			legend[0] = "SO2";
			legend[1] = "time (hr)";
			legend[2] = "SO2 (ppb)";
			legend[3] = "SO2";
			
		}else if(a.equals("風速") || a.equals("WS")) {
			find=14;
			legend[0] = "Wind Speed";
			legend[1] = "time (hr)";
			legend[2] = "WS (m/s)";
			legend[3] = "WS";
			
		}else if(a.equals("一氧化碳") || a.equals("CO")) {
			find=4;
			legend[0] = "CO";
			legend[1] = "time (hr)";
			legend[2] = "CO (ppm)";
			legend[3] = "CO";
			
		}else if(a.equals("甲烷") || a.equals("CH4")) {
			find=5;
			legend[0] = "CH4";
			legend[1] = "time (hr)";
			legend[2] = "CH4 (ppm)";
			legend[3] = "CH4";
			
		}else if(a.equals("總碳氫化合物") || a.equals("THC")) {
			find=6;
			legend[0] = "Tetrahydrocannabinol";
			legend[1] = "time (hr)";
			legend[2] = "THC (ppm)";
			legend[3] = "THC";
			
		}else if(a.equals("非甲烷碳氫化合物") || a.equals("NMHC")) {
			find=7;
			legend[0] = "Non-Methane Hydrocarbon";
			legend[1] = "time (hr)";
			legend[2] = "NMHC (ppm)";
			legend[3] = "NMHC";
			
		}else if(a.equals("臭氧") || a.equals("O3")) {
			find=8;
			legend[0] = "O3";
			legend[1] = "time (hr)";
			legend[2] = "O3 (ppb)";
			legend[3] = "O3";
			
		}else if(a.equals("懸浮微粒PM10") || a.equals("PM10")) {
			find=9;
			legend[0] = "PM10";
			legend[1] = "time (hr)";
			legend[2] = "PM10 (μg/m3)";
			legend[3] = "PM10";
			
		}else if(a.equals("懸浮微粒PM2.5") || a.equals("PM2.5") || a.equals("parameter")) {
			find=10;
			legend[0] = "PM2.5";
			legend[1] = "time (hr)";
			legend[2] = "PM2.5 (μg/m3)";
			legend[3] = "PM2.5";
			
		}else {
			find=10;
			legend[0] = "PM2.5";
			legend[1] = "time (hr)";
			legend[2] = "PM2.5 (μg/m3)";
			legend[3] = "PM2.5";			
		}
				
	}
	
	
}
