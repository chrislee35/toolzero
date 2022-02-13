function render_result_widget(app_id, result_type) {
  if(result_type['type'] == 'textarea') {
    var r = document.createElement('textarea');
    r.setAttribute('rows', 10);
    r.setAttribute('cols', 40);
    r.setAttribute('id', 'res_'+app_id);
    r.setAttribute('data-result-type', 'textarea');
    if(result_type['callback']) {
      r.setAttribute('data-callback-name', result_type['callback']);
    }
  } else if (result_type['type'] == 'table') {
    var r = document.createElement('table');
    r.setAttribute('id', 'res_'+app_id);
    r.setAttribute('data-result-type', 'table');
    r.appendChild(document.createElement("thead"));
    r.appendChild(document.createElement("tbody"));
    if(result_type['callback']) {
      r.setAttribute('data-callback-name', result_type['callback']);
    }
  } else if (result_type['type'] == 'tree') {
    var r = document.createElement('div');
    r.setAttribute('id', 'res_'+app_id);
    r.setAttribute('data-result-type', 'tree');
    if(result_type['callback']) {
      r.setAttribute('data-callback-name', result_type['callback']);
    }
  } else if (result_type['type'] == 'graph') {
    var r = document.createElement('div');
    r.setAttribute('id', 'res_'+app_id);
    r.setAttribute('data-result-type', 'graph');
    r.style.height = '500px';
    if(result_type['callback']) {
      r.setAttribute('data-callback-name', result_type['callback']);
    }
  } else if (result_type['type'] == 'chart') {
    var r = document.createElement('canvas');
    r.setAttribute('id', 'res_'+app_id);
    r.setAttribute('data-result-type', 'chart');
    r.style.height = '500px';
    if(result_type['callback']) {
      r.setAttribute('data-callback-name', result_type['callback']);
    }
  }
  return r
}

function textarea_callback(app_id, ele, res) {
  if(res != undefined) {
    ele.append(res)
  }
}

function table_callback(app_id, ele, res) {
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
    if(ele[0].dataset.callbackName) {
      tr.onclick((e) => {
        call_function_callback(app_id, JSON.stringify({'data': res}), ele[0].dataset.callbackName, null);
      });
    }
  }
}

function tree_callback(app_id, ele, res) {
  if(res == null) { return; }
  var tree_eles = render_tree(res);
  ele[0].appendChild(tree_eles);

  ele.jstree({
    "plugins": ["search", "adv_search", "themes", "html_data"],
    "search": { "case_insensitive": true, "show_only_matches": true }
  });

  if(ele[0].dataset.callbackName) {
    console.log('setting up tree callback');
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
}

function graph_callback(app_id, ele, res) {
  if(res == null) { return; }
  if(res['options']) {
    var options = res['options'];
    delete res['options'];
  }
  res['nodes'] = new vis.DataSet(res['nodes']);
  res['edges'] = new vis.DataSet(res['edges']);
  var network = new vis.Network(ele[0], res, options);

  if(ele[0].dataset.callbackName) {
    console.log('setting up graph callback');
    network.on("click", function (params) {
      var node = res['nodes'].get(params['nodes'][0]);
      var nodename = node['label'];
      call_function_callback(app_id, JSON.stringify({'data': nodename}), ele[0].dataset.callbackName, null);
    });
  }
}

function chart_callback(app_id, ele, res) {
  if(res == null) { return; }
  const ctx = ele[0].getContext('2d');
  const myChart = new Chart(ctx, res)
  if(ele[0].dataset.callbackName) {
    console.log('setting up chart callback');
  }
}

function call_function(app_id, form_data, callback_name) {
  var callback = (res) => {
    var ele = $('#res_'+app_id);
    var type = ele[0].dataset.resultType;
    if(type == 'textarea') {
      textarea_callback(app_id, ele, res);
    } else if(type == 'table') {
      table_callback(app_id, ele, res);
    } else if(type == 'tree') {
      tree_callback(app_id, ele, res);
    } else if(type == 'graph') {
      graph_callback(app_id, ele, res);
    } else if(type == 'chart') {
      chart_callback(app_id, ele, res);
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
