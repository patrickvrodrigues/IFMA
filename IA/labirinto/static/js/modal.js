$(function () {
    var loadModal = function () {
      var btn = $(this);
      $.ajax({
        url: btn.attr("data-url"),
        type: 'get',
        dataType: 'json',
        beforeSend: function () {
          $("#modal").modal("show");
        },
        success: function (data) {
          $("#modal .modal-content").html(data.html_form);
        }
      });
    };
  
    var saveModal = function () {
      var form = $(this);
      $.ajax({
        url: form.attr("action"),
        data: form.serialize(),
        type: form.attr("method"),
        dataType: 'json',
        success: function (data) {
          switch (data.is_valid) {
            case 0:
              $("#modal .modal-content").html(data.html_form);
              break;
            case 1:
              window.location.reload();
              break;
            case 2:
              window.location.replace(data.success_url);
              break;
            default:
              alert("Error, tente novamente!")
              break;
          }
        }
      });
      return false;
    };
  
    // Criar
    $(".js-criar").click(loadModal);
    $("#modal").on("submit", ".js-criar-form", saveModal);
  
    // Editar
    $("#tabela").on("click", ".js-editar", loadModal);
    $("#detail").on("click", ".js-editar", loadModal);
    $("#modal").on("submit", ".js-editar-form", saveModal);
  
    // Deletar
    $("#tabela").on("click", ".js-deletar", loadModal);
    $("#detail").on("click", ".js-deletar", loadModal);
    $("#modal").on("submit", ".js-deletar-form", saveModal);
    
  });