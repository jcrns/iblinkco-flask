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