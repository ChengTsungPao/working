#ifndef ALIGNPROCESSTHREAD_H
#define ALIGNPROCESSTHREAD_H



#include <QtCore>
#include <QThread>

#include <QFileDialog>

#include <opencv2/opencv.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/highgui.hpp>

using namespace std;
using namespace cv;


//-----------------------------------------------------------------
class AlignProcessThread : public QThread
{
    Q_OBJECT

public:
    explicit AlignProcessThread(QObject *parent=0, bool b=false);
    ~AlignProcessThread();
    bool stop; //stop flag variable

private:
    void run();

signals:
    //Main GUI Thread와 통신. signal 송신
    //만약, Thread 호출한 곳으로 데이터 전송을 원하면, 매개변수 추가 ex) void Threadfun(float, int,~~_;
    //void ThreadEnd();
    void have_calculatedval();

public slots:


};

#endif // ALIGNPROCESSTHREAD_H
