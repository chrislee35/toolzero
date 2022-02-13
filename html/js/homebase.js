$.getScript("js/render_form.js", function () {console.log('loaded render_form');});
$.getScript("js/result_widget.js", function () {console.log('loaded result_widget');});
$.getScript("js/eventsource2.js", function () {console.log('loaded eventsource2');})
$.getScript("js/open_app.js", function () {console.log('loaded open_app');})
$.getScript("js/callbacks.js", function () {console.log('loaded callbacks');})
$.getScript("js/utils.js", function () {console.log('loaded utils');})

$.getJSON( "listapps", function(data) {
  console.log(data);
  $.each(data['appslist'], function(i, app) {
    var li = document.createElement('li');
    var a = document.createElement('a');
    a.href = '#';
    if(app['type'] == 'py') {
      a.onclick = function() { open_app(app['path']) };
    } else if (app['type'] == 'js') {
      a.onclick = function() { open_jsapp(app['path']) };
    } else if (app['type'] == 'jspy') {
      a.onclick = function() { open_jspyapp(app['path']) };
    }
    a.innerText = app['name'];
    a.title = app['desc'];
    li.append(a);
    $('#app_list').append(li);
  });
});

$("#app_tabs").tabs()
