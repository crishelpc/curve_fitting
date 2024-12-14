import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline 

# x = np.array([0,5,8,12,16,20,23,31])
# y = np.array([3,3,5,6,15,17,11,18])
# norm1 = np.array([0.97656735, 3.72228227, 5.36971122, 7.56628315, 9.76285509, 11.95942702, 13.60685598, 17.99999985])
# norm2 = np.array([1.8928875, 4.62579613, 6.2655413, 8.45186821, 10.63819511, 12.82452201, 14.46426719, 18.83692099])
# norm3 = np.array([4.4433098, 6.64852549, 7.9716549, 9.73582745, 11.5, 13.26417255, 14.58730196, 18.11564706])

# plt.scatter(x, y)
# plt.plot(x, y)

# plt.scatter(x, norm1)
# plt.plot(x, norm1)

# plt.scatter(x, norm2)
# plt.plot(x, norm2)

# plt.scatter(x, norm3)
# plt.plot(x, norm3)

# plt.show()

# xnew = np.linspace(x.min(), x.max(), 100) 
# gfg1 = make_interp_spline(x, y, k=2) 
# ynew = gfg1(xnew) 

# gfg2 = make_interp_spline(x, norm1, k=3) 
# n1new = gfg2(xnew) 

# gfg3 = make_interp_spline(x, norm2, k=3) 
# n2new = gfg3(xnew) 

# gfg4 = make_interp_spline(x, norm3, k=3) 
# n3new = gfg4(xnew) 

# plt.plot(xnew, ynew)

# plt.plot(xnew, n1new)

# plt.plot(xnew, n2new)

# plt.plot(xnew, n3new)

# plt.show()

x = np.array([1, 2, 3, 5, 6, 7, 9, 10])
y = np.array([12, 18, 21, 15, 23, 25, 30, 28])

a = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
b = np.array([12, 18, 21, 13.85, 15, 23, 25, 21.58, 30, 28])

xnew = np.linspace(x.min(), x.max(), 100) 
anew = np.linspace(a.min(), a.max(), 100) 

gfg1 = make_interp_spline(x, y, k=2) 
ynew = gfg1(xnew)

gfg2 = make_interp_spline(a, b, k=2) 
bnew = gfg2(anew)

plt.plot(xnew, ynew)
plt.plot(anew, bnew)
plt.show()