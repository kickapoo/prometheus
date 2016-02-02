(function(){
    $(document).ready(function(){

      tinymce.init({ selector:'textarea' });

      // Tooltips and Init js objects
      $('[data-toggle="tooltip_logout"]').tooltip();
      $('[data-toggle="tooltip_delete"]').tooltip();
      $('[data-toggle="tooltip_edit"]').tooltip();
      $('[data-toggle="tooltip_refresh"]').tooltip();
      $('[data-toggle="tooltip_change"]').tooltip();

      $("[name='select-need']").bootstrapSwitch();
      $("[name='status']").bootstrapSwitch();

      $('#dataTables-prometheus').DataTable({
              responsive: true
      });

      $('#datepicker input').datepicker({
        orientation: "bottom auto",
        todayHighlight: true,
      });

    });
}())
