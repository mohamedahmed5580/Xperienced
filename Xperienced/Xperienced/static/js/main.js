
if(!localStorage.getItem("done")){
     window.onload=()=>{
          setTimeout(()=>{
               document.querySelector(".loading ").style=`display:none;`
               document.querySelector(".loader").style=`display:none;`
               localStorage.setItem("done",1)
          },1500)
     }
}else{
     document.querySelector(".loading ").style=`display:none;`
     document.querySelector(".loader").style=`display:none;`

}
