function Joshi(JoshiInput) {
	this.JoshiInput = new JoshiInput;		// monitors for user input
	this.whichSentence = 0;
	this.correctPosition = 0;

	this.sentences = ['明日＿日曜日です。',
										'鯨＿魚ではありません。',
										'あそこに郵便局＿あります。',
										'雨＿降っている。',
										'これは桜です。これ＿桜です。',
										'私はすし＿てんぷら＿好きです。',
										'ポールさん＿リーさんはフランス人です。',
										'りんご＿みかん＿どちらが好きですか。',
										'これはだれの傘です＿。',
										'明日のパーティに行きます＿。'];
	this.sentenceAnswer = [0,0,1,1,2,2,5,5,10,10];
	this.sentencesTranslation = ['Tomorrow is Sunday.',
															 'The whale is not a fish.',
															 'There\'s a post office over there.',
															 'It\'s raining.',
															 'This is a cherry tree. This is also a cherry tree.',
															 'I like both sushi and tempura.',
															 'Paul and Lee are French.',
															 'Which do you like better, apples or mandarin oranges?',
															 'Whose umbrella is this?',
															 'Are you going to the party tomorrow?'];
	this.particleBox = ['は','が','も','ても','でも','と','とは','や','とか','など','か','で','に','へ','から','まで','の','を',
											'ね','よ','わ','かな','かしら','な','さ','こと'];
	this.otherAnswers = [];

	this.currentScore = 0;
	this.currentStreak = 0;

	this.JoshiInput.on("answerSelected", this.pickAnswer.bind(this));

	this.sentenceBox = document.querySelector('.sentence_container');
	this.translationBox = document.querySelector('.translation_container');
	this.scoreHolder = document.querySelector('.score_update');
	this.streakHolder = document.querySelector('.score_streak');
	this.particleBox1 = document.querySelector('#answer1');
	this.particleBox2 = document.querySelector('#answer2');
	this.particleBox3 = document.querySelector('#answer3');
	this.particleBox4 = document.querySelector('#answer4');
	this.newItems();
	this.newQuestion();
};

Joshi.prototype.newQuestion = function() {
	var self = this;
	self.sentenceBox.textContent = self.sentences[self.whichSentence];
	self.translationBox.textContent = self.sentencesTranslation[self.whichSentence];
};

Joshi.prototype.newItems = function() {
	var self = this;
	self.whichSentence = Math.floor((Math.random() * 10));
	self.correctPosition = Math.floor((Math.random() * 4));
	var tempBox = self.particleBox.slice(0);
	tempBox.splice(self.sentenceAnswer[self.whichSentence], 1);
	for (i = 0; i < 3; i++) {
		var randomAnswer = Math.floor((Math.random() * tempBox.length));
		self.otherAnswers[i] = tempBox[randomAnswer];
		tempBox.splice(randomAnswer,1);
	}
	if (self.correctPosition == 0) {
		self.particleBox1.textContent = self.particleBox[self.sentenceAnswer[self.whichSentence]];
		self.particleBox2.textContent = self.otherAnswers[0];
		self.particleBox3.textContent = self.otherAnswers[1];
		self.particleBox4.textContent = self.otherAnswers[2];
	} else if (self.correctPosition == 1) {
		self.particleBox1.textContent = self.otherAnswers[0];
		self.particleBox2.textContent = self.particleBox[self.sentenceAnswer[self.whichSentence]];
		self.particleBox3.textContent = self.otherAnswers[1];
		self.particleBox4.textContent = self.otherAnswers[2];
	} else if (self.correctPosition == 2) {
		self.particleBox1.textContent = self.otherAnswers[0];
		self.particleBox2.textContent = self.otherAnswers[1];
		self.particleBox3.textContent = self.particleBox[self.sentenceAnswer[self.whichSentence]];
		self.particleBox4.textContent = self.otherAnswers[2];
	} else {
		self.particleBox1.textContent = self.otherAnswers[0];
		self.particleBox2.textContent = self.otherAnswers[1];
		self.particleBox3.textContent = self.otherAnswers[2];
		self.particleBox4.textContent = self.particleBox[self.sentenceAnswer[self.whichSentence]];
	}
};

Joshi.prototype.nextItems = function() {
	var self = this;
	self.particleBox1.style.background = '';
	self.particleBox2.style.background = '';
	self.particleBox3.style.background = '';
	self.particleBox4.style.background = '';
	self.particleBox1.style.color = '';
	self.particleBox2.style.color = '';
	self.particleBox3.style.color = '';
	self.particleBox4.style.color = '';
	self.newItems();
	self.newQuestion();
};

Joshi.prototype.pickAnswer = function(answer_choice) {
	var self = this;
	if (answer_choice == self.correctPosition) {
		self.currentScore++;
		self.currentStreak++;
		self.scoreHolder.textContent = self.currentScore;
		self.streakHolder.textContent = self.currentStreak;
		var currentSentence = self.sentences[self.whichSentence];
		currentSentence = currentSentence.replace(/＿/g,self.particleBox[self.sentenceAnswer[self.whichSentence]]);
		self.sentenceBox.textContent = currentSentence;

		switch(answer_choice) {
		case 0:	// answer1
			self.particleBox1.style.background = '#89ae13';
			self.particleBox2.style.color = '#E0E0E0';
			self.particleBox3.style.color = '#E0E0E0';
			self.particleBox4.style.color = '#E0E0E0';
			break;
		case 1:	// answer2
			self.particleBox1.style.color = '#E0E0E0';
			self.particleBox2.style.background = '#89ae13';
			self.particleBox3.style.color = '#E0E0E0';
			self.particleBox4.style.color = '#E0E0E0';
			break;
		case 2:	// answer3
			self.particleBox1.style.color = '#E0E0E0';
			self.particleBox2.style.color = '#E0E0E0';
			self.particleBox3.style.background = '#89ae13';
			self.particleBox4.style.color = '#E0E0E0';
			break;
		case 3:	// answer4
			self.particleBox1.style.color = '#E0E0E0';
			self.particleBox2.style.color = '#E0E0E0';
			self.particleBox3.style.color = '#E0E0E0';
			self.particleBox4.style.background = '#89ae13';
			break;
		default:
			break
		}

		setTimeout(function(){ self.nextItems(); },900);
	} else {
			self.currentStreak = 0;
			self.streakHolder.textContent = self.currentStreak;

			switch(answer_choice) {
			case 0:	// answer1
				self.particleBox1.style.background = '#d92425';
				self.particleBox1.style.color = '#E0E0E0';
				break;
			case 1:	// answer2
				self.particleBox2.style.background = '#d92425';
				self.particleBox2.style.color = '#E0E0E0';
				break;
			case 2:	// answer3
				self.particleBox3.style.background = '#d92425';
				self.particleBox3.style.color = '#E0E0E0';
				break;
			case 3:	// answer4
				self.particleBox4.style.background = '#d92425';
				self.particleBox4.style.color = '#E0E0E0';
				break;
			default:
				break
			}

	}

};
