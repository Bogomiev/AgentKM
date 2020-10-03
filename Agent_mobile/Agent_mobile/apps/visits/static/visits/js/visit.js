$(document).ready(function() {
    var form = $('#form_visit');
    var filter_shop = $('#id_filter_shop');

    filter_shop.on('change', function(){

        var data = {};
        data.filter = filter_shop.val();
        var url = "visit/agent_shops/";

        $.ajax({
            url: url,
            type: 'GET',
            data: data,
            cache: true,
            success: function(data) {

                shop_select = $('#id_shop');
                shop_select.empty();

                data.shops.forEach(function(entry) {
                    shop_select.append('<option value=' + entry.value + ">" + entry.name + '</option>');
                });

                shop_select.prop('selected', false);
            }
        });

    });
});