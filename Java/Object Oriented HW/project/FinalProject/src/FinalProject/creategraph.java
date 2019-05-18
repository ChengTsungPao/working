package FinalProject;


import javax.imageio.ImageIO;
import java.awt.Container;
import java.awt.GridLayout;
import javax.swing.ImageIcon;
import javax.swing.JFrame;
import javax.swing.JLabel;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import javax.swing.JScrollPane;
import org.jfree.chart.ChartFactory;
import org.jfree.chart.ChartUtilities;
import org.jfree.chart.JFreeChart;
import org.jfree.chart.labels.StandardCategoryItemLabelGenerator;
import org.jfree.chart.plot.CategoryPlot;
import org.jfree.chart.plot.PlotOrientation;
import org.jfree.chart.renderer.category.LineAndShapeRenderer;
import org.jfree.data.category.CategoryDataset;
import org.jfree.data.general.DatasetUtilities;


public class creategraph {
	
	public int number_of_graph;
	public String title;
	public String xlabel;
	public String ylabel;
	public String linename;
	public String[][] air ;
		  /*{{"SO2","SO2 (ppb)","SO2"},{"CO","CO (ppm)","CO"},{"O3","O3 (ppb)","O3"},
			{"PM10","PM10 (μg/m3)","PM10"},{"NOx","NOx (ppb)","NOx"},{"NO","NO (ppb)","NO"},
			{"NO2","NO2 (ppb)","NO2"},{"Tetrahydrocannabinol","THC (ppm)","THC"},{"Non-Methane Hydrocarbon","NMHC (ppm)","NMHC"},
			{"Air Tempature","AT (℃)","AT"},{"CH4","CH4 (ppm)","CH4"},{"Relative Humidity","RH (%)","RH"}};*/
	
	public creategraph() {
		title = "title";
		xlabel = "xlabel";
		ylabel = "ylabel";
		linename = "linename";
	}
	public creategraph(String[] legend) {
		title = legend[0];
		xlabel = legend[1];
		ylabel = legend[2];
		linename = legend[3];
	}
	
	public void graph(String[] a,double[] b) {
		CategoryDataset dataset = createDataset(a,b);
		JFreeChart freeChart = createChart(dataset);
		saveAsFile(freeChart, "D:\\program\\vscode_workspace\\private\\working\\Java\\Object Oriented HW\\project\\FinalProject\\line.jpg", 600, 400);
	}
	
	public void graphs(String[] a,double[][] b) {
		number_of_graph = b.length;
		for(int i=0;i<b.length;i++) {			
			title=air[i][0];
			ylabel=air[i][1];
			linename=air[i][2];
			CategoryDataset dataset = createDataset(a,b[i]);
			JFreeChart freeChart = createChart(dataset);
			saveAsFile(freeChart, "D:\\program\\vscode_workspace\\private\\working\\Java\\Object Oriented HW\\project\\FinalProject\\line"+String.valueOf(i+1)+".jpg", 375, 255);
		}	

		
	}
	
	private void saveAsFile(JFreeChart chart, String outputPath,
			int weight, int height) {
		FileOutputStream out = null;
		try {
			File outFile = new File(outputPath);
			if (!outFile.getParentFile().exists()) {
				outFile.getParentFile().mkdirs();
			}
			out = new FileOutputStream(outputPath);

			ChartUtilities.writeChartAsJPEG(out, chart, weight, height);
			out.flush();
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		} finally {
			if (out != null) {
				try {
					out.close();
				} catch (IOException e) {
					// do nothing
				}
			}
		}
	}

	private JFreeChart createChart(CategoryDataset categoryDataset) {

		JFreeChart jfreechart = ChartFactory.createLineChart(title, 
				xlabel, 
				ylabel, 
				categoryDataset, 
				PlotOrientation.VERTICAL, true, 
				false, 
				false); 
	
		CategoryPlot plot = (CategoryPlot)jfreechart.getPlot();
	
		plot.setBackgroundAlpha(0.5f);
	
		plot.setForegroundAlpha(0.5f);
	
		LineAndShapeRenderer renderer = (LineAndShapeRenderer)plot.getRenderer();
		renderer.setBaseShapesVisible(true); 
		renderer.setBaseLinesVisible(true); 
		renderer.setUseSeriesOffset(true); 
		renderer.setBaseItemLabelGenerator(new StandardCategoryItemLabelGenerator());
		renderer.setBaseItemLabelsVisible(true);
		return jfreechart;
	}
	
	
	private CategoryDataset createDataset(String[] colKeys,double[] b) {
		String[] rowKeys = {linename};
		double[][] data = {b,};	
		return DatasetUtilities.createCategoryDataset(rowKeys, colKeys, data);
	}
	
	
	/////////////////////////    ShowImage        /////////////////////////////
    String Filename;
    BufferedImage image;
    JFrame jf;
    public void shows()
    {
    	new picturetest();
    }
    public void show()
    {
            LoadFile();
            SetTable();
    }
    private void LoadFile()
    {
            Filename="line.jpg";
            try{
                    image=ImageIO.read(new File(Filename));
            }
            catch(Exception e){
                    javax.swing.JOptionPane.showMessageDialog(null, "載入圖檔錯誤: "+Filename);
                    image=null;
            }
    }
    private void SetTable()
    {
            jf = new JFrame("");
            JScrollPane scrollPane = new JScrollPane(new JLabel(new ImageIcon(image)));

            jf.getContentPane().add(scrollPane);
            jf.pack();
            jf.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
            jf.setTitle("Air of parameter data graph");
            jf.setLocationRelativeTo(null);
            jf.setVisible(true);
    }
    
    public class picturetest extends JFrame{
        private String [][] imgbox = new String[][]{{"line1.jpg","line2.jpg","line3.jpg","line4.jpg"},
                        {"line5.jpg","line6.jpg","line7.jpg","line8.jpg"},
                        {"line9.jpg","line10.jpg","line11.jpg","line12.jpg"}};
        private ImageIcon [] imgUP = new ImageIcon[12];
        private JLabel jl[] = new JLabel[12];
        private Container c;
     
        public picturetest (){
        	
            super("Air of parameter data graph");
            c = this.getContentPane();
            setSize(1500,800);
        
            this.setResizable(false);//視窗放大按鈕無效 
            
            setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
            setLayout(new GridLayout(3,4));
            for(int i =0 ; i < 3 ; i++ ){
            	for(int j =0 ; j < 4 ; j++ ) {
            		if(i*4+j<number_of_graph) {
                        imgUP[i*4+j] = new ImageIcon("D:\\program\\vscode_workspace\\private\\working\\Java\\Object Oriented HW\\project\\FinalProject\\"+imgbox[i][j]);
                        jl[i*4+j] = new JLabel(imgUP[i*4+j]);
                        c.add(jl[i*4+j]);
            		}else {
                        imgUP[i*4+j] = new ImageIcon("D:\\program\\vscode_workspace\\private\\working\\Java\\Object Oriented HW\\project\\FinalProject\\NULL.jpg");
                        jl[i*4+j] = new JLabel(imgUP[i*4+j]);
                        c.add(jl[i*4+j]);
            		}
            	}                
                
            } 
            setVisible(true);
        }
       
    }
    
}



