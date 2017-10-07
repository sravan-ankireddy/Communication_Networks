import numpy as np

import matplotlib.pyplot as plt

lam = 1; #arrival rate

A = [];

r = 15;	#service rate of each counter

N = 100000; #no. of customers

Lmax = 40; #max length of queue

Ln = np.random.randint(1, Lmax + 1, N);	#lengths of customers uniformly distributed
# print(len(Ln))
# print(Ln);
# print(len(Ln));

i = 0;

A.append(0);

while( i < N):	#Arrival intervals with exponential distribution
	A.append(A[i] + np.random.exponential(1/lam));
	i = i + 1;
# print(len(A))
# print(A);

delay = [];

X = np.arange(1,40);

# print(X);

for x in X:
	T1 = 0;	W1 = 0;#latest time and wait times for queue1

	T2 = 0;	W2 = 0;#latest time and wait times for queue2

	j = 0;

	for j in range(0,N):
		# print(j);
		if (Ln[j] > x):	#queue1j
			if(A[j + 1] > T1):	#direct service
				T1 = A[j + 1] + (Ln[j]/r);
			else:	#update waiting time
				W1 = W1 + (T1 - A[j + 1]);
				T1 = T1 + (Ln[j]/r);
		else :	#queue2
			if(A[j + 1] > T2):	#direct service
				T2 = A[j + 1] + (Ln[j]/r);
			else:	#update waiting time
				W2 = W2 + (T2 - A[j + 1]);
				T2 = T2 + (Ln[j]/r);
	delay.append((W1 + W2)/N);
# print(len(X));
# print(len(delay));	
print(delay);
print(len(delay));

print(np.argmin(delay));

fig = plt.figure()

ax = fig.add_subplot(111)

ax.set_title('Average delays')

ax.set_xlabel('Value of "x" ')

ax.set_ylabel('Average delay of customers in the queue')

ax.semilogy(X, delay, color = 'b', label = 'Simulation');

plt.legend(shadow=True, fancybox=True)

plt.show()