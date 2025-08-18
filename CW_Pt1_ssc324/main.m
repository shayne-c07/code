%Ask user for panelgen parameters
code = input('Enter airfoil code (4 digits): ', 's');
N = input('Enter number of panels: ');
AoA = input('Enter angle of attack (in degrees): ') * (pi/180); %converts input AoA from degrees to radians
UFree = input('Enter freestream velocity (in m/s): ');


%Discretises airfoil based on inputs and plot streamlines and vectors using the below 3 functions 
[x,z] = panelgen(code, N, AoA);
[C_l, PanelStrengths] = liftCoeff(x,z,N,AoA,UFree);
fprintf('Lift Coefficient is %.5f\n', C_l); %displays lift coefficient
plots(x,z,N,AoA,UFree, PanelStrengths, code)


%Runs if the airfoil is NACA 2412
if strcmp(code, '2412') 
    alpha = 0:1:10; %defines a range of AoA's from 0 to 10 in steps of 1
    alphaR = alpha * pi/180; %converts to radians
    N = [100,200,500]; 
    lifts = zeros(length(alphaR), length(N)); %defines array to contain calculated lift coefficients
    for i = 1:length(alphaR) %loops for each index in the alphaR array
        for j = 1:length(N) %loops for each index in the N array
            [x,z] = panelgen(code, N(j), alphaR(i)); %obtains the x and z coordinates for the airfoil for each combination of N and AoA using the panelgen() function
            [lifts(i,j), PanelStrengths] = liftCoeff(x,z,N(j),alphaR(i),UFree); %obtains lift coefficients and panel strengths for each combination of N's and AoA's using the liftCoeff function defined below
        end
    end

    table = readmatrix("NACA.txt"); % read the file as a numeric matrix
    alphaTable = table(70:108, 1); %extracts AoA values 0:1:10 from file
    clTable = table(70:108, 2); %extracts the corresponding C_l values from file
    corrCL = zeros(1, length(alpha)); 
    
    for i = 1:length(alpha)
        index = find(alphaTable == alpha(i)); % find the index of the alpha value (in order to extract values 0:1:10)
        if ~isempty(index) %checks if index is found, if it is not empty(index is found) then stores the Cl value in the corrCl array
            corrCL(i) = clTable(index); % stores the CL value
        end
    end
    
    %Plots calulated C_l against alpha graphs for each value of N on same pair of axes
    figure('Name', 'C_L vs α')
    plot(alpha,lifts(:,1), 'r--o', LineWidth=1.5) %plots first case N=100
    hold on
    plot(alpha,lifts(:,2), 'b-.^', LineWidth=1.5) %plots second case N=200
    hold on
    plot(alpha,lifts(:,3), 'g-*', LineWidth=1.5) %plots third case N=500
    hold on
    plot(alpha, corrCL, 'k-', LineWidth=1.5) %plots real values from table

    legend('N=100','N=200','N=500', 'XFOIL Data', 'Location','best')
    xlabel('Angle Of Attack [degrees]')
    ylabel('C_L')
    title('C_L Against α (NACA 2412)')
    fontsize(12,"points")
    grid on

    currentFig = gcf;
    exportgraphics(currentFig,'NACA2412_Cl_vs_α.png','Resolution',300) %saves image of plot

    %Plots of last case (N=500, α=10)
    plots(x,z,N(end),alphaR(end),UFree,PanelStrengths, code)
end




function [C_l, PanelStrengths] = liftCoeff(x,z,N,AoA,UFree)
%This function takes the x and z coordinate arrays, the number of panels,
%the angle of attack and the freestream velocity of the flow as inputs, and
%computes the lift coefficient using different formulas. It also computes
%the panel strengths acting on all panels. It returns the lift coefficient
%and the array of panel strengths.

%Initialising arrays to contain the beta values, the x midpoint values, the
%z midpoint values, the eventual A matrix and the B vector
beta = zeros(1, N);
xMid = zeros(1,N);
zMid = zeros(1, N);
A = zeros(N+1, N+1);
B = zeros(1, N+1);

%Calculating midpoint values and beta values using Equation (10)
for i = 1:N
    xMid(i) = (x(i) + x(i+1)) / 2;
    zMid(i) = (z(i) + z(i+1)) / 2;
    beta(i) = atan2( (z(i+1) - z(i)) , (x(i+1) - x(i)) );
    if beta(i) < 0 %corrects values if outside range of 0 < B < 2pi
        beta(i) = beta(i) + 2*pi;
    end
end

for i = 1:N %loops through each panel i
    for j = 1:N+1 %to find the effects of each panel j on it (including wake panel hence the N+1)
         p = [xMid(i), zMid(i)]; %sets coordinates to evaluate U,V on
         p1 = [x(j), z(j)]; %panel j start point
         p2 = [x(j+1), z(j+1)]; %panel j end point
         [uIJ, vIJ] = cdoublet(p, p1, p2); %evaluates velocity components
         A(i, j) = -uIJ * sin(beta(i)) + (vIJ * cos(beta(i))); %Equation (9)
    end
    B(i) = -UFree * sin(AoA - beta(i)); % Equation (12)
end

%Equation 13 (Kutta condition)
A(N+1, 1) = 1;
A(N+1, N) = -1;
A(N+1, N+1) = 1;    
B(N+1) = 0;

PanelStrengths = A \ B'; %Solves via matrix inversion as per Equation (14)

C_l = -2*PanelStrengths(end) / UFree; %Equation (15)
end




function [] = plots(x,z,N,AoA,UFree, PanelStrengths, code)
%This function takes the x and z arrays, the number of panels, angle og
%attack, freestream velocity, the array of panel strengths and the airfoil
%code as parameters. It uses these to generate the plots of the velocity
%vectors and the streamlines on the airfoil. It produces 2 figures which
%are programatically saved and labelled according to user input. It does
%not return anything to the console.

AoA_D =  AoA / (pi/180); %AoA in degrees for formatted printing purposes

%VECTORS
xVector = linspace(-0.2, 1.2, 20); %defines x domain for velocity vectors and creates array of equally spaced points
zVector = linspace(-0.7, 0.7, 20); %defines z domain for velocity vectors and creates array of equally spaced points
[xV, zV] = meshgrid(xVector, zVector); %generates coarse grid of points

U1 = zeros(size(xV));
V1 = zeros(size(zV));

for i = 1:numel(U1) %loops through each panel i
    if ~inpolygon(xV(i), zV(i), x, z) %if point is not in polygon, evaluate it
        for j = 1:N+1 %to find the effects of each panel j on it
             p = [xV(i), zV(i)]; %sets coordinates to evaluate u,v on
             p1 = [x(j), z(j)]; %panel j start point
             p2 = [x(j+1), z(j+1)]; %panel j end point
             [uIJ, vIJ] = cdoublet(p, p1, p2); %evaluates velocity components
             U1(i) = U1(i) + (uIJ * PanelStrengths(j)); %Summation of u-component panel effects
             V1(i) = V1(i) + (vIJ * PanelStrengths(j)); %Summatiob of v-component panel effects          
        end
        U1(i) = U1(i) + (UFree * cos(AoA)); %Equation (8a)
        V1(i) = V1(i) + (UFree * sin(AoA)); %Equation (8b)  
    end
end


%STREAMLINES
xStreamline = linspace(-0.2, 1.2, 300); %defines x domain for streamlines and creates array of equally spaced points
zStreamline = linspace(-0.7, 0.7, 300); %defines z domain for streamlines and creates array of equally spaced points
[xS, zS] = meshgrid(xStreamline, zStreamline); %generates fine grid of points

U2 = zeros(size(xS));
V2 = zeros(size(zS));


for i = 1:numel(U2) %loops through each panel i
    if ~inpolygon(xS(i), zS(i), x, z) %if point is not in polygon, evaluate it
        for j = 1:N+1 %to find the effects of each panel j on it
             p = [xS(i), zS(i)]; %sets coordinates to evaluate u,v on
             p1 = [x(j), z(j)]; %panel j start point
             p2 = [x(j+1), z(j+1)]; %panel j end point
             [uIJ, vIJ] = cdoublet(p, p1, p2); %evaluates velocity components
             U2(i) = U2(i) + (uIJ * PanelStrengths(j)); %Summation of u-component panel effects
             V2(i) = V2(i) + (vIJ * PanelStrengths(j)); %Summation of v-component panel effects
        end
        U2(i) = U2(i) + (UFree * cos(AoA)); %Equation (8a)
        V2(i) = V2(i) + (UFree * sin(AoA)); %Equation (8b)
    end
end


%Plots
%Plot airfoil and velocity vectors on figure 1
figure('Name', 'Velocity Vectors')
plot(x(1:end-1),z(1:end-1), 'r-', LineWidth=2)
hold on
plot(x([1, end-1]), z([1, end-1]), 'r', LineWidth=2)
hold on
quiver(xV, zV, U1, V1, 'b', LineWidth=1)

% Set axes limits and plot properties
xlabel('x')
ylabel('z')
title(sprintf('NACA %s at α = %d° using N = %d panels with U_∞ of %dm/s', code, AoA_D, N, UFree))
fontsize(12,"points")
xlim([-0.2, 1.2]);  
ylim([-0.7, 0.7]); 

%save velocity vector plot as png's with variable names based on user input
currentFig = gcf;
name = sprintf('NACA%s_α=%d°_N=%d_U∞=%d_V.png', code, AoA_D, N, UFree);
exportgraphics(currentFig,name,'Resolution',300)


% Plot airfoil and streamlines on figure 2
figure('Name','Streamlines')
plot(x(1:end-1),z(1:end-1), 'r-', LineWidth=2)
hold on
plot(x([1, end-1]), z([1, end-1]), 'r', LineWidth=2)
hold on
ss = streamslice(xS, zS, U2, V2);
set(ss, 'Color', 'b') %sets color to blue

% Set axes limits and plot properties
xlabel('x')
ylabel('z')
title(sprintf('NACA %s at α = %d° using N = %d panels with U_∞ of %dm/s', code, AoA_D, N, UFree))
fontsize(12,"points")
xlim([-0.2, 1.2]);  
ylim([-0.7, 0.7]); 

%save streamlines plot as png's with variable names based on user input
currentFig = gcf;
name = sprintf('NACA%s_α=%d°_N=%d_U∞=%d_S.png', code, AoA_D, N, UFree);
exportgraphics(currentFig,name,'Resolution',300)
end