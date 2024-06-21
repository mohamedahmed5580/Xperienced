var btn = document.querySelector('.toggle');
var btnst = true;
btn.onclick = function() {
    if(btnst == true) {
        document.querySelector('.toggle span').classList.add('toggle');
        document.getElementById('sidebar').classList.add('sidebarshow');
        btnst = false;
    }else if(btnst == false) {
        document.querySelector('.toggle span').classList.remove('toggle');
        document.getElementById('sidebar').classList.remove('sidebarshow');
        btnst = true;
    }
}

function autoType(elementClass, typingSpeed){
    var element = $(elementClass);
    element.css({
      "position": "relative",
      "display": "inline-block"
    });
    element.prepend('<div class="cursor" style="right: initial; left:0;"></div>');
    element = element.find(".text");
    var text = element.text().trim().split('');
    var amntOfChars = text.length;
    var newString = "";
    element.text("|");
    setTimeout(function(){
      element.css("opacity",1);
      element.prev().removeAttr("style");
      element.text("");
      for(var i = 0; i < amntOfChars; i++){
        (function(i,char){
          setTimeout(function() {        
            newString += char;
            element.text(newString);
          },i*typingSpeed);
        })(i+1,text[i]);
      }
    },1000);
  }
  
  $(document).ready(function(){
    autoType(".type",100);
  });

//   $(document).ready(function() {
//     window.onload=()=>{
//         setTimeout(function() {
//             const loadingScreen = document.getElementById('loading');
//             const mainContent = document.getElementById('main-content');
//             loadingScreen.style.display = 'none';
//             mainContent.style.display = 'block';
//         }, 200); 
//     }
// });