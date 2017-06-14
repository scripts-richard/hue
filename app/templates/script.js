function toggle (light) {
  $.ajax({
    url: '/toggle/' + light,
    success: function(id) {
      if ($('#pwr' + light).hasClass('active')) {
        $('#pwr' + light).removeClass('active');
      } else {
        $('#pwr' + light).addClass('active');
      }
    }
  });
}

{% for light in lights %}

var RGBChange{{ light }} = function () {
  $('#RGB{{ light }}').css('background', 'rgb('+r{{ light }}.getValue()+','+g{{ light }}.getValue()+','+b{{light }}.getValue() + ')')
};

var r{{ light }} = $('#R{{ light }}').slider().on('slide', RGBChange{{ light }}).data('slider');

var g{{ light }} = $('#G{{ light }}').slider().on('slide', RGBChange{{ light }}).data('slider');

var b{{ light }} = $('#B{{ light }}').slider().on('slide', RGBChange{{ light }}).data('slider');

var bright{{ light }} = $('#BR{{ light }}').slider().data('slider')

{% endfor %}
