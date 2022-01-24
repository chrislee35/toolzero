class StixNav_$app_id {
  load_stix_file(filename) {
    var data = {"filename": filename}
    call_function_callback("$app_id", JSON.stringify(data), 'load_stix_file',
      this.render_valid_types);
  }
  render_valid_types(valid_types) {
    console.log(valid_types)
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
    var data = { 'entity_type': entity_type }
    call_function_callback("$app_id", JSON.stringify(data), 'get_type', (entities) => {
      if(entities == null) {
        $("#res_$app_id").dataTable({"lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]]});
        $("#res_$app_id tbody tr").click( (event) => {
          this.view_entity(event.currentTarget.dataset.id);
        });
        return;
      }
      $("#res_$app_id thead").empty();
      $("#res_$app_id thead").append("<tr><th>Name</th><th>External Id</th></tr>");
      entities.forEach( (row) => {
        $("#res_$app_id tbody").append("<tr data-id="+row[0]+"><td>"+row[1]+"</td><td>"+row[2]+"</td></tr>");
      });
    });
  }
  view_entity(id) {
    var data = { 'id': id }
    call_function_callback("$app_id", JSON.stringify(data), 'get_details', (details) => {
      console.log(details);
    });
  }
  relationships(id) {

  }
}
var debug;

var stixnav_$app_id = new StixNav_$app_id();
