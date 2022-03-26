// Get the modal
var modal = document.getElementById("myModal");

// Get the button that opens the modal
var btn = document.getElementById("myBtn");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks on the button, open the modal
btn.onclick = function() {
  modal.style.display = "block";
}

 //  When the user clicks on the button, open the modal -->
btn.onclick = function() {
  modal.style.display = "block";
}

//  When the user clicks on <span> (x), close the modal -->
span.onclick = function() {
  modal.style.display = "none";
}


  $(document).ready(function(){
        $("#upload-btn").click(function(){
            $("#myModal").show();
        });
    });
  
    $(document).ready(function(){
       
        
        $("#exit").click(function(){
            $(".myModal").exit();
            $("#embed1").exit();
        });
        
         $(".done").click(function(){
            $("#intro").hide();
            $("#embed1").show();
        });
         $("#browse-upload").click(function(){
            $("#intro").hide();
            $("#orig").hide();
            $("#orig-uploaded").show();
        });
    });


//  When the user clicks anywhere outside of the modal, close it-->
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}

var loadFile = function(event) {
      var image = document.getElementById("output");
      image.src = URL.createObjectURL(event.target.files[0]);
  
 }; 
 

var modal = document.getElementById("modal-IRS");
var upload = document.getElementById("upload-btn");
var span = document.getElementsByClassName("close")[0];
var out = document.getElementsByClassName("cancel");


btn.onclick = function() {
  modal.style.display = "block"; 

}

span.onclick = function() {
  modal.style.display = "none";  
}
upload.onclick = function() {
  modal.style.display = "block";  
}
 
//   When the user clicks anywhere outside of the modal, close it -->
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
  
}

const upload = document.getElementById('upload-btn')
const modal = document.getElementById('myModal')
const close = document.getElementById('close')

upload.addEventListener('click', () => {
  modal.classList.add('show')
})

close.addEventListener('click', () => {
  modal_container.classList.remove('show')
})