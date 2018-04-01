function [rotationMatrix, translation] = ICP01(XY1, XY2)
   % This method repeatedly shifts so that the centroids match up 

   centroid1 = mean(XY1);
   centeredXY1 = XY1 - centroid1;
   
   

   centroid2 = mean(XY2);
   centeredXY2 = XY2 - centroid2;

   % Find the closest point in XY2 for each point in XY1
   distances = pdist2(centeredXY1, centeredXY2); 
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
   translation = centroid1' - rotationMatrix * centroid2'; 

   % Now shift/rotate all of the points and repeat
   XY2 = (rotationMatrix' * XY2')';
   XY2 = XY2 + translation';

end

%  # Find the centroids
%     oldCentroid = findCentroid(oldScanXY)
%     newCentroid = findCentroid(newScanXY)
% 
%     print 'old scan Centroid: '
%     print type(oldCentroid) 
% 
%     # Remove the centroids
%     oldScanXYcentered = oldScanXY - oldCentroid
%     newScanXYcentered = newScanXY - newCentroid
% 
%     print 'old scan Centered: '
%     print type(oldScanXYcentered) 
% 
%     print 'shape of old scan: ', oldScanXYcentered.shape
%     print 'shape of new scan: ', newScanXYcentered.shape
%    
% 
% 
%     # Find the closest points by Euclidean distance
%     pointMatches = ClosestPoints(oldScanXYcentered, newScanXYcentered)
%     #print'matches:', pointMatches
%     # find the covariance between the new scan and the point matches and then find the rotation 
%     rotMatrix = find_rotation(pointMatches, newScanXYcentered)
% 
%     # Find the translation.  
%     translation = np.transpose(np.matrix(oldCentroid)) - rotMatrix * np.transpose(np.matrix(newCentroid))

