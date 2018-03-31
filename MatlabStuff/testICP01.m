% This script creates a map and generates a set of scan points from two differenct
% locations within that map.   I tthen tries to align those two scans.

numberOfRays = 260;
noiseMagnitude = .01; % Could have UP TO this amount in meters added to each range
                      % measurement


% Create the map to be scanned.  Each row is [x y x y] and represents a line
% segment.
map = [-3,4,3,4;...  
       3,4,3,-4;...
       3,-4, 0,-3.5;...
       0,-3.5,-3,-4;...
       -3,-4, -3,4];
    
    
robotPosition = [2,.3]; % in meters
robotAngle = 0.03; % in radians

ranges1 = doScan(robotPosition,robotAngle,numberOfRays,noiseMagnitude,map);
XY1 = rangesToXY(ranges1);

robotPosition = [1.8,.22]; % in meters
robotAngle = 0.08; % in radians

ranges2 = doScan(robotPosition,robotAngle,numberOfRays,noiseMagnitude,map);
XY2 = rangesToXY(ranges2);

