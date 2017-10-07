'''
Date: 6/10/2017
Author: Sravan Kumar Ankireddy
Title: Weighted Fair Queueing packet GPS multiplexer
'''

import numpy as np

import csv

import matplotlib.pyplot as plt

Cap = 1000;

num_q = 4;

num_p = 6;

weights = [0.1, 0.2, 0.3, 0.4];

id_num = [];

t = [];

l = [];	#storing arrival lengths by queue index

l2 = []; #storing arrival lengths by packet id

Vt = [];

Vt2 = [];

for j in range(num_q):
	l.append([])
	Vt.append([])

q = [];

with open('input1.txt' , 'r') as f:
    reader = csv.reader(f, delimiter=';')
    for row in reader:
    	id_num.append(row[0]);
    	t.append(row[1]);
    	l2.append(row[2])
    	l[int(row[3]) - 1].append(row[2]);
    	q.append(row[3]);

for j in range(num_q):
	for k in range(len(l[j])):
		l[j][k] = int(l[j][k]);

for i in range(num_p):
	id_num[i] = int(id_num[i]);
	t[i] = float(t[i]);
	q[i] = int(q[i]);
	l2[i] = int(l2[i]);

C = [0] * num_q	#capacities for each queue

z = [0] * num_q; #indicator variables for each queue

lat_q = [0] * num_q;	#latest index for each queue

count_q = [-1] * num_q;	#count of packets in each queue

QID = [];

Z = 0;

cur_t = t[0];

for i in range(num_p):
	count_q[q[i] - 1] = count_q[q[i] - 1] + 1; #updating the queue count
	z[q[i] - 1] = 1; #updating the indicator variable
	w_sum = 0;
	for j in range(num_q):
		w_sum = w_sum + z[j]*weights[j]; #calculating the cumulative weight
	if (w_sum > 0):
		Z = 1;
	for j in range(num_q):
		C[j] = Cap * weights[j] * Z * z[j] / w_sum;
	if ( i < 5):
		temp_t1 = t[i];	#min time
		temp_t2 = t[i + 1];	
		
		while ( temp_t1 < temp_t2):
			t_old = temp_t1;
			temp_t_b = temp_t1;
			trig = 0;
			brk = -1;
			for j in range(num_q): 
				if ( count_q[j] >= 0 ):	#if there are packets
					if ( temp_t1 + l[j][lat_q[j]] / C[j] < t[i + 1] ):
						if ( trig == 0 ):
							temp_t1 = temp_t1 + l[j][lat_q[j]] / C[j];
							trig = trig + 1;
							t_old = temp_t1 - l[j][lat_q[j]] / C[j];
						if ( t_old + l[j][lat_q[j]] / C[j]  < temp_t1 ):
							temp_t1 = t_old + l[j][lat_q[j]] / C[j];
							t_old = temp_t1 - l[j][lat_q[j]] / C[j];
							brk = j;
			if ( temp_t1 == temp_t_b): #if the latest time doesn't change
				temp_t1 = t[i + 1];
				for j in range(num_q):
					if ( count_q[j] >= 0 ):
						l[j][lat_q[j]] = l[j][lat_q[j]] - C[j] * ( temp_t1 - temp_t_b );
			else:
				for j in range(num_q):	
					if ( count_q[j] >= 0 ):
						l[j][lat_q[j]] = l[j][lat_q[j]] - C[j] * ( temp_t1 - t_old );
						if ( l[j][lat_q[j]] < 0.1 ):
							l[j][lat_q[j]] = 0;
							Vt[j].append(temp_t1);
							Vt2.append(temp_t1);
							QID.append(j + 1);
							lat_q[j] = lat_q[j] + 1;
							count_q[j] = count_q[j] - 1;
						if ( count_q[j] == -1 ):
							z[j] = 0;
						w_sum = 0;
						for k_w in range(num_q):
							w_sum = w_sum + z[k_w]*weights[k_w];
						if (w_sum > 0):
							Z = 1;
						for j_c in range(num_q):
							C[j_c]= Cap * weights[j_c] * Z * z[j_c] / w_sum;

sum_q_count = 0;

for i in range(num_q):
	sum_q_count = sum_q_count + count_q[i]; #total remaining packets  

temp_t1 = t[ num_q + 1];
t_old = temp_t1;

end = 0;

while ( sum_q_count > -(num_q + 1) and end == 0 ):
		if ( sum_q_count == -num_q):
			end = 1;
		trig = 0;

		for j in range(num_q):
			if ( count_q[j] >= 0 ):	#if there are packets
				if ( trig == 0):
					temp_t1 =  temp_t1 + l[j][lat_q[j]] / C[j];
					trig = trig + 1;
					t_old = temp_t1 - l[j][lat_q[j]] / C[j];
				if ( t_old + l[j][lat_q[j]] / C[j] < temp_t1 ):
					temp_t1 = t_old + l[j][lat_q[j]] / C[j];
					t_old = temp_t1 - l[j][lat_q[j]] / C[j];

		for j in range(num_q):
			if ( count_q[j] >= 0 ): #if there are packets
				l[j][lat_q[j]] = l[j][lat_q[j]] - C[j] * ( temp_t1 - t_old );
				if ( l[j][lat_q[j]] < 0.1 ):
					l[j][lat_q[j]] = 0;
					Vt[j].append(temp_t1);
					Vt2.append(temp_t1);
					QID.append(j + 1);
					lat_q[j] = lat_q[j] + 1;
					count_q[j] = count_q[j] - 1;
					sum_q_count = sum_q_count - 1;
				if ( count_q[j] == -1 ):
					z[j] = 0;
				w_sum = 0;
				for j_w in range(num_q):
					w_sum = w_sum + z[j_w]*weights[j_w];
				if (w_sum > 0):
					Z = 1;
				else:
					Z = 0;
				for j_c in range(num_q):
					if ( Z == 1):
						C[j_c]= Cap * weights[j_c] * Z * z[j_c] / w_sum;

ID = []

c = [-1] * num_q;

for i in range(num_p):
	j = 0;
	while ( j <= c[QID[i] - 1] or q[j] != QID[i] ):
		j = j + 1;
	c[QID[i] - 1] = j;
	ID.append(id_num[j]);

TT = [];

QQ = [];

ct = t[0];
ctq = q[0];

rem = [0] * num_p;

for j in range(num_p):
	for i in range(num_p):
		if ( t[ID[i] - 1] <= ct and rem[ID[i] - 1] == 0):
			ct = ct + float(l2[QID[i] - 1]) / Cap;
			rem[ID[i] - 1] = 1; 
			TT.append(ct);
			QQ.append(ID[i])
			break;

print("*** Departure times of packets using GPS ***\n");
print(Vt2)
print("\n")
print("*** Order of departure of packets using GPS ***")
print(ID)
print("\n")
print("*** Departure times of packets using WFQ ***")
print(TT)
print("\n")
print("*** Order of departure of packets using WFQ ***")
print(QQ)
print("\n")