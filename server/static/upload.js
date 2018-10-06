alert("hello world");

$("#login").click(function(){
        alert("hello world");
    }
);


/*
      $("input[name="login"]").click(function() {

        $.ajax(
            type:"POST",
            url:"http://0.0.0.0:5050/faceService/addFaces",
            contentType:"application/json;charset=utf-8"
            data:JSON.stringify(GetJsonData()),
            dataType:"json",
            success: function(message) {
                alert("success");
            }
            error: function(message) {
                alert("failed");
            }
        );
        }
    )

    function GetJsonData() {

        var json = {
            "methodName":"setParameters",
            "cId":"330283199710244712",
            "cName":"xiaoziyang",
            "cType":"gonghao",
            "img":"",
            "channel":"pc"
        }
        return json;

    }
*/