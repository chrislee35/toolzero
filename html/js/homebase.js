function EventSource2(url) {
    this.url = url;
    this.es = null;
    this.listeners = {};
}

EventSource2.prototype = {
    constructor: EventSource2,

    connect: function() {
        console.log("SSE Connecting to "+this.url)
        this.es = new EventSource(this.url);
        this.bindEvents();
    },

    disconnect: function() {
      console.log("SSE Disconnecting")
        if(this.es) {
          this.es.close();
          this.es = null;
        }
    },

    bindEvents: function() {
        for ( var type in this.listeners ) {
            var evs = this.listeners[type];
            for( var i = 0; i < evs.length; ++i ) {
                this.es.addEventListener( type, evs[i], false );
            }
        }
    },

    addEventListener: function( type, fn ) {
        if( !this.listeners[type] ) {
            this.listeners[type] = [];
        }

        this.listeners[type].push( fn );
        if( this.es ) {
            this.bindEvents();
        }
    }
}

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
  if(result_type['type'] == 'textarea') {
    var r = document.createElement('textarea');
    r.setAttribute('rows', 10);
    r.setAttribute('cols', 40);
    r.setAttribute('id', 'res_'+app_id);
    r.setAttribute('data-result-type', 'textarea');
    d.appendChild(r);
  } else if (result_type['type'] == 'table') {
    var r = document.createElement('table');
    r.setAttribute('id', 'res_'+app_id);
    r.setAttribute('data-result-type', 'table');
    r.appendChild(document.createElement("thead"));
    r.appendChild(document.createElement("tbody"));
    d.appendChild(r);
  } else if (result_type['type'] == 'tree') {
    var r = document.createElement('div');
    r.setAttribute('id', 'res_'+app_id);
    r.setAttribute('data-result-type', 'tree');
    d.appendChild(r);
    if(result_type['callback']) {
      r.setAttribute('data-callback-name', result_type['callback']);
    }
  } else if (result_type['type'] == 'graph') {
    var r = document.createElement('div');
    r.setAttribute('id', 'res_'+app_id);
    r.setAttribute('data-result-type', 'graph');
    r.style.height = '500px';
    d.appendChild(r);
    if(result_type['callback']) {
      r.setAttribute('data-callback-name', result_type['callback']);
    }
  }
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
      field_td.appendChild(render_text_field(field, app_id));
    } else if (field['type'] == 'password') {
      field_td.appendChild(render_password_field(field, app_id));
    } else if (field['type'] == 'list') {
      field_td.appendChild(render_list_field(field, app_id));
    } else if (field['type'] == 'radio') {
      field_td.appendChild(render_radio_field(field, app_id));
    } else if (field['type'] == 'checkbox') {
      field_td.appendChild(render_checkbox_field(field, app_id));
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
  var onclick = field['onclick'];
  o.onclick = function(event) {
    var form_data = form_to_json(document.forms[app_id]);
    call_function(app_id, form_data, onclick);
  };
  return o;
}

function render_text_field(field, app_id) {
    var o = document.createElement('input');
    o.setAttribute('type', 'text');
    o.setAttribute('length', field['length'] || 20);
    o.setAttribute('name', field['key'] || 'no_name');
    o.setAttribute('value', field['default'] || '');
    if(field['onchange']) {
      o.onchange = (event) => {
        var form_data = form_to_json(document.forms[app_id]);
        call_function(app_id, form_data, field['onchange']);
      }
    }
    return o;
}

function render_password_field(field, app_id) {
    var o = document.createElement('input');
    o.setAttribute('type', 'password');
    o.setAttribute('length', field['length'] || 20);
    o.setAttribute('name', field['key'] || 'no_name');
    o.setAttribute('value', field['default'] || '');
    return o;
}

function render_list_field(field, app_id) {
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

function render_radio_field(field, app_id) {
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

function render_checkbox_field(field, app_id) {
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

var last_event_time = 0;

function call_function(app_id, form_data, callback_name) {
  var callback = (res) => {
    var ele = $('#res_'+app_id);
    var type = ele[0].dataset.resultType;
    if(type == 'textarea') {
      if(res != undefined) {
        ele.append(res)
      }
    } else if(type == 'table') {
      if(res == undefined) {
        ele.dataTable();
        return;
      }
      var thead = $('#res_'+app_id+' thead')[0];
      var tbody = $('#res_'+app_id+' tbody')[0];
      var cell = 'td';
      if(thead.children.length == 0) {
        cell = 'th'
      }
      var tr = document.createElement("tr");
      res.forEach( (item) => {
        var c = document.createElement(cell);
        c.innerText = item;
        tr.appendChild(c)
      })
      if(thead.children.length == 0) {
        thead.appendChild(tr);
      } else {
        tbody.appendChild(tr);
      }
    } else if(type == 'tree') {
      if(res == null) { return; }
      var tree_eles = render_tree(res);
      ele[0].appendChild(tree_eles);

      ele.jstree({
        "plugins": ["search", "adv_search", "themes", "html_data"],
        "search": { "case_insensitive": true, "show_only_matches": true }
      });

      if(ele[0].dataset.callbackName) {
        console.log('setting up callback');
        ele.on('changed.jstree', (e, data) => {
          if(e['timeStamp'] > last_event_time) {
            last_event_time = e['timeStamp'];
            //console.log(data['node']['text']);
            call_function_callback(app_id, JSON.stringify({'data': data['node']['text']}), ele[0].dataset.callbackName, null);
          }
        }).jstree(true);
      }

      if($("#res_"+app_id+" input").length == 0) {
        var search_box = document.createElement("input");
        search_box.onkeyup = () => {
          ele.jstree("search", search_box.value);
        };
        search_box.type = 'text';
        search_box.length = 30;

        var search_div = document.createElement("div");
        search_div.innerHTML = "Search: "
        search_div.appendChild(search_box);

        ele[0].prepend(search_div);
      }
    } else if(type == 'graph') {
      if(res == null) { return; }
      if(res['options']) {
        var options = res['options'];
        delete res['options'];
      }
      res['nodes'] = new vis.DataSet(res['nodes']);
      res['edges'] = new vis.DataSet(res['edges']);
      var network = new vis.Network(ele[0], res, options);

      if(ele[0].dataset.callbackName) {
        console.log('setting up callback');
        network.on("click", function (params) {
          var node = res['nodes'].get(params['nodes'][0]);
          var nodename = node['label'];
          call_function_callback(app_id, JSON.stringify({'data': nodename}), ele[0].dataset.callbackName, null);
        });
      }
    }
  };
  call_function_callback(app_id, form_data, callback_name, callback);
}

function render_tree(res) {
  if(typeof(res) == "object") {
    var e = document.createElement("ul");
    for(var k in res) {
      if(typeof(k) == "number") {
        // let's assume this is an array
        var l = document.createElement("li");
        l.appendChild(render_tree(res[k]));
        e.appendChild(l);
      } else {
        var l = document.createElement("li");
        l.innerText = k;
        l.appendChild(render_tree(res[k]));
        e.appendChild(l);
      }
    }
    return e;
  } else {
    var e = document.createElement("ul");
    var l = document.createElement("li");
    l.innerText = res;
    e.appendChild(l);
    return e;
  }
}

function call_function_callback(app_id, form_data, callback_name, callback) {
  call_callback("/call/"+app_id+"/"+callback_name, app_id, form_data, callback);
}

function call_function_promise(app_id, form_data, callback_name) {
  return call_callback_promise("/call/"+app_id+"/"+callback_name, app_id, form_data);
}

function proxy(callback, method, url, params, body, headers) {
  proxy_request = JSON.stringify(
    {
      'url': url,
      'params': params,
      'body': body,
      'headers': headers,
      'method': method
    }
  );
  call_callback("/proxy", '', proxy_request, callback);
}

function call_callback(url, app_id, form_data, callback) {
  if(document.getElementById(app_id+'_progress')) {
    document.getElementById(app_id+'_progress').value = 0;
  }
  $.ajax({
    type: "POST",
    url: url,
    data: form_data,
    success: function(data) {
      var eventSource = new EventSource2('/events/'+data['callback_id']);
      eventSource.addEventListener('message', event => {
        var data = JSON.parse(event.data);
        if(callback) {
          callback(data['results']);
        }
        if(data['progress']) {
          document.getElementById(app_id+'_progress').value = data['progress'];
        }
      });
      eventSource.addEventListener('leave', event => {
        callback(undefined);
        eventSource.disconnect();
      });
      eventSource.connect();
    },
    dataType: 'json'
  });
}

function call_callback_promise(url, app_id, form_data) {
  return new Promise( (resolve, reject) => {
    $.ajax({
      type: "POST",
      url: url,
      data: form_data,
      dataType: 'json',
      success: function(data) {
        var eventSource = new EventSource2('/events/'+data['callback_id']);
        eventSource.addEventListener('message', event => {
          var data = JSON.parse(event.data);
          resolve(data['results']);
          eventSource.disconnect();
        });
        eventSource.addEventListener('leave', event => {
          eventSource.disconnect();
        });
        eventSource.connect();
      },
      error: function(error) {
        reject(error);
      }
    });
  })
}

function uuid1() {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace( /[xy]/g , function(c) {
    var rnd = Math.random()*16 |0, v = c === 'x' ? rnd : (rnd&0x3|0x8) ;
    return v.toString(16);
  });
}

$("#app_tabs").tabs()
