$("#search_form_input").keyup(function(){
    var text = $(this).val();

    $.ajax({
      url: "/graphs",
      type: "get",
      data: {jsdata: text},
      success: function(response) {
        $("#place_for_suggestions").html(response);
      },
      error: function(xhr) {
        //Do Something to handle error
      }
    });
});

$('#my_link').click(function(e){
    e.preventDefault();
    $.ajax({
         url: "/mixedGraphs",
         type: "get",//type of posting the data
         data: "",
         success: function(response) {
          $("#place_for_suggestions").html(response);
        },
         error: function(xhr, ajaxOptions, thrownError){
            //what to do in error
         },
    });
  
  });