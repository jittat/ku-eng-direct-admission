
var MajorSelection = {

    maxRank: 0,

    shiftSelection: function(rank, myself) {
	var sels = new Array();
	$("select").each(function(i) {
	    if(this != myself)
		sels[Number(this.value)] = this;
	});
	var bump = rank;
	while(sels[bump]!=null) {
	    if(bump != MajorSelection.maxRank)
		sels[bump].value = String(bump+1);
	    else
		sels[bump].value = '--';
	    bump++;
	}
    }

};
