// Ajac Functions
$(document).ready(function(){
  $('#myModal').modal('show');
  // Setup Form
  $('#setup-connect-form').on('submit', function(event){
    $.ajax({
      type : 'POST',
      url : '/setup-update',
      data : {
        website_name : $('#website-name-setup').val(),
        website_url : $('#website-url-setup').val()
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
  $('#connect-website-form').on('submit', function(event){
    $.ajax({
      type : 'POST',
      url : '/connect-website',
      data : {
        website_name : $('#website-name').val(),
        website_url : $('#website-url').val()
      },
      success: function (value) {
        // var evalue = JSON.parse(value);
        if(value == "success"){
          location.reload();
        } else if (value == 'failed') {
          $('#connect-website-form-message').html(value)
        }
      }
    });
    event.preventDefault();
  });
});
function dismissTip(e){
  tipDiv = $(e).parent()
  $(tipDiv).fadeOut( "normal", function() {
    // Fade out complete
  });
  // $(e).parent().remove();
  // element = document.getElementById('sidebar-status');

  // alert(element.childNodes.length);

  if(element.childNodes.length == 4){
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
