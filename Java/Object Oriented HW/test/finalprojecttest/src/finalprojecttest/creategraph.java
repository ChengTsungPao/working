package finalprojecttest;

import javax.imageio.ImageIO;
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
		saveAsFile(freeChart, "D:\\program\\vscode_workspace\\private\\working\\Java\\Object Oriented HW\\project\\selenium\\line.jpg", 600, 400);
		
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
                    javax.swing.JOptionPane.showMessageDialog(null, "¸ü¤J¹ÏÀÉ¿ù»~: "+Filename);
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
}
