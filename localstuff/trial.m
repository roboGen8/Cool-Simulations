
close all; clear all; clc;
[num3test, ~, ~] = xlsread("test3.xls");
[time, ~] = size(num3test);
x1 = num3test(:, 1);
x2 = num3test(:, 2);
x3 = num3test(:, 3);
y1 = num3test(:, 4);
y2 = num3test(:, 5);
y3 = num3test(:, 6);

x1o = x1(1);
x2o = x2(1);
x3o = x3(1);
y1o = y1(1);
y2o = y2(1);
y3o = y3(1);
EnKF(time, x1, y1, x1o, y1o, 1);
EnKF(time, x2, y2, x2o, y2o, 2);
EnKF(time, x3, y3, x3o, y3o, 3);



function [] = EnKF(time, x, y, x0, y0, fig)
out = [];
for i = 1: 100
    noise = rand();
    initialCondition = [x0 y0] + noise * randn(1, 2);
    tdata = time(1:50:end);
    error=rand();
    xdata = x(1:50:end) + error * randn(length(tdata), 1);
    ydata = y(1:50:end) + error * randn(length(tdata), 1);

    curr = [];
    for j = 1:length(tdata)-1
        t = 0:0.01:0.5;
        [t, xyz] = ode45(handler, t, initialCondition);
        initialCondition0 = [xyz(end,1); xyz(end,2)];
        data = [xdata(j+1); ydata(j+1)];
        kalmanFilter = noise/ (noise + error);
        initialCondition = initialCondition0 + (kalmanFilter * (data - initialCondition0));
        curr = [curr; xyz(1:end-1,:)];
    end
    curr = [curr; xyz(end,:)];
    out(:, :, i) = curr;
end
out = mean(out, 3);

figure(fig*10);
plot(time, x,'r',time, out(:,1),'k');
xlabel('time');
ylabel('x');
legend('original','EnKF');

figure(fig*10 + 1);
plot(time, y,'r',time, out(:,2),'k');
xlabel('time');
ylabel('y');
legend('original','EnKF');
end
