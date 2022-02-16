function open_app(app_type, app_path) {
  if(app_type == 'py') { return open_pyapp(app_path); }
  if(app_type == 'js') { return open_jsapp(app_path); }
  if(app_type == 'jspy') { return open_jspyapp(app_path); }
}

function open_pyapp(app_name) {
  $.getJSON("apps/"+app_name, function(data) {
    var app_id = data['app_id'];
    var fields = data['fields'];
    var name = data['name']
    var result_type = data['result_type'];
    open_app_tab(app_id, name, fields, result_type);
  });
}

function open_jsapp(app_name) {
  $.getJSON("jsapps/"+app_name, open_jsapp_callback);
}

function open_jspyapp(app_name) {
  $.getJSON("jspyapps/"+app_name, open_jsapp_callback);
}

function open_jsapp_callback(data) {
  var app_id = data['app_id'];
  var page = data['page'];
  var name = data['name'];
  var li = $("<li />");
  var h = $('<a />', {href: '#app_'+app_id});
  h.text(name);
  li.append(h);
  $("#apps_list").append(li);
  $("#app_tabs").append(page);
  $("#app_tabs").tabs("refresh");
  // activate the last tab
  $("#app_tabs").tabs("option", "active", "-1");
}

function open_app_tab(app_id, name, fields, result_type) {
  // create new div
  var d = $("<div />", {
    app_id: app_id,
    id: 'app_'+app_id
  });

  // render progress meter
  var p = $('<progress />', {
    id: app_id+'_progress',
    min: 0,
    max: 0,
    value: 0
  });

  d.append(p);

  // create the form
  var f = $('<form />', {
    name: app_id
  });
  var t = $('<table />', {
    name: app_id
  });

  $.each(fields, function(i, field) {
    var r = render_field_row(field, app_id);
    t.append(r);
  });
  f.append(t);
  // append the form to the div
  d.append(f);
  // create the result widget
  r = render_result_widget(app_id, result_type);
  // append the result widget to the div
  d.append(r);

  // add the div to the tab
  $("#app_tabs").append(d);
  // add the tab
  var li = $("<li />");
  var h = $('<a />', {href: '#app_'+app_id});
  h.text(name);
  li.append(h);
  $("#apps_list").append(li);

  $("#app_tabs").tabs("refresh");
  // activate the last tab
  $("#app_tabs").tabs("option", "active", "-1");
}
