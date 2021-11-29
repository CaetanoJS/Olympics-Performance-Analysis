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

$('#graph_by_country').click(function(e){
  e.preventDefault();
  $.ajax({
        url: "/graphByCountry",
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