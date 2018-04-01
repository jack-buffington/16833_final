% This script creates a map and generates a set of scan points from two differenct
% locations within that map.   It then tries to align those two scans.

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

robotPosition = [2.3,.22]; % in meters
robotAngle = 0.15; % in radians

ranges2 = doScan(robotPosition,robotAngle,numberOfRays,noiseMagnitude,map);
XY2 = rangesToXY(ranges2);

% % Perform ICP on the data to find the optimal alignment.
% [rotationMatrix, translation] = ICP02(XY1, XY2);
% 
% 
% % Apply the rotation and translation that was found.
% % rotation first
% XY3 = (rotationMatrix * XY2')';
% XY3 = XY3 + translation;
% 


% repeat a few more times for good measure
XY4 = XY2;

for I = 1:10
   [rotationMatrix, translation] = ICP02(XY1, XY4);
   XY4 = (rotationMatrix * XY4')';
   XY4 = XY4 + translation;
end


% Plot things out and see how it did.
figure(1);
clf
plot(XY1(:,1),XY1(:,2),'.r');
hold on
plot(XY2(:,1),XY2(:,2),'.g');
plot(XY4(:,1),XY4(:,2),'.b');
%plot(XY4(:,1),XY4(:,2),'+k');

axis equal



