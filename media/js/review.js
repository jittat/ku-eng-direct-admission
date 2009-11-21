function register_doc_recevied_toggle_click() {
    $(".doc-received-toggle").click(
	function() {
	    var url = $(this).attr("href");
	    var id = this.id.replace('doc-received-toggle-','');
	    $.get(url, function(data) {
		      $("#doc-received-status-" + id).text(data);    
		  });
	    return false;
	}
    );
}
