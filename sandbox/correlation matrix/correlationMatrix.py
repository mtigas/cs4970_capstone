# Matrix of Correlation algorithm prepared by Nick Roma (algorithm specification pseudo code in sandbox directory in repository)
# Python code based on algorthm written by Graham Greenfield

def getCorrelationMatrix(dataTable):
    dataTable # (from the dataset, get from external)
    n = dataTable[0].length # the number of samples
    
    # declare and initialize the correlation matrix

    corrMatrix[][] = new double[ dataTable.length ][ dataTable.length ];

    # initialize the correlation matrix ...
    # iterate thru the outer array of the dataTable

    for(int i=0;i<dataTable.length;i++){
        for(int s=i;s<dataTable.length;s++){
            if(s==i){
                corrMatrix[i][s] = 1.0;
                continue;
            } #if
            
            double sx = sum( dataTable[i] );
            double sy = sum( dataTable[s] );
            double sxy = sum( product(dataTable[i],dataTable[s]) );
            double sxx = sum( product(dataTable[i],dataTable[i]) );
            double syy = sum( product(dataTable[s],dataTable[s]) );
        
            corrMatrix[i][s] = (n*sxy - sx*sy) / Math.sqrt( (n*sxx - sx*sx)*(n*syy - sy*sy) );
        } # for
    } # for
    
    return corrMatrix;
} # getCorrelationMatrix
  
# correlation matrix uses these following functions...

# sum: takes an array (column of dataTable) and returns total sum
# theres probably a function in python to do the same
def sum(arrayArg) {
     double sum=0.0
     for(int i=0;i<arrayArg.length;i++) {
         sum+=arrayArg[i];
     } # for
    
     return sum
} # sum

# product: takes two arrays (columns), returns an array of corresponding products
# again, its probably a library function
def product(double arrayArg1[], double arrayArg2[]) {
     double rt[] = new double[ arrayArg1.length ]; #both array args should be same size
    
     for(int i=0;i<arrayArg1.length;i++) {
         rt[i] = arrayArg1[i]*arrayArg2[i];
     } # for
    
     return rt;
  
} # product
