$(function() {

    // Submit post on submit
    $('#post-form').on('submit', function(event){
        event.preventDefault();
        $(".loading").fadeOut("slow");
        console.log("form submitted!")  // sanity check
        textprocess();
    });

    // AJAX for posting
    function create_post() {
        console.log("create post is working!") // sanity check
        $.ajax({
            url : "create_post/", // the endpoint
            type : "POST", // http method
            data : { the_post : $('#post-text').val() }, // data sent with the post request
            // handle a successful response
            success : function(json) {
                // $('#post-text').val(''); // remove the value from the input
                console.log(json); // log the returned json to the console
                //$("#talk").prepend("<li><strong>"+json.text+"</strong> - <em> "+json.author+"</em> - <span> "+json.created+
                //    "</span> - <a id='delete-post-"+json.postpk+"'>delete me</a></li>");
                $("#talk").prepend("<label>"+json.result+"</label>");
                console.log("success"); // another sanity check
            },
            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    };

    $('#loadpage').click(function () {
        $.ajax({
            url: "/browsing",
            type: "get",
            success: function (data) {
                var testing = "<iframe width='940px' height='600px' src="+$('#post-text').val()+"></iframe>"
                $("#talk").html("<div class='row white'><div class='columns large-12'><div style='margin-left:20px' id='talk'></div>");
                $("#talk").prepend(testing).slideDown();
            },
            error: function (data) {
                alert("Error. " + "Status: " + data.status + " Text: " + data.statusText);
            }
        });
    });
    function textprocess() {
        if($('.text').prop("checked") == true && $('.image').prop("checked") == false){
        $("#talk").html("<center><img src='http://202.169.224.53/static/loading.gif'/></center>")
        $.ajax({
            url: "text_process/",
            type: "POST",
            data : { the_post : $('#post-text').val() }, // data sent with the post request
            success: function (json) {
                console.log("berhasil")
                var testing = "<h4>Total word in website: "+json.jumlahteks+"</h4><br><h4>Total negative word in website: "+json.jumlahteksporno+"</h4><br><h4>"+json.keputusan+"</h4><iframe width='940px' height='600px' src="+json.hasil+"></iframe>"
                $("#talk").html("<div class='row white'><div class='columns large-12'><div style='margin-left:20px' id='talk'></div>");
                $("#talk").prepend(testing);
            },
            error : function(xhr,errmsg,err) {
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
      }
      else if($('.image').prop("checked") == true && $('.text').prop("checked") == false){
        $("#talk").html("<center><img src='http://202.169.224.53/static/loading.gif'/></center>")
        $.ajax({
            url: "image_process/",
            type: "POST",
            data : { the_post : $('#post-text').val() }, // data sent with the post request
            success: function (json) {
                console.log("berhasil")
                //var testing = "<h4>Total image in website: "+json.jumlahgambar+"</h4><br><h4>Total negative image in website: "+json.jumlahgambarporno+"</h4><br><h4>Fusion decision factor: "+json.decisionfactor+"</h4><br><h4>"+json.keputusan+"</h4><br><h5>Decision factor above 1 is negative site</h5><iframe width='940px' height='600px' src="+json.hasil+"></iframe>"
                var testing = "<h4>Fusion decision factor: "+json.decisionfactor+"</h4><br><h4>"+json.keputusan+"</h4><br><h5>Decision factor above 1 is negative site</h5><iframe width='940px' height='600px' src="+json.hasil+"></iframe>"
                $("#talk").html("<div class='row white'><div class='columns large-12'><div style='margin-left:20px' id='talk'></div>");
                $("#talk").prepend(testing);
            },
            error : function(xhr,errmsg,err) {
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
      }
      else if($('.text').prop("checked") == true && $('.image').prop("checked") == true){
        $("#talk").html("<center><img src='http://202.169.224.53/static/loading.gif'/></center>")
        $.ajax({
            url: "text_image_process/",
            type: "POST",
            data : { the_post : $('#post-text').val() }, // data sent with the post request
            success: function (json) {
                console.log("berhasil")
                //var testing = "<h4>Total image in website: "+json.jumlahgambar+"</h4><br><h4>Total negative image in website: "+json.jumlahgambarporno+"</h4><br><h4>Fusion decision factor: "+json.decisionfactor+"</h4><br><h4>"+json.keputusan+"</h4><br><h5>Decision factor above 1 is negative site</h5><iframe width='940px' height='600px' src="+json.hasil+"></iframe>"
                var testing = "<h4>Fusion decision factor: "+json.decisionfactor+"</h4><br><h4>"+json.keputusan+"</h4><br><h5>Decision factor above 1 is negative site</h5><iframe width='940px' height='600px' src="+json.hasil+"></iframe>"
                $("#talk").html("<div class='row white'><div class='columns large-12'><div style='margin-left:20px' id='talk'></div>");
                $("#talk").prepend(testing);
            },
            error : function(xhr,errmsg,err) {
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
      }
      else if($('.video').prop("checked") == true){
        $("#talk").html("<center><img src='http://202.169.224.53/static/loading.gif'/></center>")
        $.ajax({
            url: "video_process/",
            type: "POST",
            data : { the_post : $('#post-text').val() }, // data sent with the post request
            success: function (json) {
                console.log("berhasil")
                //var testing = "<h4>Total image in website: "+json.jumlahgambar+"</h4><br><h4>Total negative image in website: "+json.jumlahgambarporno+"</h4><br><h4>Fusion decision factor: "+json.decisionfactor+"</h4><br><h4>"+json.keputusan+"</h4><br><h5>Decision factor above 1 is negative site</h5><iframe width='940px' height='600px' src="+json.hasil+"></iframe>"
                var testing = "<h4>"+json.keputusan+"</h4><br><iframe width='940px' height='600px' src="+json.hasil+"></iframe>"
                $("#talk").html("<div class='row white'><div class='columns large-12'><div style='margin-left:20px' id='talk'></div>");
                $("#talk").prepend(testing);
            },
            error : function(xhr,errmsg,err) {
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
      }
    };
    // This function gets cookie with a given name
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    /*
    The functions below will create a header with csrftoken
    */

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

});
