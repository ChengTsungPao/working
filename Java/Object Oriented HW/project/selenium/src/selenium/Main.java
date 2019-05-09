package selenium;

public class Main {
	public static void main(String[] args) {
		String[] day = {"2019/5/1","2019/5/5","2019/5/8"};
		getdata data = new getdata();
		//data.Immediate_data();
		//data.Immediate_data_process();		
		data.History_data(day);
		data.History_data_process();
		/*creategraph line = new creategraph();
		line.graph();
		line.show();*/	
		 
	}
}
