$('.ui.search.dropdown').search({
    type          : 'category',
    minCharacters : 3,
    apiSettings   : {
      url        : '/search_queries?query={query}',
      onResponse : function(res) {
        var
          response = {
            results : {}
          }
        ;
        if(!res || !res.result) {
          return;
        }
        $.each(res.result, function(index, item) {
          $.each(item,function(key,value){
              var campus   = value[1] || 'lol',maxResults = 10;
              if(index >= maxResults) {
                return false;
              }
              // create new campus category
              if(response.results[campus] === undefined) {
                response.results[campus] = {
                  name    : campus,
                  results : []
                };
              }
              // add result to category
              response.results[campus].results.push({
                title       : key,
                description : value[0]
              });
          });
        });
        return response;
      }
    }
});
