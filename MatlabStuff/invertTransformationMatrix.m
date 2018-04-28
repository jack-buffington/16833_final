function newMatrix = invertTransformationMatrix(matrix)
   rotationPart = matrix(1:2,1:2);
   translationPart = matrix(1:2,3);

   rinv = inv(rotationPart);
   tinv = -rinv*translationPart;

   newMatrix = [rinv tinv; 0 0 1];
end