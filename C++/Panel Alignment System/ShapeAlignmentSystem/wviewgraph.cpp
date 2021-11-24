#include "wviewgraph.h"
#include "ui_wviewgraph.h"

wViewgraph::wViewgraph(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::wViewgraph)
{
    ui->setupUi(this);
}

wViewgraph::~wViewgraph()
{
    delete ui;
}
