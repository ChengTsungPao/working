#include "secdialog.h"
#include "ui_secdialog.h"

#include "QIODevice"
#include <algorithm>
#include <vector>
#include <iostream>
#include <QPainter>
#include <math.h>
#include <tuple>
#include <QtAlgorithms>
#include <map>

#include <QtCharts>
#include <QtCharts/QChartView>
#include <QtCharts/QLineSeries>

using namespace std;


std::vector<std::tuple<unsigned short,int,int>> data_mag_secdlg,data_ang_secdlg,data_mag_smooth_secdlg,data_ang_smooth_secdlg,data_dev_mag_secdlg,data_dev_ang_secdlg;
//std::vector<int> index;
//std::vector<unsigned short> value;
//QVector<double> index,index2,index3,index4,index5,index6;
//QVector<double> value,value_ang,value_mag_smooth,value_angle_smooth,value_mag_dev,value_ang_dev;


//QT_CHART_USE_NAMESPACE


SecDialog::SecDialog(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::SecDialog)
{
    ui->setupUi(this);

}

void SecDialog::Recv_value_mag(std::vector<std::tuple<float,int,int>> data)
{
  /*
    data_mag_secdlg.assign(data.begin(), data.end());

    for(int i=0; i<data_mag_secdlg.size(); i++)
    {
        index.append(i);
        value.append(std::get<0>(data_mag_secdlg.at(i)));
    }


    ui->widget->addGraph();
    ui->widget->graph(0)->setData(index,value);
    ui->widget->graph(0)->setLineStyle(QCPGraph::lsLine);
    ui->widget->xAxis->setLabel("Index");
    ui->widget->yAxis->setLabel("Magnitude");
    ui->widget->xAxis->setRange(0,1000);
    ui->widget->yAxis->setRange(0,10);

    ui->widget->replot();

    data_mag_secdlg.clear();
    index.clear();
    value.clear();
    */

}

void SecDialog::Recv_value_ang(std::vector<std::tuple<float,int,int>> data)
{
    /*
    data_ang_secdlg.assign(data.begin(), data.end());

    for(int i=0; i<data_ang_secdlg.size(); i++)
    {
        index2.append(i);
        value_ang.append(std::get<0>(data_ang_secdlg.at(i)));
    }


    ui->widget->addGraph();
    ui->widget->graph(0)->setData(index2,value_ang);
    ui->widget->graph(0)->setLineStyle(QCPGraph::lsLine);

    ui->widget->xAxis->setLabel("Index");
    ui->widget->yAxis->setLabel("angle");

    ui->widget->xAxis->setRange(0,1000);
    ui->widget->yAxis->setRange(0,360);
    ui->widget->replot();

    data_ang_secdlg.clear();
    index2.clear();
    value_ang.clear();
    */

}


void SecDialog::Recv_value_mag_smooth(std::vector<std::tuple<float,int,int>> data)
{
    /*
    data_mag_smooth_secdlg.assign(data.begin(), data.end());

    for(int i=1; i<data_mag_smooth_secdlg.size(); i++)
    {
        index3.append(i);
        value_mag_smooth.append(std::get<0>(data_mag_smooth_secdlg.at(i)));
    }


    ui->widget->addGraph();
    ui->widget->graph(0)->setData(index3,value_mag_smooth);
    ui->widget->graph(0)->setLineStyle(QCPGraph::lsLine);

    ui->widget->xAxis->setLabel("Index");
    ui->widget->yAxis->setLabel("Magnitude_smooth");

    ui->widget->xAxis->setRange(1,1000);
    ui->widget->yAxis->setRange(0,100);
    ui->widget->replot();

    data_mag_smooth_secdlg.clear();
    index3.clear();
    value_mag_smooth.clear();
    */

}

void SecDialog::Recv_value_ang_smooth(std::vector<std::tuple<float,int,int>> data)
{
    /*
    data_ang_smooth_secdlg.assign(data.begin(), data.end());

    for(int i=1; i<data_ang_smooth_secdlg.size(); i++)
    {
        index4.append(i);
        value_angle_smooth.append(std::get<0>(data_ang_smooth_secdlg.at(i)));
    }


    ui->widget->addGraph();
    ui->widget->graph(0)->setData(index4,value_angle_smooth);
    ui->widget->graph(0)->setLineStyle(QCPGraph::lsLine);

    ui->widget->xAxis->setLabel("Index");
    ui->widget->yAxis->setLabel("smooth_angle");

    ui->widget->xAxis->setRange(1,1000);
    ui->widget->yAxis->setRange(0,360);
    ui->widget->replot();

    data_ang_smooth_secdlg.clear();
    index4.clear();
    value_angle_smooth.clear();
    */
}

//void Recv_value_ang_smooth(std::vector<std::tuple<int,int,float>> data);
void SecDialog::Recv_value_dev_mag(std::vector<std::tuple<float,int,int>> data)
{
    /*
    data_dev_mag_secdlg.assign(data.begin(), data.end());

    for(int i=1; i<data_dev_mag_secdlg.size(); i++)
    {
        index5.append(i);
        value_mag_dev.append(std::get<0>(data_dev_mag_secdlg.at(i)));
    }


    ui->widget->addGraph();
    ui->widget->graph(0)->setData(index5,value_mag_dev);
    ui->widget->graph(0)->setLineStyle(QCPGraph::lsLine);

    ui->widget->xAxis->setLabel("Index");
    ui->widget->yAxis->setLabel("dev_magnitude");

    ui->widget->xAxis->setRange(1,1000);
    ui->widget->yAxis->setRange(0,100);
    ui->widget->replot();

    data_dev_mag_secdlg.clear();
    index5.clear();
    value_mag_dev.clear();
    */
}


void SecDialog::Recv_value_dev_ang(std::vector<std::tuple<float,int,int>> data)
{
    /*
    data_dev_ang_secdlg.assign(data.begin(), data.end());

    for(int i=1; i<data_dev_ang_secdlg.size(); i++)
    {
        index6.append(i);
        value_ang_dev.append(std::get<0>(data_dev_ang_secdlg.at(i)));

    }



    ui->widget->addGraph();

    ui->widget->graph(0)->setData(index6,value_ang_dev);
    ui->widget->graph(0)->setLineStyle(QCPGraph::lsLine);

    ui->widget->xAxis->setLabel("Index");
    ui->widget->yAxis->setLabel("dev_angle");

    ui->widget->xAxis->setRange(1,1000);
    ui->widget->yAxis->setRange(0,360);
    ui->widget->replot();

    data_dev_ang_secdlg.clear();
    index6.clear();
    value_ang_dev.clear();
    */
}




SecDialog::~SecDialog()
{
    delete ui;
}
