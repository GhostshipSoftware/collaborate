$(document).ready(function(){    

    function poll(channel) {
        setTimeout(function(){
            $.ajax({
                url: "https://collaborate.ghostship.org/channels/" + channel + "/messages/",
                type: 'GET',
                dataType: 'json',
                complete: poll(channel),
                headers: {"Authorization": "Token " + $.cookie("token")},
                success: function(data){
                    if (typeof this != 'undefined'){
                           $(this).remove();
                        };
                    if (data.response == "No msgs"){
                        console.log(data.response)
                        return false;
                    }else{
                        $("#chatbox"+channel+" .chatp").remove();
                        $.each(data, function(i, item){
                            var string = "<p class=\"chatp\">["+ humanize_date_string(data[i].sent) + "] <strong>"+ data[i].username +"</strong>: " + data[i].msg + "</p>";
                            $("#chatbox" + channel).append(string);
                        });
                        if ($("#chatbox"+channel).height() == $("#chatbox"+channel).scrollTop() - 2){
                            $("#chatbox" + channel).animate({scrollTop: $("#chatbox" + channel).prop("scrollHeight") - $("#chatbox" + channel).height() });
                        }else{
                            console.log("nope")
                        }
                    }
                }
            });
            $.ajax({
                    url: "https://collaborate.ghostship.org/channels/" + channel + "/",
                    type: 'GET',
                    headers: {"Authorization": "Token " + $.cookie("token")},
                    dataType: 'json',
                    success: function(data){
                            $("#users" + channel).html('')    
                            $("#users" + channel).html("<h4>Connected users:</h4>");
                            $.each(data.users, function(i, item) {
                                $("#users" + channel).append('<p>'+ data.users[i] + '</p>');
                            });
                        }
           });
}, 3000);
    }

    function send(event){
        var sender = $("#user").val(); 
        var channel = event.data.channel; 
        var msg = $("#msg"+channel).val(); 
        $.ajax({
            url: "https://collaborate.ghostship.org/channels/" + channel +"/messages/",
            type: 'POST',
            headers: {"Authorization": "Token " + $.cookie("token")},
            dataType: 'json',
            data: {"msg": msg, "sender": sender, "channel": channel},
            success: function(data){
                data.sent = data.sent.slice(0, -4);
                var string = "<p class=\"chatp\">["+ humanize_date_string(data.sent) + "] " + "<strong>"+data.username +"</strong>"+ ": " + data.msg + "</p>";
                $("#chatbox" + channel).append(string);
                $("#msg"+channel).val("");
                $("#chatbox" + channel).animate({scrollTop: $("#chatbox" + channel).prop("scrollHeight") - $("#chatbox" + channel).height() });                        }

        });
    }

    function dismiss(event){
        var channel = event.data.channel;
        var user = $("#user").val();
        $.ajax({
            url: "https://collaborate.ghostship.org/channels/" +channel+"/remove/",
            type: "POST",
            headers: {"Authorization":  "Token " + $.cookie("token")},
            dataType: 'json',
            data: {"user": user},
            success: function(data){
                $('#'+channel).empty();
                $('#'+channel).remove();
                $("#channel"+channel).remove();
                $('#lobbyli').addClass("active");
                $('#lobby').addClass("active");
                $.removeCookie(channel);
                window.location.replace("/chat/");
            }
        });

    }

    var channel = $("#channel").attr("value");
    var user = $("#user").val();
    $.ajax({
        url: "https://collaborate.ghostship.org/channels/" + channel + "/users/",
        type: 'POST',
        headers: {"Authorization":  "Token " + $.cookie("token")},
        dataType: 'json',
        data: {"user": user},
        success: function(data){
                $.cookie(channel, true, {expires: 1 });
                $("#send").on("click", { channel: channel}, send);
                $("#dismiss").on("click", { channel: channel }, dismiss);
                $.ajax({
                    url: "https://collaborate.ghostship.org/channels/" + channel + "/",
                    type: 'GET',
                    headers: {"Authorization": "Token " + $.cookie("token")},
                    dataType: 'json',
                    success: function(data){
                            $("#channel" + channel).html('<a href="#' + channel + '" data-toggle="tab">' + data.name + '</a>');
                            $("#users" + channel).html("<h4>Connected users:</h4>");
                            $("#motd"+ data.id).html("<i>"+data.motd+"</i>");
                            $("#title").html(data.name);
                            $.each(data.users, function(i, item) {
                                $("#users" + channel).append('<p>'+ data.users[i] + '</p>');
                            });
                        }
                        });
                        $("#form").keydown(function(e) {
                            if  (e.keyCode==13){
                                $('#send').click();
                                return false;
                            } else {
                                 return true;
                            }
                        });
                    $("#chatbox" + channel).animate({scrollTop: $("#chatbox" + channel).prop("scrollHeight") - $("#chatbox" + channel).height() });
                    poll(channel);
                }
            });

});


