from scipy import linspace, polyval, polyfit, sqrt, stats, randn
from pylab import plot, title, show, legend

#This is a basic linear regression example that I found at http://www.scipy.org/Cookbook/LinearRegression.
#However, i've been modifying it slightly to test some of the aspects of the way it works to be more familiar with it.
#It uses two scipy tools for linear regression, polyfit and stats.linregress, the output is plotted using matplotlib.

n=100 #the number of points in the plot that will be the "noise"
t=linspace(-3,3,n) #the range -3 to 3 (inclusive) numbered on the x axis
a=0.8; b=-4 #the parameters
x=polyval([a,b],t)
xn=x+randn(n) #add some noise by generating some random numbers within the bound defined by t

(ar,br)=polyfit(t,xn,1)
xr=polyval([ar,br],t)
err=sqrt(sum((xr-xn)**2)/n) #the mean square error

print('a basic linear regression using polyfit')
print('parameters: a=%.2f b=%.2f \nregression: a=%.2f b=%.2f, ms error= %.3f' % (a,b,ar,br,err))

#matplotlib plotting commands
title('Linear Regression Example')
plot(t,x,'g.--') #original graph line
plot(t,xn,'k.') #random noise points
plot(t,xr,'r.-') #regression line derived from randomly placed points
legend(['original line','random noise','regression line'])

show() #show the actual plot output

print('parameters: a=%.2f b=%.2f \nregression: a=%.2f b=%.2f, std error= %.3f' % (a,b,a_s,b_s,stderr))
