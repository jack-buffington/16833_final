% This script creates a map and generates a set of scan points from two differenct
% locations within that map.   It then tries to align those two scans.


initialPosition = [.4 -1]; % in meters
initialAngle = .5; % in radians

offsetPosition = [.5 .3];
offsetAngle = .2;



% Create the map to be scanned.  Each row is [x y x y] and represents a line
% segment.
map = [-3,4,3,4;...  
       3,4,3,-4;...
       3,-4, 0,-3.5;...
       0,-3.5,-3,-4;...
       -3,-4, -3,4];
    
% First scan
numberOfRays = 260;
robotPosition = initialPosition; 
robotAngle = initialAngle; 
noiseMagnitude = .05;

ranges1 = doScan(robotPosition,robotAngle,numberOfRays,noiseMagnitude,map);
XY1 = rangesToXY(ranges1);


% Second scan
numberOfRays = 200;
robotPosition = initialPosition + offsetPosition;
robotAngle = initialAngle + offsetAngle;
noiseMagnitude = .05; 

ranges2 = doScan(robotPosition,robotAngle,numberOfRays,noiseMagnitude,map);
XY2 = rangesToXY(ranges2);





[rotationMatrix, translation] = ICP04(XY1, XY2);

XY3 = (rotationMatrix * XY2')';
XY3 = XY3 + translation;



% Plot things out and see how it did.
figure(1);
clf
plot(XY1(:,1),XY1(:,2),'.r');
hold on
plot(XY2(:,1),XY2(:,2),'.g');
plot(XY3(:,1),XY3(:,2),'.b');

rotm3D = [rotationMatrix [0;0]; 0 0 0];

computedAngle = rotm2eul(rotm3D);

% Report the angle and displacement that it found
fprintf('Given translation: \t%f, %f\n',offsetPosition);
fprintf('Computed translation: \t%f, %f\n',translation);
fprintf('Given angle: %f\n',offsetAngle);
fprintf('Computed angle: %f\n',computedAngle(1));

axis equal



