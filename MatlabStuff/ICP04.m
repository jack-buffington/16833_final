function [rotationMatrix, translation] = ICP04(XY1, XY2)
   % This version interpolates the first point set to make matching more accurate.
   % Additionally, it is the first version that actually implements the full ICP
   % algorithm.
   
   
   % Interpolate between points in the first scan
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
   
   
   originalXY2 = XY2;

   
   % ###############
   % Do the ICP part
   % ###############
   totalTranslation = [0,0];
   totalRotationMatrix = eye(2);
   maxIterations = 50;
   %errorThreshold = .00008; % This value seems to be good enough.
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
