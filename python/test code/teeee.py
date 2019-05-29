import multiprocessing as mp

def job(i):
    while i > 0:
        i -= 1
    return None

if __name__=='__main__':

    A = int(1e8)

    process = []
    for i in range(8):
        process.append(mp.Process(target = job, args = (A,)))
    for i in process:
        i.start()
    for i in process:
        i.join()

    print('Done!')
