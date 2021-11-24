#ifndef COMMUNICATION_H
#define COMMUNICATION_H

#include <QMainWindow>
#include <QMessageBox>
#include <QMetaType>
#include <QProcess>
#include <QString>
#include <QTcpSocket>
#include <QHostAddress>
#include <cmath>

class Communication : public QObject
{
    Q_OBJECT
public:
    explicit Communication(QObject *parent = 0);
    ~Communication();

    /// public function
    QString Send(const QString& str);
    QString Connect();
    QString Read() { return return_msg; }
    void Disconnect();

private:
    QString PLC_IP  = "192.168.250.1";
    int PLC_PORT  = 52997;
    QTcpSocket* m_socket;
    QString return_msg;

signals:
    void newMessage(QString);

private slots:
    void readSocket();
    void discardSocket();
    void setup();

    QString displayMessage(const QString& str) { return str; }

};

#endif // COMMUNICATION_H
