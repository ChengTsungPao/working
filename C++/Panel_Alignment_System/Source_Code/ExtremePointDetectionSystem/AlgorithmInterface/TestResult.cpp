#include "TestResult.h"


/* ======================================================================== */
// Linux Pthread Class
class Thread {
    pthread_t t;
    string path;
    char imageType;

    public:
        Thread(string path, char imageType) {
            this->path = path;
            this->imageType = imageType;
            cout << "Thread => " << path << "\n";
        }

        void create_thread() {
            if (pthread_create(&t, NULL, run, this) != 0) {
                cerr << "Error: pthread_create\n";
            }
        }

        void join_thread() {
            pthread_join(t, NULL);
        }

    private:
        static void * run(void *arg) {
            Thread *self = (Thread *)arg;
            Point result = getExtremePoint(self->path, self->imageType);
            cout << self->path + "L.png" << ": " << result << endl;
            return NULL;
        }
};
/* ======================================================================== */

void test_all_data(){
    cout << "This is test result function !!!" << endl;

    string str;
    vector<string> paths;
    Point result;

    ifstream file("../../Test Image_20210913/all_image_path.txt");
    while (getline(file, str)){
        paths.push_back(str);
    }

    double start = clock();

    // Single Thread
//    for(unsigned int i = 0; i < paths.size(); i++){
//        result = getExtremePoint(paths[i] + "L.png", 'L');
//        cout << paths[i] + "L.png" << ": " << result << endl;
//        result = getExtremePoint(paths[i] + "R.png", 'R');
//        cout << paths[i] + "R.png" << ": " << result << endl;
//    }

    // Double Thread
    for(unsigned int i = 0; i < paths.size(); i++){
        Thread leftImageThread(paths[i] + "L.png", 'L');
        Thread rightImageThread(paths[i] + "R.png", 'R');

        leftImageThread.create_thread();
        rightImageThread.create_thread();

        leftImageThread.join_thread();
        rightImageThread.join_thread();
    }

    // Four Thread
//    for(unsigned int i = 0; i < paths.size(); i+=2){
//        Thread leftImageThread1(paths[i] + "L.png", 'L');
//        Thread rightImageThread1(paths[i] + "R.png", 'R');
//        Thread leftImageThread2(paths[i + 1] + "L.png", 'L');
//        Thread rightImageThread2(paths[i + 1] + "R.png", 'R');

//        leftImageThread1.create_thread();
//        rightImageThread1.create_thread();
//        leftImageThread2.create_thread();
//        rightImageThread2.create_thread();

//        leftImageThread1.join_thread();
//        rightImageThread1.join_thread();
//        leftImageThread2.join_thread();
//        rightImageThread2.join_thread();
//    }

    double end = clock();

    cout << "Total Time: " << end - start << endl;
    cout << "Average Time: " << (end - start) / (paths.size() * 2) << endl;
}
