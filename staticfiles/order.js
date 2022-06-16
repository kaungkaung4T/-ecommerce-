$(document).on("submit", "#form", function(e){
                            e.preventDefault();
                            const url = $(this).attr('action')

                     $.ajax({
                        type: "POST",
                        url: url,
                     data: {
            csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
                     },
                     success: function(data){
                            alert(data);
                     },
                     });
            });