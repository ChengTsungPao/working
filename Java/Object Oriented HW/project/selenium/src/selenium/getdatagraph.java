package selenium;

public class getdatagraph {
	
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
	
	public getdatagraph(String[] d,String[] label) {
		day = new String[d.length];
		legend = new String[4];
		for(int i=0;i<d.length;i++) {
			day[i]=d[i];
		}
		for(int i=0;i<4;i++) {
			legend[i]=label[i];
		}		
	}
	
	public String instant_button(){
		data.Immediate_data();
		data.Immediate_data_process();
		return data.total;
	}
	
	public void history_button(){
		data.History_data(day);
		data.History_data_process();
		String[] x = new String[day.length*24];
		for(int i=0;i<x.length;i++) {
			x[i]=String.valueOf(i);
		}
		double[] y = data.all_data[0];
		creategraph line = new creategraph(legend);
		line.graph(x,y);
		line.show();
	}
	
	
}
