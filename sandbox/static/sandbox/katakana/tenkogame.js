function TenkoGame(TenkoInput, TenkoStorage) {
	this.tenkoInput = new TenkoInput;		// monitors for user input
	this.tenkoStorage = new TenkoStorage;	// saved game state
	this.tc = new TenkoContent;				// preps tenbits/choices

	this.gp_question = document.querySelector("#question_space");
	this.score_update = document.querySelector("#score");
	this.level_update = document.querySelector("#level");
	this.streak_update = document.querySelector("#streak");
	this.reverse_update = document.querySelector("#reversemode");

	this.gp_answers = [];
	this.gp_answers[0] = document.querySelector(".answer_space0");
	this.gp_answers[1] = document.querySelector(".answer_space1");
	this.gp_answers[2] = document.querySelector(".answer_space2");
	this.gp_answers[3] = document.querySelector(".answer_space3");

	this.tenkoInput.on("move", this.move.bind(this));
	this.tenkoInput.on("reverseMode", this.reverseMode.bind(this));
	this.tenkoInput.on("resetGame", this.resetGame.bind(this));
	this.tenkoInput.on("skipLevels", this.skipLevels.bind(this));

	this.answerLoc = 0;				// 0: top, 1: right, 2: bottom, 3: left
	this.scoreTracker = 0;			// ++ for right, -- for wrong
	this.streakTracker = 0;			// how many right in a row
	this.level_leap = 20;			// how many right (score >0) to level++
	this.contentDirection = 0;		// 0: hiragana->A, 1: A->hiragana
	this.newQ = null;				// holds the question_holder <div>
	this.wrongFlag = false;			// if answer was wrong
	this.tenbitNow = this.tc.tenbits[this.currentQ];
	this.setup();
};

// if there's a previous game, recover it, otherwise start new
TenkoGame.prototype.setup = function() {
	var self = this;
	var previousState = self.tenkoStorage.getGameState();

	if (previousState) {	// reload previous variables
		self.scoreTracker = previousState.score;
		self.tc.current_level = previousState.level;
		self.streakTracker = previousState.streak;
		self.contentDirection = previousState.mode;
		self.level_leap = previousState.leap;
		self.tc.level_index_min = previousState.imin;
		self.tc.level_index_max = previousState.imax;
		self.level_update.textContent = self.tc.current_level;
		self.streak_update.textContent = self.streakTracker;
		self.score_update.textContent = self.scoreTracker;
	};
	self.addQA();		// start with new question
};

// save variables from current game
TenkoGame.prototype.tenkoSave = function () {
	var self = this;
	return {
		score:		self.scoreTracker,
		level:		self.tc.current_level,
		streak:		self.streakTracker,
		mode:		self.contentDirection,
		leap:		self.level_leap,
		imin:		self.tc.level_index_min,
		imax:		self.tc.level_index_max
	};
};

// write to middle tile what the ? element is + fill other tiles
TenkoGame.prototype.addQA = function() {
    var self = this;
    self.newQ = document.createElement("div");		// holder of ? tile
    self.newQ.id = "question_holder";
    self.gp_question.appendChild(self.newQ);

	// pick a random number in the level range that user is currently at
    var currentQ = Math.floor(Math.random() * (self.tc.level_index_max - self.tc.level_index_min + 1)) + self.tc.level_index_min;

	self.tenbitNow = self.tc.tenbits[currentQ];
	self.answerLoc = Math.floor(Math.random() * 4);	// location of right answer

	if (self.contentDirection == 0) {
		self.newQ.textContent = self.tenbitNow.a;
		self.gp_answers[self.answerLoc].textContent = self.tenbitNow.b;
	} else {
		self.newQ.textContent = self.tenbitNow.b;
		self.gp_answers[self.answerLoc].textContent = self.tenbitNow.a;
	};

	var plants = self.tc.makePlants(currentQ, self.contentDirection);
	for (var x = 0; x < 4; x++) {
		if (x != self.answerLoc) {
			self.gp_answers[x].textContent = plants[x];
		};
	};
};

TenkoGame.prototype.skipLevels = function() {
	var self = this;
	if (self.tc.current_level < 10) {
		self.tc.levelUp();
		self.level_update.textContent = self.tc.current_level;
		while (self.gp_question.firstChild) {
			self.gp_question.removeChild(self.gp_question.firstChild);
		};
		self.addQA();
	};
};

TenkoGame.prototype.resetGame = function(move_choice) {
	var self = this;
	self.tenkoStorage.clearGameState();
	while (self.gp_question.firstChild) {
		self.gp_question.removeChild(self.gp_question.firstChild);
	};
	self.tc.level_index_max = 4;
	self.tc.level_index_min = 0;
	self.level_leap = 20;
	self.scoreTracker = 0;
	self.score_update.textContent = self.scoreTracker;
	self.tc.current_level = 1;
	self.level_update.textContent = self.tc.current_level;
	self.streakTracker = 0;
	self.streak_update.textContent = self.streakTracker;
	self.addQA();
};

TenkoGame.prototype.reverseMode = function(move_choice) {
	var self = this;
	if (self.contentDirection == 0) {
		self.contentDirection = 1;
		self.reverse_update.textContent = "A";
	} else if (self.contentDirection == 1) {
		self.contentDirection = 0;
		self.reverse_update.textContent = "ア";
	};

	while (self.gp_question.firstChild) {
		self.gp_question.removeChild(self.gp_question.firstChild);
	};

	self.tc.level_index_max = 4;
	self.tc.level_index_min = 0;
	self.level_leap = 5;
	self.scoreTracker = 0;
	self.score_update.textContent = self.scoreTracker;
	self.tc.current_level = 1;
	self.level_update.textContent = self.tc.current_level;
	self.streakTracker = 0;
	self.streak_update.textContent = self.streakTracker;
	self.addQA();
};

TenkoGame.prototype.move = function(move_choice) {
	var element = document.getElementById('question_holder');
	var self = this;
	for (var x = 0; x < 4; x++) {
		if (x != self.answerLoc) {
			self.gp_answers[x].textContent = '';
		};
	};
	self.newQ.classList.toggle('moveLeft',false);
	self.newQ.classList.toggle('moveRight',false);
	self.newQ.classList.toggle('moveUp',false);
	self.newQ.classList.toggle('moveDown',false);
	self.gp_answers[move_choice].classList.toggle('correct',false);
	self.gp_answers[move_choice].offsetHeight;
	self.newQ.offsetHeight;

	if (move_choice == self.answerLoc) {
		self.gp_answers[move_choice].classList.toggle('correct',true);
		if (!self.wrongFlag) {
			self.tenbitNow.right++;
			self.scoreTracker++;
			self.streakTracker++;
		}
		switch(move_choice) {
		case 0:	// up
			self.newQ.classList.toggle('moveUp',true);
			self.wrongFlag = false;
			break;
		case 1:	// right
			self.newQ.classList.toggle('moveRight',true);
			self.wrongFlag = false;
			break;
		case 2:	// down
			self.newQ.classList.toggle('moveDown',true);
			self.wrongFlag = false;
			break;
		case 3:	// left
			self.newQ.classList.toggle('moveLeft',true);
			self.wrongFlag = false;
			break;
		default:
			break;
		}
	} else {
		self.tenbitNow.wrong++;
		if (self.scoreTracker > -100) {
			self.scoreTracker--;
		}
		self.wrongFlag = true;
		self.streakTracker = 0;
	};
	self.streak_update.textContent = self.streakTracker;
	self.score_update.textContent = self.scoreTracker;
	self.tenkoStorage.setGameState(self.tenkoSave());
	element.addEventListener('transitionend', function() {
	//self.move.addEventListener('webkitTransitionEnd', function() {
		while (self.gp_question.firstChild) {
			self.gp_question.removeChild(self.gp_question.firstChild);
		};
		if (self.scoreTracker >= self.level_leap) {
			self.tc.levelUp();
			self.level_update.textContent = self.tc.current_level;
			self.level_leap = self.scoreTracker + 20;
		}
		self.addQA();
	});
};
