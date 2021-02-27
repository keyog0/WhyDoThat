$(document).ready(function(){
    $('#email').change( function(e){
        var email = $('#email').val();
        console.log(email)
        if(email != ''){
  
           $.ajax({
              url: '/checkloginemail',
              type: 'post',
              data: {email: email},
              success: function(response){
                    if (response == "No User"){
                        $('#uname_response').html("User does not exist").css({'color':'red', 'text-align':'right'});
                        $('#button').prop('disabled', true);
                    }else{
                        $('#uname_response').html("");
                        $('#button').removeAttr('disabled');
                    }
               }
           });
        }else{
           $("#uname_response").html("");
        }
    })
})