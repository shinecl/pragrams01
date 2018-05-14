function addshop(goods_id) {
    csrf = $('input[name="csrfmiddlewaretoken"]').val()
    $.ajax({
        url: '/usr/addgoods/',
        type: 'POST',
        data: {'goods_id': goods_id},
        dataType: 'json',
        headers: {'X-CSRFToken': csrf},
        success: function (msg) {
            $('#num_' + goods_id).html(msg.c_num)
            $('#sum').html(msg.total)
        },
        error: function (msg) {
            alert('请求失败')
        }
    })

}


function subshop(goods_id) {
    csrf = $('input[name="csrfmiddlewaretoken"]').val()
    $.ajax({
        url: '/usr/subgoods/',
        type: 'POST',
        data: {'goods_id': goods_id},
        dataType: 'json',
        headers: {'X-CSRFToken': csrf},
        success: function (msg) {

            $('#num_' + goods_id).html(msg.c_num)
            $('#sum').html(msg.total)
        },
        error: function (msg) {
            alert('请求失败')
        },

    })

}

function selectGoods(cart_id) {
    csrf = $('input[name="csrfmiddlewaretoken"]').val()
    $.ajax({
        url: '/usr/goodsel/',
        type: 'POST',
        data: {'cart_id': cart_id},
        dataType: 'json',
        headers: {'X-CSRFToken': csrf},
        success: function (msg) {
            if (msg.is_select) {
                s = '<span onclick="selectGoods(' + cart_id + ')">√</span>'
            } else {
                s = '<span onclick="selectGoods(' + cart_id + ')">X</span>'
            }
            if (msg.allsel) {
                m = '<span onclick="allSelectChange(1)">√</span>'
            } else {
                m = '<span onclick="allSelectChange(0)">X</span>'
            }
            $('#checkgoods_' + cart_id).html(s)
            $('#sum').html(msg.total)
            $('#changesel').html(m)

        },
        error: function (msg) {
            alert('请求失败')
        }
    })

}


function allSelectChange(all_select) {
    csrf = $('input[name="csrfmiddlewaretoken"]').val()
    $.ajax({
        url: '/usr/allselt/',
        type: 'POST',
        data: {'all_select': all_select},
        dataType: 'json',
        headers: {'X-CSRFToken': csrf},
        success: function (msg) {
            if (msg.allselt) {
                m = '<span onclick="allSelectChange(1)">√</span>'

            } else {
                m = '<span onclick="allSelectChange(0)">X</span>'
            }
            for (var i = 0; i < msg.carts_id.length; i++) {
                if (msg.allselt) {
                    s = '<span onclick="selectGoods(' + msg.carts_id[i] + ')">√</span>'
                } else {
                    s = '<span onclick="selectGoods(' + msg.carts_id[i] + ')">X</span>'
                }
                $('#checkgoods_' + msg.carts_id[i]).html(s)
            }
            $('#changesel').html(m)
            $('#sum').html(msg.total)

        },
        error: function (msg) {
            alert('请求失败')
        }
    })
}





