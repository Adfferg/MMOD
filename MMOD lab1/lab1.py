import scipy.stats, numpy, random, matplotlib.pyplot as plt

theoretical_probabilities = [
    [0.0450, 0.0375, 0.0675, 0.0300],
    [0.0640, 0.0425, 0.0595, 0.0845],
    [0.0250, 0.0695, 0.0670, 0.0765],
    [0.0980, 0.0760, 0.0880, 0.0695]
]

print('Теоретическая матрица вероятностей:')
print(numpy.array(theoretical_probabilities))
x = random.sample(range(1, 10), len(theoretical_probabilities[0]))
x.sort()
y = random.sample(range(1, 10), len(theoretical_probabilities))
y.sort()
print('x: ', x)
print('y: ', y)


def calculate_expected_values(probabilities, x, y, amount):
    x_expected_value = 0
    y_expected_value = 0
    for i in range(len(probabilities[0])):
        for j in numpy.array(probabilities)[:, i]:
            x_expected_value += x[i] * j
    for i in range(len(probabilities)):
        for j in numpy.array(probabilities)[i, :]:
            y_expected_value += y[i] * j
    return x_expected_value / amount, y_expected_value / amount


def calculate_dispersion(x_expected_value, y_expected_value, x, y, amount):
    x_dispersion = sum([((xi - x_expected_value) ** 2) / amount for xi in x])
    y_dispersion = sum([((yi - y_expected_value) ** 2) / amount for yi in y])
    return x_dispersion, y_dispersion


def calculate_correlation(x, y, x_expected_value, y_expected_value):
    correlation = sum([xi - x_expected_value for xi in x]) * sum([yi - y_expected_value for yi in y]) / \
                  ((sum([(xi - x_expected_value) ** 2 for xi in x])) * (
                      sum([(yi - y_expected_value) ** 2 for yi in y]))) ** (0.5)
    return correlation / ((len(x)) ** 1 / 2 * len(y) ** 1 / 2)


def calculate_interval_expected_values(expected_value, dispersion, alpha, amount):
    left_border = expected_value - scipy.stats.t.ppf(1 - (alpha / 2), amount - 1) * (dispersion / amount) ** 1 / 2
    right_border = expected_value + scipy.stats.t.ppf(1 - (alpha / 2), amount - 1) * (dispersion / amount) ** 1 / 2
    return left_border, right_border


def calculate_interval_dispersion(dispersion, amount, alpha):
    left_border = (amount - 1) * dispersion / scipy.stats.chi2.ppf(1 - alpha / 2, amount - 1)
    right_border = (amount - 1) * dispersion / scipy.stats.chi2.ppf(alpha / 2, amount - 1)
    return left_border, right_border


def calculate_pierce_criterion(theoretical_probabilities, empirical_probabilities, amount):
    xi_kvadrat = 0
    for i in range(len(theoretical_probabilities[0])):
        xi_kvadrat += amount * (sum(numpy.array(theoretical_probabilities)[:, i]) -
                                sum(numpy.array(empirical_probabilities)[:, i])) ** 2 / sum(
            numpy.array(empirical_probabilities)[:, i])
    return xi_kvadrat


def show_histogramms(probabilities, x, y, amount):
    x_heights = []
    y_heights = []
    for i in range(len(probabilities[0])):
        x_heights.append(sum(numpy.array(probabilities)[:, i]) * amount)
    for i in range(len(probabilities)):
        y_heights.append(sum(numpy.array(probabilities)[i, :]) * amount)
    fig1, ax1 = plt.subplots(figsize=(10, 5))
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    ax1.bar(x, x_heights)
    ax2.bar(y, y_heights)
    plt.show()


def lab1(theortical_probabilities, x, y, amount):
    n = len(theortical_probabilities[0])
    m = len(theortical_probabilities)
    intervals = [0]
    empirical_probabilities = [[0 for j in range(n)] for i in range(m)]
    for i in range(m):
        for j in range(n):
            intervals.append(intervals[-1] + theortical_probabilities[i][j])
    intervals.pop(0)
    for i in range(amount):
        random_value = random.random()
        for j in range(len(intervals)):
            if random_value <= intervals[j]:
                empirical_probabilities[int(j / m)][j % n] += 1 / amount
                break
    print('Эмперическая матрица вероятностей:')
    print(numpy.array(empirical_probabilities))
    show_histogramms(empirical_probabilities,x,y,amount)
    x_expected_value, y_expected_value = calculate_expected_values(theortical_probabilities, x, y, amount)
    print('\nТочечная оценка мат ожидания')
    print('Теоретическая:\nx: ', x_expected_value, 'y: ', y_expected_value)
    x_expected_emperical_value, y_expected_emperical_value = calculate_expected_values(empirical_probabilities, x, y,
                                                                                       amount)
    print('Эмперическая:')
    print('x: ', x_expected_emperical_value, 'y: ', y_expected_emperical_value)
    x_dispersion, y_dispersion = calculate_dispersion(x_expected_value, y_expected_value, x, y, amount)
    print('\nТочечная оценка дисперсии')
    print('Теоретическая:\nx: ', x_dispersion, 'y: ', y_dispersion)
    x_emperical_dispersion, y_emperical_dispersion = calculate_dispersion(x_expected_emperical_value,
                                                                          y_expected_emperical_value, x, y, amount)
    print('Эмперическая:')
    print('x: ', x_emperical_dispersion, 'y: ', y_emperical_dispersion)
    correlation = calculate_correlation(x, y, x_expected_value, x_dispersion)

    print('Коэффициент корреляции:')
    print(correlation)
    alpha = 0.05
    print('\nИнтервальная оценка мат ожидания')
    print('Теоретическая:')
    print('x: ', calculate_interval_expected_values(x_expected_value, x_dispersion, alpha, amount))
    print('y: ', calculate_interval_expected_values(y_expected_value, y_dispersion, alpha, amount))
    print('Эмперическая:')
    print('x: ', calculate_interval_expected_values(x_expected_emperical_value, x_emperical_dispersion, alpha, amount))
    print('y: ', calculate_interval_expected_values(y_expected_emperical_value, y_emperical_dispersion, alpha, amount))
    print('\nИнтервальная оценка дисперсии')
    print('Теоретическая:')
    print('x:', calculate_interval_dispersion(x_dispersion, amount, alpha))
    print('y:', calculate_interval_dispersion(y_dispersion, amount, alpha))
    print('Эмперическая:')
    print('x:', calculate_interval_dispersion(x_emperical_dispersion, amount, alpha))
    print('y:', calculate_interval_dispersion(y_emperical_dispersion, amount, alpha))
    print('\nКритерий согласия пирсона: ')
    pierce_criterion = calculate_pierce_criterion(theoretical_probabilities, empirical_probabilities, amount)
    print(pierce_criterion)
    print('Xi квадрат для alpha = ', alpha, ' и k = 1 :')
    xi_kvadrat = scipy.stats.chi2.ppf(1-alpha, 1)
    print(xi_kvadrat)
    if (pierce_criterion < xi_kvadrat):
        print('Подтверждена гипотеза о соответствии полученных оценок характеристик  случайной величины требуемым')
    else:
        print('Гипотеза о соответствии полученных оценок характеристик случайной величины требуемым не подтверждена')


lab1(theoretical_probabilities, x, y, 1000)
