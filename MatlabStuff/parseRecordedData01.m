
filename = 'firstFloor2.txt';
%filename = 'basement2.txt';
% filename = 'highbay2.txt';


fileData = csvread(filename);
% fileData will be in the form of one scan per line and each line is angle, distance, angle, distance, ...





close all
figure(1)

firstFrame = 90;
lastFrame = size(fileData,1);


lastXY = getScanXY(fileData(firstFrame - 5,:));
% Strip away any 'points' that ended up being [0 0]
lastXY = lastXY(sum(lastXY==0,2) < 2,:);
cumulativeTransform = eye(3);

colorIndex = 1;






for I = firstFrame:5:lastFrame
   XY = getScanXY(fileData(I,:));
   
   % Strip away any 'points' that ended up being [0 0]
   % TODO:  Check to see if this is necessary in Python.  Some points that aren't at 
   % the end are also 0's 
   XY = XY(sum(XY==0,2) < 2,:);
   
   
   thisTransform = ICP06(lastXY, XY);
   lastXY = XY;
   
 
   
   cumulativeTransform = cumulativeTransform * thisTransform;
   
   % plot the transformed points and robot location
   XY = [XY ones(size(XY,1),1)];  %#ok<AGROW>
   XY = XY * cumulativeTransform';
   XY = XY(:,1:2);
   
   
   robotLocation = [0 0 1];
   robotLocation = robotLocation * cumulativeTransform';
   robotLocation = robotLocation(1,1:2);

   hold on
   

   plot(XY(:,2), XY(:,1),'r.');
   plot(robotLocation(2),robotLocation(1),'b.');

   axis equal
   drawnow
   pause(.05); 
end
   
