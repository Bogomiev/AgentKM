$(function () {
    var to = false;
    $('#products_tree_search').keyup(function () {
        if(to) { clearTimeout(to); }
        to = setTimeout(function () {
            var v = $('#products_tree_search').val();
            $('#products_tree').jstree(true).search(v);
        }, 250);
    });

    $('#products_tree')
        .dblclick(function () {
            var data = $('#products_tree').jstree().get_selected(true)[0].children;

            console.log(data);
         })

        .bind("before.jstree", function (e, data) {
            // байндинг на событие перед загрузкой дерева
        })

        .jstree({
            "plugins" : [
                "themes","sort","json_data", "search"
            ],
            'core' : {
                "animation" : 1,
                'data' : {
                    "url" : "../../../../../../items",
                    "dataType" : "json",
                    'data': function (node) {
                        return { 'id': node.id };
                    }
                }
            }
        });
});

