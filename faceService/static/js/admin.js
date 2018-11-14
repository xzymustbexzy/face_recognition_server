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

    $.ajax({
        "url":"./",
        "type":"post",
        "data":data,
        success:function(result) {
            $("#main_body").html(result)
        }
    });
}
