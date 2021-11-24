#ifndef WVIEWGRAPH_H
#define WVIEWGRAPH_H

#include <QWidget>

namespace Ui {
class wViewgraph;
}

class wViewgraph : public QWidget
{
    Q_OBJECT

public:
    explicit wViewgraph(QWidget *parent = nullptr);
    ~wViewgraph();


private:
    Ui::wViewgraph *ui;
};

#endif // WVIEWGRAPH_H
