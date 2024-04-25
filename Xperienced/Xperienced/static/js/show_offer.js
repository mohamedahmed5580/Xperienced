
function dspliayoffers() {
  var offerListItems = document.getElementById("offer-list-items");
  offerDataArray.forEach(function(offerData, index) {
      var listItem = document.createElement("div");
      listItem.innerHTML = `
      <div class="box">
        <p>
        ${offerData.title}
        </p>
        <div class="text">
        ${offerData.description}

        </div>
        <div class="Add">
          <div class="price">
          ${offerData.salary} EGP
          </div>
          <div class="btnAR">
          <a href="#" class="btn_add">Add an offer</a>
          <a href="#" class="btn_add" onclick="removeoffer(${index})">Remove offer</a>
          </div>

        </div>
      </div>  
      
         
      `;
      offerListItems.appendChild(listItem);
  });
}
function removeoffer(index) {
  offerDataArray.splice(index, 1);
  
  window.localStorage.setItem('offerDataArray', JSON.stringify(offerDataArray));
  window.location.reload();
}

dspliayoffers();  



