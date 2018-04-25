
filename = 'firstFloor2.txt';
fileData = csvread(filename);
% fileData will be in the form of one scan per line and each line is angle, distance, angle, distance, ...



close all
figure(1)
lastXY = getScanXY(fileData(75,:));

cumulativeTransform = eye(3);

for I = 80:4:3010
   XY = getScanXY(fileData(I,:));
   thisTransform = ICP06(lastXY, XY);
   lastXY = XY;
   
   cumulativeTransform = cumulativeTransform * thisTransform;
   
   % plot the transformed points
   XY = [XY ones(size(XY,1),1)];  %#ok<AGROW>
   XY = XY * cumulativeTransform';
   XY = XY(:,1:2);

   
   hold on
   plot(XY(:,2), XY(:,1),'r.');
%    xlim([-8000 8000])
%    ylim([-8000 8000])
   axis equal
   drawnow
   pause(.05);
%    clf
   
end
   
