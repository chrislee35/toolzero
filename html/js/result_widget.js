function render_result_widget(app_id, result_type) {
  if(result_type['type'] == 'textarea') {
    var r = $('<textarea />', {
      rows: 10,
      cols: 40,
      id: 'res_'+app_id,
      'data-result-type': 'textarea',
      'data-callback-name': result_type['callback']
    });
  } else if (result_type['type'] == 'table') {
    var r = $('<table />', {
      id: 'res_'+app_id,
      'data-result-type': 'table',
      'data-callback-name': result_type['callback']
    })
    r.append($('<thead/>'));
    r.append($('<tbody/>'));
  } else if (result_type['type'] == 'tree') {
    var r = $('<div />', {
      id: 'res_'+app_id,
      'data-result-type': 'tree',
      'data-callback-name': result_type['callback']
    })
  } else if (result_type['type'] == 'graph') {
    var r = $('<div />', {
      id: 'res_'+app_id,
      'data-result-type': 'graph',
      'data-callback-name': result_type['callback']
    });
    r.css('height', '500px');
  } else if (result_type['type'] == 'chart') {
    var r = $('<canvas />', {
      id: 'res_'+app_id,
      'data-result-type': 'chart',
      'data-callback-name': result_type['callback']
    })
    r.css('height', '500px');
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
  var tr = $("<tr/>");
  res.forEach( (item) => {
    var c = $('<'+cell+'/>');
    c.text(item);
    tr.append(c)
  })
  if(thead.children.length == 0) {
    thead.append(tr);
  } else {
    tbody.append(tr);
    if(ele[0].dataset.callbackName) {
      tr.onclick((e) => {
        call_function_callback(app_id, JSON.stringify({'data': res}), ele[0].dataset.callbackName, null);
      });
    }
  }
}

var last_event_time = 0;

function tree_callback(app_id, ele, res) {
  if(res == null) { return; }
  var tree_eles = render_tree(res);
  ele.append(tree_eles);

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
    var search_box = $("<input/>", {
      type: 'text',
      length: 30
    });
    search_box.on('keyup', () => {
      ele.jstree("search", search_box.val());
    });

    var search_div = $("<div />");
    search_div.text("Search: ")
    search_div.append(search_box);

    ele.prepend(search_div);
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
  var e = $("<ul />");
  if(typeof(res) == "object") {
    for(var k in res) {
      var l = $("<li />");
      if(typeof(k) != "number") {
        l.text(k);
      }
      l.append(render_tree(res[k]));
      e.append(l);
    }
  } else {
    var l = $("<li />");
    l.text(res);
    e.append(l);
  }
  return e;
}
