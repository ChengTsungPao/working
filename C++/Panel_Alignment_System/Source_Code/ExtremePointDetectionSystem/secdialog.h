#ifndef SECDIALOG_H
#define SECDIALOG_H

#include <QMainWindow>
#include <QFileDialog>
#include <QDialog>
#include <algorithm>
#include <vector>
#include <iostream>
#include <QPainter>
#include <algorithm>
#include <vector>
#include <iostream>
#include <QPainter>
#include <math.h>
#include <tuple>
#include <QtAlgorithms>
#include <map>
#include <string.h>
#include <string>
#include <QtCore>

namespace Ui {
class SecDialog;
}

class SecDialog : public QDialog
{
    Q_OBJECT

public:
    explicit SecDialog(QWidget *parent = nullptr);
    ~SecDialog();


private:
    Ui::SecDialog *ui;

public slots:
    //Left Cam Data
    void Recv_value_mag(std::vector<std::tuple<float,int,int>> data);
    void Recv_value_ang(std::vector<std::tuple<float,int,int>> data);
    void Recv_value_mag_smooth(std::vector<std::tuple<float,int,int>> data);
    void Recv_value_ang_smooth(std::vector<std::tuple<float,int,int>> data);
    void Recv_value_dev_mag(std::vector<std::tuple<float,int,int>> data);
    void Recv_value_dev_ang(std::vector<std::tuple<float,int,int>> data);


};

#endif // SECDIALOG_H
