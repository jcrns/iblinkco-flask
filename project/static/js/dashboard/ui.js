// Ajac Functions
$(document).ready(function(){

  // Showing setup modal
  $('#setup-modal').modal('show');

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

  // Connecting website form
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

  // Submiting niche
  $('#niche-submit').on('submit', function(event){
    $.ajax({
      type : 'POST',
      url : '/post-niche',
      data : {
        niche_text : $('#niche-text').val(),
      },
      success: function (value) {
        if(value == "success"){
          location.reload();
        }
      }
    });
    event.preventDefault();
  });

  // Disconnecting website
  $('#disconnect-website').click(function() {
    $.ajax({
      type: 'POST',
      url : '/disconnect-website',
      success: function (value) {
        if(value == "success"){
          location.reload();
        }
      } 
    });
  });

  // Find competition refresh
  $('#find-competition-refresh').click(function() {
    $.ajax({
      type: 'POST',
      url : '/refresh-search',
      success: function (value) {
        if(value == "success"){
          location.reload();
        }
      } 
    });
  });
});
function refreshCompetition() {
    alert('aa')
    $.ajax({
    type: 'POST',
    url : '/refresh-search',
    success: function (value) {
      if(value == "success"){
        location.reload();
      }
    } 
  });
}
// Removing tip
function dismissTip(e){
  tipDiv = $(e).parent();
  $(tipDiv).fadeOut( "normal", function() {
    // Fade out complete
    $(e).parent().remove();
  });
  // numberOfTips = document.getElementsByClassName("tip-card").length;
  // element = document.getElementById('sidebar-status');
  // tipsNoneDifference = element.childNodes.length - numberOfTips
  // console.log('tips dif: ' + tipsNoneDifference)
  // console.log('element length: : ' + element.childNodes.length)
  // console.log('numberOfTips: : ' + numberOfTips)
  if(element.childNodes.length == 6){
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
