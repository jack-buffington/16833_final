

numberOfRays = 400;
robotPosition = [0,0]; % in meters
robotAngle = 0; % in radians
noiseMagnitude = .01; % Could have UP TO this amount in meters added to each range
                      % measurement


% Create the map to be scanned.  Each row is [x y x y] and represents a line
% segment.
map = [-3,4,3,4;...  
       3,4,3,-4;...
       3,-4, 0,-3.5;...
       0,-3.5,-3,-4;...
       -3,-4, -3,4];

    
% plot out the line segments in the actual orientation
for I = 1:size(map,1)
   x = [map(I,1); map(I,3)];
   y = [map(I,2); map(I,4)];
   plot(x,y,'r');
   hold on
end

figure(1)
clf
axis equal

% This is the actual scan
ranges1 = doScan(robotPosition,robotAngle,numberOfRays,noiseMagnitude,map);


% Convert the ranges into X and Y coordinates
scan1 = zeros(numberOfRays,2);
for I = 1:numberOfRays
   angle = 2*pi*(I/numberOfRays);
   scan1(I,:) = [ranges1(I)*cos(angle), ranges1(I)*sin(angle)];
end


% Plot the ranges as the robot sees things.
plot(scan1(:,1),scan1(:,2),'.');
axis equal
plot(robotPosition(1),robotPosition(2),'*r');






