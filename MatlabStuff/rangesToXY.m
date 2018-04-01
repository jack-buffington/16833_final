function XY = rangesToXY(ranges)
   % Convert the ranges into X and Y coordinates
   numberOfRays = size(ranges,1);
   XY = zeros(numberOfRays,2);
   for I = 1:numberOfRays
      angle = 2*pi*(I/numberOfRays);
      XY(I,:) = [ranges(I)*cos(angle), ranges(I)*sin(angle)];
   end
end