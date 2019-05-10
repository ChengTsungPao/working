package selenium;

public class Main {
	public static void main(String[] args) {
		String[] day = {"2019/5/1"};
		getdata data = new getdata();
		data.Immediate_data();
		data.Immediate_data_process();		
		data.History_data(day);
		data.History_data_process();
		
		/*for(int i=0;i<3;i++) {
			for(int j=0;j<16;j++) {
				for(int k=0;k<24;k++) {						
					System.out.printf("%f ",data.all_data[j][k+24*i]);
				}
				System.out.println();
			}
			System.out.println();
		}*/	
		
		String[] x = new String[day.length*24];
		for(int i=0;i<x.length;i++) {
			x[i]=String.valueOf(i);
		}
		double[] y = data.all_data[0];
		/*String[] x = {"5/8", "1:00", "2:00", "7:00", "8:00", "9:00", "10:00", 
				      "11:00", "12:00", "13:00", "16:00", "20:00", "21:00", "23:00"};
		double[] y = {1,2,3,4,5,6,7,8,9,10,11,12,13,14};*/
		
		String[] legend = {"graph","time","parameter","parameter"};
		creategraph line = new creategraph(legend);
		line.graph(x,y);
		line.show();	
		 
	}
}
