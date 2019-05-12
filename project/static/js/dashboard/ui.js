// showing dashboard row by default
$("#admin").show();

// hiding analytics by default
$("#analytics").hide();
$("#accounts").hide();
$("#settings").hide();

// Hidding and Showing Dashboard content onclick

$("#show-analytics").click(function(){
 $("#admin").hide();
 $("#analytics").show();
 $("#settings").hide();
 $("#accounts").hide();
});

$("#show-accounts").click(function(){
  $("#admin").hide();
  $("#analytics").hide();
  $("#settings").hide();
  $("#accounts").show();
});
$("#show-home").click(function(){
  $("#admin").show();
  $("#analytics").hide();
  $("#settings").hide();
  $("#accounts").hide();
});


$("#show-settings").click(function(){
  $("#admin").hide();
  $("#analytics").hide();
  $("#accounts").hide();
  $("#settings").show();
});