function [x,z] = panelgen(code, N, AoA)
%validate inputs 
if (length(code)) == 4 && (N>3) && isnumeric(N) && mod(N,1) ==0 && isnumeric(AoA) 
    %input is valid and code continues
else
    error('Please check input. Should be a valid NACA 4-series airfoil with more than 3 panels.');
end

%define different variables from the numbers in the airfoil
m = str2double(code(1)) / 100;
p = str2double(code(2)) / 10;
t = str2double(code(3:4)) / 100;

x_ND = 1:1:N+1; %defines array of non dimensional x values
x_ND = 1 - 0.5*(1 - cos(2*pi * ((x_ND - 1) / N))); %Equation (7)

%Defines arrays 
y_c = zeros(1, length(x_ND));
theta = zeros(1, length(x_ND));

for i = 1:length(x_ND)
    if x_ND(i) <= p
        y_c(i) = (m / (p^2)) * (2*p*x_ND(i) - (x_ND(i)^2)); %Equation (1) & (6)
        theta(i) = (2*m / (p^2)) * (p-x_ND(i));
    else
        y_c(i) = (m / ((1 - p)^2)) * ((1-(2*p)) + 2*p*x_ND(i) - (x_ND(i)^2)); %Equation (1) & (6)
        theta(i) = (2*m / ((1-p)^2)) * (p-x_ND(i));
    end
end

theta = atan(theta); %Equation (5)
y_t = 5*t*(0.2969*sqrt(x_ND) - 0.126*x_ND - 0.3516*(x_ND.^2) + 0.2843*(x_ND.^3) - 0.1015*(x_ND.^4)); %Equation (2)

xU = x_ND - y_t .* sin(theta); %Equation (3)
xL = x_ND + y_t .* sin(theta); %Equation (4)
zU = y_c + y_t .* cos(theta); %Equation (3)
zL = y_c - y_t .* cos(theta); %Equation (4)

%Correctly concatenates and orders the x and z arrays
x = cat(2, xL(1 : floor((N/2)+1)), xU(floor((N/2)+2) : N+1));
z = cat(2, zL(1 : floor((N/2)+1)), zU(floor((N/2)+2) : N+1));

%Adds extra wake panel that extends to a very large number
x = [x, 99999]; 
z = [z, zU(end)]; 

%Sets any NaN values to 0 (may not be necessary in most cases)
x(isnan(x)) = 0;
z(isnan(z)) = 0;
end