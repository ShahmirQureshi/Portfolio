% Load your custom occupancy map
load('Final_occupancy_grid.mat', 'occupancy_grid');  % Load your map variable

% Create a binary occupancy map from your data
cell_size_mm = 10;  % Adjust the resolution as needed (e.g., 1 meter per cell)
map = binaryOccupancyMap(occupancy_grid, cell_size_mm);

% Display the binary occupancy map
figure;
show(map);
title('Binary Occupancy Grid');
xlabel('X [meters]');
ylabel('Y [meters]');

% Prompt the user to click on the map to select start and end locations
disp('Click on the map to select the start location.');
[startLocationX, startLocationY] = ginput(1);
startLocation = [startLocationX, startLocationY];

disp('Click on the map to select the goal location.');
[goalLocationX, goalLocationY] = ginput(1);
endLocation = [goalLocationX, goalLocationY];

% Close the figure after selecting points
close;

% Define the robot's track width
robot.TrackWidth = 0.5;  % Replace with your robot's actual track width

% Inflate the map for robot clearance
mapInflated = copy(map);
inflate(mapInflated, robot.TrackWidth / 2);

% Create a PRM object
prm = robotics.PRM(mapInflated);
prm.NumNodes = 100;
prm.ConnectionDistance = 10;

% Find a path
path = findpath(prm, startLocation, endLocation);
show(prm);
title('Probabilistic Roadmap');
xlabel('X [meters]');
ylabel('Y [meters]');

% Initialize the controller with the new path
controller = robotics.PurePursuit('Waypoints', path);

% Set initial robot state
robotInitialLocation = path(1,:);
robotGoal = path(end,:);
initialOrientation = 0;
robotCurrentPose = [robotInitialLocation initialOrientation]';

% Compute distance to goal
distanceToGoal = norm(robotInitialLocation - robotGoal);
goalRadius = 0.1;

% Initialize visualization
vizRate = robotics.Rate(10);  % Rate of visualization update
figure;

% Main loop to drive the robot
while distanceToGoal > goalRadius
    % Compute the controller outputs
    [v, omega] = controller(robotCurrentPose);
    
    % Update the current pose
    sampleTime = 0.1;  % Adjust the sample time as needed
    theta = robotCurrentPose(3);
    deltaX = v * cos(theta) * sampleTime;
    deltaY = v * sin(theta) * sampleTime;
    deltaTheta = omega * sampleTime;
    robotCurrentPose = robotCurrentPose + [deltaX; deltaY; deltaTheta]; 
    
    % Re-compute the distance to the goal
    distanceToGoal = norm(robotCurrentPose(1:2) - robotGoal(:));
    
    % Update the plot
    hold off;
    show(map);
    hold on;
    
    % Plot path
    plot(path(:,1), path(:,2), 'k--d');
    
    % Plot robot path
    plotTrVec = [robotCurrentPose(1:2); 0];
    plotRot = axang2quat([0 0 1 robotCurrentPose(3)]);
    plotTransforms(plotTrVec', plotRot, 'MeshFilePath', 'groundvehicle.stl', 'Parent', gca, 'View', '2D', 'FrameSize', 1);  % Adjust 'FrameSize' as needed
    
    % Set plot limits
    xlim([0 10]);
    ylim([0 10]);
    
    % Wait for the next iteration
    waitfor(vizRate);
end
