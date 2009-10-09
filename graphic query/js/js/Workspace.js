function Workspace(node){
    //add node
    n = document.createElement('div');
    n.setAttribute("id","Workspace");
    n.setAttribute("class","ofWorkspace");
    
    node.appendChild(n);
    this.myDiv = n;
    
    //setup tables for ws
    this.tables = new Array();
    
    //points to next add table location
    this.current = 0;
    
    //adding table
    this.addNewTable = function(tableName){
         
      if( this.current<5 ){ //max num of tables in ws
        //add node
        t = document.createElement('div');
        t.setAttribute("id","Table"+this.current);
        t.setAttribute("class","ofTable");
    
        this.myDiv.appendChild(t);
        this.tables[this.current++] = new Table(tableName,t); 
        
          
      }
    };
    
    this.clear = function(){
      /* remove table divs from the dom */
      alert("clearing");
      for(i=0;i<current-1;i++){
        this.myDiv.removeChild(this.myDiv.childNodes[i]);
      }
      
      this.tables = new Array();
      this.current = 0;
    };
    
    /*Class will need to be registered...*/
    $("#"+this.myDiv.id).addClass("ofWorkspace");
}

function Table(tableName,node){
  this.x = null;
  this.y = null;
  
  this.myDiv = node;
  
  /* the table's name also provides an id for the associated div */
  this.id = tableName;
  
  /* add a paragraph of table name */
  t = document.createElement('p');
  this.myDiv.appendChild(t);
  
  u = document.createTextNode(tableName);
  t.appendChild(u);
  
  
  /* Register me with draggable */
  $("#"+this.myDiv.id).draggable({ containment:'parent'
        
        //add attrs here...
        });
 
    
  /* and add class... */
  $("#"+this.myDiv.id).addClass("ofTable");
  
  
}