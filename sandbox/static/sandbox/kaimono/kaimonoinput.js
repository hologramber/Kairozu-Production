function KaimonoInput() {
  this.events = {};
  this.listen();
};

KaimonoInput.prototype.on = function(event, callback) {
  if (!this.events[event]) {
    this.events[event] = [];
  }
  this.events[event].push(callback);
};

KaimonoInput.prototype.emit = function(event, data) {
  var callbacks = this.events[event];
  if (callbacks) {
    callbacks.forEach(function(callback) {
      callback(data);
    });
  }
};

KaimonoInput.prototype.listen = function() {
	var self = this;
	document.addEventListener("keydown", function(event) {
		if (event.keyCode == 13) {
			event.preventDefault();
			self.emit("submitted");
		};
	});

  this.bindOption("#kanjikana", this.switchChars);
};

KaimonoInput.prototype.switchChars = function() {
  event.preventDefault();
  this.emit("switcheroo");
};

KaimonoInput.prototype.bindOption = function (selector, fn) {
  var button = document.querySelector(selector);
  button.addEventListener("click", fn.bind(this));
};
