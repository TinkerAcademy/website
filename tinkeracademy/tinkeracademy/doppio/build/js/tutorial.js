var __extends = (this && this.__extends) || function (d, b) {
    for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p];
    function __() { this.constructor = d; }
    d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
};

var Tutorial = (function () {
	function Tutorial(fs, terminal, control) {
		this._terminal = terminal;
		this._control = control;
		this._fs = fs;
		this._pendingControls = [];
	}
	return Tutorial;
}());

Tutorial.prototype.process = function(tutorial) {
	var _this = this;
	var fs = this._fs;
	var terminal = this._terminal;
	var control = this._control;
	var pendingControls = this._pendingControls;
	fs.readFile("/home/tutorials/" + tutorial + ".json", function (e, data) {
		terminal.stdout("\u00A9 Tinker Academy 2015\n\n");
		var tut = jQuery.parseJSON(data);
		_this._tutorial = tut;
		terminal.stdout(tut.title);
		var lines = tut.lines;
		var controls = tut.controls;
		var output = tut.output;
		var events = tut.events;
		var event;
		var eventID;
		for (eventID in events) {
			event = events[eventID];
			switch(event.name) {
				case "$load":
					var i;
					var ref;
					for (i = 0; i < event.lines.length; i++) {
						ref = event.lines[i];
						var line = lines[ref];
						terminal.stdout(line);
					}
					for (i = 0; i < event.controls.length; i++) {
						ref = event.controls[i];
						pendingControls.push(ref);
					}
					if (event.showPrompt) {
						terminal.showPrompt();
					}
					break;
				default:
					break;
			}
		}
	});
}

Tutorial.prototype.click = function(name) {
	var terminal = this._terminal;
	var tut = this._tutorial;
	var lines = tut.lines;
	var controls = tut.controls;
	var output = tut.output;
	var events = tut.events;
	var pendingControls = this._pendingControls;
	var idx;
	var jdx;
	var ref;
	var control;
	var event;
	var line;
	for (idx in pendingControls) {
		ref = pendingControls[idx];
		control = controls[ref];
		switch (control.name) {
			case "Save":
				event = events[control.event];
				for (jdx in event.lines) {
					ref = event.lines[jdx];
					line = lines[ref];
					terminal.stdout(line);
				}
				if (event.showPrompt) {
						terminal.showPrompt();
				}
				break;
			case "Redo":
				break;
			default:
				break;
		}
	}
}