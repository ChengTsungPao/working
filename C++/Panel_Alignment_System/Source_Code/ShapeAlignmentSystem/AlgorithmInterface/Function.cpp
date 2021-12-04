#include "Function.h"

void split(std::string const &str, const char delim, std::vector<std::string> &out)
{
    size_t start;
    size_t end = 0;

    while ((start = str.find_first_not_of(delim, end)) != std::string::npos)
    {
        end = str.find(delim, start);
        out.push_back(str.substr(start, end - start));
    }
}

/*!
 * read Json file and handle string
 */
tuple<int, int> readJsonFile(QString path){

    QFile file;
    file.setFileName(path); //File Read
    file.open(QIODevice::ReadOnly);

    QByteArray load_data = file.readAll();
    QJsonDocument doc = QJsonDocument::fromJson(load_data);
    QJsonObject body = doc.object();
    QJsonArray s_array = body.value("shapes").toArray();
    QJsonObject array_4 = s_array.at(3).toObject();
    QJsonArray array_4_point = array_4.value("points").toArray();

    QJsonDocument QJsonArray_conv;
    QJsonArray_conv.setArray(array_4_point);

    QString dataToString = QJsonArray_conv.toJson();
    string t = dataToString.toUtf8().constData();

    char chars[] = "[] ";
    for(size_t i = 0; i < strlen(chars); i++) {
        t.erase(std::remove(t.begin(), t.end(), chars[i]), t.end());
    }
    const char delim = ',';
    vector<string> out;
    split(t, delim, out);

    int x = stoi(out.at(0));
    int y = stoi(out.at(1));

    file.close();
    out.clear();

    return make_tuple(x, y);
}
