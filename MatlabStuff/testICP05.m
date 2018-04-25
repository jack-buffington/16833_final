% This script creates a map and generates a set of scan points from two differenct
% locations within that map.   It then tries to align those two scans.


% This function differs from testICP04.m in that it quantizes the first scan's points
% into a grid to simulate what will happen with an occupancy map.  It also has a much
% bigger map now.  
% This version restricts ranges to less than 8 meters

% version 04E differs from 04D in that it takes three scans and progressively aligns
% them.  

close all
clc

initialPosition = [1.5 6.5]; % in meters
initialAngle = 0; % in radians

offsetPosition = [1 .1];
offsetAngle = .1;
offsetPosition2 = [1 -.2];
offsetAngle2 = -.3;

useMaximumRange = 1;
useMovingObject = 1;

noiseMagnitude = 00;
movingObjectHeight = .75;
movingObjectTop = 7;


% Create the map to be scanned.  Each row is [x y x y] and represents a line
% segment.

% map = [-3,4,3,4;...      % This was the original map
%        3,4,3,-4;...
%        3,-4, 0,-3.5;...
%        0,-3.5,-3,-4;...
%        -3,-4, -3,4];
    
map = [0,0,0,8;...      % 1
       0,8,6,8;...      % 2
       6,8,6,13;...     % 3
       6,13,14,13;...   % 4
       14,13,14,8;...   % 5
       14,13,14,15;...  % 6
       14,15,23,15;...  % 7
       23,15,23,8;...   % 8
       17,8,23,8;...    % 9
       23,8,23,1;...    % 10
       20,1,23,1;...    % 11
       20,5,20,1;...    % 12
       3,5,20,5;...     % 13
       3,5,3,0;...      % 14
       0,0,3,0;...      % 15
       9,8,9,10;...     % 16
       9,10,11,10;...   % 17
       11,10,11,8;...   % 18
       9,8,11,8];       % 19
    
if useMovingObject == 1
   map = [map;...
          5,movingObjectTop,5,movingObjectTop-movingObjectHeight];        % 20 - extra 'wall' to simulate a moving object
end
    
% Draw the map
% figure(3)
% clf
% for I = 1:size(map,1)
%    plot([map(I,1); map(I,3)],[map(I,2); map(I,4)], 'r');
%    hold on
% end
% axis equal
% plot(initialPosition(1),initialPosition(2),'g*');
    
    
% First scan
numberOfRays = 260;
robotPosition = initialPosition; 
robotAngle = initialAngle; 


ranges1 = doScan(robotPosition,robotAngle,numberOfRays,noiseMagnitude,map);
XY1 = rangesToXY(ranges1);


% Get rid of max range values
if useMaximumRange == 0
   rangesToUse = ranges1 < 8;
   XY1 = XY1(rangesToUse == 1,:);
end

% plot(XY1(:,1)+initialPosition(1), XY1(:,2)+ initialPosition(2),'g.')

% ################
% Quantize the map
% ################
% gridSize = .01;
% XY1B = int32(XY1 ./ gridSize); % These will be integer numbers so convert back to floats
% XY1B = double(XY1B) * gridSize;

XY1B =XY1;


% Second scan
if useMovingObject == 1
   map(20,:) = [7,movingObjectTop,7,movingObjectTop - movingObjectHeight];  % move the 'moving' object
end
   
numberOfRays = 260;
robotPosition = initialPosition + offsetPosition;
robotAngle = initialAngle + offsetAngle;


ranges2 = doScan(robotPosition,robotAngle,numberOfRays,noiseMagnitude,map);
XY2 = rangesToXY(ranges2);

if useMaximumRange == 0
   rangesToUse = ranges2 < 8;
   XY2 = XY2(rangesToUse == 1,:);
end


% Third scan
if useMovingObject == 1
   map(20,:) = [8,movingObjectTop,8,movingObjectTop - movingObjectHeight];  % move the 'moving' object
end

numberOfRays = 260;
robotPosition = robotPosition + offsetPosition2;
robotAngle = robotAngle + offsetAngle2;


ranges3 = doScan(robotPosition,robotAngle,numberOfRays,noiseMagnitude,map);
XY3 = rangesToXY(ranges3);

if useMaximumRange == 0
   rangesToUse = ranges3 < 8;
   XY3 = XY3(rangesToUse == 1,:);
end






[rotationMatrix, translation] = ICP05(XY1B, XY2); % 1B because I was testing
                                                  % quantization 
disp('offset1:'); 
disp(offsetPosition);
disp('rotation1:')
disp(offsetAngle)

disp('computed offset1:'); 
disp(translation);
disp('computed rotation1:')
rotm3D = [rotationMatrix [0;0]; 0 0 0];
rotAngle = rotm2eul(rotm3D);
disp(rotAngle)


[rotationMatrix2, translation2] = ICP05(XY2, XY3);



disp('offset1:'); 
disp(offsetPosition2);
disp('rotation1:')
disp(offsetAngle2)

disp('computed offset2:'); 
disp(translation2);
disp('computed rotation2:')
rotm3D = [rotationMatrix2 [0;0]; 0 0 0];
rotAngle = rotm2eul(rotm3D);
disp(rotAngle)



cumulativeTransform = [rotationMatrix translation'; [0 0 1]]; 

% transform the 2nd set of points now
XY2temp = [XY2 ones(size(XY2,1),1)];
XY2temp = XY2temp * cumulativeTransform';
XY2 = XY2temp(:,1:2);


% update the cumulative transformation matrix
tempTransform = [rotationMatrix2 translation2'; [0 0 1]]; 
cumulativeTransform = cumulativeTransform * tempTransform;


% transform the third set of points
XY3temp = [XY3 ones(size(XY3,1),1)]; 
XY3temp = XY3temp * cumulativeTransform';
XY3 = XY3temp(:,1:2);





% Plot things out and see how it did.
figure(1);
clf
plot(XY1B(:,1),XY1B(:,2),'.r');
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



