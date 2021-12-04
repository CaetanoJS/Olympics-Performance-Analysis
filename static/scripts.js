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

$('#top_10_countries_with_economical_index').click(function(e){
  e.preventDefault();
  $.ajax({
        url: "/top10CountriesWithIndex",
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

$('#top_10_medalist_by_country').click(function(e){
  e.preventDefault();
  $.ajax({
        url: "/top10MedalistByCountry",
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


$('#top_10_best_countries').click(function(e){
  e.preventDefault();
  $.ajax({
        url: "/top10BestCountries",
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

$('#top_10_worst_countries_with_high_IDH_GDP').click(function(e){
  e.preventDefault();
  $.ajax({
        url: "/topCountriesLowSocialEconomicIndex",
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

$('#top_10_worst_countries_with_low_IDH_GDP').click(function(e){
  e.preventDefault();
  $.ajax({
        url: "/topCountriesHighSocialEconomicIndex",
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

$('#idh_gpd_performance_scatter_plot').click(function(e){
  e.preventDefault();
  $.ajax({
        url: "/idhGdpPerformance",
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