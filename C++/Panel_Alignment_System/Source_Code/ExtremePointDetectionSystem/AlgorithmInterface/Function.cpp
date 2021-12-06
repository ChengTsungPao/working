#include "Function.h"

double distance(Vec4i position){
    return distance(position[0], position[1], position[2], position[3]);
}

double distance(double x1, double y1, double x2, double y2){
    return sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2));
}

double innerProduct(Vec4i position1, Vec4i position2){
    return innerProduct(position1[0] - position1[2], position1[1] - position1[3], position2[0] - position2[2], position2[1] - position2[3]);
}

double innerProduct(tuple<double, double> position1, tuple<double, double> position2){
    return innerProduct(get<0>(position1), get<1>(position1), get<0>(position2), get<1>(position2));
}

double innerProduct(double x1, double y1, double x2, double y2){
    return x1 * x2 + y1 * y2;
}

tuple<double, double> normalize(double x, double y){
    double length = distance(x, y, 0, 0);
    return { x / length, y / length };
}

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
