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
        url: "/countryMedals",
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

$('#competidor_medals').click(function(e){
  e.preventDefault();
  $.ajax({
        url: "/competidorMedals",
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

$('#top_10_countries').click(function(e){
  e.preventDefault();
  $.ajax({
        url: "/top_10_countries",
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