    $(document).ready(function(){
		$('#email').keyup( function(e){
            var email = $('#email').val();

            if(email != ''){
      
               $.ajax({
                  url: '/checkemail',
                  type: 'post',
                  data: {email: email},
                  success: function(response){
                        if (response == "Available"){
                      $('#uname_response').html(response).css({'color':'blue', 'text-align':'right'});
                      $('#button').removeAttr('disabled');
                        }else{
                            $('#uname_response').html(response).css({'color':'red', 'text-align':'right'});
                        }
                   }
               });
            }else{
               $("#uname_response").html("");
            }
		})
	})