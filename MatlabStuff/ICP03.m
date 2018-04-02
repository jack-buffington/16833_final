function [rotationMatrix, translation] = ICP03(XY1, XY2)
   % This version is the same as version 2 but it makes sure that there is a point in
   % XY1 every minDistance units.  This will hopefully allow the algorithm to find a
   % better match.   
   
   
   
   % Find the distances between successive points.
   numberOfPoints = size(XY1,1);
   
   maxDist = .07;
   
   for I = 1:numberOfPoints - 1
      A = XY1(I,:);
      B = XY1(I+1,:);
      
      distance = pdist([A;B]);
      if distance > maxDist % Create one or more interpolated points between them
         numberOfInterpolatedPoints = int32(distance / maxDist);
         offset = (B-A)/double(numberOfInterpolatedPoints + 1);
        
         currentLocation = A;
         for J = 1:numberOfInterpolatedPoints
            currentLocation = currentLocation + offset;
            XY1 = [XY1; currentLocation]; 
         end
      end
   end
   
   % Check the first and last points as a special case.
   A = XY1(numberOfPoints,:);
   B = XY1(1,:);

   distance = pdist([A;B]);
   if distance > maxDist % Create one or more interpolated points between them
      numberOfInterpolatedPoints = int32(distance / maxDist);
      offset = (B-A)/double(numberOfInterpolatedPoints + 1);

      currentLocation = A;
      for J = 1:numberOfInterpolatedPoints
         currentLocation = currentLocation + offset;
         XY1 = [XY1; currentLocation]; 
      end
   end
   
%    figure(1);
%    clf
%    plot(XY1(:,1),XY1(:,2),'.r');
%    hold on
%    plot(XY2(:,1),XY2(:,2),'.g');
%    axis equal
%    
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


