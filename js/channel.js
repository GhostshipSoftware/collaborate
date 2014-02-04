$(document).ready(function(){    

    lastmsg = null 
    first_poll = true
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
                            $("#chatbox"+channel).animate({scrollTop: $("#chatbox"+channel).prop("scrollHeight") - $("#chatbox"+channel).height() });
                        }
                    }
                    console.log(lastmsg)
                    if (lastmsg != null){
                        console.log(data[data.length - 1].id)
                        if (lastmsg != data[data.length - 1].id){
                            $.titleAlert("New Message", {requireBlur:true});
                        }
                    }
                    lastmsg = data[data.length - 1].id
                },
                complete: function(data){
                    if (first_poll == true){
                        $("#chatbox"+channel).animate({scrollTop: $("#chatbox"+channel).prop("scrollHeight") - $("#chatbox"+channel).height() });
                        first_poll = false
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
                $("#chatbox"+channel).append(string);
                $("#msg"+channel).val("");
                $("#chatbox"+channel).animate({scrollTop: $("#chatbox" + channel).prop("scrollHeight") - $("#chatbox" + channel).height() });                        }

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

    //magical channel object.
    cobj = new Channel()
    cobj.populate_object(channel)
    //add the user, the api makes sure to not double add, and this
    //serves as a boolean indicator of whether things went ok or failed.
    rv = cobj.add_user(user) 
    if (rv == true){ 
        $.cookie(channel, true, {expires: 1 });
        $("#send").on("click", { channel: channel}, send);
        $("#dismiss").on("click", { channel: channel }, dismiss);
        $("#users"+channel).html('');
        $("#motd"+ cobj.id).html("<i>"+cobj.motd+"</i>");
        $("#title").html(cobj.name);
        $.each(cobj.users, function(i, item) {
            $("#users" + channel).append('<p>'+ cobj.users[i] + '</p>');
        });
        $("#form").keydown(function(e) {
           if  (e.keyCode==13){
               $('#send').click();
               return false;
           } else {
               return true;
           }
        });
        poll(channel)
    }else{
        // do something clever to say hey there was an error.
        //  
        return
    }

});


