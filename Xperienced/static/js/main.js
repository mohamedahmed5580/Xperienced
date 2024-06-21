
if(!localStorage.getItem("done")){
     window.onload=()=>{
          setTimeout(()=>{
               
               document.querySelector(".loading").style=`display:none;`;
               localStorage.setItem("done",1);
          },100)
     }
}else{
     document.querySelector(".loading").style=`display:none;`;

}
