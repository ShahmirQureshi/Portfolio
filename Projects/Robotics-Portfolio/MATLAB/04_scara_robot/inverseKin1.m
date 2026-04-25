function [th1,th2,d3] = inverseKin1(xc,yc,zc,sol)
d3 = 0.575 - zc;
th1 = 0;
th2 = 0;

switch sol
    case 0
        D = (xc^2 + yc.^2 - 0.425^2 - 0.5^2)/(2*0.5*0.425);
        th2 = atan2d(-sqrt(1-D^2),D);
        th1 = atan2d(yc,xc) - atan2d(0.425*sind(th2),(0.5+0.425*cosd(th2)));
    case 1
        D = (xc^2 + yc.^2 - 0.425^2 - 0.5^2)/(2*0.5*0.425);
        th2 = atan2d(sqrt(1-D^2),D);
        th1 = atan2d(yc,xc) - atan2d(0.425*sind(th2),(0.5+0.425*cosd(th2)));
end