package finalprojecttest;

import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JCheckBox;
import javax.swing.JTextArea;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JTextField;
import javax.swing.JRadioButton;
import java.awt.*;
import javax.swing.BorderFactory;
import javax.swing.ButtonGroup;


public class parentGui extends JFrame{

    private JButton historybutton,instantbutton;  
    private JCheckBox historyCheckBox,instantCheckBox,instantCheckBox1; 
    //private JRadioButton city;
    private JRadioButton[] city = new JRadioButton[18];
    public JTextField daytextfield,labeltextfield;
    private ButtonGroup group;


    public parentGui(){
        super("The Data of Air Parameter");
        //setLayout(new GridBagLayout());  
        

        
        
        ImagePanel imagePanel = new ImagePanel();  
        imagePanel.setOpaque(true); 
        imagePanel.setLayout(new FlowLayout(FlowLayout.LEFT));
        //imagePanel.setBackground(Color.white); 
        //GridLayout gridLayout = new GridLayout();
        //imagePanel.setLayout(gridLayout);
        //imagePanel.setBorder(BorderFactory.createEtchedBorder());       
        
        
        
        //GridBagConstraints Panellayout = new GridBagConstraints();
        //Panellayout.gridx=0;
        //Panellayout.gridy=0;
        //Panellayout.gridwidth = 800;
        //Panellayout.gridheight = 600;
        //Panellayout.fill = GridBagConstraints.BOTH;  
        //Panellayout.anchor = GridBagConstraints.NORTHWEST;
        add(imagePanel);  
        imagePanel.setVisible(true);
        
        
        JTextArea blank1 = new JTextArea("                                                                                    "
        		+ "                                                                        " );
        blank1.setOpaque(false);
        imagePanel.add(blank1); 
        
        JTextArea blank2 = new JTextArea("                                                                               "
        		+ "                     ");
        //text.setBackground(Color.white);//SystemColor.control
        blank2.setOpaque(false);       
        imagePanel.add(blank2);
        
        city[17] = new JRadioButton("基隆       "
				+ "                                                                     ");
		//Tapie.setFont(new Font("Serif", Font.PLAIN, 14));
        city[17].setOpaque(false); 
        imagePanel.add(city[17]); 
        

        
        

 
        
        JTextArea blank3 = new JTextArea("                                                                            "
        		+ "              ");
        blank3.setOpaque(false);
        imagePanel.add(blank3);    
        
        city[0] = new JRadioButton("台北"
				+ "              ");
		//Tapie.setFont(new Font("Serif", Font.PLAIN, 14));
        city[0].setOpaque(false); 
        imagePanel.add(city[0]); 
        
        JTextArea text1 = new JTextArea("可使用參數:                                                           ");
        
        //text.setBackground(Color.white);//SystemColor.control
        text1.setOpaque(false);       
        imagePanel.add(text1); 
 
        JTextArea blank4 = new JTextArea("                                                                           ");

        blank4.setOpaque(false);
        imagePanel.add(blank4); 

        city[1] = new JRadioButton("桃園");
        city[1].setOpaque(false); 
        imagePanel.add(city[1]);
        
        city[2] = new JRadioButton("新北"
				+ "           ");
        //New_Taipei.setFont(new Font("Serif", Font.PLAIN, 14));
        city[2].setOpaque(false); 
        imagePanel.add(city[2]);       

        
        JTextArea text2 = new JTextArea("NO (一氧化氮)                     NO2 (二氧化氮)"
        		+ "                              ");
        //text.setBackground(Color.white);//SystemColor.control
        text2.setOpaque(false);       
        imagePanel.add(text2);
        
        JTextArea blank5 = new JTextArea("                                                                       ");

        blank5.setOpaque(false);
        imagePanel.add(blank5);
        
        city[3] = new JRadioButton("新竹"
				+ "         ");
        //New_Taipei.setFont(new Font("Serif", Font.PLAIN, 14));
        city[3].setOpaque(false); 
        imagePanel.add(city[3]);   
        
        city[4] = new JRadioButton("宜蘭"
				+ "      ");
        //New_Taipei.setFont(new Font("Serif", Font.PLAIN, 14));
        city[4].setOpaque(false); 
        imagePanel.add(city[4]);      
        
        
        
        JTextArea text3 = new JTextArea("NOx (氮氧化物)                   SO2 (二氧化硫)");
        //text.setBackground(Color.white);//SystemColor.control
        text3.setOpaque(false);       
        imagePanel.add(text3);
        
        JTextArea blank6 = new JTextArea("                                                             ");

        blank6.setOpaque(false);
        imagePanel.add(blank6);        
        
        city[5] = new JRadioButton("苗栗"
				+ "                                          ");
        //New_Taipei.setFont(new Font("Serif", Font.PLAIN, 14));
        city[5].setOpaque(false); 
        imagePanel.add(city[5]);       
        
        JTextArea text4 = new JTextArea("CO (一氧化碳)                     CH4 (甲烷)              ");
        //text.setBackground(Color.white);//SystemColor.control
        text4.setOpaque(false);       
        imagePanel.add(text4);
        
        JTextArea blank7 = new JTextArea("                                                     ");

        blank7.setOpaque(false);
        imagePanel.add(blank7);        
        
        city[6] = new JRadioButton("台中"
				+ "                                                  ");
        //New_Taipei.setFont(new Font("Serif", Font.PLAIN, 14));
        city[6].setOpaque(false); 
        imagePanel.add(city[6]);         
        
        JTextArea text5 = new JTextArea("THC (總碳氫化合物)            NMHC (非甲烷碳氫化合物)");
        //text.setBackground(Color.white);//SystemColor.control
        text5.setOpaque(false);       
        imagePanel.add(text5);
 
        
        JTextArea blank8 = new JTextArea("                                             ");

        blank8.setOpaque(false);
        imagePanel.add(blank8);        
        
        city[7] = new JRadioButton("彰化"
				+ "                                                          ");
        //New_Taipei.setFont(new Font("Serif", Font.PLAIN, 14));
        city[7].setOpaque(false); 
        imagePanel.add(city[7]);        
        
        JTextArea text6 = new JTextArea("O3 (臭氧)                              PM10 (懸浮微粒PM10)              ");
        //text.setBackground(Color.white);//SystemColor.control
        text6.setOpaque(false);       
        imagePanel.add(text6);
        
        JTextArea blank9 = new JTextArea("                                    ");

        blank9.setOpaque(false);
        imagePanel.add(blank9); 
        
        city[8] = new JRadioButton("雲林            ");
        //New_Taipei.setFont(new Font("Serif", Font.PLAIN, 14));
        city[8].setOpaque(false); 
        imagePanel.add(city[8]);        
        
        city[9] = new JRadioButton("南投"
				+ "      ");
        //New_Taipei.setFont(new Font("Serif", Font.PLAIN, 14));
        city[9].setOpaque(false); 
        imagePanel.add(city[9]); 
        
        city[10] = new JRadioButton("花蓮"
				+ "              ");
        //New_Taipei.setFont(new Font("Serif", Font.PLAIN, 14));
        city[10].setOpaque(false); 
        imagePanel.add(city[10]);        
        
        JTextArea text7 = new JTextArea("PM2.5 (懸浮微粒PM2.5)      AT (大氣溫度)                                               ");
        //text.setBackground(Color.white);//SystemColor.control
        text7.setOpaque(false);       
        imagePanel.add(text7);
        
        JTextArea blank10 = new JTextArea("     ");

        blank10.setOpaque(false);
        imagePanel.add(blank10); 
        
        city[11] = new JRadioButton("澎湖                      ");
        //New_Taipei.setFont(new Font("Serif", Font.PLAIN, 14));
        city[11].setOpaque(false); 
        imagePanel.add(city[11]); 
        
        city[12] = new JRadioButton("嘉義"
				+ "                                                           ");
        //New_Taipei.setFont(new Font("Serif", Font.PLAIN, 14));
        city[12].setOpaque(false); 
        imagePanel.add(city[12]); 
        
        JTextArea text8 = new JTextArea("RH (相對溼度)                      WS (風速)                        ");
        //text.setBackground(Color.white);//SystemColor.control
        text8.setOpaque(false);       
        imagePanel.add(text8);
        
        JTextArea blank11 = new JTextArea("                                                                            "
        		+ "                                                                                                   "
        		+ "                                                                                              ");

        blank11.setOpaque(false);
        imagePanel.add(blank11);      

        

        
        JTextArea blank12 = new JTextArea("                                         ");

        blank12.setOpaque(false);
        imagePanel.add(blank12);  
        
        city[13] = new JRadioButton("台南"
				+ "                                                              ");
        //New_Taipei.setFont(new Font("Serif", Font.PLAIN, 14));
        city[13].setOpaque(false); 
        imagePanel.add(city[13]); 
        
		instantCheckBox = new JCheckBox("儲存即時數據        ");
        instantCheckBox.setFont(new Font("Serif", Font.PLAIN, 14));
        instantCheckBox.setOpaque(false); 
        imagePanel.add(instantCheckBox); 
        
        historyCheckBox = new JCheckBox("儲存歷史數據    ");
        historyCheckBox.setFont(new Font("Serif", Font.PLAIN, 14));
        historyCheckBox.setOpaque(false); 
        imagePanel.add(historyCheckBox); 
        
        JTextArea blank13 = new JTextArea("                                                 ");

        blank13.setOpaque(false);
        imagePanel.add(blank13); 
        
        city[14] = new JRadioButton("高雄"
				+ "        ");
        //New_Taipei.setFont(new Font("Serif", Font.PLAIN, 14));
        city[14].setOpaque(false); 
        imagePanel.add(city[14]); 
        
        city[15] = new JRadioButton("台東"
				+ "                             ");
        //New_Taipei.setFont(new Font("Serif", Font.PLAIN, 14));
        city[15].setOpaque(false); 
        imagePanel.add(city[15]); 
        
        daytextfield = new JTextField("Input the date before", 20);
        daytextfield.setFont(new Font("Serif", Font.PLAIN, 14));
        imagePanel.add(daytextfield); 
        
        instantbutton = new JButton("Instant  data");
        imagePanel.add(instantbutton); 
        
        JTextArea blank14 = new JTextArea("                                                      ");

        blank14.setOpaque(false);
        imagePanel.add(blank14); 
        

        
        city[16] = new JRadioButton("屏東"
				+ "                                                 ");
        //New_Taipei.setFont(new Font("Serif", Font.PLAIN, 14));
        city[16].setOpaque(false); 
        imagePanel.add(city[16]); 
        
        labeltextfield = new JTextField("Input the parameter", 20);
        labeltextfield.setFont(new Font("Serif", Font.PLAIN, 14));
        imagePanel.add(labeltextfield); 
                
        historybutton = new JButton("History data");
        imagePanel.add(historybutton);
        
        
        /*JLabel blank1 = new JLabel("Hi");
        blank1.setFont(new Font("Serif", Font.PLAIN, 14));
        GridBagConstraints blanklayout = new GridBagConstraints();
        blanklayout.gridx = 0;
        blanklayout.gridy = 0;
        blanklayout.gridwidth = 1;
        blanklayout.gridheight = 1;
        imagePanel.add(blank1, blanklayout); 
        
        
        String tmp="可使用參數:\n\n"
       		 + "NO (一氧化氮)                     NO2 (二氧化氮)\nNOx (氮氧化物)                   SO2 (二氧化硫)\n"
       		 + "CO (一氧化碳)                     CH4 (甲烷)\nTHC (總碳氫化合物)            NMHC (非甲烷碳氫化合物)\n"
       		 + "O3 (臭氧)                              PM10 (懸浮微粒PM10)\nPM2.5 (懸浮微粒PM2.5)      AT (大氣溫度)\n"
       		 + "RH (相對溼度)                      WD (風向)\n";
        JTextArea text = new JTextArea(tmp);
        //text.setBackground(Color.white);//SystemColor.control
        text.setOpaque(false); 
        GridBagConstraints textlayout = new GridBagConstraints();
        textlayout.gridx=2;
        textlayout.gridy=0;
        textlayout.gridwidth = 10;
        textlayout.gridheight = 10;
        //textlayout.fill = GridBagConstraints.BOTH;
        textlayout.anchor = GridBagConstraints.NORTHEAST;        
        imagePanel.add(text, textlayout);     
        

        
		instantCheckBox = new JCheckBox("儲存即時數據");
        instantCheckBox.setFont(new Font("Serif", Font.PLAIN, 14));
        instantCheckBox.setOpaque(false); 
        GridBagConstraints instantCheckBoxlayout = new GridBagConstraints();
        instantCheckBoxlayout.gridx=1;
        instantCheckBoxlayout.gridy=11;
        instantCheckBoxlayout.gridwidth = 4;
        instantCheckBoxlayout.gridheight = 1;
        instantCheckBoxlayout.fill = GridBagConstraints.NONE;
        instantCheckBoxlayout.anchor = GridBagConstraints.WEST; 
        imagePanel.add(instantCheckBox, instantCheckBoxlayout); 
        
        historyCheckBox = new JCheckBox("儲存歷史數據");
        historyCheckBox.setFont(new Font("Serif", Font.PLAIN, 14));
        historyCheckBox.setOpaque(false); 
        GridBagConstraints historyCheckBoxlayout = new GridBagConstraints();
        historyCheckBoxlayout.gridx=2;
        historyCheckBoxlayout.gridy=11;
        historyCheckBoxlayout.gridwidth = 4;
        historyCheckBoxlayout.gridheight = 1;
        historyCheckBoxlayout.fill = GridBagConstraints.NONE;
        historyCheckBoxlayout.anchor = GridBagConstraints.WEST; 
        imagePanel.add(historyCheckBox, historyCheckBoxlayout); */
        

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        //System.out.println(this);
        
        /*String tmp="可使用參數:\n\n"
        		 + "NO (一氧化氮)                     NO2 (二氧化氮)\nNOx (氮氧化物)                   SO2 (二氧化硫)\n"
        		 + "CO (一氧化碳)                     CH4 (甲烷)\nTHC (總碳氫化合物)            NMHC (非甲烷碳氫化合物)\n"
        		 + "O3 (臭氧)                              PM10 (懸浮微粒PM10)\nPM2.5 (懸浮微粒PM2.5)      AT (大氣溫度)\n"
        		 + "RH (相對溼度)                      WD (風向)\n";
        JTextArea text = new JTextArea(tmp);
        //text.setBackground(Color.white);//SystemColor.control
        text.setOpaque(false); 
        GridBagConstraints textlayout = new GridBagConstraints();
        textlayout.gridx=0;
        textlayout.gridy=0;
        textlayout.gridwidth = 800;
        textlayout.gridheight = 400;
        textlayout.fill = GridBagConstraints.NONE;
        textlayout.anchor = GridBagConstraints.EAST;        
        imagePanel.add(text, textlayout);     
        
		instantCheckBox = new JCheckBox("儲存即時數據");
        instantCheckBox.setFont(new Font("Serif", Font.PLAIN, 14));
        GridBagConstraints instantCheckBoxlayout = new GridBagConstraints();
        instantCheckBoxlayout.gridx=0;
        instantCheckBoxlayout.gridy=0;
        instantCheckBoxlayout.gridwidth = 800;
        instantCheckBoxlayout.gridheight = 1;
        instantCheckBoxlayout.fill = GridBagConstraints.HORIZONTAL;
        instantCheckBoxlayout.anchor = GridBagConstraints.EAST;  
        imagePanel.add(instantCheckBox, instantCheckBoxlayout); */ 
        
        /*historyCheckBox = new JCheckBox("儲存歷史數據");
        historyCheckBox.setFont(new Font("Serif", Font.PLAIN, 14));
        GridBagConstraints historyCheckBoxlayout = new GridBagConstraints();
        historyCheckBoxlayout.gridwidth = 15;
        historyCheckBoxlayout.gridheight = 30;
        imagePanel.add(historyCheckBox, historyCheckBoxlayout);  
        
        JLabel blank = new JLabel("");
        blank.setFont(new Font("Serif", Font.PLAIN, 14));
        GridBagConstraints blanklayout = new GridBagConstraints();
        blanklayout.gridwidth = 0;
        blanklayout.gridheight = 30;
        imagePanel.add(blank, blanklayout); 
        
        daytextfield = new JTextField("Input the date before", 20);
        daytextfield.setFont(new Font("Serif", Font.PLAIN, 14));
        GridBagConstraints daytextfieldlayout = new GridBagConstraints();
        daytextfieldlayout.gridwidth = 30;
        daytextfieldlayout.gridheight = 30;
        imagePanel.add(daytextfield, daytextfieldlayout); 
        
        instantbutton = new JButton("Instant  data");
        GridBagConstraints instantbuttonlayout = new GridBagConstraints();
        instantbuttonlayout.gridwidth = 0;
        instantbuttonlayout.gridheight = 30;
        imagePanel.add(instantbutton, instantbuttonlayout); 
        
        labeltextfield = new JTextField("Input the parameter", 20);
        labeltextfield.setFont(new Font("Serif", Font.PLAIN, 14));
        GridBagConstraints labeltextfieldlayout = new GridBagConstraints();
        labeltextfieldlayout.gridwidth = 30;
        labeltextfieldlayout.gridheight = 30;
        imagePanel.add(labeltextfield, labeltextfieldlayout); 
                
        historybutton = new JButton("History data");
        GridBagConstraints historybuttonlayout = new GridBagConstraints();
        historybuttonlayout.gridwidth = 0;
        historybuttonlayout.gridheight = 30;
        imagePanel.add(historybutton, historybuttonlayout);*/
        
        group = new ButtonGroup();
        for(JRadioButton c:city) {
        	group.add(c);
        }
        
        HandlerClass handler = new HandlerClass();
        historybutton.addActionListener(handler);
        instantbutton.addActionListener(handler);
        historyCheckBox.addActionListener(handler);
        instantCheckBox.addActionListener(handler);
        

        
        
    }
    
    private class HandlerClass implements ActionListener{

        public void actionPerformed(ActionEvent event){
        	String wh="NULL";        	
        	for(JRadioButton c:city) {
        		if(c.isSelected()) {
        			wh = c.getText().replaceAll(" ", "");;
        			break;
        		}
        	}
        	System.out.println(wh);
        	if(wh=="NULL") {
        		JOptionPane.showMessageDialog(null, String.format("%s", "Please choose the city !!!"));
        	}else {
            	if(event.getActionCommand()=="Instant  data"){
                    //System.out.println(event.getActionCommand());
                    getdatagraph use = new getdatagraph();
                    childGui go = new childGui(use.instant_button(instantCheckBox.isSelected(),wh));
                    go.setSize(800,350);
                    go.setVisible(true);                                
                }
                if(event.getActionCommand()=="History data") {
                	if(daytextfield.getText().equals("Input the date before") || daytextfield.getText().equals("")) {
                		JOptionPane.showMessageDialog(null, String.format("%s", "Please input the date !!!"));
                		
                	}else {
                    	//System.out.println(daytextfield.getText());
                    	//System.out.println(labeltextfield.getText());
                    	String[] d = daytextfield.getText().split("~");                	
                    	getdatagraph use = new getdatagraph(d,labeltextfield.getText());
                    	use.history_button(historyCheckBox.isSelected(),wh);
                	}
                }
        	}
            
        }

    }

}

class ImagePanel extends JPanel {  
    public void paintComponent(Graphics g) {  
        super.paintComponent(g);  
        ImageIcon img = new ImageIcon("D:\\program\\vscode_workspace\\private\\working\\Java\\Object Oriented HW\\test\\finalprojecttest\\graph.jpg"); 
        setSize(800, 600);
        img.paintIcon(this, g, 0, 0);  

    }  
} 
