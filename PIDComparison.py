import numpy as np
import matplotlib.pyplot as plt
import mpmath


def porownaj_regulatory(a, h, y0, T, dest, zachowanie):
    t = np.arange(0, T, h)
    nazwa_procesu = ""
    if zachowanie == 'losowe':
        nazwa_procesu = "Losowa temperatura zadana"
        dest = np.random.randint(15, 25, t.shape[0])
        dest_table = dest
    else:
        dest_table = np.empty(t.shape[0])
        dest_table.fill(dest)

    if zachowanie == 'rosnace1':
        nazwa_procesu = "Rosnaca temperatura zadana o 1"

    if zachowanie == 'malejace1':
        nazwa_procesu = "Spadajaca temperatura zadana o 1"

    if zachowanie == 'rosnace2':
        nazwa_procesu = "Rosnaca temperatura zadana o 2"

    if zachowanie == 'malejace2':
        nazwa_procesu = "Spadajaca temperatura zadana o 2"

    if zachowanie == 'stale':
        nazwa_procesu = "Stala temperatura zadana"

    if zachowanie == 'zaklocenia':
        nazwa_procesu = "Stała temperatura zadana z zakłóceniami"
        t = np.arange(0, T, h)
        z = np.random.randint(-5, 5, t.shape[0])
    else:
        z = np.zeros(t.shape[0])

    print(nazwa_procesu)

    def model(kp, ki, kd):

        y = np.zeros(t.shape[0])
        e = np.zeros(t.shape[0])
        u = np.zeros(t.shape[0])

        if zachowanie == 'losowe':
            d = dest[0]
        else:
            d = dest

        y[0] = y0
        # d - wartosc zadana
        # e - blad
        # y -wartosc aktualna
        integral = 0
        derive = 1.0
        error_sum = 0
        for i in range(t.shape[0] - 1):
            if i % 100 == 0 and zachowanie == 'rosnace1':
                d += 1
                for j in range(0, 100):
                    dest_table[i + j] = d
            if i % 100 == 0 and zachowanie == 'malejace1':
                d -= 1
                for j in range(0, 100):
                    dest_table[i + j] = d
            if i % 100 == 0 and zachowanie == 'rosnace2':
                d += 2
                for j in range(0, 100):
                    dest_table[i + j] = d
            if i % 100 == 0 and zachowanie == 'malejace2':
                d -= 2
                for j in range(0, 100):
                    dest_table[i + j] = d
            if i % 100 == 0 and zachowanie == 'losowe':
                d = dest[i]
                for j in range(0, 100):
                    dest_table[i + j] = d

            e[i] = d - y[i]
            error_sum += e[i] ** 2
            derive = (e[i] - e[i - 1]) / h
            integral += e[i] * h

            u[i] = kp * e[i] + ki * integral + kd * derive
            if u[i] > 10:
                u[i] = 10
            if u[i] < -10:
                u[i] = -10

            y[i + 1] = y[i] + h * (a * y[i] + u[i] + z[i])
        e[-1] = e[-2]
        u[-1] = u[-2]
        return t, y, e, u, mpmath.floor(error_sum)

    def get_optimal_P():

        min_sum_error = float('inf')
        param_p = np.arange(0, 10, 1)
        optimal_param = param_p[0]

        for i in range(param_p.shape[0]):
            t, y, e, u, error_sum = model(kp=param_p[i], ki=0, kd=0)

            if error_sum < min_sum_error :
                min_sum_error = error_sum
                optimal_param = param_p[i]

        print('Regulator P optymalny parametr P: ' + str(optimal_param))
        print('Błąd dla regulatora P: ' + str(min_sum_error))
        return optimal_param

    def get_optimal_PI():

        min_sum_error = float('inf')
        param_p = np.arange(0, 10, 1)
        param_i = np.arange(0, 10, 0.1)
        optimal_param_P = param_p[0]
        optimal_param_I = param_i[0]

        for i in range(param_p.shape[0]):

            for j in range(param_i.shape[0]):
                t, y, e, u, error_sum = model(kp=param_p[i], ki=param_i[j], kd=0)

                if error_sum < min_sum_error :
                    min_sum_error = error_sum
                    optimal_param_P = param_p[i]
                    optimal_param_I = param_i[j]

        print('Regulator PI optymalne parametry  P: ' + str(optimal_param_P) + " I: " + str(optimal_param_I))
        print('Błąd dla regulatora PI: ' + str(min_sum_error))
        return optimal_param_P, optimal_param_I

    def get_optimal_PID():

        min_sum_error = float('inf')
        param_p = np.arange(0, 10, 1)
        param_i = np.arange(0, 10, 0.1)
        param_d = np.arange(0, 1, 0.1)

        optimal_param_P = param_p[0]
        optimal_param_I = param_i[0]
        optimal_param_D = param_d[0]

        for i in range(param_p.shape[0]):

            for j in range(param_i.shape[0]):

                for k in range(param_d.shape[0]):
                    t, y, e, u, error_sum = model(kp=param_p[i], ki=param_i[j], kd=param_d[k])

                    if error_sum < min_sum_error - 1:
                        min_sum_error = error_sum
                        optimal_param_P = param_p[i]
                        optimal_param_I = param_i[j]
                        optimal_param_D = param_d[k]

        print('Regulator PID optymalne parametry  P: ' + str(optimal_param_P) + " I: " + str(
            optimal_param_I) + " D: " + str(
            optimal_param_D))
        print('Błąd dla regulatora PID: ' + str(min_sum_error))
        return optimal_param_P, optimal_param_I, optimal_param_D

    P_P = get_optimal_P()
    PI_P, PI_I = get_optimal_PI()
    PID_P, PID_I, PID_D = get_optimal_PID()

    p_t, p_y, p_e, p_u, _ = model(kp=P_P, ki=0, kd=0)
    pi_t, pi_y, pi_e, pi_u, _ = model(kp=P_P, ki=PI_I, kd=0)
    pid_t, pid_y, pid_e, pid_u, _ = model(kp=P_P, ki=PID_I, kd=PID_D)

    fig = plt.figure()
    fig.suptitle(nazwa_procesu)
    ax1 = fig.add_subplot(2, 1, 1)
    ax1.plot(t, dest_table, color='black', label='temperatura zadana')
    ax1.plot(p_t, p_y, label='P')
    ax1.plot(pi_t, pi_y, label='PI')
    ax1.plot(pid_t, pid_y, label='PID')
    ax1.set_xlabel('Czas')
    ax1.set_ylabel('Temperatura')
    ax1.set_title("")
    ax1.grid()
    ax1.legend(loc='best')

    ax4 = fig.add_subplot(2, 1, 2)
    ax4.plot(p_t, p_u, label='P')
    ax4.plot(pi_t, pi_u, label='PI')
    ax4.plot(pid_t, pid_u, label='PID')
    ax4.set_xlabel('Czas')
    ax4.set_ylabel('Moc')
    ax4.set_title("")
    ax4.grid()
    ax4.legend(loc='best')

    plt.savefig(nazwa_procesu)

    # plt.show()

    print()


d = 20
T = 10
y0 = 15
h = 0.01
a = -1 / 10

porownaj_regulatory(a=a, h=h, y0=y0, T=T, dest=d, zachowanie='stale')
porownaj_regulatory(a=a, h=h, y0=y0, T=T, dest=d, zachowanie='rosnace1')
porownaj_regulatory(a=a, h=h, y0=y0, T=T, dest=d, zachowanie='malejace2')
porownaj_regulatory(a=a, h=h, y0=y0, T=T, dest=d, zachowanie='losowe')
porownaj_regulatory(a=a, h=h, y0=y0, T=T, dest=d, zachowanie='zaklocenia')
