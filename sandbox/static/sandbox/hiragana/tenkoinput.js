function TenkoInput() {
	this.events = {};
	this.listen();
}

TenkoInput.prototype.on = function(event, callback) {
  if (!this.events[event]) {
    this.events[event] = [];
  }
  this.events[event].push(callback);
};

TenkoInput.prototype.emit = function(event, data) {
  var callbacks = this.events[event];
  if (callbacks) {
    callbacks.forEach(function(callback) {
      callback(data);
    });
  }
};

TenkoInput.prototype.listen = function() {
	var self = this;
	var keyboard_map = {
		38: 0, // up
		39: 1, // right
		40: 2, // down
		37: 3, // left
		87: 0, // w
		68: 1, // d
		83: 2, // s
		65: 3  // a
	};

	document.addEventListener("keydown", function(event) {
		var mapped_key = keyboard_map[event.which];
		if (mapped_key !== undefined) {
			event.preventDefault();
			self.emit("move", mapped_key);
		}
	});

	document.getElementById("direction_space0").addEventListener("click", function(event) {
			event.preventDefault();
			self.emit("move", 0);
	});
	document.getElementById("direction_space1").addEventListener("click", function(event) {
			event.preventDefault();
			self.emit("move", 1);
	});
	document.getElementById("direction_space2").addEventListener("click", function(event) {
			event.preventDefault();
			self.emit("move", 2);
	});
	document.getElementById("direction_space3").addEventListener("click", function(event) {
			event.preventDefault();
			self.emit("move", 3);
	});

	this.bindOption("#mode_display", this.reverseMode);
	this.bindOption("#mode_reset", this.resetAll);
	this.bindOption("#status_level", this.levelJump);
};

TenkoInput.prototype.reverseMode = function (event) {
  event.preventDefault();
  this.emit("reverseMode");
};

TenkoInput.prototype.resetAll = function (event) {
  event.preventDefault();
  this.emit("resetGame");
};

TenkoInput.prototype.levelJump = function (event) {
	event.preventDefault();
	this.emit("skipLevels");
};

TenkoInput.prototype.bindOption = function (selector, fn) {
  var button = document.querySelector(selector);
  button.addEventListener("click", fn.bind(this));
  button.addEventListener(this.eventTouchend, fn.bind(this));
};
