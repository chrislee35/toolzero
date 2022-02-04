class StixNav_$app_id {
  load_stix_file(filename) {
    var data = {"filename": filename}
    call_function_callback("$app_id", JSON.stringify(data), 'load_stix_file',
      this.render_valid_types);
  }
  render_valid_types(valid_types) {
    if(valid_types == null) {
      return;
    }
    var ele = $('#entity_types_$app_id');
    valid_types.forEach( (vt) => {
      var option = "<option value='"+vt+"'>"+vt+"</option>";
      ele.append(option);
    });
  }
  load_entity_type(entity_type) {
    var data = { 'entity_type': entity_type };
    var tbody = $("#res_$app_id tbody");
    tbody.empty();
    call_function_callback("$app_id", JSON.stringify(data), 'get_type', (entities) => {
      if(entities == null) {
        $("#res_$app_id tbody tr").click((event) => {
          this.view_entity(event.currentTarget.dataset.id);
        });
        return;
      }

      entities.forEach((row) => {
        tbody.append("<tr data-id='"+row[0]+"'><td>"+row[1]+"</td><td>"+row[2]+"</td></tr>");
      });
    });
  }
  view_entity(id) {
    var data = { 'id': id }
    call_function_callback("$app_id", JSON.stringify(data), 'get_details', (details) => {
      if(details == null) { return; }
      if(details['type'] == 'intrusion-set') {
        var markup = `
        <h2 class='entity_name'>${details.name}</h2>
        type: ${details.type}
        <div class='description'>${details.description}</div>
        <div class='aliases'>${details.aliases.join(", ")}</div>`;

        if(details['external_references']) {
          markup += "<table class='external_references'><tr><th>Source</th><th>Id</th></tr>";
          details['external_references'].forEach( (ref) => {
            if(ref['source_name'] == 'mitre-attack') {
              markup += `<tr><td>${ref.source_name}</td><td><a href='${ref.url}'>${ref.external_id}</a></td></tr>`;
            } else {
              markup += `<tr><td>${ref.source_name}</td><td>${ref.description}</td></tr>`;
            }
          });
        }
        markup += "</table>";
        document.getElementById('entity_display_$app_id').innerHTML = markup;
        stixnav_$app_id.relationships(id);
      }
      console.log(details);
    });
  }
  relationships(id) {
    var data = {'id': id, 'hops': 1}
    call_function_callback("$app_id", JSON.stringify(data), 'get_relationship_graph', this.relationships_callback);
  }
  relationships_callback(graph) {
    if(graph == null) {return;}
    console.log(graph);
    $('#entity_display_$app_id').empty();
    var graph_div = document.createElement('div');
    graph_div.id = "graph_$app_id";
    graph_div.style.height = '500px';
    $('#entity_display_$app_id').append(graph_div);
    var network = new vis.Network(graph_div, graph);

    network.on("click", function (params) {
      var nodename = params['nodes'][0];
      if(nodename == null) {return;}
      console.log(nodename);
      var data = {'id': nodename, 'hops': 1};
      call_function_callback("$app_id", JSON.stringify(data), 'get_relationship_graph', stixnav_$app_id.relationships_callback);
    });
  }
}
var debug;

var stixnav_$app_id = new StixNav_$app_id();
