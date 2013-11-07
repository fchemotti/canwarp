# Frank Chemotti
# fchemotti@gmail.com
# Fixes geometric distortions of images made with cylindrical pinhole cameras.
# Input is an image made by projection onto the surface of a cylinder
# from an opening in the side of the cylinder.
# Output uses spherical projection (from center) instead.
# Use in interactive python like this:
# file_cyl2sph("imgtest/fuentes800.jpg", "imgout/fuentes800.jpg", .9)

import numpy as np
import cv2
import math

def cyl2sph(x, y, d):
  """Convert cyclindrical coordinates to spherical.

  Assume the cylinder (and its axis of symmetry) is vertical.
  Fovea is the point on cyclinder diametrically opposite the aperture.
  Input:
  x - horizontal distance around cylinder from fovea
  y - vertical distance along cylinder from fovea
  d - diameter of cylinder, in same units as x and y
  Output:
  theta - azimuth (in radians) from fovea
  phi - elevation (in radians) from fovea
  """  
  theta = float(x) / d
  phi = math.atan(y / math.cos(theta) / d)
  return (theta, phi)

def sph2cyl(theta, phi, d):
  """Convert spherical coordinates to cylindrical.

  Assume the cylinder (and its axis of symmetry) is vertical.
  Fovea is the point on cyclinder diametrically opposite the aperture.
  Input:
  theta - azimuth (in radians) from fovea
  phi - elevation (in radians) from fovea
  d - diameter of cylinder, in same units as x and y
  Output:
  x - horizontal distance around cylinder from fovea
  y - vertical distance along cylinder from fovea
  """  
  return (d * theta, d * math.tan(phi) * math.cos(theta))

def img_cyl2sph(img_in, coverage):
  """Return image transformed from cylindrical image img_in using cyl2sph.

  Input:
  img_in - numpy image with 3 channels of type uint8
  coverage - proportion of the cylinder circumference covered by image
  Output:
  return value - numpy square image with same width as img_in,
                 in spherical coordinates where vert/horiz edges represent
                 +/- pi/2 radians from center."""
  x_center = img_in.shape[1] / 2
  y_center = img_in.shape[0] / 2
  d = img_in.shape[1] / coverage / math.pi

  theta_max = math.pi / 2
  theta_min = -theta_max
  phi_max = math.pi / 2
  phi_min = -phi_max
  t_max = img_in.shape[1]
  p_max = img_in.shape[1] 

  img_out = np.zeros((p_max, t_max, 3), dtype='uint8')

  for t in range(t_max):
    for p in range(p_max):
      theta = float(t) / t_max * (theta_max - theta_min) + theta_min
      phi = float(p) / p_max * (phi_max - phi_min) + phi_min
      cyl = sph2cyl(theta, phi, d)
      x = int(cyl[0] + x_center)
      y = int(cyl[1] + y_center)
      if x in range(img_in.shape[1]) and y in range(img_in.shape[0]):
        img_out[p, t] = img_in[y, x]

  return img_out

def file_cyl2sph(file_in, file_out, coverage):
  if coverage <= 0 or coverage > 1:
    coverage = 0.9
  img = cv2.imread(file_in)
  img2 = img_cyl2sph(img, coverage)
  cv2.imwrite(file_out, img2)
