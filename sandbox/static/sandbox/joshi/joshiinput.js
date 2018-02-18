function JoshiInput() {
	this.events = {};
	this.listen();
};

JoshiInput.prototype.on = function(event, callback) {
  if (!this.events[event]) {
    this.events[event] = [];
  }
  this.events[event].push(callback);
};

JoshiInput.prototype.emit = function(event, data) {
  var callbacks = this.events[event];
  if (callbacks) {
    callbacks.forEach(function(callback) {
      callback(data);
    });
  }
};

JoshiInput.prototype.listen = function() {
	var self = this;
	var keyboard_map = {
		65: 0, // a
		83: 1, // s
		68: 2, // d
		70: 3, // f
		49: 0, // 1
		50: 1, // 2
		51: 2, // 3
		52: 3 // 4
	};

	document.addEventListener("keydown", function(event) {
		var mapped_key = keyboard_map[event.which];
		if (mapped_key !== undefined) {
			event.preventDefault();
			self.emit("answerSelected", mapped_key);
		};
	});

	this.bindOption("#answer1", this.answerOne);
	this.bindOption("#answer2", this.answerTwo);
	this.bindOption("#answer3", this.answerThree);
	this.bindOption("#answer4", this.answerFour);
};

JoshiInput.prototype.answerOne = function() {
	event.preventDefault();
	this.emit("answerSelected", 0);
};

JoshiInput.prototype.answerTwo = function() {
	event.preventDefault();
	this.emit("answerSelected", 1);
};

JoshiInput.prototype.answerThree = function() {
	event.preventDefault();
	this.emit("answerSelected", 2);
};

JoshiInput.prototype.answerFour = function() {
	event.preventDefault();
	this.emit("answerSelected", 3);
};

JoshiInput.prototype.bindOption = function(selector, fn) {
	var button = document.querySelector(selector);
	button.addEventListener("click", fn.bind(this));
};
