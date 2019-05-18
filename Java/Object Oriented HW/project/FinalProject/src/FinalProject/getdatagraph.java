package FinalProject;


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
	
	public String instant_button(boolean b,String wh){
		data.Immediate_data(wh);
		data.Immediate_data_process();
		if(b) data.File_immediate();
		return data.immediate_data;
	}
	
	
	public void history_button(boolean b,String wh){
		data.History_data(day,wh,find);
		data.History_data_process(day);		
		if(b) data.File_History(day,legend[3]);		
		if(day.length==1) {
			String[] x = new String[data.all_data1[0].length];
			for(int i=0;i<x.length;i++) {
				x[i]=String.valueOf(i);
			}
			double[][] y = data.all_data1;
			creategraph line = new creategraph(legend);
			line.air = data.air;
			line.graphs(x,y);
			line.shows();
			
		}else {
			String[] x = new String[data.all_data2.length];
			for(int i=0;i<x.length;i++) {
				x[i]=String.valueOf(i);
			}
			double[] y = data.all_data2;
			creategraph line = new creategraph(legend);			
			line.graph(x,y);
			line.show();
		}
	}
	
	public void choose(String a) {
		
		if(a.equals("�@��ƴ�") || a.equals("NO")) {
			find=5;
			legend[0] = "NO";
			legend[1] = "time (hr)";
			legend[2] = "NO (ppb)";
			legend[3] = "NO";		
			
		}else if(a.equals("�j��ū�") || a.equals("AT")) {
			find=11;
			legend[0] = "Air Tempature";
			legend[1] = "time (hr)";
			legend[2] = "AT (�J)";
			legend[3] = "AT";
			
		}else if(a.equals("�G��ƴ�") || a.equals("NO2")) {
			find=6;
			legend[0] = "NO2";
			legend[1] = "time (s)";
			legend[2] = "NO2 (ppb)";
			legend[3] = "NO2";
			
		}else if(a.equals("�۹�ë�") || a.equals("RH")) {
			find=18;
			legend[0] = "Relative Humidity";
			legend[1] = "time (hr)";
			legend[2] = "RH (%)";
			legend[3] = "RH";
			
		}else if(a.equals("���ƪ�") || a.equals("NOx")) {
			find=4;
			legend[0] = "NOx";
			legend[1] = "time (hr)";
			legend[2] = "NOx (ppb)";
			legend[3] = "NOx";
			
		}else if(a.equals("�G��Ʋ�") || a.equals("SO2")) {
			find=0;
			legend[0] = "SO2";
			legend[1] = "time (hr)";
			legend[2] = "SO2 (ppb)";
			legend[3] = "SO2";
			
		}else if(a.equals("���t") || a.equals("WS")) {
			find=9;
			legend[0] = "Wind Speed";
			legend[1] = "time (hr)";
			legend[2] = "WS (m/s)";
			legend[3] = "WS";
			
		}else if(a.equals("�@��ƺ�") || a.equals("CO")) {
			find=1;
			legend[0] = "CO";
			legend[1] = "time (hr)";
			legend[2] = "CO (ppm)";
			legend[3] = "CO";
			
		}else if(a.equals("���J") || a.equals("CH4")) {
			find=15;
			legend[0] = "CH4";
			legend[1] = "time (hr)";
			legend[2] = "CH4 (ppm)";
			legend[3] = "CH4";
			
		}else if(a.equals("�`�ҲB�ƦX��") || a.equals("THC")) {
			find=7;
			legend[0] = "Tetrahydrocannabinol";
			legend[1] = "time (hr)";
			legend[2] = "THC (ppm)";
			legend[3] = "THC";
			
		}else if(a.equals("�D���J�ҲB�ƦX��") || a.equals("NMHC")) {
			find=8;
			legend[0] = "Non-Methane Hydrocarbon";
			legend[1] = "time (hr)";
			legend[2] = "NMHC (ppm)";
			legend[3] = "NMHC";
			
		}else if(a.equals("���") || a.equals("O3")) {
			find=2;
			legend[0] = "O3";
			legend[1] = "time (hr)";
			legend[2] = "O3 (ppb)";
			legend[3] = "O3";
			
		}else if(a.equals("�a�B�L��PM10") || a.equals("PM10")) {
			find=3;
			legend[0] = "PM10";
			legend[1] = "time (hr)";
			legend[2] = "PM10 (�gg/m3)";
			legend[3] = "PM10";
			
		}else if(a.equals("�a�B�L��PM2.5") || a.equals("PM2.5") || a.equals("parameter")) {
			find=11;
			legend[0] = "PM2.5";
			legend[1] = "time (hr)";
			legend[2] = "PM2.5 (�gg/m3)";
			legend[3] = "PM2.5";
			
		}else {
			find=11;
			legend[0] = "Air Tempature";
			legend[1] = "time (hr)";
			legend[2] = "AT (�J)";
			legend[3] = "AT";			
		}
				
	}
	
	
}

