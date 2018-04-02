
function ranges = doScan(robotPosition, robotAngle, numberOfRays, noiseMagnitude, map) 


%    % For testing only
%    intersectionPoint = findIntersection([20 12 20 13], [14 15 23 15]);

   lineSegments = map;            
   numberOfSegments = size(lineSegments,1); 

   ranges = zeros(numberOfRays,1);
   
   for I = 1:numberOfRays
      angle = 2*pi*(I/numberOfRays)+robotAngle; % The angle is the robot angle + sweep angle
      angleDegrees = (angle/pi)* 180;

      unitVector = [cos(angle) sin(angle)]; % For the 'laser'
      segment1 = [robotPosition, robotPosition + unitVector];

      % Figure out which line segment it intersects with first.  
      closestIntersection = 10; % distance in meters
      closestSegment = -1;
      
  
      
      for J = 1:numberOfSegments
         % Find the intersection, if any, between the current vector and this line 
         % segment
         segment2 = lineSegments(J,:);
         intersectionPoint = findIntersection(segment1, segment2);
         x = intersectionPoint(1);
         y = intersectionPoint(2);

         
         
        
         
         % Check to see if this intersection is within the length of the line
         % segment.
         x1 = segment2(1);
         x2 = segment2(3);
         y1 = segment2(2);
         y2 = segment2(4);

         % sort the x and y points.  
         if x1 > x2
            temp = x1;
            x1 = x2;
            x2 = temp;
         end
         
         if y1 > y2
            temp = y1;
            y1 = y2;
            y2 = temp;
         end
         
       

            % if the intersection is in the line segment
            minDif = .000001;
            betweenX = (x > x1 && x < x2) || abs(x-x1) < minDif || abs(x-x2) < minDif;
            betweenY = (y > y1 && y < y2) || abs(y-y1) < minDif || abs(y-y2) < minDif;


            if betweenX && betweenY % then it intersected this 
               inter = [x y];  % The intersection point
               interVector = inter - robotPosition;


               % If the intersection is in the direction of the vector  (ie: not
               % behind it)
               intersectionDirection = atan2(interVector(2),interVector(1));
               rayDirection = atan2(unitVector(2),unitVector(1));
               
               if abs(wrapToPi(intersectionDirection - rayDirection)) < .01 
               
               
                  % Adjust the intersection point to get the true range, not the range
                  % from (0,0)
                  %inter = inter - robotPosition;
                  x = interVector(1);
                  y = interVector(2);
                  distance = sqrt(x^2 + y^2);
                  if distance < closestIntersection
                     closestIntersection = distance;
                     closestSegment = J;
                  end
               end
            end


      end % Of going through all of the line segments looking for the nearest intersection
      fprintf ('Angle: %.01f\t\tline segment: %d\n',angleDegrees,closestSegment);
      
      % take this distance and add a small amount of noise to it
      closestIntersection = closestIntersection + ((rand(1)-.5) * noiseMagnitude); 
      ranges(I) = closestIntersection;
   end % of going through every angle
  
   ranges(ranges > 1000) = 0;
   
end






function intersectionPoint = findIntersection(segment1, segment2)
   % segment1 is given as [x1,y1, x2, y2] and is the vector that is swept around
   % segment2 is given as [x1,y1, x2, y2] and is the line segment from the map
   % 

   
   x1 = [segment1(1) segment1(3)];
   y1 = [segment1(2) segment1(4)];
   
   x2 = [segment2(1) segment2(3)];
   y2 = [segment2(2) segment2(4)];
   
   m1 = (y1(2) - y1(1)) / (x1(2) - x1(1));
   m2 = (y2(2) - y2(1)) / (x2(2) - x2(1));

   % using y-y0 = m(x-x0)
   % y = mx -mx0 + y0
   % m1x - m1x1 + y1 = m2x - m2x2 + y2 
   % x(m1 - m2) = m1x1 - m2x2 + y2 - y1
   
   
   if abs(m1) == Inf % then the ray is vertical, solve for x = segment1(1)
      x = segment1(1);
      y = m2 * x - m2*x2(1) + y2(1);
      
   elseif abs(m2) == Inf % then the segment is vertical, solve for x = segment2(1)
      x = segment2(1);
      y = m1 * x - m1*x1(1) + y1(1);
      
      
   else % everything else
      x = (m1*x1(1) - m2*x2(1) + y2(1) - y1(1)) / (m1-m2);
      y = m1 * x - m1*x1(1) + y1(1);
   end

   intersectionPoint = [x y];
end