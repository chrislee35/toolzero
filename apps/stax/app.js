function add_processor(name, folder_class, output_type) {
  $('#pipeline_app_id').append(
    "<div class='processor_instance "+folder_class+"'>"+name+"</div>"
  );
  $('#pipeline_app_id').append(
    "<div class='processor_output_type "+output_type+"'>"+output_type+"</div>"
  );
}

$(".processor_block").click(function () {
  var button = $( this )[0];
  var name = button.innerText;
  var folder = button.classList[1];
  var output_type = 'generator';
  add_processor(name, folder, output_type);
});
