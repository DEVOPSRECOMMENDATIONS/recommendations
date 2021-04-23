 $(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#id").val(res.id);
        $("#product_a").val(res.product_a);
        $("#product_b").val(res.product_b);
        $("#recom_type").val(res.recom_type);
        $("#likes").val(res.likes);
    }

    /// Clears all form fields
    function clear_form_data() {
        $("#product_a").val("");
        $("#product_b").val("");
        $("#recom_type").val("");
        $("#likes").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    // ****************************************
    // Create a recommendation
    // ****************************************

    $("#create-btn").click(function () {

        var product_a = $("#product_a").val();
        var product_b = $("#product_b").val();
        var recom_type = $("#recom_type").val();
        var likes = $("#likes").val();

        var data = {
            "product_a": product_a,
            "product_b": product_b,
            "recom_type": recom_type,
            "likes": parseInt(likes)
        };

        var ajax = $.ajax({
            type: "POST",
            url: "/recommendations",
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });


    // ****************************************
    // Update a Recommendation
    // ****************************************

    $("#update-btn").click(function () {

        var recomm_id = $("#id").val();
        var product_a = $("#product_a").val();
        var product_b = $("#product_b").val();
        var recom_type = $("#recom_type").val();
        var likes = $("#likes").val();

        var data = {
            "product_a": product_a,
            "product_b": product_b,
            "recom_type": recom_type,
            "likes": likes
        };

        var ajax = $.ajax({
                type: "PUT",
                url: "/recommendations/" + recomm_id,
                contentType: "application/json",
                data: JSON.stringify(data)
            })

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Like a Recommendation
    // ****************************************

    $("#like-btn").click(function () {

        var recomm_id = $("#id").val();
        var product_a = $("#product_a").val();
        var product_b = $("#product_b").val();
        var recom_type = $("#recom_type").val();
        var likes = $("#likes").val();

        var data = {
            "product_a": product_a,
            "product_b": product_b,
            "recom_type": recom_type,
            "likes": likes
        };

        var ajax = $.ajax({
                type: "PUT",
                url: "/recommendations/"+ recomm_id+ "/likes",
                contentType: "application/json",
                data: JSON.stringify(data)
            })
            
        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    })


    // ****************************************
    // Retrieve a Recommendation
    // ****************************************

    $("#retrieve-btn").click(function () {

        var id = $("#id").val();
        var ajax = $.ajax({
            type: "GET",
            url: "/recommendations/" + id,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Delete a Recommendation
    // ****************************************

    $("#delete-btn").click(function () {

        var id = $("#id").val();

        var ajax = $.ajax({
            type: "DELETE",
            url: "/recommendations/" + id,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_form_data()
            flash_message("Recommendation has been Deleted!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        $("#id").val("");
        clear_form_data()
    });

    // ****************************************
    // Search for a Recommendation
    // ****************************************

    $("#search-btn").click(function () {

        var product_a = $("#product_a").val();
        var product_b = $("#product_b").val();
        var recom_type = $("#recom_type").val();
        var likes = $("#likes").val();

        var queryString = ""
        
        if (product_a) {
            queryString += 'product_a=' + product_a
        }

        if (product_b) {
            if (queryString.length > 0) {
                queryString += '&product_b=' + product_b
            } else {
                queryString += 'product_b=' + product_b
            }
        }

        if (recom_type) {
            if (queryString.length > 0) {
                queryString += '&recom_type=' + recom_type
            } else {
                queryString += 'recom_type=' + recom_type
            }
        }
        if (likes) {
            if (queryString.length > 0) {
                queryString += '&likes=' + likes
            } else {
                queryString += 'likes=' + likes
            }
        }

        var ajax = $.ajax({
            type: "GET",
            url: "/recommendations?" + queryString,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            $("#search_results").empty();
            $("#search_results").append('<table class="table-striped" cellpadding="10">');
            var header = '<tr>'
            header += '<th style="width:5%">ID</th>'
            header += '<th style="width:5%">Product A</th>'
            header += '<th style="width:5%">Product B</th>'
            header += '<th style="width:5%">Recommendation Type</th>'
            header += '<th style="width:5%">Likes</th></tr>'
            $("#search_results").append(header);
            var firstRec = "";
            for(var i = 0; i < res.length; i++) {
                var recommendation = res[i];
                var row = "<tr><td>"+recommendation.id+"</td><td>"+recommendation.product_a+"</td><td>"+recommendation.product_b+"</td><td>"+recommendation.recom_type+"</td><td>"+recommendation.likes+"</td></tr>";
                $("#search_results").append(row);
                if (i == 0) {
                    firstRec = recommendation;
                }
            }

            $("#search_results").append('</table>');

            // copy the first result to the form
            if (firstRec != "") {
                update_form_data(firstRec)
            }

            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

})
