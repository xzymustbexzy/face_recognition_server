function setParameters()
{
    $.ajax({
        "url":"./", 
        "type":"post",
        "data":{"resource":"parameters", "action":"get"},
        success:function(result){
            $("#main_body").html(result);
        }
    })
}

function loginedFace()
{
    $(window).attr('location','./loginedFace');
}

function chekcLog()
{
    alert('checkLog');
}

function image()
{
    alert('image');
}