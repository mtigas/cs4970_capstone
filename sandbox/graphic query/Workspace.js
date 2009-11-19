function Workspace(divId){
  var window.wsRef;
  wsRef = this;
  
  /* Definitions */
  /* IE doesnt support const... */
  var MAX_TABLES = 5;
  
  var TAB_WIDTH = 100;
  var TAB_HEIGHT = 72;
  
  var WS_WIDTH = 20+MAX_TABLES*TAB_WIDTH;
  var WS_HEIGHT = 300+2*TAB_HEIGHT;

  /* Wo-mandeer this node */
  this.myDivNode = document.getElementById(divId); 
  //this.myDivNode.setAttribute('class','ofWorkspace');
 // $.('this.myDivNode').css('class','ofWorkspace');
  
  /* workspace members */
  this.current = 0; 
  this.joinSet = new Array();
  for(var i=0;i<MAX_TABLES;i++){
    this.joinSet[i]="";
  }
  this.E_joinSet = false;
  
  /* Add table method */
  this.addNewTable = function(name,location){
    if(this.current>=MAX_TABLES) return;
    
    //create table node, set attributes
    var t = document.createElement('div');
    t.setAttribute("id","Table"+this.current);
    //t.setAttribute("class","ofTable");
    
    
    t.style.position = "absolute";    
    t.style.top = location.top;
    t.style.left = location.left;
    
    //convenient storage in the node
    t.isJoined = false;
    t.overlaps = "";
    
    t.appendChild( document.createTextNode(name) );
    
    //add to the ws node
    this.myDivNode.appendChild(t);
    
    this.current++;
    
    //tables are draggable
    $("#"+t.id).draggable( {containment:'parent',
      drag:function(e,ui){
        wsRef.check(e.target.id);
      },
      
      start:function(e,ui){
        var index=wsRef.find(e.target.id);
        if(index>-1 && !(index+1>=MAX_TABLES || index-1<0) &&wsRef.areBothOccupied(e.target.id) )
          alert("Cant drag tables out of the middle of the join set! Drag tables off the ends.");
      },
      
      stop:function(e,ui){
        wsRef.reposition(e.target.id);
      } });
      
    //jQuery for class...(ie)
    $("#"+t.id).addClass("ofTable");
    
  };

  /* remove table divs from the dom */ 
  this.clear = function(){

    for(var i=this.current-1;i>=0;i--){
      this.myDivNode.removeChild(this.myDivNode.childNodes[i]);
    }

    this.current = 0;
    
    this.E_joinSet=false;
    for(i=0;i<this.joinSet.length;i++){
      this.joinSet[i]="";
    }
    for(i=0;i<this.myDivNode.childNodes.length;i++){
      this.myDivNode.childNodes[i].isJoined=false;
    }
  };
  
  /* Remove argument from joinset */
  this.removeFromJoinSet = function(removingId){
    this.joinSet[ this.find(removingId) ] = "";
  };
  
  this.find = function(tableId){
    
    for(var i=0;i<this.joinSet.length;i++){
      if(tableId === this.joinSet[i]){
        return i;
      } 
    }

    return -1;
  };
  
  this.joinOnRight = function(first,second){
    this.joinSet[ this.find(second)+1 ] = first;
  };
  
  this.joinOnLeft = function(first,second){
    this.joinSet[ this.find(second)-1 ] = first;
  };
  
  this.areBothOccupied = function(tableId){
      var index = this.find(tableId);
      if(index+1>MAX_TABLES || index-1<0) return true;   
    return this.joinSet[index+1]!=="" && this.joinSet[index-1]!==""; 
  };
  
  this.isRightOccupied = function(tableId){
    return this.joinSet[ this.find(tableId)+1 ]!="";
  };
  
  this.addInMiddle = function(tableId){
    this.joinSet[parseInt(MAX_TABLES/2)]=tableId;
  };
  
  this.countJoinSet = function(){
    var count=0;
    for(var i=0;i<this.joinSet.length;i++){
      if(this.joinSet[i]!="") count++;
    }
    
    return count;
  };
  
  this.showJoinCount=function(){
    var c=this.countJoinSet();
    alert(c);
  };
  
  this.showJoins = function(){
    for(var i=0;i<this.joinSet.length;i++){
      alert(i+" "+this.joinSet[i]);
    }
    for(var i=0;i<this.myDivNode.childNodes.length;i++){
      alert(i+" "+this.myDivNode.childNodes[i].isJoined);
    }
  };
  
  /* Check if argument overlaps any other child */
  this.check = function(draggingId){
    var dragging = document.getElementById(draggingId);
    
    if(dragging.isJoined){
      dragging.isJoined = false;
      this.removeFromJoinSet(draggingId);
      
      //is there one tab left?
      //alert(this.countJoinSet());
      if( this.countJoinSet()===1 ){
      //alert("left 1 tab in join set...");
        for(var i=0;i<this.joinSet.length;i++){
          this.joinSet[i]="";          
        }
       // alert(this.myDivNode.childNodes.length);
        for(var i=0;i<this.myDivNode.childNodes.length;i++){
          this.myDivNode.childNodes[i].isJoined=false;
          //alert("unsetting border "+i);
          this.myDivNode.childNodes[i].style.border="";
        }
        
        this.E_joinSet=false;
      }
    }
    for(var i=0;i<this.myDivNode.childNodes.length;i++){
      var sibling = this.myDivNode.childNodes[i];
      var siblingId = sibling.id;
      if(siblingId === draggingId) continue;
      
      var dt = parseInt(dragging.style.top);
      var dl = parseInt(dragging.style.left);
      var st = parseInt(sibling.style.top);
      var sl = parseInt(sibling.style.left);
      
      if(sl <= dl+TAB_WIDTH && 
    			dl <= sl+TAB_WIDTH &&
    			st <= dt+TAB_HEIGHT &&
    			dt <= st+TAB_HEIGHT){
        
        if(dragging.overlaps==""){
          if(!this.E_joinSet){
            dragging.overlaps = siblingId;
            
            dragging.style.border = "2px solid green";
            sibling.style.border = "2px solid green";
          } else{
            //sibling is in joinset then set overlap
            if( this.find(siblingId)>-1 && !this.areBothOccupied(siblingId) ){
              dragging.overlaps=siblingId;
              dragging.style.border="2px solid green";
            }
          }
        }

      } else{
        if(dragging.overlaps == siblingId){
          dragging.overlaps = "";
          dragging.style.border = "";
          
          if(!sibling.isJoined) sibling.style.border="";
        }
      }
      
      //this.E_joinSet &= !sibling.isJoined;
      
      
    }
    
  };
  
  /* Reposition the children tables */
  this.reposition = function(draggingId){
    if(dragging.overlaps == "") return;
    
    dragging = document.getElementById(draggingId);
    
    if(this.E_joinSet){
      if( !this.areBothOccupied(dragging.overlaps) ){
        if( this.isRightOccupied(dragging.overlaps) ){
          this.joinOnLeft(draggingId,dragging.overlaps);
        } else{
          this.joinOnRight(draggingId,dragging.overlaps);
        }
        dragging.isJoined=true;
      }
      
      
    } else{
      this.addInMiddle(dragging.overlaps);
      this.joinOnRight(draggingId,dragging.overlaps);
      
      this.E_joinSet = true;
      dragging.isJoined = true;
      document.getElementById(dragging.overlaps).isJoined = true;
    }
    
    /* Repositioning */


    for(var i=0;i<this.joinSet.length;i++){
    //alert(i+" "+this.joinSet[i]);
      if(this.joinSet[i]!=""){
        var n = document.getElementById(this.joinSet[i]);
        n.style.left = 10+TAB_WIDTH*i;
        n.style.top = (WS_HEIGHT-(2*TAB_HEIGHT))/3;
      }
    }
    
    for(var i=0;i<this.myDivNode.childNodes.length;i++){
      var n=this.myDivNode.childNodes[i];
      if(!n.isJoined){
     // alert(i+" "+this.myDivNode.childNodes[i].isJoined);
        n.style.left = i*(10+TAB_WIDTH);
        n.style.top = 2*((WS_HEIGHT-2*TAB_HEIGHT)/3)+TAB_HEIGHT;
      }
    }
    
    //unset moving variable
    dragging.overlaps="";
    
    /* seek the join columns... */
    /* seek the columns of the join set, django can join (?) */
    
  };
  
  /* Jquery */
  //add class. setting the class otherwise wont work in ie
  this.myDivNode.setAttribute("class","ofWorkspace");
  $("#"+this.myDivNode.id).addClass("ofWorkspace");
  
  //add as droppable 
  $("#"+this.myDivNode.id).droppable( {
    drop:function(e,ui){
    //alert(ui.draggable[0].iClass);
      if(ui.draggable[0].iClass == "TableItem")
        wsRef.addNewTable( ui.draggable[0].id,ui.offset );
    }
  });
}