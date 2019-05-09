package selenium;

public class Main {
	public static void main(String[] args) {
		String[] day = {"2019/5/1","2019/5/5","2019/5/8"};
		getdata data = new getdata();
		data.Immediate_data();	
		data.History_data(day);
		
		creategraph line = new creategraph();
		line.graph();
		line.show();	
		 
	}
}
