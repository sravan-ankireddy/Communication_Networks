import numpy as np

import matplotlib.pyplot as plt

lam = [ 0.01, 0.03, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.92, 0.93, 0.94, 0.95, 0.96, 0.97, 0.98];	#Values of arrival rate lambda

N = [];	#Buffer to store average number of customers for each arrival rate

T = 100000;	#Simulation time

for k in range(0, len(lam)):

	T0 = 0; 	#Current time

	delT = 0; 	

	state = 0; 	#Current state

	Tcus = 0; 	#Cumulative time spent by customers 

	A = [];

	D = [];

	i = 0; j = 0;

	A.append(0);

	D.append(0);


	mu = 1;

	while( A[i] < T):	#Arrival intervals with exponential distribution
		A.append(A[i] + np.random.exponential(1/lam[k]));
		i = i+1;

	while( D[j] < T):	#Departure intervals with deterministic distribution
		D.append(D[j] + mu);
		j = j + 1;

	ai = 1; di = 1;

	while (A[ai] < T):	#When arrival occurs
		if (A[ai] < D[di]):
			Tcus = Tcus + state * (A[ai] - T0);
			T0 = A[ai];
			ai = ai + 1;
			state = state + 1;
		else :	#When departure occurs
			Tcus = Tcus + state * (D[di] - T0);
			T0 = D[di];
			di = di + 1;
			if (state > 0):	
				state = state - 1;
	N.append(Tcus/A[ai]);	#Average number of customers in the Queue

Nt = [];

for l in range(0, len(lam)):	#Analytical values
	Nt.append( lam[l] + (0.5)*(lam[l]*lam[l])/(1 - lam[l]));

fig = plt.figure()

ax = fig.add_subplot(111)

ax.set_title('MD1 queueing')

ax.set_xlabel('Load')

ax.set_ylabel('Average no. of customers in the queue')

ax.plot(lam, N, color = 'b', label = 'Simulation');

ax.plot(lam, Nt, color = 'r', label = 'Analytical');

plt.legend(shadow=True, fancybox=True)

plt.show()