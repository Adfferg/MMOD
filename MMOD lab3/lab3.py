import math
import matplotlib.pyplot as plt
import random


class Request():
    def __init__(self, time_of_request):
        self.time_of_request = time_of_request
        self.time_of_processing_start = 0
        self.time_of_processing_end = 0
        self.time_of_processing = 0
        self.time_in_queque_start = 0
        self.time_in_queque_end = 0
        self.time_in_queque = 0

    def calculateTimeOfProcessingEnd(self, h):
        self.time_of_processing_end = self.time_of_processing_start + -1 / h * math.log(random.random())
        self.time_of_processing = self.time_of_processing_end - self.time_of_processing_start


def simulation(n, m, l, h, simulation_duration):
    h = 1 / h
    pk = [0 for i in range(m + 1)]
    requests_in_work = []
    requests_in_queque = []
    processed_requests = []
    t1 = [0, 0]
    t = 0
    future_requests = []
    while t < simulation_duration:
        while len(future_requests) < m - len(requests_in_work) - len(requests_in_queque):
            future_requests.append(t+(-1 / l * math.log(random.random())))
        future_requests.sort()
        print('\n',future_requests)
        if len(future_requests) == 0:
            processed_request = requests_in_work.pop(0)
            t = processed_request.time_of_processing_end
            print('Заявка была обработана в', t)
            if len(requests_in_queque) > 0:
                request = requests_in_queque.pop(0)
                request.time_in_queque_end = processed_request.time_of_processing_end
                request.time_of_processing_start = processed_request.time_of_processing_end
                request.calculateTimeOfProcessingEnd(h)
                requests_in_work.append(request)
                print('Заявка поступила из очереди в:', processed_request.time_of_processing_end)
            pk[t1[1]] += t - t1[0]
            t1 = [t, len(requests_in_work) + len(requests_in_queque)]
            if t > simulation_duration:
                break
            continue
        else:
            t = future_requests.pop(0)
            if t > simulation_duration:
                break
        while len(requests_in_work) > 0 and t > requests_in_work[0].time_of_processing_end:
            processed_request = requests_in_work.pop(0)
            print('Заявка была обработана в:', processed_request.time_of_processing_end)
            if len(requests_in_queque) > 0:
                request = requests_in_queque.pop(0)
                request.time_in_queque_end = processed_request.time_of_processing_end
                request.time_of_processing_start = processed_request.time_of_processing_end
                request.calculateTimeOfProcessingEnd(h)
                requests_in_work.append(request)
                print('Заявка поступила из очереди в:', processed_request.time_of_processing_end)
            pk[t1[1]] += processed_request.time_of_processing_end - t1[0]
            t1 = [processed_request.time_of_processing_end, len(requests_in_work) + len(requests_in_queque)]

        if len(requests_in_work) < n:
            request = Request(t)
            request.time_of_processing_start = t
            request.calculateTimeOfProcessingEnd(h)
            requests_in_work.append(request)
            print('Заявка поступила в:', t)
            pk[t1[1]] += t - t1[0]
            t1 = [t, len(requests_in_work) + len(requests_in_queque)]
        elif len(requests_in_work) == n:
            request = Request(t)
            request.time_in_queque_start = t
            requests_in_queque.append(request)
            print('Заявка попала в очередь в:', t)
            pk[t1[1]] += t - t1[0]
            t1 = [t, len(requests_in_work) + len(requests_in_queque)]
    t = simulation_duration
    while len(requests_in_work) > 0 and t > requests_in_work[0].time_of_processing_end:
        processed_request = requests_in_work.pop(0)
        print('Заявка была обработана в:', processed_request.time_of_processing_end)
        if len(requests_in_queque) > 0:
            request = requests_in_queque.pop(0)
            request.time_in_queque_end = processed_request.time_of_processing_end
            request.time_of_processing_start = processed_request.time_of_processing_end
            request.calculateTimeOfProcessingEnd(h)
            requests_in_work.append(request)
            print('Заявка поступила из очереди в:', processed_request.time_of_processing_end)
        pk[t1[1]] += processed_request.time_of_processing_end - t1[0]
        t1 = [processed_request.time_of_processing_end, len(requests_in_work) + len(requests_in_queque)]
    pk[t1[1]] += t - t1[0]
    t1 = [t, len(requests_in_work) + len(requests_in_queque)]
    pk = [i / simulation_duration for i in pk]
    print('Результаты работы симуляции:\n')
    print('pk:',pk)
    print('A:', (1 - pk[0])*h*60)
    p = l/h
    w = m - (1 - pk[0]) / p
    print('w:',w)
    R = m - (1 - pk[0]) / p - (1 - pk[0])
    print('R:',R)
    Pzan = 1 - pk[0]
    print('Рзан:',Pzan)
    return pk


def theor(m, l, h):
    h = 1/h
    p = l / h
    p0 = 1 + m * p
    for k in range(2, m + 1):
        temp = 1
        for i in range(0, k):
            temp *= m - i
        p0 += temp * p ** k
    p0 = p0 ** (-1)
    pk = [p0]
    for k in range(1, m + 1):
        pi = p0 * p ** k
        temp = 1
        for i in range(0, k):
            temp *= m - i
        pi *= temp
        pk.append(pi)
    print('\n\nТеоретические результаты:\n')
    print('pk:',pk)
    A = (1 - p0) * h
    print('A:',A)
    w = m - (1 - p0) / p
    print('w:',w)
    R = m - (1 - p0) / p - (1 - p0)
    print('R:',R)
    Pzan = 1 - p0
    print('Рзан:',Pzan)
    return pk

n = 1
m = 5
l = 1/24  # заявок в час
t_ob = 60  # время на 1 заявку в минутах
pk_simulation = simulation(n, m, l/60, t_ob, 200000)
pk_theor = theor(m, l, t_ob/60)
if pk_simulation is not None:
    fig, ax = plt.subplots()
    ax.plot([i for i in range(n + m)], pk_simulation, label='simulation')
    ax.plot([i for i in range(n + m)], pk_theor, label='theoretical')
    ax.legend()
    plt.show()