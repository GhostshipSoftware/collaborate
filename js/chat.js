/**
 * Collaborate Chat Api jquery plugin.
 * Written By: Geoff Brodniak
 * Date: 4/17/2013
 * This library serves as a resource for ajax calls to the collaborate api for use
 * in building client applications for the respective services.  All authentication
 * is done via token which is receive by passing a proper username/password combination
 * to the endpoint's token url.
 * */
function humanize_date_string(dstring){
     result = dstring.split('T');
     return result[1];
}
$(document).ready(function(){
    //maps to a send button somewhere that does the actual posting.
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
                var string = "<p class=\"chatp\">["+ data.sent + "] " + data.username + ": " + data.msg + "</p>";
                $("#chatbox" + channel).append(string);
                $("#msg"+channel).val("");
                $("#chatbox" + channel).animate({scrollTop: $("#chatbox" + channel).prop("scrollHeight") - $("#chatbox" + channel).height() });         
            }

        });
    }

    $("#create_channel_btn").click(function(){
        // modal button for opening the channel creation form
        // which currently looks like shit and probably will for a while longer.
        var channel_name = $("#channel_name").val();
        var channel_desc = $("#channel_desc").val()
        var channel_motd = $("#channel_motd").val()
        var user = $("#user").val()
            
        $.ajax({
            url: "https://collaborate.ghostship.org/channels/",
            type: 'POST',
            headers: {"Authorization": "Token " + $.cookie("token")},
            dataType: 'json',
            data: {"name": channel_name, "motd": channel_motd, "description": channel_desc, "account": $.cookie("account_id")},
            success: function(data){
                $("#lobby table").append('<tr><td>' + channel_name + '</td><td>' + channel_desc + '</td><td><button class="btn btn-small btn-success channel join" value="'+data.id+'">Join Channel</button> <button class="btn btn-small delete" value="'+data.id+'">Delete </button></td>');
                $("#cchannelmodal").modal('toggle');
            }
        });
    });

    
    function dismiss(event){ 
        channel = event.data.channel
        var user = $("#user").val()
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
                window.location.reload()
            }
        });
        
    }
 
    $(".join").click(function(){
        //The 'Join Channel' button is directly mapped to this.
        //so we send a join notice to the api and we are in.
        //this is obviously very bare bones. Later permissions
        //will need to be checked against the rooms perms etc.
        var channel = $(this).attr("value");
        var user = $("#user").val();
        $.ajax({
            url: "https://collaborate.ghostship.org/channels/" + channel + "/users/",
            type: 'POST',
            headers: {"Authorization":  "Token " + $.cookie("token")},
            dataType: 'json',
            data: {"user": user},
            success: function(data){
                if ( $("#"+channel).length) {
                    alert("You already have a tab to that channel open.");
                }else{
                /*
                    $("#chatroom_list").append('<li id="channel' + channel + '" class="channel"><a href="#' + channel + '" data-toggle="tab">Loading..</a></li>');
            $("#tabcontent").append('<div class="tab-pane" id="' + channel + '"> <div class="row"><div class="col-md-8"  id="chatbox' + channel + '" style="overflow-y: scroll; height: 400px;"></di><div id="motd' +channel+ '" style="position: fixed; margin-top: .2%; padding: 5px;" class="col-md-4 alert alert-info">MOTD: Loading...</div></div><div class="col-md-4" id="users' + channel + '"></div> </div><div class="row"><div class="container span9 form" id="form'+channel+'" style="margin-top: 1%;">  <input type="text" id="msg'+channel+'" style="margin-top: 2%;width: 85%; height: 2em;"> <input type="submit" class="btn btn-small btn-success" id="send'+channel+'" channel="'+channel+'"value="Send"><button class="btn btn-mini btn-danger" id=dismiss'+channel+'>Leave</button> <input type="hidden" id="user" value=' + user + '> <input type="hidden" id="channel'+channel+'" value=' + channel + '> </div></div>');
                */
                    window.location.replace('/chat/channel/?channel='+channel)
/*
                    $.cookie(channel, true, {expires: 1 });
                    $("#send"+channel).on("click", { channel: channel}, send);
                    $("#dismiss"+channel).on("click",{channel: channel},dismiss);
                    $.ajax({
                        url: "https://collaborate.ghostship.org/channels/" + channel + "/",
                        type: 'GET',
                        headers: {"Authorization": "Token " + $.cookie("token")},
                        dataType: 'json',
                        success: function(data){
                            $("#channel" + channel).html('<a href="#' + channel + '" data-toggle="tab">' + data.name + '</a>');
                            $("#users" + channel).html("<h4>Connected users:</h4>");
                            $("#motd"+ data.id).html("<strong>MOTD: "+data.motd);
                            $.each(data.users, function(i, item) {
                                $("#users" + channel).append('<p>'+ data.users[i] + '</p>');
                            });
                        }
                        });
                        $("#form"+channel).keydown(function(e) {
                            if  (e.keyCode==13){
                                $('#send'+channel).click();
                                return false;
                            } else {
                                 return true;
                            }
                        });
                    $("#chatbox" + channel).animate({scrollTop: $("#chatbox" + channel).prop("scrollHeight") - $("#chatbox" + channel).height() });
                    poll(channel);
    */
                }
            }
    });
    });

    $(".delete").click(function(){
        //delete a channel object.
        var channel = $(this).attr("value");
        $.ajax({
            url: "https://collaborate.ghostship.org/channels/" +channel+"/",
            type: "DELETE",
            headers: {"Authorization": "Token " + $.cookie("token")},
            dataType: "json",
            success: function(data){
                $("#chatroom_list #channel"+channel).remove();
                $("#tbl_channel"+channel).remove();
                $.removeCookie(channel)
            }
        });
    });
    

        
                     

    /**get_token()
        *when this function is called, it posts the username and password combination to the api
        *server and if a valid authentication receives a token in return.  This token must be included
        *in the request headers for ALL future calls.  If you write custom calls not contained in this
        *api bindings, you must authorize yourself first, then store the token and use it on every
        *call you write.
    **/    
    function get_token(){
        var creds = {"username": "admin", "password": "emorock", "csrfmiddlewaretoken": $.cookie("csrftoken")};
        $.ajax({
            url: "https://collaborate.ghostship.org/tokens/",
            type: 'POST',
            contentType: "application/json",
            dataType: 'json',
            headers: {"X-CSRFToken": $.cookie("csrftoken")},
            data:  JSON.stringify(creds),
            success: function(data){
                console.log(data)
                $.cookie("token", data.token, {expires: 1});
                $.cookie("account_id", data.account_id, {expires: 1});
            }
        });
    }
  
     
    //function check_connected_users(channel){
    //    $.ajax({
    //        url: "https://collaborate.ghostship.org/channels/"+channel+"/ 

    function poll(channel){
    //long comet type pulling that requests new messages from the chat api
    //server side there is a ton of 'm
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
                            var string = "<p class=\"chatp\" style=\"margin-left: 3%;\">["+ humanize_date_string(data[i].sent) + "] " + data[i].username + ": " + data[i].msg + "</p>";
                            $("#chatbox" + channel).append(string);
                        });  
                        if ($("#chatbox"+channel).height() == $("#chatbox"+channel).scrollTop() + 2){
                            console.log("i am animating")
                            $("#chatbox" + channel).animate({scrollTop: $("#chatbox" + channel).prop("scrollHeight") - $("#chatbox" + channel).height() });
                        }else{
                            console.log("nope")
                        }
                        //$.titleAlert("New Message!");
                    }
                }
            });
        }, 3000);
    }
    get_token();
    $(".channel").each(function(){
        channel = $(this).attr("value");
        if ($.cookie(channel) === 'true'){
            $("#chatroom_list").append('<li id="channel' + channel + '"><a href="#' + channel + '" data-toggle="tab">Loading..</a></li>');
 $("#tabcontent").append('<div class="tab-pane" id="' + channel + '"> <div class="row"><div class="col-md-8"  id="chatbox' + channel + '" style="overflow-y: scroll; padding-right: 10px; height: 400px;"><div id="motd' +channel+ '" style="margin-top: .2%; position: fixed; padding: 5px;" class="col-md-4 alert alert-info">MOTD: Loading...</div> </div><div class="col-md-4" id="users' + channel + '"></div> </div><div class="row"><div class="container span9" id="form'+channel+'" style="margin-top: 1%;"> <input type="text" id="msg'+channel+'" class="sender" data-channel='+channel+' style="margin-top: 2%;width: 85%; height: 2em;"> <button class="send btn btn-small btn-success" id="send'+channel+'" channel="'+channel+'">Send</button> <button class="btn btn-mini btn-danger" id=dismiss'+channel+'>Leave</button><input type="hidden" id="user" value=' + user + '> <input type="hidden" id="channel'+channel+'" value=' + channel + '> </div></div>');
            $("#send"+channel).on("click",{channel: channel}, send);
            $("#dismiss"+channel).on("click", {channel: channel}, dismiss);
            
            $.ajax({
                url: "https://collaborate.ghostship.org/channels/" + channel + "/",
                type: 'GET',
                headers: {"Authorization": "Token " + $.cookie("token")},
                dataType: 'json',
                success: function(data){
                    $("#channel" + data.id).html('<a href="#' + data.id + '" data-toggle="tab">' + data.name + '</a>');
                    $("#motd"+ data.id).html("<strong>MOTD: "+data.motd);
                    $("#users" + data.id).append("<h4>Connected users:</h4>");
                    $.each(data.users, function(i, item) {
                        $("#users" + data.id).append('<p>'+ data.users[i] + '</p>');
                    });
                  }
                });
                $("#msg"+channel).keypress(function(e) {
                      console.log("Setting up form "+this.id)
                      console.log("Setting up form "+this.getAttribute('data-channel'));
                      if  (e.keyCode==13){
                          $("#send"+this.getAttribute('data-channel')).click();
                          return false;
                      } else {
                          return true;
                      }
                });
            $("#chatbox" + channel).animate({scrollTop: $("#chatbox" + channel).prop("scrollHeight") - $("#chatbox" + channel).height() });
             poll(channel);
        }
    });
    //scroll that shit
    //$("#chatbox" + channel).animate({scrollTop: $("#chatbox" + channel).prop("scrollHeight") - $("#chatbox" + channel).height() });
});
