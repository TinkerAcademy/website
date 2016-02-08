var __extends = (this && this.__extends) || function (d, b) {
    for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p];
    function __() { this.constructor = d; }
    d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
};

var Tutorial = (function () {
	function Tutorial(fs, terminal) {
		var _this = this;
		this._terminal = terminal;
		this._fs = fs;
	}
	return Tutorial;
}());

Tutorial.prototype.process = function(tutorial) {
	var fs = this._fs;
	var terminal = this._terminal;
	fs.readFile("/home/tutorials/" + tutorial + ".json", function (e, data) {
		var tut = jQuery.parseJSON(data);
		terminal.stdout(tut.description);
		terminal.showPrompt();
	});
}