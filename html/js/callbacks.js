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
