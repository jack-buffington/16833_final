function XY = getScanXY(data)
   % data is the raw data from one scan.  It is in the format:
   % angle, distance, angle, distance, ...
   % angle is 0-360 degrees
   % distance is in millimeters
   
   reshapedData = reshape(data,2,length(data)/2)';
   
   % reshapedData should be in the form of 
   % angle distance
   % angle distance
   % ...
   angles = reshapedData(:,1);
   
   
   distances = reshapedData(:,2);
   
   Xs = distances .* cosd(angles);
   Ys = distances .* sind(angles);
   
   XY = [Xs,Ys];
   
end