function setParameters()
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
  alert("hello world")
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
