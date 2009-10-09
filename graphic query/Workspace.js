var wsRef;

function Workspace(node){
	wsRef = this;
	
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
         
      if( this.current<2 ){ //max num of tables in ws
        //add node
        t = document.createElement('div');
        t.setAttribute("id","Table"+this.current);
        t.setAttribute("class","ofTable");
    
        this.myDiv.appendChild(t);
        this.tables[this.current] = new Table(tableName,t,this.current); 
        this.current++;
      }
    };
    
    this.clear_ws = function(){
      /* remove table divs from the dom */
      for(i=this.current-1;i>=0;i--){
        this.myDiv.removeChild(this.myDiv.childNodes[i]);
      }
      
      this.tables = new Array();
      this.current = 0;
    };
    
    this.check = function(id){
    	for(i=0;i<this.current;i++){
    		if(i==id) continue;
    		
    		tb = this.tables[i];
    		tbc = this.tables[id];
    		
    		//consts are table w on x and h on y
    		if(tb.myDiv.tableX <= tbc.myDiv.tableX+100 && 
    			tbc.myDiv.tableX <= tb.myDiv.tableX+100 &&
    			tb.myDiv.tableY <= tbc.myDiv.tableY+70 &&
    			tbc.myDiv.tableY <= tb.myDiv.tableY+70){
    			
    			tb.myDiv.overlap = tbc.myDiv.tableId;
    			tbc.myDiv.overlap = tb.myDiv.tableId;
    			
    			tb.myDiv.style.border="2px solid green";
    			tbc.myDiv.style.border="2px solid green";
    		} else{
    			tb.myDiv.overlap = -1;
    			tbc.myDiv.overlap = -1;
    			
    			tb.myDiv.style.border="";
    			tbc.myDiv.style.border="";
    			
    		}
    	}
    };
    
    /*Class will need to be registered...*/
    $("#"+this.myDiv.id).addClass("ofWorkspace");
}

function Table(tableName,node,id){
  
  this.myDiv = node;
  this.myDiv.tableId = id;
  
  this.myDiv.tableX = "";
  this.myDiv.tableY = "";
  
  /* add a paragraph of table name */
  t = document.createElement('p');
  this.myDiv.appendChild(t);
  
  u = document.createTextNode(this.myDiv.id+","+this.x+","+this.y);
  t.appendChild(u);
  
  
  /* Register me with draggable */
  $("#"+this.myDiv.id).draggable({ containment:'parent',
        drag:function(e,ui){        	        
        	tn = e.target;
        	tn.tableX = ui.offset.left;
        	tn.tableY = ui.offset.top;
        	tn.firstChild.firstChild.nodeValue = tn.id+","+tn.tableX+","+tn.tableY;
        	
        	wsRef.check(tn.tableId);
        },
        
        stop:function(e,ui){
          if( e.target.overlap>-1 ){
            stopped = document.getElementById("Table"+e.target.overlap);
            dragging = e.target;
            
            iff = ( stopped.tableX+200>256);//ws size 
            //alert( dragging.tableX+","+(dragging.tableX+200)+","+(dragging.tableX+200>256));
                           
            dragging.style.position = "absolute";
            dragging.style.left = iff?stopped.tableX-100:stopped.tableX+100;
            dragging.style.top = stopped.tableY;
              
            dragging.tableX = iff?stopped.tableX-100:stopped.tableX+100;
            dragging.tableY = stopped.tableY;                                                           
            
            dragging.firstChild.firstChild.nodeValue = dragging.id+","+dragging.tableX+","+dragging.tableY;
          }
        }
  });
 
    
  /* and add class... */
  $("#"+this.myDiv.id).addClass("ofTable");
  
  
}