from sympy import Symbol, nsolve

t1 = 23000.0 # tr0 guess
d1 = 1.385459 # dtr guess

n1 = -0.014 # number of turns clockwise between ring 1 and ring 4.
n2 = -0.002 # number of turns clockwise between ring 4 and ring 8.

r = 24.5 # starting radius (mm)
rs1 = r+1*4 # ring 1 radius (one away from the innermost that is equal to the starting radius) (mm)
rs2 = r+4*4 # ring 4 radius (mm)
rs3 = r+8*4 # ring 8 radius (mm)

e1 = Symbol('e1')
e2 = Symbol('e2')

t0 = t1-e1
d0 = d1-e2

LS1 = (rs1/r-1)*t0/d0
A1 = LS1+1
B1 = (LS1+1)*LS1/2
C1 = 4*t0**2-4*t0*d0+d0**2+8*A1*d0*t0+8*B1*d0**2
D1 = ((C1+8*e1*A1*d0+8*e2*B1*d0)**(1/2)-C1**(1/2))/(2*d0)

LS2 = (rs2/r-1)*t0/d0
A2 = LS2+1
B2 = (LS2+1)*LS2/2
C2 = 4*t0**2-4*t0*d0+d0**2+8*A2*d0*t0+8*B2*d0**2
D2 = ((C2+8*e1*A2*d0+8*e2*B2*d0)**(1/2)-C2**(1/2))/(2*d0)

LS3 = (rs3/r-1)*t0/d0
A3 = LS3+1
B3 = (LS3+1)*LS3/2
C3 = 4*t0**2-4*t0*d0+d0**2+8*A3*d0*t0+8*B3*d0**2
D3 = ((C3+8*e1*A3*d0+8*e2*B3*d0)**(1/2)-C3**(1/2))/(2*d0)

n1s = D2-D1-n1
n2s = D3-D2-n2

solved_res = nsolve((n1s, n2s), (e1, e2), (0, 0))
print("New guess for tr0: ",t1-solved_res[0])
print("New guess for dtr: ",d1-solved_res[1])
