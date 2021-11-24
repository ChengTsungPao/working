#include "communication.h"

Communication::Communication(QObject *parent) : QObject(parent)
{
    m_socket = new QTcpSocket(this);
    return_msg = "";

    connect(this, SIGNAL(newMessage(QString)), this, SLOT(displayMessage(QString)));
    connect(m_socket, SIGNAL(readyRead()), this, SLOT(readSocket()));
    connect(m_socket, SIGNAL(disconnected()), this, SLOT(discardSocket()));
}

Communication::~Communication(){
    m_socket->close();
    m_socket->deleteLater();
}

void Communication::setup()
{
    QString commandLine;
    char *ipset = "192.168.250.2";
    commandLine.sprintf("ifconfig eth1 %s netmask 255.0.0.0 up", ipset);

    QProcess *mypro = new QProcess();
    mypro->start(commandLine);
    mypro->waitForFinished();
}

void Communication::readSocket()
{
    QString receiveString;
    QByteArray block = m_socket->readAll();

    receiveString = QString(block);
    //receiveString.prepend(QString("PLC %1 :: ").arg(m_socket->socketDescriptor()));
//    qDebug() << "The PLC msg: " << receiveString;
    return_msg = receiveString;
    emit newMessage(receiveString);
}

void Communication::discardSocket()
{
    m_socket->disconnectFromHost();
    m_socket->waitForDisconnected();
    m_socket->deleteLater();
    m_socket = nullptr;
}

// Public function
QString Communication::Send(const QString &str)
{
    if (m_socket){
        if (m_socket->isOpen()){
            //QString feedback = "#Nothing#";

            m_socket->waitForBytesWritten();
            m_socket->write(str.toStdString().c_str());
            m_socket->waitForReadyRead();
//            qDebug() << "Send msg: " << str;
            return "Send already";

//            m_socket->waitForReadyRead();
//            QString msj = readSocket();
//            if (msj.isEmpty())
//                return feedback;
//            else{
//                feedback = msj;
//                return feedback;
//            }
//            QByteArray block = m_socket->readAll();
//            feedback = QString(block);
//            feedback.prepend(QString("PLC %1 :: ").arg(m_socket->socketDescriptor()));
        }
        else
            return "Error: Socket didn't open.";
    }
    else
        return "Error: No build socket.";
}

QString Communication::Connect()
{
    //setup();
    m_socket->connectToHost(QHostAddress(PLC_IP), PLC_PORT);
    if (m_socket->waitForConnected()){
        return "Connect!";
    }
    else{
        return QString("The following error occurred: %1.").arg(m_socket->errorString());
    }
}

void Communication::Disconnect()
{
    discardSocket();
}
