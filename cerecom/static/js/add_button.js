  $(document).on('click', '#add-button', function (e) {
    e.preventDefault();
    $.ajax({
      type: 'POST',
      url: '{% url "cart:cart_add" %}',
      data: {
        productid: $('#add-button').val(),
        csrfmiddlewaretoken: "{{csrf_token}}",
        action: 'post',
      },

      success: function (json) {

      },
      error: function (xhr, errmsg, err) {}
    })
  })
