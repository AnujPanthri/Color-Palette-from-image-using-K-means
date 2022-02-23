document.querySelector('.numofcolors').setAttribute("size", document.querySelector('.numofcolors').value.length );
var base64='';
var numofcolors=document.querySelector('.numofcolors').value;


const img_boxes=document.getElementsByClassName('image-box');

for(let i = 0; i < img_boxes.length; i++) {
    (function(index) {
        img_boxes[index].addEventListener("click", function() {
        change_image(img_boxes[index]);
       })
    })(i);
  }

function change_image(imgbtn)
{
  const img=imgbtn.querySelector('.img');
  
  var image=document.querySelector(".image");
  image.src=img.src
  console.log("Send this to Python:"+image.src);

  // base64=src_to_base64(image.src)
  
  to_base64(image.src);
}


function to_base64(src)
{
  let img = new Image()
    img.src = src

    img.onload = () => {
      let canvas = document.createElement('canvas');
      // canvas.setAttribute('type','image/jpeg')
      canvas.height = img.height
      canvas.width = img.width
      // canvas.height = this.naturalheight;
      // canvas.width = this.naturalwidth;
      let ctx = canvas.getContext('2d');
      
      ctx.fillStyle = "white";
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      ctx.drawImage(img, 0, 0);
    
      // var encoded=canvas.toDataURL()
      var encoded=canvas.toDataURL('image/jpeg');
      
      // console.log("img height , width: ",img.height,img.width);
      // console.log("canvas height , width: ",canvas.height,canvas.width);
      
      send_image(encoded);
    }
}

function send_image(src)
{
  base64=src;
  if (numofcolors>20)
      {
          alert("Warning to many number of colors are requested");
      }
      else{
  $.ajax({
    type: "POST",
    url: "/test",   // the data processing route 
    contentType: "application/json",
    data: JSON.stringify({image: src , numofcolors: numofcolors}),
    dataType: "json",

    success: function(response) {
        // console.log('success:',response);
        
        //run callback function
        set_color_pallete(response)
        
    },
    error: function(err) {
        console.log('err:',err);
        alert("error")
    }
});
      }

}

function set_color_pallete(data)
{
  var pallete=document.querySelector('.color-pallete');
  pallete.innerHTML = '';

  var best=0;
  var dom_color;
  for(let color in data)
  {
    support=data[color];
    var div=document.createElement("div");
    div.setAttribute('class','colors');
    div.setAttribute('style',`background-color:${color}`);
    div.innerHTML=support
    pallete.appendChild(div);
    if (support>best)
    {
      best=support;
      dom_color=color;
    }
  }
  document.body.style.background =dom_color
  color_handler()

}





const addimage=document.querySelector('.add_image');

addimage.addEventListener("change", function() {
        encodeImageFileAsURL();

});

function encodeImageFileAsURL() {

var filesSelected = document.getElementById("file-input").files;
if (filesSelected.length > 0) {
  var fileToLoad = filesSelected[0];
  var fileReader = new FileReader();
  fileReader.onload = function(fileLoadedEvent) {
  var srcData = fileLoadedEvent.target.result; // <--- data: base64
    
  var image=document.querySelector(".image");
  image.src=srcData;
  //send data now 
    send_image(srcData);
  }
  fileReader.readAsDataURL(fileToLoad);
}
}


function color_handler()
{
  const colors=document.getElementsByClassName('colors');

for(let i = 0; i < colors.length; i++) {
    (function(index) {
      colors[index].addEventListener("click", function() {
        // console.log(colors[i].style.backgroun dColor);
          document.body.style.background =colors[i].style.backgroundColor;
       })
    })(i);
  }
}



(document.querySelector('.numofcolors')).addEventListener('keyup', function () {
  // console.log("hi",this.value);
  this.setAttribute("size", this.value.length );
  if (document.querySelector('.image').src=='')
  {
    console.log("no image selected");
    // console.log(base64);
  }
  else if(document.querySelector('.numofcolors').value!=numofcolors)
  {
    numofcolors=document.querySelector('.numofcolors').value;
    if (! isNaN(numofcolors) && numofcolors>0)
    {
      if (numofcolors>20)
      {
          alert("Warning to many number of colors are requested");
      }
      else{
        console.log('image is there');
        console.log('numofcolors:',numofcolors);
        // console.log(base64);
        send_image(base64)
      }
      
    }

  }
});