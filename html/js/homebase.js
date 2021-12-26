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
    }
    a.innerText = app['name'];
    a.title = app['desc'];
    li.append(a);
    $('#app_list').append(li);
  });
});

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

function open_app_tab(app_id, name, fields, result_type) {
  // create new div
  var d = document.createElement('div');
  d.setAttribute('app_id', app_id);
  d.setAttribute('id', 'app_'+app_id);
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
  // add the div to the tab
  f.appendChild(t);
  d.appendChild(f);
  var r = document.createElement('textarea');
  r.setAttribute('rows', 10);
  r.setAttribute('cols', 40);
  r.setAttribute('id', 'res_'+app_id);
  d.appendChild(r);
  $("#app_tabs").append(d);
  // add the tab
  var li = document.createElement('li');
  var h = document.createElement('a');
  h.setAttribute('href', '#app_'+app_id);
  h.innerHTML = name;
  li.append(h);

  $("#apps_list").append(li);
  $("#app_tabs").tabs("refresh");
  //$("#app_tabs").tabs("option", "active", "1");
}

function render_field_row(field, app_id) {
  var tr = document.createElement('tr');
  var label_td = document.createElement('th');
  if(field['label']) {
    if(field['key']) {
      var l = document.createElement('label');
      l.setAttribute('for', field['key']);
      l.innerText = field['label'];
      label_td.appendChild(l);
    } else {
      label_td.innerText = field['label'];
    }
  }
  tr.appendChild(label_td);

  var field_td = document.createElement('td');
  if(field['type']) {
    if(field['type'] == 'button') {
      field_td.appendChild(render_button(field, app_id));
    } else if(field['type'] == 'text') {
      field_td.appendChild(render_text_field(field));
    } else if (field['type'] == 'password') {
      field_td.appendChild(render_password_field(field));
    } else if (field['type'] == 'list') {
      field_td.appendChild(render_list_field(field));
    } else if (field['type'] == 'radio') {
      field_td.appendChild(render_radio_field(field));
    } else if (field['type'] == 'checkbox') {
      field_td.appendChild(render_checkbox_field(field));
    }
  }

  tr.appendChild(field_td);
  return tr;
}

function form_to_json(formElem) {
  var object = {};
  var formData = new FormData(formElem);
  formData.forEach((value, key) => {
    // Reflect.has in favor of: object.hasOwnProperty(key)
    if(!Reflect.has(object, key)){
        object[key] = value;
        return;
    }
    if(!Array.isArray(object[key])){
        object[key] = [object[key]];
    }
    object[key].push(value);
  });
  var json = JSON.stringify(object);
  return json;
}

function render_button(field, app_id) {
  var o = document.createElement('input');
  o.setAttribute('type', 'button');
  o.setAttribute('value', field['text']);
  console.log(field);
  var onclick = field['onclick'];
  o.onclick = function(event) {
    var form_data = form_to_json(document.forms[app_id]);
    call_function(app_id, form_data, onclick);
  };
  return o;
}

function render_text_field(field) {
    var o = document.createElement('input');
    o.setAttribute('type', 'text');
    o.setAttribute('length', field['length'] || 20);
    o.setAttribute('name', field['key'] || 'no_name');
    o.setAttribute('value', field['default'] || '');
    return o;
}

function render_password_field(field) {
    var o = document.createElement('input');
    o.setAttribute('type', 'password');
    o.setAttribute('length', field['length'] || 20);
    o.setAttribute('name', field['key'] || 'no_name');
    o.setAttribute('value', field['default'] || '');
    return o;
}

function render_list_field(field) {
    var o = document.createElement('select');
    o.name = field['key'] || 'no_name';
    $.each(field['values'], function(i, item) {
      var op = document.createElement('option');
      op.value = item;
      op.innerHTML = item;
      if(field['default'] == item) {
        o.selectedIndex = i;
      }
      o.appendChild(op);
    });

    return o;
}

function render_radio_field(field) {
  var o = document.createElement('div');
  $.each(field['values'], function(i, item) {
    var op = document.createElement('radio');
    op.value = item;
    op.name = field['key'] || 'no_name';
    op.innerHTML = item;
    if(field['default'] == item) {
      op.setSelected();
    }
    o.appendChild(op);
  });
  return o;
}

function render_checkbox_field(field) {
  var o = document.createElement('div');
  $.each(field['values'], function(i, item) {
    var op = document.createElement('input');
    op.type = 'checkbox';
    op.value = item;
    op.name = field['key'] || 'no_name';
    op.innerHTML = item;
    if(field['default'] == item) {
      op.setSelected();
    }
    o.appendChild(op);
  });
  return o;
}

function call_function(app_id, form_data, callback_name) {
  document.getElementById(app_id+'_progress').value = 0;
  $.ajax({
    type: "POST",
    url: "call/"+app_id+"/"+callback_name,
    data: form_data,
    success: function(data) {
      connect_websocket(data, app_id);
    },
    dataType: 'json'
  });
}

function proxy(callback, method, url, params, body, headers) {
  proxy_request = JSON.stringify(
    {
      'url': url,
      'params': params,
      'body': body,
      'headers': headers
    }
  );

  $.ajax({
    type: "POST",
    url: "proxy",
    data: proxy_request,
    success: function(data) {
      connect_websocket_callback(data, callback); // how do we connect this to the result pane?
    },
    dataType: 'json'
  });
}

function connect_websocket(data, app_id) {
  var ws = new WebSocket(data['websocket'], 'results');
  var res = $('#res_'+app_id);
  ws.onopen = function(event) {
    ws.send(data['callback_id']);
  };
  ws.onmessage = function(event) {
    data = JSON.parse(event.data);
    if(data['status'] == 'success') {
      res.append(data['results']);
    }
    if(data['progress'] != undefined) {
      document.getElementById(app_id+'_progress').value = data['progress'];
    }
  };
  ws.onclose = function(event) {
    console.log(event.reason);
  };
}

function connect_websocket_callback(data, callback) {
  console.log(data);
  var ws = new WebSocket(data['websocket'], 'results');
  ws.onopen = function(event) {
    ws.send(data['callback_id']);
  };
  ws.onmessage = function(event) {
    data = JSON.parse(event.data);
    console.log(data);
    if(data['status'] == 'success') {
      callback(data['results']);
    }
    if(data['progress'] != undefined) {
      document.getElementById('progress').value = data['progress'];
    }
  };
  ws.onclose = function(event) {
    console.log(event.reason);
  };
}

$("#app_tabs").tabs()
