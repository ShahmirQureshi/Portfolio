% Open the Simulink model
open_system('Lesson7_DOF3_RRR_PD');

% Define the blocks to be tuned
TunedBlocks = {'PD1', 'PD2', 'PD3'};

% Create the slTuner interface for the Simulink model
ST0 = slTuner('Lesson7_DOF3_RRR_PD', TunedBlocks);

% Add analysis points for the tuned blocks
addPoint(ST0, TunedBlocks);

% Add analysis points for the measurements
addPoint(ST0, 'Lesson7_DOF3_RRR_PD/Robot/1');

% Define the reference signals
RefSignals = {...
    'Lesson7_DOF3_RRR_PD/Sine Wave/1', ...
    'Lesson7_DOF3_RRR_PD/Sine Wave1/1', ...
    'Lesson7_DOF3_RRR_PD/Sine Wave2/1'};

addPoint(ST0, RefSignals);

% Define the controls and measurements
Controls = TunedBlocks;
Measurements = 'Lesson7_DOF3_RRR_PD/Robot/1';

% Define looptune options
options = looptuneOptions('RandomStart', 80, 'UseParallel', false);

% Define the tracking goal
TR = TuningGoal.StepTracking(RefSignals, Measurements, 0.05);

% Perform the tuning
ST1 = looptune(ST0, Controls, Measurements, TR, options);

% Write the tuned values back to the Simulink blocks
writeBlockValue(ST1);
