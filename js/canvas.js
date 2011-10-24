
var canvas;
var context;
var width = 450;
var height = 300;
var clickX = new Array();
var clickY = new Array();
var clickTool = new Array();
var clickDrag = new Array();
var paint;
var currentTool = "p"
var index = 1;
var scaleAmount = 0.4;

function drawCanvas(toId,drawing)
{
   clickX.length = 0
   clickY.length = 0
   clickTool.length = 0
   clickDrag.length = 0
   currentTool = "p"
   
   var canvasDiv = document.getElementById(toId);
   canvas = document.createElement('canvas');
   canvas.setAttribute('width', width);
   canvas.setAttribute('height', height);
   canvas.setAttribute('id', 'canvas_'+index);
   canvas.setAttribute('style', 'border:1px solid #111111');
   canvasDiv.appendChild(canvas);
   context = canvas.getContext("2d");
    if(typeof G_vmlCanvasManager != 'undefined') {
        canvas = G_vmlCanvasManager.initElement(canvas);
    }           
        
    if (drawing)
    {
        elements = drawing.split("|");
        for(var i=0; i < elements.length-1 ; i++)
        {		
            components = elements[i].split("_");
            clickX.push(parseInt(components[0]));
            clickY.push(parseInt(components[1]));
            clickTool.push(components[2]);
            clickDrag.push(parseBoolean(components[3]));
            
        } 
       
            redraw();
    
    }
    else 
    {
    }
  
    index ++;
}

function parseBoolean(str) {
  return /^true$/i.test(str);
}


function setCanvas(drawing)
{
    clickX.length = 0
    clickY.length = 0
    clickTool.length = 0
    clickDrag.length = 0
    currentTool = "p"
    
    var canvasDiv = document.getElementById('canvasWrapper');
    canvas = document.createElement('canvas');
    canvas.setAttribute('width', width);
    canvas.setAttribute('height', height);
    canvas.setAttribute('id', 'canvas');
    canvas.setAttribute('style', 'border:1px solid #111111');
    canvasDiv.appendChild(canvas);
    context = canvas.getContext("2d");
    if(typeof G_vmlCanvasManager != 'undefined') {
        canvas = G_vmlCanvasManager.initElement(canvas);
    }
           
    $('#canvas').mousedown(function(e){
      var mouseX = e.pageX - this.offsetLeft;
      var mouseY = e.pageY - this.offsetTop;
            
      paint = true;
      addClick(e.pageX - this.offsetLeft, e.pageY - this.offsetTop,false);
      redraw();
    });


    $('#canvas').mouseleave(function(e){    
      paint = false;
    });

    $('#canvas').mousemove(function(e){
      if(paint==true){
        addClick(e.pageX - this.offsetLeft, e.pageY - this.offsetTop, true);
        redraw();
      }
    });
    
    $('#canvas').mouseup(function(e){
      paint = false;
      redraw();
    });
    
    $('.eraser').click (function (){
            currentTool = "e"         
         });

      $('.pencil').click (function (){
        currentTool = "p"         
     });
     
     $('.show').click(function(){
   
        $('#drawing').val(getDrawingText())
     });
     
      $('.draw').click(function(){
          eraseAll();        
      
        elements =  $('#drawing').val().split("|");
        for(var i=0; i < elements.length-1 ; i++)
        {		
            components = elements[i].split("_");
            clickX.push(parseInt(components[0]));
            clickY.push(parseInt(components[1]));
            clickTool.push(components[2]);
            clickDrag.push(parseBoolean(components[3]));
            
        } 
        redraw();
     
     });
     
     
     if (drawing)
    {
        elements = drawing.split("|");
        for(var i=0; i < elements.length-1 ; i++)
        {		
            components = elements[i].split("_");
            clickX.push(parseInt(components[0]));
            clickY.push(parseInt(components[1]));
            clickTool.push(components[2]);
            clickDrag.push(parseBoolean(components[3]));
            
        } 
        redraw();
    
    }
}

function getDrawingText()
{
  var ret = "";
  for(var i=0; i < clickX.length; i++)
  {		
    ret += clickX[i]+"_"+clickY[i]+"_"+clickTool[i]+"_"+clickDrag[i]+"|";  
  }
  return ret;
}


function clearCanvas()
{
	context.fillStyle = '#ffffff'; 
	context.fillRect(0, 0, width, height); 
	canvas.width = canvas.width; 
}

function eraseAll()
{
clickX.length = 0;
clickY.length = 0;
clickTool.length = 0;
clickDrag.length = 0;

}




function addClick(x, y, dragging)
{
  clickX.push(x);
  clickY.push(y);
  clickTool.push(currentTool);
  clickDrag.push(dragging);
}



function redraw(){
  clearCanvas()
      
  for(var i=0; i < clickX.length; i++)
  {		
    context.beginPath();
    if(clickDrag[i] && i){
        
      context.moveTo(clickX[i-1], clickY[i-1]);
     }else{
       context.moveTo(clickX[i]-1, clickY[i]-1);
     }
     context.lineTo(clickX[i], clickY[i]);
     context.closePath();
     
     if(clickTool[i] == "e"){
			context.strokeStyle = 'white';
            context.lineWidth = 10; 
    }else{			
			context.strokeStyle = "#AD6C35";
            context.lineWidth = 5; 
    }
    
    context.lineJoin = "round";
    
    context.stroke();
  }
  context.restore();
}