function open_app(app_name) {
  $.getJSON( "apps/"+app_name, function(data) {
    var app_id = data['app_id'];
    var fields = data['fields'];
    var name = data['name']
    var result_type = data['result_type'];
    open_app_tab(app_id, name, fields, result_type);
  });
}

function open_jsapp(app_name) {
  $.getJSON( "jsapps/"+app_name, function(data) {
    var app_id = data['app_id'];
    var page = data['page'];
    var name = data['name'];
    var li = document.createElement('li');
    var h = document.createElement('a');
    h.setAttribute('href', '#app_'+app_id);
    h.innerHTML = name;
    li.append(h);
    $("#apps_list").append(li);
    $("#app_tabs").append(page);
    $("#app_tabs").tabs("refresh");
  });
}

function open_jspyapp(app_name) {
  $.getJSON( "jspyapps/"+app_name, function(data) {
    var app_id = data['app_id'];
    var page = data['page'];
    var name = data['name'];
    var li = document.createElement('li');
    var h = document.createElement('a');
    h.setAttribute('href', '#app_'+app_id);
    h.innerHTML = name;
    li.append(h);
    $("#apps_list").append(li);
    $("#app_tabs").append(page);
    $("#app_tabs").tabs("refresh");
  });
}

function open_app_tab(app_id, name, fields, result_type) {
  // create new div
  var d = document.createElement('div');
  d.setAttribute('app_id', app_id);
  d.setAttribute('id', 'app_'+app_id);
  // render progress meter
  var p = document.createElement('progress');
  p.setAttribute('id', app_id+'_progress');
  p.setAttribute('min', 0);
  p.setAttribute('max', 100);
  p.setAttribute('value', 0);
  d.appendChild(p);
  // create the form
  var f = document.createElement('form');
  var t = document.createElement('table');
  f.setAttribute('name', app_id);
  $.each(fields, function(i, field) {
    var r = render_field_row(field, app_id);
    t.appendChild(r);
  });
  f.appendChild(t);
  // append the form to the div
  d.appendChild(f);
  // create the result widget
  r = render_result_widget(app_id, result_type);
  // append the result widget to the div
  d.appendChild(r);

  // add the div to the tab
  $("#app_tabs").append(d);
  // add the tab
  var li = document.createElement('li');
  var h = document.createElement('a');
  h.setAttribute('href', '#app_'+app_id);
  h.innerHTML = name;
  li.append(h);

  $("#apps_list").append(li);
  $("#app_tabs").tabs("refresh");
  // activate the last tab
  $("#app_tabs").tabs("option", "active", "-1");
}
