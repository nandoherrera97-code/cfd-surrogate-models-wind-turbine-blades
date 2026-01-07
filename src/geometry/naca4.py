import numpy as np
import cadquery as cq

class NACA4Airfoil:
    def __init__(self, M_digit, P_digit, T_digits,
                 closed_te=True):

        self.M_digit = M_digit
        self.P_digit = P_digit
        self.T_digits = T_digits
        self.closed_te = closed_te

        self.M = M_digit / 100
        self.P = P_digit / 10
        self.T = T_digits / 100

        self.__validate()

    @classmethod
    def from_code(cls, code: str, closed_te=True, orientation_deg=0.0):
        if len(code) != 4 or not code.isdigit():
            raise ValueError("Invalid NACA 4-digit code.")
        return cls(int(code[0]), int(code[1]), int(code[2:]),
                   closed_te=closed_te)

    # ==========================
    # PRIVATE INTERNAL METHODS
    # ==========================

    def __validate(self):
        errors = []
        if not (0.0 <= self.M <= 0.09):
            errors.append(f"M={self.M_digit} must be between 0 and 9.")
        if self.M > 0 and not (0.1 <= self.P <= 0.9):
            errors.append(f"P={self.P_digit} must be between 1 and 9 if M > 0.")
        if not (0.01 <= self.T <= 0.40):
            errors.append(f"T={self.T_digits} must be between 01 and 40.")
        if errors:
            raise ValueError("\n".join(errors))
            
    # ==========================
    # PUBLIC INTERFACE
    # ==========================


    def coordinates(self, step):
        x = np.arange(0.0, 1.0 + step / 2, step)

        a0, a1, a2, a3 = 0.2969, -0.1260, -0.3516, 0.2843
        a4 = -0.1036 if self.closed_te else -0.1015

        yt = (self.T / 0.2) * (
            a0*np.sqrt(x) + a1*x + a2*x**2 + a3*x**3 + a4*x**4
        )

        yc = np.zeros_like(x)
        dyc_dx = np.zeros_like(x)

        if self.P <= 0 or self.P >= 1 or self.M == 0:
            yc[:] = 0.0
            dyc_dx[:] = 0.0
        else:
            front = x < self.P
            back = ~front

            yc[front] = (self.M / self.P**2) * (2*self.P*x[front] - x[front]**2)
            dyc_dx[front] = (2*self.M / self.P**2) * (self.P - x[front])

            yc[back] = (self.M / (1-self.P)**2) * (
                1 - 2*self.P + 2*self.P*x[back] - x[back]**2
            )
            dyc_dx[back] = (2*self.M / (1-self.P)**2) * (self.P - x[back])

        theta = np.arctan(dyc_dx)

        xu = x - yt*np.sin(theta)
        yu = yc + yt*np.cos(theta)
        xl = x + yt*np.sin(theta)
        yl = yc - yt*np.cos(theta)

        upper = np.column_stack([xu, yu])
        lower = np.column_stack([xl, yl])
        contour = np.vstack([upper[::-1], lower[1:]])

        return contour