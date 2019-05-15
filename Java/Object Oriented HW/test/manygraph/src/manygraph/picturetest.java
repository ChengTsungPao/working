package manygraph;

import java.awt.Container;
import java.awt.GridLayout;
import javax.swing.ImageIcon;
import javax.swing.JFrame;
import javax.swing.JLabel;
 
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
   
  public static void main(String[] args) {
    // TODO Auto-generated method stub
	  new picturetest();
  }
}