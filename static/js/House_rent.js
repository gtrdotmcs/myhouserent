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
	//date picker code javascript needed 'bootstrap-datepicker.js' 	
		$('#sandbox-container.input-append.date').datepicker({
			format: "yyyy-mm-dd",
			autoclose: true
		});
	DateAutogenetareonRneterCreation();	
			
});

function DateAutogenetareonRneterCreation(){
	var ispresent = $('input[name="Start_Rent_Date"]').val()
	if (ispresent == ""){
		var today = new Date();
		var dd = today.getDate();
		var mm = today.getMonth()+1; //January is 0!
		var yyyy = today.getFullYear();
	
		if(dd<10) {
		    day='0'+dd
		}else{
			day= dd
		} 
	
		if(mm<10) {
			
		    month='0'+mm
		}else{
			month = mm
		} 
	
		today = yyyy+'-'+month+'-'+day;
		//after 11 months
		if(mm > 1){
			if(mm<10) {		
				var mounthtoleavehouse = '0' + (mm -1) //January is 0!
			}else{
				var mounthtoleavehouse = mm -1
			} 
			if( dd < 29){
				if(dd<10) {
				    dayend='0'+dd
				}else{
					dayend= dd
				} 
			}else{
				dayend = '28' 
			}
			var yeartoleavehouse = yyyy+1;
			after11mounth = yeartoleavehouse+'-'+mounthtoleavehouse+'-'+dayend;	
		}else{
			after11mounth = yyyy+'-'+(mm+11)+'-'+'28';
		}
		$("input[name='Start_Rent_Date']").val(today);
		$('input[name="End_Rent_Date"]').val(after11mounth);
	}//for adding new renter joindate
}

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