$( document ).ready(function() {
	var Check_months = "";
	$(".advpayeemonth").each(function(){
		// add months in the 
	    var isChecked = $(this).is(':checked');
        if(isChecked){
        	Check_months = Check_months + $(this).val()+","; } 
	});
	
    Check_months = Check_months.slice(0, - 1); // strip out last element
	$( "#submitmonths" ).val(Check_months);

		$( ".advpayeemonth" ).on( "click", function(elem){
			var isChecked = $(this).is(':checked');
			if(isChecked){
				// Add the months for the renter in hidden field  
				var check_month_list = checkouttext(this);
				$( "#submitmonths" ).val(check_month_list);
				} else{
					// Remove the months for the renter in hidden field  
					var present_mounths = $( "#submitmonths" ).val();
					var list_present = present_mounths.split(",");
					var index = list_present.indexOf($(this).val());
					if (index > -1) {
						list_present.splice(index, 1);
					}
					$( "#submitmonths" ).val(list_present.join(","));	
			}
		}); 
			
});

function checkouttext(elem) {
	 // Add the months for the renter in hidden field  
	  var present_mounths = $( "#submitmonths" ).val();
	  var list_present = present_mounths.split(",");
	  if (present_mounths == ""){
		  return $(elem).val();  
	  }
	  else {
		  var dosenotexixts = true;
	    for (var i = 0; i < list_present.length; i++) {
	    	if($(elem).val() === list_present[i]){
	    		
	    		dosenotexixts = false; }	
	 } //for loop end
	    if(dosenotexixts){
	    	present_mounths = present_mounths + "," +$(elem).val()
	    }
	return present_mounths;
	  }
	}