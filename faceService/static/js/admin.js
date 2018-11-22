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

function loginedFace(page_id)
{
    var page_id = page_id ? page_id : 1;
    $.ajax({
        "url":"./",
        "type":"post",
        "data":{"resource":"loginedFace", "action":"get", "page_id":page_id},
        success:function(result) {
            $("#main_body").html(result);
        }
    });

    var init_total_page_num = function() {
      var total_page_num_label = document.getElementById("total_page_num");
      if (total_page_num_label == null || total_page_num_label == undefined) {
        setTimeout(init_total_page_num, 100);
      }
      else {
        total_page_num = parseInt(total_page_num_label.innerHTML);
      }
    }


    init_total_page_num();
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
    var x = event.clientX + document.body.scrollLeft -600;
    var y = event.clientY + document.body.scrollTop - 5;
    img.style.left = x + "px";
    img.style.top = y + "px";
    img.style.display = "block";
}

//图片消失
function vanishImg(img_id){
    img_id = "img_" + img_id;
    var img = document.getElementById(img_id);
    img.style.display = "none";
}


var page_num = 1;
var total_page_num = 0;
function firstPage() {
    turnToPage(1);
}

function previousPage() {
    if (page_num == 1) {
        alert("已经到第一个了！");
        return;
    }
    turnToPage(page_num - 1);
}

function nextPage() {
    if (page_num == total_page_num) {
        alert("已经到最后一页了！");
        return;
    }
    turnToPage(page_num + 1);
}

function lastPage() {
    turnToPage(total_page_num);
}

function turnToPage(page_num_to_set) {
    var page_num_to_set = page_num_to_set ? page_num_to_set : document.getElementById("page_to_set").value;
    page_num = page_num_to_set;
    loginedFace(page_num_to_set);
    setNearPages();
}

function setNearPages() {
    var near_pages = new Array(5);
    for (var i = -2; i < 3; i++) {
        if (i + page_num < 1)
            continue;
        near_pages.push(page_num + i);
    }
    var near_page_html = "";
    for (var page in near_pages) {
        near_page_html += "<a";
        near_page_html += " href=\"javascript:turnToPage('" + page.toString() + "')\"";
        near_page_html += ">";
        near_page_html += (" " + page.toString() + " ");
        near_page_html += "</a>";
    }
    $("#near_pages").html(near_page_html);
}
