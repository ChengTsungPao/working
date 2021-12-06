#ifndef DRAWGRAPH_H
#define DRAWGRAPH_H

#include <QWidget>
#include <QWindow>
#include <QGridLayout>
#include <QtCharts/QChartView>
#include <Qtcharts/QLineSeries>
#include <QValueAxis>

#include <vector>

QT_CHARTS_USE_NAMESPACE

class Drawgraph:public QWidget
{
    Q_OBJECT

public:
    explicit Drawgraph();
    ~Drawgraph();

    void addNewPoints();

private:
    QLineSeries *ls1;

    QChart *chart;
    QChartView *chartView;

    QGridLayout *grid;

    QValueAxis *axisX;
    QValueAxis *axisY;
};


#endif // DRAWGRAPH_H
