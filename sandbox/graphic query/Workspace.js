function Workspace(divId){

  
  window.wsRef = this;
  
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
    //alert(location.top+","+location.left); 
    t.style.top = parseInt(location.top)+"px";
    t.style.left = parseInt(location.left)+"px";
    
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
        window.wsRef.check(e.target.id);
      },
      
      start:function(e,ui){
        var index=window.wsRef.find(e.target.id);
        if(index>-1 && !(index+1>=MAX_TABLES || index-1<0) &&window.wsRef.areBothOccupied(e.target.id) )
          alert("Cant drag tables out of the middle of the join set! Drag tables off the ends.");
      },
      
      stop:function(e,ui){
        window.wsRef.reposition(e.target.id);
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
      //alert(dt);
      
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
 // alert("Repostion");//debug
  //this.showJoins();//debug
    var dragging = document.getElementById(draggingId);

    if(dragging.overlaps == "") return;
    
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
      //this.showJoins();//debug
    }
    
    /* Repositioning */


    for(var i=0;i<this.joinSet.length;i++){
    //alert(i+" "+this.joinSet[i]);
      if(this.joinSet[i]!=""){
        var n = document.getElementById(this.joinSet[i]);
       // alert(this.joinSet[i]+": "+n.style.left+","+n.style.top);
        n.style.left = parseInt(10+TAB_WIDTH*i)+"px";
        n.style.top = parseInt((WS_HEIGHT-(2*TAB_HEIGHT))/3)+"px";
        //n.style.left+="px";
        //n.style.top+="px";
       // alert(this.joinSet[i]+": "+n.style.left+","+n.style.top);
      }
    }
    
    for(var i=0;i<this.myDivNode.childNodes.length;i++){
      var n=this.myDivNode.childNodes[i];
      if(!n.isJoined){
     // alert(i+" "+this.myDivNode.childNodes[i].isJoined);
     //alert(n.id+": "+n.style.left+","+n.style.top);
        n.style.left = parseInt(i*(10+TAB_WIDTH))+"px";
        n.style.top = parseInt(2*((WS_HEIGHT-2*TAB_HEIGHT)/3)+TAB_HEIGHT)+"px";
        //alert(n.id+": "+n.style.left+","+n.style.top);
        //n.style.left+="px";
        //n.style.top+="px";
      }
    }
    
    //unset moving variable
    dragging.overlaps="";
    
    /* seek the join columns... */
    /* seek the columns of the join set, django can join (?) */
    
  };
  
  /* Jquery */
  //add class. setting the class otherwise wont work in ie
 // this.myDivNode.setAttribute("class","ofWorkspace");
  $("#"+this.myDivNode.id).addClass("ofWorkspace");
  
  //add as droppable 
  $("#"+this.myDivNode.id).droppable( {
    drop:function(e,ui){
    //alert(ui.draggable[0].iClass);
      if(ui.draggable[0].iClass == "TableItem")
        window.wsRef.addNewTable( ui.draggable[0].id,ui.offset );
    }
  });
}

/* functions for selection */
function  addSelector(containerId){
//alert("hey13")c;
//alert("addSelector running "+window.scount);
SELECTION_MAX=5;
  if(window.scount>=SELECTION_MAX){
  
    return;
  }
  //alert("hey17");
  //create a div for this selector
  newSelectionDiv = document.createElement('div');
  newSelectionDiv.id = "selector"+window.scount;
  //alert("hey21");
  
  //create the buttons
  innerHt = "<input id=\"del"+window.scount+"\" type=\"button\" value=\"Del\" onclick=\"delSelector('selector"+window.scount+"');\"/>";
  innerHt += "<input id=\"addButton\" type=\"button\" value=\"Add\" onclick=\"addSelector('selections');\"/>";
  //alert("hey26");
  //add the option box
  innerHt+= addOptionToSelector("column"+window.scount,tables);
  
  //add the ops box
  innerHt+= "<select id=\"op"+window.scount+"\"><option>></option><option><</option><option>=</option><option>>=</option><option><=</option></select>";
  //alert("hey32");
  //add textfield
  innerHt+="<input id=\"val"+window.scount+"\" />";
  
  newSelectionDiv.innerHTML=innerHt;
  document.getElementById(containerId).appendChild(newSelectionDiv);
  //alert("hey38");
  window.scount++;
  //alert("created a selector");
}

function addOptionToSelector(id,options){
  //alert("hey44");
  var test="";
  test+="<select id=\""+id+"\" width=\"99\">";
  //alert("hey46");
  for(i=0;i<options.length;i++){
    for(s=0;s<options[i].length;s++){
    test+="<option value='"+aliass[i]+"."+options[i][s]+"'>"+aliass[i]+"."+options[i][s]+"</option>";
    //alert("hey");
    }
  }
  test+="</select>";
  return test;
}

function delSelector(selectId){
  if(window.scount-1==0){
    return;
  }
  
  document.getElementById("selections").removeChild( document.getElementById(selectId) ); //uh, yeah..
  window.scount--;
}

/* Tablestore */
function TableStore(node){

    //control my node
    node.setAttribute("id","TableStore");
   // node.setAttribute("class","ofTableStore"); 

    this.myDiv = node;
    
    /* get table names from ... */
    this.tableNames = ["nation","state","county","socialcharacteristics","crimedata","placepopulation"];
    
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
          e.target.style.top=0+"px";
          e.target.style.left=0+"Px";          
        }
      });
       $("#"+ti.id).addClass("OfTableItem");
    }
    
    
    
    $("#"+this.myDiv.id).addClass("ofTableStore");
    /* tablestore needs to know where its associated ws is ??*/
    
    /* access items with tab store node children */
    
}

/* for projection */
function scream(){
//alert("scream");

  var GET_STRING="";
  var URL = "http://nationbrowse.com/querybuilder/get_columns/";
  //create a get

  //gets the table names from the join set, puts into comma sepd string
  //post to server , get back col names
  for(i=0;i<window.wsRef.joinSet.length;i++){
    j = document.getElementById(window.wsRef.joinSet[i]);
    if(j){
      GET_STRING += j.innerHTML+",";
    }
  }
  window.fTables=GET_STRING;
  //window.tables=GET_STRING;
  GET_STRING += ".js"; 
  //alert(URL+GET_STRING);
  /*
    sailor=["sname","sid","rating","age","one","two","three","four"];
  reserves=["bid","sid"];
  boat=["bid","color","bname"];
   tables=new Array();

  tables[0]=sailor;
  tables[1]=boat;
  tables[2]=boat;
  tables[3]=reserves;
  
  tNames=new Array();
  tNames[0] ="Sailor";
  tNames[1] = "Boat";
  tNames[2]="Boat";
  tNames[3]="Reserves"; 
  tNames[4]="Boat";
  tNames[5]="Pigeon";
  tNames[6]="Reserves";
  tNames[7]="Poopy"; */
  
  //alert(URL+GET_STRING);
  //use ajax to submit
  /*
  var http = false;

if(navigator.appName == "Microsoft Internet Explorer") {
  http = new ActiveXObject("Microsoft.XMLHTTP");
} else {
  http = new XMLHttpRequest();
}

http.open("GET", URL+GET_STRING);
http.onreadystatechange=function() {
  if(http.readyState == 4) {
  alert("returned");
    alert(http.responseText);
     //tables=data.columns;

    //tNames=data.tables;
    
    //examine for duplicates 
    handle_duplicates();
    go();
    
  }
}
http.send(null);*/
  jQuery.ajax({
      type:"GET",
      url:URL+GET_STRING,
      dataType:"jsonp",
      success: function(data, status) {
          //alert(data);
          
            if(data==null){
              document.getElementById("chus").innerHTML="Could not load columns..";
              return;
            }
            tables=data.columns;
 
            tNames=data.tables;
            window.ftables=data.tables;
    
            //examine for duplicates
            handle_duplicates();
      		window.scount=0;
            go();
      },
      error: function (XMLHttpRequest, textStatus, errorThrown) {
          document.getElementById("chus").innerHTML="Could not load columns..";
    }
  });
 /* $.getJSON(URL+GET_STRING,function(data){
  alert("returned");//debug
    if(data==null){
      document.getElementById("chus").innerHTML="Could not load columns..";
      return;
    }
    tables=data.columns;

    tNames=data.tables;
    
    //examine for duplicates 
    handle_duplicates();
    go();
    
  }); */
  
}
  function go(){
  //document.getElementById("test").innerHTML=aliass[1];
    n=document.getElementById("chus");
    var test="";
    var blockNum=0;
    for(table=0;table<tables.length;table++){
    test+="<h3>"+aliass[table]+"</h3>";
      test+="<table>";
      for(i=0;i<parseInt(tables[table].length/layout);i++){
        test+="<tr>";
          for(s=0;s<layout;s++){
          //alert(aliass[tables]);
            test+="<td><input type='checkbox' value='"+aliass[table]+"."+tables[table][blockNum*layout+s]+"'/></td><td>"+tables[table][blockNum*layout+s]+"</td>";
          }
          test+="</tr>";
          blockNum++;
      }
      
      test+="<tr>";
      
      for(i=0;i<(tables[table].length%layout);i++){
      
        test+="<td><input type='checkbox' value='"+aliass[table]+"."+tables[table][blockNum*layout+i]+"'/></td><td>"+tables[table][blockNum*layout+i]+"</td>";
      }
      test+="</tr></table><hr/>"
      blockNum=0;
    }
     n.innerHTML=test;
  }

  function handle_duplicates(){
  
    //if joinsets contained ids whose node has the same name, create alias appropriately
    counts = new Array(); 
    var test="";
    for(i=0;i<tNames.length;i++){
     // alert(tNames[i]);
      
      counts[tNames[i]]=1;
     // alert(count[tNames[i]]);
    }
    
    aliass[0]=tNames[0];
    counts[tNames[0]]=1;
   
    for(i=1;i<tNames.length;i++){
     
      test=tNames[i];
     
      for(s=i-1;s>=0;s--){
        if(test==tNames[s]){
          //theres another duplicate for this tName
          counts[test]++;
          
          aliass[i]=test+counts[test];
          break;
        }
        if(!s){
          aliass[i] = test;
        }
        
      }
    }
     
    //document.getElementById("test").innerHTML = aliass+"<hr/>";
    
  }

  function finish_project(){
    //publish the projection info
    inputs=document.getElementsByTagName("input");
    count=0;
    projections = new Array();
    
    for(i=0;i<inputs.length;i++){
      
      if(inputs[i].checked){
       // alert(inputs[i].type);
        
        projections[count++]=inputs[i].value;
      }
    }
    
    //if no cols selected, project all cols (or only the pks)
    if(!count){
      for(i=0;i<inputs.length;i++){
      if(inputs[i].type=="checkbox"){
        projections[count++]=inputs[i].value;
      }
      }
    }
      // document.getElementById("test").innerHTML = projections; 
    //select next tab
    TAB_SELECT_OK=true;
    $tabs.tabs('select',2);
    TAB_SELECT_OK=false;
    addSelector('selections');//debug
  }
 
 function publishSelections(){
 //alert(document.getElementById("op0").value);
 SELECTION_MAX=5;//debug
   TAB_SELECT_OK=true;
    $tabs.tabs('select',3);
    TAB_SELECT_OK=false;
    
    window.columns="";
    for(var i=0;i<projections.length;i++){
      window.columns+=projections[i]+",";
    }
    
    
    var URL = "http://nationbrowse.com/querybuilder/get_results/";
    
    

    window.selections = "";
    for(var i=0;i<=SELECTION_MAX;i++){
    
      n=document.getElementById("column"+i);
      m=document.getElementById("op"+i);
      o=document.getElementById("val"+i);
      
      if(n!=null && m!=null & o!=null){
      
        if(o.value!='')
          window.selections+= n.value+"|"+verb(m.value)+"|"+o.value+",";
      }
      
    }
    
     t=document.getElementById("results");
    
    GET_STRING="tables=";
    GET_STRING+=window.fTables;
    
    GET_STRING+="&"+"columns=";
    GET_STRING+=window.columns;
    
    GET_STRING+="&"+"filters=";
    GET_STRING+=window.selections;
    alert(URL+"?"+GET_STRING);
    jQuery.ajax({
      type:"GET",
      url:URL,
      data:GET_STRING,
      dataType:"text",
      success: function(data, status) {
      	alert(data);
      	alert(status);
            if(data==null){
              document.getElementById("results").innerHTML="Could not load columns..";
              return;
            }
            document.getElementById("results").innerHTML=data;
    
            
      },
      error: function (XMLHttpRequest, textStatus, errorThrown) {
          document.getElementById("results").innerHTML="Could not load columns..";
    }
  });
  /*
   var http = false;

if(navigator.appName == "Microsoft Internet Explorer") {
  http = new ActiveXObject("Microsoft.XMLHTTP");
} else {
  http = new XMLHttpRequest();
}

http.open("GET", URL+"?"+GET_STRING);
http.onreadystatechange=function() {
  if(http.readyState == 4) {
  alert("returned");
    alert(http.responseText);
   
       
  }
*/
  
 }
 
 function verb(t){
 switch(t){
 
  case ">":
    return "gt";
    break;
  case "<":
    return "lt";
    break;
  case "=":
    return "e";
    break;
   case ">=":
   return "gte";
   break;
   case "<=":
   return "lte";
   break;
   default:
   return t;
   
  
  }
  
 }