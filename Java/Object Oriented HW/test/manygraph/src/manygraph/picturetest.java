package manygraph;

import java.awt.Container;
import java.awt.GridLayout;
import javax.swing.ImageIcon;
import javax.swing.JFrame;
import javax.swing.JLabel;
 
public class picturetest extends JFrame{
    private String [][] imgbox = new String[][]{{"graph1.jpg","graph1.jpg","graph2.jpg"},
                    {"graph3.jpg","graph4.jpg","graph5.jpg"},
                    {"graph6.jpg","graph7.jpg","graph8.jpg"}};
    private ImageIcon [] imgUP = new ImageIcon[9];
    private JLabel jl[] = new JLabel[9];
    private Container c;
 
    public picturetest (){
    	
        super("利用按鈕控制圖片切換");
        c = this.getContentPane();
        setSize(800,600);
    
        this.setResizable(false);//視窗放大按鈕無效 
        
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLayout(new GridLayout(3,3));
        for(int i =0 ; i < 9 ; i++ ){
            imgUP[i] = new ImageIcon("D:\\program\\vscode_workspace\\private\\working\\Java\\Object Oriented HW\\test\\manygraph\\"+imgbox[i/imgbox.length][i%imgbox.length]);
            jl[i] = new JLabel(imgUP[i]);
            
            c.add(jl[i]);
            
        } 
        setVisible(true);
    }
   
  public static void main(String[] args) {
    // TODO Auto-generated method stub
	  new picturetest();
  }
}