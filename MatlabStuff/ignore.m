% This is a script that will help me figure out how to invert a transformation matrix

angle = (20/180)*pi;
translation = [1 2];

eul = [angle 0 0];
rotMatrix = eul2rotm(eul);

transformationMatrix = rotMatrix;

transformationMatrix(1:2,3) = translation';



points = [randi(9,8,2) ones(8,1)];

transformedPoints1 = points * transformationMatrix';

% Now invert the transformation
rotationPart = transformationMatrix(1:2,1:2);
translationPart = transformationMatrix(1:2,3);

rinv = inv(rotationPart);
tinv = -rinv*translationPart;

inverseMatrix = [rinv tinv; 0 0 1];

transformedPoints2 = transformedPoints1 * inverseMatrix';

disp(points)
disp('----');
disp(transformedPoints2);