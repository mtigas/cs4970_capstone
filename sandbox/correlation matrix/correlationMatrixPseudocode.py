#
# Matrix of Correlation algorithm prepared by Nick Roma
#

#function getCorrelationMatrix(dataTable[][]){

# double dataTable[][]; #(from the dataset, get from external)
    
# int n = dataTable[0].length; #number of samples
    
## declare and initialize the correlation matrix

# double corrMatrix[][] = new double[ dataTable.length ][ dataTable.length ];
## initialize the correlation matrix ...
    
## iterate thru the outer array of the dataTable
# for(int i=0;i<dataTable.length;i++){
      
#      for(int s=i;s<dataTable.length;s++){
      
#        if(s==i){
#          corrMatrix[i][s] = 1.0;
#          continue;
#        }
        
#        double sx = sum( dataTable[i] );
#        double sy = sum( dataTable[s] );
#        double sxy = sum( product(dataTable[i],dataTable[s]) );
#        double sxx = sum( product(dataTable[i],dataTable[i]) );
#        double syy = sum( product(dataTable[s],dataTable[s]) );
        
#        corrMatrix[i][s] = (n*sxy - sx*sy) / Math.sqrt( (n*sxx - sx*sx)*(n*syy - sy*sy) );
      
#      }
      
# }
    
# return corrMatrix;
#}
  
#
## correlation matrix uses these functions
#

#
## sum: takes an array (column of dataTable) and returns total sum
## theres probably a function in python to do the same
#function sum(double arrayArg[]){
  
#    double sum=0.0;
#    for(int i=0;i<arrayArg.length;i++){
#      sum+=arrayArg[i];
#    }
    
#    return sum;
#}

#
## product: takes two arrays (columns), returns an array of corresponding products
## again, its probably a library function
#function product(double arrayArg1[], double arrayArg2[]){
  
#    double rt[] = new double[ arrayArg1.length ]; #both array args should be same size
    
#    for(int i=0;i<arrayArg1.length;i++){
#      rt[i] = arrayArg1[i]*arrayArg2[i];
#    }
    
#    return rt;
  
#}