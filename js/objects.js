
function Channel(){
    urlbase = "https://collaborate.ghostship.org/";
    this.populate_object = function(channel_id){
        $.ajax({
            url: urlbase+"channels/"+channel_id+"/",
            type: 'GET',
            async: false,
            contentType: "application/json",
            dataType: 'json',
            headers: {"Authorization": "Token " + $.cookie('token')},
            success: function(data){
                obj_data = data;
            }

        });
        $.extend(this, obj_data);
    };


    this.add_user = function(user){
        rv = null
        $.ajax({
            url: "https://collaborate.ghostship.org/channels/" + this.id + "/users/",
            type: 'POST',
            async: false,
            headers: {"Authorization":  "Token " + $.cookie("token")},
            dataType: 'json',
            data: {"user": user},
            success: function(data){
                rv = true
            },
            error: function(data){
                rv = false
            },
        });
        return rv;
    };

        
    this.update = function(obj){
       rv = false
       json_obj = JSON.stringify(obj);
       $.ajax({
            url: urlbase+"channels/"+this.id+"/",
            type: "PUT",
            async: true,
            contentType: "application/json",
            dataType: 'json',
            data: json_obj,
            headers: {"Authorization": "Token " + $.cookie('token')},
            success: function(data){
                rv = true;
                return rv;
            },
            error: function(data){
                rv = false;
                return rv;
            }

        });
    }
}    
    
    
