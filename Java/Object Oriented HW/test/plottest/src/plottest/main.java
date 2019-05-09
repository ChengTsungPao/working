package plottest;


import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
 
import org.jfree.chart.ChartFactory;
import org.jfree.chart.ChartUtilities;
import org.jfree.chart.JFreeChart;
import org.jfree.chart.labels.StandardCategoryItemLabelGenerator;
import org.jfree.chart.plot.CategoryPlot;
import org.jfree.chart.plot.PlotOrientation;
import org.jfree.chart.renderer.category.LineAndShapeRenderer;
import org.jfree.data.category.CategoryDataset;
import org.jfree.data.general.DatasetUtilities;
 
   
public class main {

	public static void main(String[] args) {

		CategoryDataset dataset = createDataset();

		JFreeChart freeChart = createChart(dataset);

		saveAsFile(freeChart, "D:\\program\\vscode_workspace\\private\\working\\Java\\Object Oriented HW\\test\\plottest\\line.jpg", 600, 400);
		
		ShowImage test = new ShowImage();
		test.show();
	}
 

	public static void saveAsFile(JFreeChart chart, String outputPath,
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
 

	public static JFreeChart createChart(CategoryDataset categoryDataset) {

		JFreeChart jfreechart = ChartFactory.createLineChart("graph", 
				"year", 
				"number", 
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
 

	public static CategoryDataset createDataset() {
		String[] rowKeys = {"A¥­¥x"};
		String[] colKeys = {"0:00", "1:00", "2:00", "7:00", "8:00", "9:00",
				"10:00", "11:00", "12:00", "13:00", "16:00", "20:00", "21:00",
				"23:00"};
		double[][] data = {{4, 3, 1, 1, 1, 1, 2, 2, 2, 1, 8, 2, 1, 1},};

		// DefaultCategoryDataset categoryDataset = new
		// DefaultCategoryDataset();
		// categoryDataset.addValue(10, "rowKey", "colKey");
		return DatasetUtilities.createCategoryDataset(rowKeys, colKeys, data);
	}
}

