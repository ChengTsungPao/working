/*JButton and Icon example*/

import java.awt.FlowLayout;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JButton;

import javax.swing.JOptionPane;

public class Gui extends JFrame{

    private JButton reg;
    private JButton custom;

    public Gui(){
        super("The title");
        setLayout(new FlowLayout());
        JLabel label=new JLabel("NO (一氧化氮): 7.13 ppb AT (大氣溫度): 20.7 ℃ Door (門禁狀態)： 關閉
        NO2 (二氧化氮): 14.88 ppb RH (相對溼度): 98.4 % RT (站內溫度)： 24.5 ℃
        NOx (氮氧化物): 22.01 ppb WD (風向): 340.8 degrees  
        SO2 (二氧化硫): 1.24 ppb WS (風速): 0.9 m/s  
        CO (一氧化碳): 0.48 ppm  
        CH4 (甲烷): 2.09 ppm  
        THC (總碳氫化合物): 2.48 ppm    
        NMHC (非甲烷碳氫化合物): 0.39 ppm    
        O3 (臭氧): 設備校正維護中    
        PM10 (懸浮微粒PM10): 31 μg /m3    
        PM2.5 (懸浮微粒PM2.5): 3 μg /m3 ");
        add(label);

        reg = new JButton("reg Button");
        add(reg);



        HandlerClass handler = new HandlerClass();
        reg.addActionListener(handler);
        
        
    }

    private class HandlerClass implements ActionListener{

        public void actionPerformed(ActionEvent event){
            
            if(event.getActionCommand()=="reg Button"){
                System.out.println(event.getActionCommand());
            }
            JOptionPane.showMessageDialog(null, String.format("%s", event.getActionCommand()));
        }

    }

}