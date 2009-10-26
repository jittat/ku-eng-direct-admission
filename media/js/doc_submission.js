// mainly taken from django snippet http://www.djangosnippets.org/snippets/679/

var DocSubmission = {

    // Generate 32 char random uuid 
    genUuid: function() {
	var uuid = ""
	    for (var i=0; i < 32; i++) {
		uuid += Math.floor(Math.random() * 16).toString(16); 
	    }
	return uuid
    },

    handleFormSubmit: function(this_form, field_name) {
        // Prevent multiple submits
        if (jQuery.data(this_form, 'submitted'))
	    return false;

        var freq = 100; // freqency of update in ms
        var uuid = DocSubmission.genUuid(); // id for this upload so we can fetch progress info.
        
	var progress_url = '/doc/progress/'; // ajax view serving progress info

        // Append X-Progress-ID uuid form action
        this_form.action += (
	    (this_form.action.indexOf('?') == -1 ? '?' : '&') + 
		'X-Progress-ID=' + uuid);
        
        var $progress = ($('#upload-progress-' + field_name)
			 .append('<div class="progress-container">' +
				 '<span class="progress-info">' +
				 'uploading 0%' +
				 '</span>' +
				 '<div class="progress-bar">' +
				 '<div class="progress-indicator"></div>' +
				 '</div>' +
				 '</div>'));
	var $input_control = $("#upload-form-" + field_name + " input");
	$input_control.hide();
        // Update progress bar
	function update_progress_info() {
            $progress.show();
            $.getJSON(progress_url, 
		      {'X-Progress-ID': uuid}, 
		      function(data, status){
			  if (data) {
			      var progress = parseInt(data.uploaded) / parseInt(data.length);
			      if(progress>1)
				  progress = 1;
			      var width = $progress.find('.progress-container').width()
			      var progress_width = width * progress;
			      $progress.find('.progress-indicator').width(progress_width);
			      $progress.find('.progress-info').text('uploading ' + parseInt(progress*100) + '%');
			  }
			  if(!data.finished) 
			      window.setTimeout(update_progress_info, freq);
			  else {
			      $progress.hide();
			      $input_control.show();
			  }
		      });
        };
        window.setTimeout(update_progress_info, freq);
	
        jQuery.data(this_form, 'submitted', true); // mark form as submitted.
    }
};
