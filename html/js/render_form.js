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
