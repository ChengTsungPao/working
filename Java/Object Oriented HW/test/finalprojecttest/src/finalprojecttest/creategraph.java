package finalprojecttest;

import javax.imageio.ImageIO;

import java.awt.Container;
import java.awt.GridLayout;
import javax.swing.ImageIcon;
import javax.swing.JFrame;
import javax.swing.JLabel;

import java.awt.Container;
import java.awt.GridLayout;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import javax.swing.ImageIcon;
import javax.swing.JFrame;
import javax.swing.JLabel;
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
	
	public String title;
	public String xlabel;
	public String ylabel;
	public String linename;
	
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
		saveAsFile(freeChart, "D:\\program\\vscode_workspace\\private\\working\\Java\\Object Oriented HW\\test\\finalprojecttest\\line.jpg", 600, 400);
		new picturetest();
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

			ChartUtilities.writeChartAsJPEG(out, chart, 600, 400);
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
		// DefaultCategoryDataset categoryDataset = new
		// DefaultCategoryDataset();
		// categoryDataset.addValue(10, "rowKey", "colKey");
		return DatasetUtilities.createCategoryDataset(rowKeys, colKeys, data);
	}
	
	
	/////////////////////////    ShowImage        /////////////////////////////
    String Filename;
    BufferedImage image;
    JFrame jf;
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
        private String [][] imgbox = new String[][]{{"graph1.jpg","graph1.jpg","graph2.jpg","graph2.jpg"},
                        {"graph3.jpg","graph4.jpg","graph5.jpg","graph2.jpg"},
                        {"graph6.jpg","graph7.jpg","graph8.jpg","graph2.jpg"}};
        private ImageIcon [] imgUP = new ImageIcon[12];
        private JLabel jl[] = new JLabel[12];
        private Container c;
     
        public picturetest (){
        	
            super("利用按鈕控制圖片切換");
            c = this.getContentPane();
            setSize(1000,600);
        
            this.setResizable(false);//視窗放大按鈕無效 
            
            setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            setLayout(new GridLayout(3,4));
            for(int i =0 ; i < 3 ; i++ ){
            	for(int j =0 ; j < 4 ; j++ ) {
                    imgUP[i*4+j] = new ImageIcon("D:\\program\\vscode_workspace\\private\\working\\Java\\Object Oriented HW\\test\\manygraph\\"+imgbox[i][j]);
                    jl[i*4+j] = new JLabel(imgUP[i*3+j]);
                    c.add(jl[i*4+j]);
            	}

                
                
                
            } 
            setVisible(true);
        }
       
    }
    
}


