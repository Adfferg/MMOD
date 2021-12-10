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
        self.max_waiting_time = 0

    def calculateMaxWaitingTime(self, v):
        self.max_waiting_time = self.time_in_queque_start + -1 / v * math.log(random.random())

    def calculateTimeOfProcessingEnd(self, h):
        self.time_of_processing_end = self.time_of_processing_start + -1 / h * math.log(random.random())
        self.time_of_processing = self.time_of_processing_end - self.time_of_processing_start

    def calculateTimeInQueue(self):
        self.time_in_queque = self.time_in_queque_end - self.time_in_queque_start


def checkQueque(requests_in_queque, finished_request, rejected_requests, pk, t1, requests_in_work, rejected_by_time,graphs):
    # Удаляем из очереди заявки, ущедшие до выполненной
    gone_from_queue = []
    for i in requests_in_queque:
        if i.max_waiting_time < finished_request:
            gone_from_queue.append(i.max_waiting_time)
    gone_from_queue.sort()

    for j in gone_from_queue:
        for i in requests_in_queque:
            if i.max_waiting_time == j:
                requests_in_queque.remove(i)
                i.time_in_queque_end = i.max_waiting_time
                i.calculateTimeInQueue()
                rejected_requests.append(i)
                pk[t1[1]] += i.time_in_queque_end - t1[0]
                graphs[0].append([pk[k] / i.time_in_queque_end for k in range(n + m + 1)])
                graphs[1].append(i.time_in_queque_end)
                t1 = [i.time_in_queque_end, len(requests_in_work) + len(requests_in_queque)]
                rejected_by_time += 1
                print('Заявка ушла из очереди в',
                      i.max_waiting_time)
    return requests_in_queque, finished_request, rejected_requests, pk, t1, requests_in_work, rejected_by_time,graphs


def createRequests(l, simulation_duration):
    time_of_request = 0
    requests = []
    while True:
        time_of_request += -1 / l * math.log(random.random())
        if time_of_request < simulation_duration:
            requests.append(Request(time_of_request))
        else:
            break
    return requests


def showPlots(graphs):
    plots = [[[], []] for i in range(len(graphs[0][0]))]
    for i in range(len(graphs[0])):
        for j in range(len(graphs[0][i])):
            plots[j][0].append(graphs[0][i][j])
            plots[j][1].append(graphs[1][i])
    fig, ax = plt.subplots()
    for i in range(len(plots)):
        s = 'p' + str(i)
        ax.plot(plots[i][1], plots[i][0], label=s)
    ax.legend()
    plt.show()


def simulation(n, m, l, h, v, simulation_duration):
    v = 1 / v
    h = 1 / h
    pk = [0 for i in range(n + m + 1)]
    graphs = [[], []]
    requests = createRequests(l, simulation_duration)
    processed_requests, rejected_requests, rejected_by_time = [], [], 0
    len_requests = len(requests)
    requests_in_work = []
    requests_in_queque = []
    t1 = [0, 0]
    while len(requests) > 0:
        request = requests.pop(0)
        t = request.time_of_request

        finished_requests = []
        # Получаем выполненные заявки
        for i in range(len(requests_in_work)):
            if requests_in_work[i].time_of_processing_end < t:
                finished_requests.append(requests_in_work[i].time_of_processing_end)
        finished_requests.sort()

        # Проходимся по выполненным заявкам
        while len(finished_requests) > 0:
            finished_request = finished_requests.pop(0)

            requests_in_queque, finished_request, rejected_requests, pk, t1, requests_in_work, rejected_by_time,graphs = checkQueque(
                requests_in_queque, finished_request, rejected_requests, pk, t1, requests_in_work,
                rejected_by_time,graphs)

            for i in requests_in_work:
                if i.time_of_processing_end == finished_request:
                    processed_requests.append(i)
                    requests_in_work.remove(i)
                    break
            print('Заявка обработана в', finished_request)

            if len(requests_in_queque) > 0:
                first_in_queue = requests_in_queque.pop(0)
                first_in_queue.time_in_queque_end = finished_request
                first_in_queue.calculateTimeInQueue()
                first_in_queue.time_of_processing_start = finished_request
                first_in_queue.calculateTimeOfProcessingEnd(h)
                requests_in_work.append(first_in_queue)
                print('Заявка принята из очереди в', first_in_queue.time_of_processing_start)
                if first_in_queue.time_of_processing_end < t:
                    finished_requests.append(first_in_queue.time_of_processing_end)
                    finished_requests.sort()
            pk[t1[1]] += finished_request - t1[0]
            graphs[0].append([pk[k] / finished_request for k in range(n + m + 1)])
            graphs[1].append(finished_request)
            t1 = [finished_request, len(requests_in_work) + len(requests_in_queque)]

        requests_in_queque, t, rejected_requests, pk, t1, requests_in_work, rejected_by_time, graphs = checkQueque(
            requests_in_queque, t, rejected_requests, pk, t1, requests_in_work,
            rejected_by_time, graphs)

        nm = len(requests_in_work) + len(requests_in_queque)
        if nm >= n + m:
            rejected_requests.append(request)
            print('Заявка не поместилась в очереди и ушла в', t)
            continue
        elif len(requests_in_work) == n and len(requests_in_queque) < m:
            request.time_in_queque_start = t
            request.calculateMaxWaitingTime(v)
            requests_in_queque.append(request)
            print('Заявка попала в очередь в', t)
            pk[t1[1]] += t - t1[0]
            graphs[0].append([pk[k] / t for k in range(n + m + 1)])
            graphs[1].append(t)
            t1 = [t, len(requests_in_work) + len(requests_in_queque)]
            continue
        elif len(requests_in_work) < n:
            request.time_of_processing_start = t
            request.calculateTimeOfProcessingEnd(h)
            requests_in_work.append(request)
            print('Заявка поступила в', t)
            pk[t1[1]] += t - t1[0]
            graphs[0].append([pk[k] / t for k in range(n + m + 1)])
            graphs[1].append(t)
            t1 = [t, len(requests_in_work) + len(requests_in_queque)]

    t = simulation_duration
    finished_requests = []
    # Получаем выполненные заявки
    for i in range(len(requests_in_work)):
        if requests_in_work[i].time_of_processing_end < t:
            finished_requests.append(requests_in_work[i].time_of_processing_end)
    finished_requests.sort()

    # Проходимся по выполненным заявкам
    while len(finished_requests) > 0:
        finished_request = finished_requests.pop(0)

        requests_in_queque, finished_request, rejected_requests, pk, t1, requests_in_work, rejected_by_time, graphs = checkQueque(
            requests_in_queque, finished_request, rejected_requests, pk, t1, requests_in_work,
            rejected_by_time, graphs)

        for i in requests_in_work:
            if i.time_of_processing_end == finished_request:
                processed_requests.append(i)
                requests_in_work.remove(i)
                break
        print('Заявка обработана в', finished_request)

        if len(requests_in_queque) > 0:
            first_in_queue = requests_in_queque.pop(0)
            first_in_queue.time_in_queque_end = finished_request
            first_in_queue.calculateTimeInQueue()
            first_in_queue.time_of_processing_start = finished_request
            first_in_queue.calculateTimeOfProcessingEnd(h)
            requests_in_work.append(first_in_queue)
            print('Заявка принята из очереди в', first_in_queue.time_of_processing_start)
            if first_in_queue.time_of_processing_end < t:
                finished_requests.append(first_in_queue.time_of_processing_end)
                finished_requests.sort()
        pk[t1[1]] += finished_request - t1[0]
        graphs[0].append([pk[k] / finished_request for k in range(n + m + 1)])
        graphs[1].append(finished_request)
        t1 = [finished_request, len(requests_in_work) + len(requests_in_queque)]

    print('\n\n')
    pk[t1[1]] += t - t1[0]
    graphs[0].append([pk[k] / t for k in range(n + m + 1)])
    graphs[1].append(t)
    t1 = [t, len(requests_in_work) + len(requests_in_queque)]
    pk = [i / simulation_duration for i in pk]
    print('Результаты работы симуляции:\n')
    print('pk:', pk)
    processing_time = 0
    time_in_que = 0
    for i in processed_requests:
        processing_time += i.time_of_processing
        if i.time_in_queque > 0:
            time_in_que += i.time_in_queque
    for i in rejected_requests:
        if i.time_in_queque > 0:
            time_in_que += i.time_in_queque
    L_och = sum([i * pk[n + i] for i in range(1, m + 1)])
    L_k = sum([i * pk[i] for i in range(1, n + 1)])
    L_obs = sum([k * pk[k] for k in range(1, n + 1)]) + sum([n * pk[n + i] for i in range(1, m + 1)])
    print('Общее число запросов: ', len_requests)
    print("Обработанные запросы:", len(processed_requests))
    print("Запросы, которым отказали:", len(rejected_requests))
    print("Вероятность отказа",
          len(rejected_requests) / (len_requests - len(requests_in_work) - len(requests_in_queque)))
    print("Относительная пропускная способность",
          len(processed_requests) / (len_requests - len(requests_in_work) - len(requests_in_queque)))
    print("Абсолютная пропускная способность", len(processed_requests) / simulation_duration * 60)
    print("Среднее число заявок, обсуживаемых в смо:", L_obs)
    print("Среднее число заявок, находящихся в очереди:", L_och)
    print("Среднее число занятых каналов:", L_k)
    print("Среднее время пребывания заявки в СМО:", (processing_time + time_in_que) / len_requests)
    return pk, graphs


def theor(n, m, l, h, v):
    p = l / h
    v = 1 / v
    B = v / h
    p0 = sum([(p ** i) / math.factorial(i) for i in range(n + 1)])
    r = 0
    for i in range(1, m + 1):
        r1 = p ** i
        z = 1
        for j in range(1, i + 1):
            z *= n + j * B
        r1 /= z
        r += r1
    p0 += p ** n / math.factorial(n) * r
    p0 = p0 ** -1
    pk = [p0]
    for i in range(1, n + 1):
        pk.append(p ** i / math.factorial(i) * p0)
    for i in range(1, m + 1):
        r1 = p ** i
        z = 1
        for j in range(1, i + 1):
            z *= n + j * B
        r1 /= z
        pk.append(pk[n] * r1)
    print('\n\nТеоретические результаты:\n')
    print('pk:',pk)
    L_obs = sum([k * pk[k] for k in range(1, n + 1)]) + sum([n * pk[n + i] for i in range(1, m + 1)])
    L_och = sum([i * pk[n + i] for i in range(1, m + 1)])
    L_k = sum([i * pk[i] for i in range(1, n + 1)])
    p_otk = 1 - h / l * L_obs
    Q = 1 - p_otk
    A = l * Q
    print("Вероятность отказа:", p_otk)
    print("Относительная пропускная способность:", Q)
    print("Абсолютная пропускная способность:", A)
    print("Среднее число заявок, обсуживаемых в смо:", L_obs)
    print("Среднее число заявок, находящихся в очереди:", L_och)
    print("Среднее число занятых каналов:", L_k)
    print("Среднее время пребывания заявки в СМО:", L_obs / l * 60)
    return pk


n = 3
m = 4
l = 10
h = 4
t_oz = 5
pk_simulation, graphs = simulation(n, m, l / 60, 60 / h, t_oz, 50000)
pk_theor = theor(n, m, l, h, t_oz / 60)

if pk_simulation is not None and pk_theor is not None:
    fig, ax = plt.subplots()
    ax.plot([i for i in range(n + m + 1)], pk_simulation, label='simulation')
    ax.plot([i for i in range(n + m + 1)], pk_theor, label='theoretical')
    ax.legend()
    plt.show()
    showPlots(graphs)
