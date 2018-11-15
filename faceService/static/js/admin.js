function parameters()
{
    $.ajax({
        "url":"./",
        "type":"post",
        "data":{"resource":"parameters", "action":"get"},
        success:function(result){
            $("#main_body").html(result);
        }
    });
}

function loginedFace()
{
    $.ajax({
        "url":"./",
        "type":"post",
        "data":{"resource":"loginedFace", "action":"get"},
        success:function(result) {

            $("#main_body").html(result);
        }
    });
}

function chekcLog()
{
    alert('checkLog');
}

function image()
{
    alert('image');
}

function setParameters()
{
    var data = {};
    data["resource"] = "parameters";
    data["action"] = "post";
    var t = $('form').serializeArray();
    $.each(t, function() {
        data[this.name] = this.value;
    });

    alert("成功修改参数!")

    $.ajax({
        "url":"./",
        "type":"post",
        "data":data,
        success:function(result) {
            $("#main_body").html(result)
        }
    });
}


//显示图片
function displayImg(img_id) {
    var event =  window.event || arguments.callee.caller.arguments[0];//兼容火狐浏览器

    img_id = "img_" + img_id;
    var img = document.getElementById(img_id);
    var x = event.clientX + document.body.scrollLeft + 20;
    var y = event.clientY + document.body.scrollTop - 5;
    img.style.left = x + "px";
    img.style.top = y + "px";
    img.style.display = "none";
}

//图片消失
function vanishImg(img_id){
    img_id = "img_" + img_id;
    var img = document.getElementById(img_id);
    img.style.display = "none";
}
