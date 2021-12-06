#include "Drawgraph.h"

Drawgraph::Drawgraph()
{
    ls1 = new QLineSeries();

    chart = new QChart();
    ls1 = new QLineSeries(chart);
    chart->setTitle("Graph Test");

    chart->addSeries(ls1);

    axisX = new QValueAxis;
    axisY = new QValueAxis;

    axisX->setRange(0,50);
    axisX->setTickCount(1);

    chart->addAxis(axisX, Qt::AlignBottom);
    chart->addAxis(axisY, Qt::AlignLeft);
    chart->setTheme(QChart::ChartThemeDark);

    chartView = new QChartView(chart);
    chartView->setRenderHint(QPainter::Antialiasing);

    grid = new QGridLayout;
    grid->addWidget(chartView, 0, 0);

    this->setLayout(grid);
    this->resize(800,600);
}


Drawgraph::~Drawgraph()
{

}


void Drawgraph::addNewPoints()
{
    ls1->append(9,12);
}
