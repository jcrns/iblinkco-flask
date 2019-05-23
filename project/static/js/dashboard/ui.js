// Ajac Functions
$(document).ready(function(){
  $('#myModal').modal('show');
  // Setup Form
  $('#setup-connect-form').on('submit', function(event){
    $.ajax({
      type : 'POST',
      url : '/setup-update',
      data : {
        website_name : $('#website-name').val(),
        website_url : $('#website-url').val()
      },
      success: function (value) {
        // var evalue = JSON.parse(value);
        $('#setup-form-message').html(value)
        if(value == "success"){
          location.reload();
        }
      }
    });
    event.preventDefault();
  });


});
function dismissTip(e){
    $(e).parent().remove();
  element = document.getElementById('sidebar-status');

// alert(element.childNodes.length);

if(element.childNodes.length == 5){
    // div = document.getElementById('sidebar-status');
        var noneDiv = document.createElement('p');
        var noneText = document.createTextNode('No Tips');
        noneDiv.appendChild(noneText);
        element.appendChild(noneDiv);
} 

}
function tipsExist(){
  element = document.getElementById('sidebar-status');

}
tipsExist();
