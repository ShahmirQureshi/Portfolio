% Load example maps
load exampleMaps
map = binaryOccupancyMap(simpleMap);
figure

% Show original map
map = binaryOccupancyMap(map, 1);
subplot(121), show(map);
title('Original Map');

% Commented out the inflation part
% inflatedMap = copy(map);
% inflate(inflatedMap, 0.1); % Reduced inflation radius
% subplot(122), show(inflatedMap);
% title('Inflated Map');

% Create PRM object
prm = mobileRobotPRM;
prm.NumNodes = 50;
prm.ConnectionDistance = 80;
prm.Map = map; % Use the original map

% Get start and goal locations
disp('Click for the Start Location');
startLocation = ginput(1);
disp('Click for the Goal Location');
endLocation = ginput(1);
path = findpath(prm, startLocation, endLocation);

% Increase number of nodes until a path is found
while isempty(path)
    prm.NumNodes = prm.NumNodes + 20;
    update(prm);
    path = findpath(prm, startLocation, endLocation);
    show(prm);
    pause(1);
end

show(prm);
title('Path on Original Map');

% Commented out the second inflation part
% inflatedMap = copy(map);
% inflate(inflatedMap, 1); % Reduced inflation radius
% subplot(121), show(map);
% subplot(122), show(inflatedMap);
% title('Inflated Map');

% prm = mobileRobotPRM;
% prm.NumNodes = 50;
% prm.ConnectionDistance = 80;
% prm.Map = inflatedMap;

% disp('Click for the Start Location');
% startLocation = ginput(1);
% disp('Click for the Goal Location');
% endLocation = ginput(1);
% path = findpath(prm, startLocation, endLocation);

% while isempty(path)
%     prm.NumNodes = prm.NumNodes + 20;
%     update(prm);
%     path = findpath(prm, startLocation, endLocation);
%     show(prm);
%     pause(1);
% end

% show(prm);
% title('Path on Inflated Map');
