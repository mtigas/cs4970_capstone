function TableStore(node){

    //control my node
    node.setAttribute("id","TableStore");
    node.setAttribute("class","ofTableStore"); 

    this.myDiv = node;
    
    /* get table names from ... */
    this.tableNames = ["state","county","datasource","placepopulation"];
    
    for( var i=0;i<this.tableNames.length;i++){
     
     /* adding a node to my div adds a table item to the table store */     
     this.myDiv.appendChild( ti = document.createElement('div') );
     
     ti.id = this.tableNames[i];
      
     /* Set the class oftableitem to this table item (for ie) */
     ti.setAttribute("class","ofTableItem");
    
     ti.iClass = "TableItem"; //ws examines iclass to know what was dropped on it (ti or table)
     ti.appendChild( document.createTextNode( ti.id ) ); //set the text of this table item from tablenames[]
     
     //set style tops and lefts. set absolute postioning to lay the tabs out correctly****************
      
     /* register this table item as draggable */
     $("#"+ti.id).draggable({
        stop:function(e,ui){
                  
          //will have to move div back to tablestore so it can be dragged again
          e.target.style.top=0;
          e.target.style.left=0;          
        }
      });
       $("#"+ti.id).addClass("OfTableItem");
    }
    
    
    
    $("#"+this.myDiv.id).addClass("OfTableStore");
    /* tablestore needs to know where its associated ws is ??*/
    
    /* access items with tab store node children */
    
}