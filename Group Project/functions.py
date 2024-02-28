"""
A library of functions
"""
import numpy as np
import matplotlib.pyplot as plt
import numbers


class AbstractFunction:
    """
    An abstract function class
    """

    def derivative(self):
        """
        returns another function f' which is the derivative of x
        """
        raise NotImplementedError("derivative")


    def __str__(self):
        return "AbstractFunction"


    def __repr__(self):
        return "AbstractFunction"


    def evaluate(self, x):
        """
        evaluate at x

        assumes x is a numeric value, or numpy array of values
        """
        raise NotImplementedError("evaluate")


    def __call__(self, x):
        """
        if x is another AbstractFunction, return the composition of functions

        if x is a string return a string that uses x as the indeterminate

        otherwise, evaluate function at a point x using evaluate
        """
        if isinstance(x, AbstractFunction):
            return Compose(self, x)
        elif isinstance(x, str):
            return self.__str__().format(x)
        else:
            return self.evaluate(x)

    # problem 2 (a)
    def taylor_series(self, x0, deg=5):
        """
        Returns the Taylor series of f centered at x0 truncated to degree k.
        """
        if isinstance(x0, numbers.Number):
            p = Polynomial(self.evaluate(x0))  # f(x0)
            deriv = self
            if isinstance(self.evaluate(x0), str):  # for symbolic functions
                for i in range(deg):
                    deriv = deriv.derivative()  # f^{n}(x0)
                    f = Polynomial(deriv.evaluate(x0)+'/{}'.  # divided by (n)!
                                   format(np.math.factorial(i+1))) 
                    p = p+f*(Affine(1,-x0))**(i+1)    
                return p 
            else:  # for other type of abstractfunctions
                for i in range(deg): 
                    deriv = deriv.derivative()  # f^{i+1}(x0)
                    if deriv.evaluate(x0)==0:
                        p = p
                    else:
                        f = Polynomial(deriv.evaluate(x0)/np.math.factorial(i+1))
                        p = p+f*(Affine(1,-x0))**(i+1)
                return p
        else:
            return NotImplementedError("taylor series")



    # the rest of these methods will be implemented when we write the appropriate functions
    def __add__(self, other):
        """
        returns a new function expressing the sum of two functions
        """
        return Sum(self, other)


    def __mul__(self, other):
        """
        returns a new function expressing the product of two functions
        """
        return Product(self, other)


    def __neg__(self):
        return Scale(-1)(self)


    def __truediv__(self, other):
        return self * other**-1


    def __pow__(self, n):
        return Power(n)(self)


    def plot(self, vals=np.linspace(-1,1,100), **kwargs):
        """
        plots function on values
        pass kwargs to plotting function
        """

        # Compute ys
        ys = self.evaluate(vals)

        # Make plot with optional arguments
        plt.plot(vals, ys, **kwargs)

        return


class Polynomial(AbstractFunction):
    """
    polynomial c_n x^n + ... + c_1 x + c_0
    """

    def __init__(self, *args):
        """
        Polynomial(c_n ... c_0)

        Creates a polynomial
        c_n x^n + c_{n-1} x^{n-1} + ... + c_0
        """
        self.coeff = np.array(list(args))


    def __repr__(self):
        return "Polynomial{}".format(tuple(self.coeff))


    def __str__(self):
        """
        We'll create a string starting with leading term first

        there are a lot of branch conditions to make everything look pretty
        """
        s = ""
        deg = self.degree()
        for i, c in enumerate(self.coeff):
            if i < deg-1:
                if c == 0:
                    # don't print term at all
                    continue
                elif c == 1:
                    # supress coefficient
                    s = s + "({{0}})^{} + ".format(deg - i)
                else:
                    # print coefficient
                    s = s + "{}({{0}})^{} + ".format(c, deg - i)
            elif i == deg-1:
                # linear term
                if c == 0:
                    continue
                elif c == 1:
                    # suppress coefficient
                    s = s + "{0} + "
                else:
                    s = s + "{}({{0}}) + ".format(c)
            else:
                if c == 0 and len(s) > 0:
                    continue
                else:
                    # constant term
                    s = s + "{}".format(c)

        # handle possible trailing +
        if s[-3:] == " + ":
            s = s[:-3]

        return s


    def evaluate(self, x):
        """
        evaluate polynomial at x
        """
        if isinstance(x, numbers.Number):
            ret = 0
            for k, c in enumerate(reversed(self.coeff)):
                ret = ret + c * x**k
            return ret
        elif isinstance(x, np.ndarray):
            x = np.array(x)
            # use vandermonde matrix
            return np.vander(x, len(self.coeff)).dot(self.coeff)


    def derivative(self):
        if len(self.coeff) == 1:
            return Polynomial(0)
        return Polynomial(*(self.coeff[:-1] * np.array([n+1 for n in reversed(range(self.degree()))])))


    def degree(self):
        return len(self.coeff) - 1


    def __add__(self, other):
        """
        Polynomials are closed under addition - implement special rule
        """
        if isinstance(other, Polynomial):
            # add
            if self.degree() > other.degree():
                coeff = self.coeff
                coeff[-(other.degree() + 1):] += other.coeff
                return Polynomial(*coeff)
            else:
                coeff = other.coeff
                coeff[-(self.degree() + 1):] += self.coeff
                return Polynomial(*coeff)

        else:
            # do default add
            return super().__add__(other)


    def __mul__(self, other):
        """
        Polynomials are clused under multiplication - implement special rule
        """
        if isinstance(other, Polynomial):
            return Polynomial(*np.polymul(self.coeff, other.coeff))
        else:
            return super().__mul__(other)    
    


class Affine(Polynomial):
    """
    affine function a * x + b
    """
    def __init__(self, a, b):
        super().__init__(a, b)

class Scale(Polynomial):
    # Scale(a) should be equivalent to the polynomial a * x + 0

    def __init__(self, a):
        super().__init__(a, 0)

class Constant(Polynomial):
    # Constant(c) should be equivalent to the polynomial c

    def __init__(self, c):
        super().__init__(c)

class Sum(AbstractFunction):
    # Sum, where Sum(f,g)(x) acts as f(x) + g(x)

    def __init__(self, f, g):
        self.f = f
        self.g = g

    def __str__(self):
        return self.f.__str__()+'+'+self.g.__str__()

    def __repr__(self):
        return 'Sum('+self.f.__repr__()+', '+self.g.__repr__()+')'

    def derivative(self):
        return Sum(self.f.derivative(), self.g.derivative())
    
    def evaluate(self, x):
        if isinstance(self.f.evaluate(x), str):
            return self.f.evaluate(x) + '+' + self.g.evaluate(x)
        else:
            return self.f.evaluate(x) + self.g.evaluate(x)
    
    

class Product(AbstractFunction):
    # Product, where Product(f, g)(x) acts as f(x) * g(x)

    def __init__(self, f, g):
        self.f = f
        self.g = g

    def __str__(self):
        return '('+self.f.__str__()+')*('+self.g.__str__()+')'

    def __repr__(self):
        return 'Product('+self.f.__repr__()+', '+self.g.__repr__()+')'

    def derivative(self):
        return Sum(
            Product(self.f.derivative(), self.g),
            Product(self.f, self.g.derivative())
            )

    def evaluate(self, x):
        if isinstance(self.f.evaluate(x), str):
            return self.f.evaluate(x) + '*' + self.g.evaluate(x)
        else:
            return self.f.evaluate(x) * self.g.evaluate(x)
    

class Compose(AbstractFunction):
    # Compose, where Compose(f, g)(x) acts as f(g(x))

    def __init__(self, f, g):
        self.f = f
        self.g = g

    def __str__(self):
        return self.f.__str__().format(self.g.__str__())

    def __repr__(self):
        return 'Compose('+self.f.__repr__()+', '+self.g.__repr__()+')'

    def derivative(self):
        return Product(self.f.derivative()(self.g), self.g.derivative())

    def evaluate(self, x):
        return self.f.evaluate(self.g.evaluate(x))
    
    
    
# Part D
class Power(AbstractFunction):
    # Power, where Power(n)(x) acts as x**n (n can be negative, or non-integer)

    def __init__(self, n):
        self.n = n

    def __str__(self):
        return "({0})^" + str(self.n)

    def __repr__(self):
        return "Power(" + str(self.n) + ")"

    def derivative(self):
        return Scale(self.n)(Power(self.n-1))

    def evaluate(self, x):
        return x**self.n
    
    

class Log(AbstractFunction):
    # Log, where Log()(x) acts as np.log(x)
    
    def __init__(self):
        return

    def __str__(self):
        return "log({0})"

    def __repr__(self):
        return "Log()"
    
    def derivative(self):
        return Power(-1)
    
    def evaluate(self, x):
        return np.log(x)
    
    
class Exponential(AbstractFunction):
    # Exponential, where Exponential()(x) acts as np.exp(x)
    
    def __init__(self):
        return
  
    def __str__(self):
        return "exponential({0})"

    def __repr__(self):
        return "Exponential()"
    
    def derivative(self):
        return Exponential()
    
    def evaluate(self, x):
        return np.exp(x)
    
    
                                                     
class Sin(AbstractFunction):
    # Sin, where Sin()(x) acts as np.sin(x)
    
    def __init__(self):
        return

    def __str__(self):
        return "sin({0})"

    def __repr__(self):
        return "Sin()"
    
    def derivative(self):
        return Cos()
    
    def evaluate(self, x):
        return np.sin(x)     

        
    
class Cos(AbstractFunction):
    # Cos, where Cos()(x) acts as np.cos(x)
    
    def __init__(self):
        return

    def __str__(self):
        return "cos({0})"

    def __repr__(self):
        return "Cos()"
    
    def derivative(self):
        return Scale(-1)(Sin())
    
    def evaluate(self, x):
        return np.cos(x)
    
    
# Part E
class Symbolic(AbstractFunction):
    # Define a symbolic function with the name of the function as input
    
    def __init__(self, name):
        if isinstance(name, str):
            self.name = name
        else:
            raise TypeError ("name must be a string") 
        
    def __str__(self):
        return self.name + "({0})"

    def __repr__(self):
        return "Symbolic(" + self.name + ")"
    
    def derivative(self):
        return Symbolic(self.name + "'")
    
    def evaluate(self, x):
        return self.name + "({})".format(x)    
        

#Problem1 (a)
def newton_root(f, x0, tol=1e-8):
    """
    find a point x so that f(x) is close to 0,
    measured by abs(f(x)) < tol

    Use Newton's method starting at point x0
    """
    if isinstance(f,Symbolic):
        raise ValueError('Funtion must not be Symbolic')
    if not isinstance(f, AbstractFunction):
        raise ValueError('Funtion must be AbstractFunction')

    while True:
        x1=x0 - f(x0) / f.derivative()(x0)
        if abs(f(x1)) < tol:
            break
        x0=x1
    return x1
	
#Problem1 (b)   
def newton_extremum(f, x0, tol=1e-8):
    """
    find a point x so that f(x) is close to 0,
    measured by abs(f(x)) < tol

    Use Newton's method starting at point x0
    """
    if isinstance(f,Symbolic):
        raise ValueError('Funtion must not be Symbolic')
    if not isinstance(f, AbstractFunction):
        raise ValueError('Funtion must be AbstractFunction')

    while True:
        x1=x0 - f.derivative()(x0) / f.derivative().derivative()(x0)
        if abs(f.derivative()(x1)) < tol:
            break
        x0=x1
    return x1  
 
    
    
    
    
    
    
    
    
    
