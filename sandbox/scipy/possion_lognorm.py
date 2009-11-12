from scipy.stats import poisson, lognorm

#A general example of creating a distribution, generating random variables
#and calculating the probability desnity function.

myShape = 5
myMu = 10

ln = lognorm(MyShape)
p = poisson(myMu)

ln.rvs((10,)) #generate 10 random vaiables from ln
#output: array([  2.09164812e+00,   3.29062874e-01,   1.22453941e-03,
#                 3.80101527e+02,   7.67464002e-02,   2.53530952e+01,
#                 1.41850880e+03,   8.36347923e+03,   8.69209870e+03,
#                 1.64317413e-01])
p.rvs((10,)) #generate 10 random variables from p
#output: array([ 8,  9,  7, 12,  6, 13, 11, 11, 10,  8])
ln.pdf(3) #lognorm probability density function at x=3
#output: array(0.02596183475208955)
