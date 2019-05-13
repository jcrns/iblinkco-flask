// showing dashboard row by default
$("#admin").show();

// hiding analytics by default
$("#analytics").hide();
$("#accounts").hide();
$("#settings").hide();
 $("#stream").hide();

// Hidding and Showing Dashboard content onclick

$("#show-analytics").click(function(){
 $("#admin").hide();
 $("#analytics").show();
 $("#settings").hide();
 $("#accounts").hide();
 $("#stream").hide();
});

$("#show-accounts").click(function(){
  $("#admin").hide();
  $("#analytics").hide();
  $("#settings").hide();
  $("#accounts").show();
  $("#stream").hide();
});
$("#show-home").click(function(){
  $("#admin").show();
  $("#analytics").hide();
  $("#settings").hide();
  $("#accounts").hide();
  $("#stream").hide();

});

$("#show-settings").click(function(){
  $("#admin").hide();
  $("#analytics").hide();
  $("#accounts").hide();
  $("#settings").show();
  $("#stream").hide();
});

$("#show-stream").click(function(){
  $("#admin").hide();
  $("#analytics").hide();
  $("#accounts").hide();
  $("#settings").hide();
  $("#stream").show();
});