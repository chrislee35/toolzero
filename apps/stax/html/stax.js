var debug;

class Stax_$app_id {
  constructor() {
    this.processors = {};
    this.last_output = 'None';
    this.pipeline = [];
    this.output_id = undefined;
  }
  get_proc(name) {
    return this.processors[name];
  }
  render_block(proc) {
    var button = $("<div class='processor_block folder_"+proc['folder']+"'>"+proc['name']+"</div>");
    button.click(this.add_block_to_pipeline_cb);
    $('#processor_list_$app_id').append(button);
  }
  render_processor(proc) {
    var name = proc['name'];
    var folder_class = 'folder_'+proc['folder'];
    var params = proc['parameters'];
    var output_type = proc['output'];
    // render parameters
    var param_form = "";
    if(params.length > 0) {
      param_form = "<form><table>";
      for(var i in params) {
        var p = params[i];
        var d = "";
        if(p['default']) {
          d = " value='" + p['default'] + "'";
        }
        var input_id = uuid1();
        p['id'] = input_id;
        param_form += "<tr>";
        param_form += "<th>" + p['name'] + "</th>";
        if ( p['type'] == 'textarea' ) {
          d = p['default'] || ""
          param_form += "<td><textarea id='" + input_id + "' class='outputs'>" + d + "</textarea></td>";
        } else if ( p['type'] == 'boolean' ) {
          d = '';
          if(p['default']) { d = 'checked'; }
          param_form += "<td><input type='checkbox' id='" + input_id + "'" + d + "></td>";
        } else if ( p['type'] == 'combo' ) {
          d = p['default'];
          param_form += "<td><select id='"+ input_id + "'>";
          for(var i in p['options']) {
            var op = p['options'][i]
            param_form += "<option value='"+ op +"'";
            if( d == op ) {
              param_form += " checked";
            }
            param_form += ">"+op+"</option>\n";
          }
          param_form += "</select></td>\n";
        } else {
          param_form += "<td><input type='" + p['type'] + "' id='" + input_id + "'" + d + "></td>";
        }
        param_form += "</tr>\n";
      }
    }
    // create the next pipeline processor id
    var proc_id = this.pipeline.length;

    // append the processor to the pipeline visualization
    if(proc['inputs'].indexOf('None') > -1) {
      $('#pipeline_$app_id').append(
        "<div data-proc-id='"+ proc_id +"' class='processor_instance "+folder_class+" playable' onclick='stax_$app_id.submit_pipeline(this.dataset.procId);'><span class='proc_inst_name'>"+name+"</span>"+param_form+"</div>"
      );
    } else {
      $('#pipeline_$app_id').append(
        "<div data-proc-id='"+ proc_id +"' class='processor_instance "+folder_class+"'><span class='proc_inst_name'>"+name+"</span>"+param_form+"</div>"
      );
    }

    $('#pipeline_$app_id').append(
      "<div class='processor_output_type "+output_type+"'>"+output_type+"</div>"
    );
  }
  activate_valid_blocks() {
    var self = this;
    $('#processor_list_$app_id .processor_block').each(function(index, ele) {
      var name = ele.innerText;
      var proc = self.get_proc(name);
      if(proc['inputs'].indexOf(self.last_output) == -1) {
        ele.classList.add('disabled');
      } else {
        ele.classList.remove('disabled');
      }
    });
  }
  add_block_to_pipeline_cb() {
    var self = stax_$app_id;
    var button = $( this )[0];
    var name = button.innerText;
    self.add_block_to_pipeline(name, undefined);
  }
  add_block_to_pipeline(name, parameters) {
    // if parameters is undefined, then it defaults to the defaults
    console.log(name);
    // copy the Proc Block to a Proc Instance
    var proc = Object.assign({}, this.get_proc(name));
    console.log(proc);
    // copy the Parameters
    var params = [];
    for(var i in proc['parameters']) {
      params.push(Object.assign({}, proc['parameters'][i]));
    }
    proc['parameters'] = params;

    // check if the last output is compatible.
    if(proc['inputs'].indexOf(this.last_output) == -1) {
      console.log(proc);
      alert("Last output type was "+this.last_output+". "+name+" takes in one of "+proc['inputs'].join(", ") );
      return
    }

    // check for dynamic output type and then set output_type
    if(proc['output'] == 'input') {
      proc['output'] = this.last_output;
    } else if (proc['output'] == 'rule') {
      this.resolve_processor_output_rule(name, proc);
      return;
    } else if (proc['output'] == 'select') {
      this.resolve_processor_output_rule(name, proc);
      return;
    }
    this.register_proc(proc);
  }
  resolve_processor_output_rule(name, proc) {
    var form_data = JSON.stringify({ "processor_name": name, "input_type": this.last_output });
    var p = call_function_promise("$app_id", form_data, 'calculate_processor_output');
    p.then((output_type) => {
      if(output_type == 'select') {
        this.resolve_processor_output_selection(name, proc);
        return;
      }
      proc['output'] = output_type;
      this.register_proc(proc);
    }).catch((error) => {
      console.log(error);
    });
  }
  resolve_processor_output_selection(name, proc) {
    var form_data = JSON.stringify({ "processor_name": name, "input_type": this.last_output });
    var p = call_function_promise("$app_id", form_data, 'calculate_selectable_outputs');
    p.then((selectable_output_types) => {
      this.show_output_type_selection_dialog(name, proc, selectable_output_types)
    }).catch((error) => {
      console.log(error);
    });
  }
  register_proc(proc) {
    this.render_processor(proc);
    this.pipeline.push(proc);
    this.last_output = proc['output'];
    this.activate_valid_blocks();
  }
  show_output_type_selection_dialog(name, proc, selectable_output_types) {
    var output_type = 'asdfasdfasdf';
    while(selectable_output_types.indexOf(output_type) == -1) {
      output_type = prompt("Select an output type for "+name+":\n"+selectable_output_types.join(', '));
    }
    proc['output'] = output_type;
    this.register_proc(proc);
  }
  remove_block_from_pipeline() {
    var self = stax_$app_id;

    if ( self.pipeline.length == 0 ) { return; }

    var proc_id = self.pipeline.length - 1;
    self.pipeline.pop();
    var ele = $(".processor_instance[data-proc-id="+proc_id+"]");
    // need to update the last output type
    // console.log(ele.prev());
    self.last_output = ele.prev().text();
    if(self.last_output == undefined) {
      self.last_output = 'None';
    }
    // console.log(self.last_output);
    ele.next().remove();
    ele.remove();
    self.activate_valid_blocks();
  }
  render_processor_blocks(data) {
    var self = stax_$app_id;
    self.processors = data;
    for(var i in self.processors) {
      var proc = self.processors[i];
      self.render_block(proc);
    }
    self.activate_valid_blocks();
    self.render_menu_buttons();
    if(localStorage.getItem("last_pipeline") != undefined) {
      self.load_pipeline("last_pipeline")
    }
  }
  to_data(start) {
    if(start == undefined) {
      start = 0;
    }
    var pipeline = [];
    for( var i in this.pipeline ) {
      var block = this.pipeline[i];
      var processor_name = block['name'];
      var params = {};
      for ( var j in block['parameters' ] ) {
        var p = block['parameters'][j];
        var input_id = p['id'];
        var input_value = $('#'+input_id)[0].value;
        if (p['type'] == "boolean") {
          input_value = $('#'+input_id)[0].checked;
        } else if (p["type"] == "number") {
          input_value = parseInt(input_value);
        }
        var input_name = p['name'];
        params['id'] = input_id;
        params[input_name] = input_value;
      }
      pipeline.push( { 'processor': processor_name, 'parameters': params, 'output': block['output'] } );
    }
    return { pipeline: pipeline, submit_time: Date.now(), start: start };
  }
  to_json(start) {
    return JSON.stringify(this.to_data(start));
  }
  submit_pipeline(start) {
    $(".outputs").val("");

    var pipeline = this.to_json(0);
    localStorage.setItem("last_pipeline", pipeline);

    call_function_callback("$app_id", this.to_json(start), "run_pipeline", (data) => {
      console.log(data);
      if(data['type'] == 'output' && data['id']) {
        var message = data['message'];
        if(typeof message == "string" || typeof message == "number") {
          $("#"+data['id'])[0].value += message;
        } else {
          $("#"+data['id'])[0].value += JSON.stringify(message);
        }
      } else {
        alert(JSON.stringify(data));
      }
    });
  }
  load_pipeline(name) {
    var job = JSON.parse(localStorage.getItem(name));
    var pipeline = job['pipeline'];
    for( var i in pipeline ) {
      var block = pipeline[i];
      this.add_block_to_pipeline(block['processor'], block['parameters']);
    }
  }
  save_pipeline(name) {
    localStorage.setItem(name, this.to_json(0));
  }
  clear_pipeline() {
    this.last_output = 'None';
    this.pipeline = [];
    this.output_id = undefined;
    $('#pipeline_$app_id').empty();
    this.render_menu_buttons();
  }
  render_menu_buttons() {
    $('#pipeline_$app_id').append("<input type='button' value='load' onclick='stax_$app_id.load_dialog()'>");
    $('#pipeline_$app_id').append("<input type='button' value='save' onclick='stax_$app_id.save_dialog()'>");
    $('#pipeline_$app_id').append("<input type='button' value='clear' onclick='stax_$app_id.clear_dialog()'>");
  }
  load_dialog() {
    var pipeline_names = [];
    for( var i=0; i < localStorage.length; i++) {
      pipeline_names.push(localStorage.key(i));
    }
    var name = prompt("Load pipeline: "+pipeline_names.join(', '), 'last_pipeline');
    if(name == undefined) {
      return;
    }
    if(localStorage.getItem(name)) {
      this.load_pipeline(name);
    } else {
      alert("Could not find a saved pipeline with the name "+name);
    }
  }
  save_dialog() {
    var name = prompt("Save pipeline as...", new Date().toISOString());
    if(name == undefined) {
      return;
    }
    this.save_pipeline(name);
    alert("Saved pipeline.")
  }
  clear_dialog() {
    if(confirm("Do you want to clear the current pipeline?")) {
      this.clear_pipeline();
    }
  }

}
var stax_$app_id = new Stax_$app_id();
call_function_callback("$app_id", '{}', 'list_processors', stax_$app_id.render_processor_blocks);
