a0 = 1.4142;
b0 = 0.7071;

y = [0,0,0]
x = [1,0,0]

for i in range(16):
    y[0] = a0*y[1]-y[2]+b0*x[0];
    y[2]=y[1];
    y[1] = y[0];
    x[0] = 0;
    print y[0]

