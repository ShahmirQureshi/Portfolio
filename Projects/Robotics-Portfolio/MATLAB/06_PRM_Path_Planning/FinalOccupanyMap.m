% Define grid parameters (scaled down by a factor of 100)
grid_size_mm = 10;  % Size of the grid in millimeters (previously 10,000 mm)
cell_size_mm = 0.1;   % Size of each cell in millimeters (changed)
grid_size_cells = floor(grid_size_mm / cell_size_mm);  % Grid size in cells
border_width_mm = 0.152;  % Border width in millimeters (previously 152 mm)
border_width_cells = floor(border_width_mm / cell_size_mm);  % Border width in cells

% Define cylinder parameters (scaled down by a factor of 100)
cylinder_outer_radius_mm = 2.7;  % Outer radius of the cylinder in millimeters (previously 2,700 mm)
cylinder_outer_radius_cells = floor(cylinder_outer_radius_mm / cell_size_mm);  % Radius in cells

% Initialize the original grid with free space (0)
occupancy_grid = zeros(grid_size_cells, grid_size_cells);

% Calculate the center of the grid
center = floor(grid_size_cells / 2);

% Create the border wall
occupancy_grid(1:border_width_cells, :) = 1;  % Top border
occupancy_grid(end-border_width_cells+1:end, :) = 1;  % Bottom border
occupancy_grid(:, 1:border_width_cells) = 1;  % Left border
occupancy_grid(:, end-border_width_cells+1:end) = 1;  % Right border

% Create the cylindrical wall with an open sector from 90 to 180 degrees
for i = 1:grid_size_cells
    for j = 1:grid_size_cells
        distance = sqrt((i - center)^2 + (j - center)^2);
        angle = rad2deg(atan2(j - center, i - center));
        if angle < 0
            angle = angle + 360;
        end
        % Adjust cylinder radius and angle conditions
        if (cylinder_outer_radius_cells - 1 <= distance && distance <= cylinder_outer_radius_cells + 1) && ~(90 <= angle && angle <= 180)
            occupancy_grid(i, j) = 1;
        end
    end
end

% Define robot base diameter (changed)
robot_base_diameter_mm = 0.512;
robot_base_radius_cells = floor(robot_base_diameter_mm / (2 * cell_size_mm));

% Function to inflate occupied cells
function inflated_grid = inflate_map(grid, radius)
    [grid_size_cells, ~] = size(grid);
    inflated_grid = grid;
    for i = 1:grid_size_cells
        for j = 1:grid_size_cells
            if grid(i, j) == 1
                for k = max(1, i - radius):min(grid_size_cells, i + radius)
                    for l = max(1, j - radius):min(grid_size_cells, j + radius)
                        inflated_grid(k, l) = 1;
                    end
                end
            end
        end
    end
end

% Inflate the original map
inflated_occupancy_grid = inflate_map(occupancy_grid, robot_base_radius_cells);

% Save the inflated occupancy grid map
save('Final_occupancy_grid_inflated.mat', 'inflated_occupancy_grid');
save('Final_occupancy_grid.mat', 'occupancy_grid');

% Plot both original and inflated maps
figure;
subplot(1, 2, 1);
imshow(occupancy_grid, 'InitialMagnification', 'fit');
title('Original Map');
colormap('gray');
colorbar;
% Add grid size labels
xticks(0:floor(grid_size_cells/10):grid_size_cells);
yticks(0:floor(grid_size_cells/10):grid_size_cells);
xticklabels(num2str((0:floor(grid_size_cells/10):grid_size_cells) * cell_size_mm));
yticklabels(num2str((0:floor(grid_size_cells/10):grid_size_cells) * cell_size_mm));




subplot(1, 2, 2);
imshow(inflated_occupancy_grid, 'InitialMagnification', 'fit');
title('Inflated Map');
colormap('gray');
colorbar;
xticks(1:100:grid_size_cells);
yticks(1:100:grid_size_cells);
xticklabels(round((1:100:grid_size_cells) * cell_size_mm, 2));
yticklabels(round((1:100:grid_size_cells) * cell_size_mm, 2));
xlabel('X (meters)');
ylabel('Y (meters)');
 