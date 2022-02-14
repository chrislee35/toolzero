$.getScript("js/render_form.js", function () {console.log('loaded render_form');});
$.getScript("js/result_widget.js", function () {console.log('loaded result_widget');});
$.getScript("js/eventsource2.js", function () {console.log('loaded eventsource2');})
$.getScript("js/open_app.js", function () {console.log('loaded open_app');})
$.getScript("js/callbacks.js", function () {console.log('loaded callbacks');})
$.getScript("js/utils.js", function () {console.log('loaded utils');})

// on load, list all the apps by querying the
// server for the list of apps
$.getJSON( "listapps", function(data) {
  $.each(data['appslist'], function(i, app) {
    var li = render_app_launcher(app)
    $('#app_list').append(li);
  });
});

// render the app launcher
function render_app_launcher(app) {
  var li = $('<li />');
  var a = $('<a />', {
    href: '#',
    title: app['title'],
    click: function() { open_app(app['type'], app['path']); }
  });
  a.text(app['name']);
  li.append(a);
  return(li);
}

$("#app_tabs").tabs()
