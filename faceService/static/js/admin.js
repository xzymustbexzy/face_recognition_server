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

    $.ajax({
        "url":"./",
        "type":"post",
        "data":JSON.stringify(data),
        success:function(result) {
            $("#main_body").html(result)
        }
    });
}
