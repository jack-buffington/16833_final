function [transformMatrix] = ICP06(XY1, XY2)
   % This version interpolates the first point set to make matching more accurate.
   % Additionally, it is the first version that actually implements the full ICP
   % algorithm.
   
   % This is the same as ICP04 except that it attempts to refine the solution once it
   % has run ICP once.  It does this by removing points from the solution that are
   % greater than 1.5 times maxDist from their nearest point. 
   
   % version 06 changes the output to be a homogenous transform matrix.  
   
   
   % Interpolate between points in the first scan
   % Find the distances between successive points.
   numberOfPoints = size(XY1,1);
   
   maxDist = 50; % millimeters
   
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
   
   


   
   % ###############
   % Do the ICP part
   % ###############
   
   [rotationMatrix, translation] = actualICP(XY1, XY2);
   
   % rotate and translate the XY2 points
   XY2temp = (rotationMatrix * XY2')';
   XY2temp = XY2temp + translation;
   
   
   % #########################################
   % Remove points that don't align very well:
   % #########################################
   
   
   % * Find the distances to all of the closest points again
   distances = pdist2(XY1, XY2temp);  %XY2 is the moved set of points
   [minDistances, ~] = min(distances);
   
   % * Figure out if there are any points that don't sit close to any points in the old
   %     To find points that are outliers, look for points that are more than 1.5 times
   %     the maxDist 
   pointsToKeep = minDistances < maxDist * 1.5; % 1's and 0's
   count  = 1:size(pointsToKeep,2);
   pointsToKeep = pointsToKeep .* count;
   pointsToKeep = pointsToKeep(pointsToKeep > 0);
   
   % and temporarily remove them from the new set.
   XY2refined = XY2(pointsToKeep,:);
   
   A = 0;

   
   % ##############################################################
   % Do ICP again with the two sets of points that match up better.
   % ##############################################################
   
   [rotationMatrix, translation] = actualICP(XY1, XY2refined);
   
   
   transformMatrix = [rotationMatrix translation'; [0 0 1]]; 
end




function [rotationMatrix, translation] = actualICP(XY1, XY2)
totalTranslation = [0,0];
   totalRotationMatrix = eye(2);
   maxIterations = 50;
   errorThreshold = .00001; % This value seems to be good enough.

   
   for I = 1:maxIterations
      [rotationMatrix, translation,err] = doOneIteration(XY1,XY2);
      
      %fprintf('Error for revision %02d = %f\n',I,err);
      if err < errorThreshold
         break;
      end
      
      XY2 = (rotationMatrix * XY2')';
      XY2 = XY2 + translation;
      
      % Keep track of the total rotation and translation  
      totalTranslation = (rotationMatrix * totalTranslation')' + translation;
      totalRotationMatrix = rotationMatrix * totalRotationMatrix; 
   end

   rotationMatrix = totalRotationMatrix;
   translation = totalTranslation;
end






function [rotationMatrix, translation,err] = doOneIteration(XY1,XY2)
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
   XY2 = (rotationMatrix * XY2')';
   % Find their average translation from their corresponding closest points
   difs = XY2 - closestPoints;
   offset = mean(difs);
   translation = -offset;
   
   % Calculate the error in alignment as the sum of squared distances between point
   % matches.
   err = sqrt(offset(1)^2 + offset(2)^2);
   
   
end
