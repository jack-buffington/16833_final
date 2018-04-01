function [rotationMatrix, translation] = ICP02(XY1, XY2)
   % This version uses the centroid as a starting point but then iterates without
   % shifting the centroid.
   
   centroid1 = mean(XY1);
   centroid2 = mean(XY2);
   
%    centeredXY1 = XY1 - centroid1;
%    centeredXY2 = XY2 - centroid2;
   
   % Find the closest point in XY2 for each point in XY1
   distances = pdist2(XY1, XY2); 
   % distances is a matrix where each row corresponds to a point in XY1
   % and each column corresponds to a point in XY2
   % The values are the distances between those points
   [~, XY1index] = min(distances);
   
   % Create a new matrix that contains the nearest point to each point in centeredXY2
   closestPoints = XY1(XY1index,:);
   
   % Find covariance between the two matrices
   cov = XY2' * closestPoints;
   
   % Use that to find the rotation.
   [U, ~, V] = svd(cov);
   rotationMatrix = V*U';
   
   % Find the optimal translation
   %translation = centroid1' - rotationMatrix * centroid2'; 
   % Rotate the points
   XY2 = (rotationMatrix * XY2')';
   % Find their average translation from their corresponding closest points
   difs = XY2 - closestPoints;
   offset = mean(difs);
   translation = -offset;
end


