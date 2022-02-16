function render_field_row(field, app_id) {
  var tr = $('<tr />');
  var label_td = $('<th />');
  tr.append(label_td);

  if(field['label']) {
    if(field['key']) {
      var l = $('<label/>', {
        for: field['key']
      });
      l.text(field['label']);
      label_td.append(l);
    } else {
      label_td.text(field['label']);
    }
  }

  var field_td = $('<td />');
  if(field['type']) {
    if(field['type'] == 'button') {
      field_td.append(render_button(field, app_id));
    } else if(field['type'] == 'text') {
      field_td.append(render_text_field(field, app_id));
    } else if (field['type'] == 'password') {
      field_td.append(render_password_field(field, app_id));
    } else if (field['type'] == 'list') {
      field_td.append(render_list_field(field, app_id));
    } else if (field['type'] == 'radio') {
      field_td.append(render_radio_field(field, app_id));
    } else if (field['type'] == 'checkbox') {
      field_td.append(render_checkbox_field(field, app_id));
    }
  }

  tr.append(field_td);
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
  var o = $('<input />', {
    type: 'button',
    value: field['text']
  });
  var onclick = field['onclick'];

  o.click(function(event) {
    var form_data = form_to_json(document.forms[app_id]);
    call_function(app_id, form_data, onclick);
  });
  return o;
}

function render_text_field(field, app_id) {
    var o = $('<input />', {
      type: 'text',
      length: field['length'] || 20,
      name: field['key'] || 'no_name',
      value: field['default'] || ''
    });
    if(field['onchange']) {
      o.on('change', (event) => {
        var form_data = form_to_json(document.forms[app_id]);
        call_function(app_id, form_data, field['onchange']);
      });
    }
    return o;
}

function render_password_field(field, app_id) {
    var o = $('<input />', {
      type: 'password',
      length: field['length'] || 20,
      name: field['key'] || 'no_name',
      value: field['default'] || ''
    });
    if(field['onchange']) {
      o.on('change', (event) => {
        var form_data = form_to_json(document.forms[app_id]);
        call_function(app_id, form_data, field['onchange']);
      });
    }
    return o;
}

function render_list_field(field, app_id) {
    var o = $('<select />', {
      name: field['key'] || 'no_name'
    })
    $.each(field['values'], function(i, item) {
      var op = $('<option/>', {
        value: item
      });
      op.text(item);
      if(field['default'] == item) {
        op.prop('selectedIndex', i);
      }
      o.append(op);
    });
    return o;
}

function render_radio_field(field, app_id) {
  var o = $('<div/>');

  $.each(field['values'], function(i, item) {
    var op = $('<radio/>', {
      value: item,
      name: field['key'] || 'no_name'
    });
    op.text(item);
    if(field['default'] == item) {
      op[0].setSelected();
    }
    o.append(op);
  });
  return o;
}

function render_checkbox_field(field, app_id) {
  var o = $('<div/>');
  $.each(field['values'], function(i, item) {
    var op = $('<input/>', {
      type: 'checkbox',
      value: item,
      name: field['key'] || 'no_name'
    });
    op.text(item);
    if(field['default'] == item) {
      op[0].setSelected();
    }
    o.append(op);
  });
  return o;
}
