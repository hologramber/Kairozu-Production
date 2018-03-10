function Kaimono(KaimonoInput) {
	this.KaimonoInput = new KaimonoInput;		// monitors for user input
	this.objectType = 0;
	this.numOfObjects = 0;
	this.kOrK = 1;

	this.newItems();

	this.objectSets = ['degreesc',
                        'coffee','beer','misosoup',
                        'bento','balloons','burger','ramen','fries',
                        'people',
                        'pills',
                        'tomatoes','candies','baseballs','apples','doughnuts','onigiri','cookies','chestnuts','batteries','paperclip',
                        'oden','rulers','dango','paintbrushes','pencils','bananas',
                        'papers','photographs','envelopes','shirts','pizza',
                        'books',
                        'bicycles','cars','computers',
                        'cats','mice','dogs','bees','insects','fish',
                        'birds','rabbits',
                        'boxes',
                        'floors',
                        'customers',
                        'hours'];
	this.objectIcon = ['ic icon-degreesc',
                        'ic icon-coffee','ic icon-beer','ic icon-misosoup',
                        'ic icon-bento','ic icon-balloon','ic icon-burger','ic icon-ramen','ic icon-fries',
                        'ic icon-person',
                        'ic icon-pill',
                        'ic icon-tomato','ic icon-candy','ic icon-baseball','ic icon-apple','ic icon-doughnut','ic icon-onigiri','ic icon-cookie','ic icon-chestnut','ic icon-battery','ic icon-paperclip',
                        'ic icon-oden','ic icon-ruler','ic icon-dango','ic icon-paintbrush','ic icon-pencil','ic icon-banana',
                        'ic icon-paper','ic icon-photo','ic icon-envelope','ic icon-tshirt','ic icon-pizza',
                        'ic icon-book',
                        'ic icon-bicycle','ic icon-car','ic icon-computer',
                        'ic icon-cat','ic icon-mouse','ic icon-dog','ic icon-bee','ic icon-insect','ic icon-fish',
                        'ic icon-bird','ic icon-rabbit',
                        'ic icon-box',
                        'ic icon-floor',
                        'ic icon-customer',
                        'ic icon-hour'];
	this.objectDescription = ['degrees Celsius',
                                'cups of coffee','pints of beer','cups of miso soup',
                                'bento','balloons','burgers','bowls of ramen (generic counter)','orders of fries',
                                'people',
                                'pills',
                                'tomatoes','candies','baseballs','apples','doughnuts','onigiri','cookies','chestnuts','batteries','paperclips',
                                'oden','rulers','dango','paintbrushes','pencils','bananas',
                                'sheets of paper','photographs','envelopes','shirts','pieces of pizza',
                                'books',
                                'bicycles','cars','computers',
                                'cats','mice','dogs','bees','insects','fish',
                                'birds','rabbits',
                                'boxes',
                                'building floors',
                                'customers (people; polite)',
                                'hours (duration)'];
	this.objectDescriptionSingular = ['degree Celsius',
                                        'cup of coffee','pint of beer','cup of miso soup',
                                        'bento','balloon','burger','bowl of ramen (generic counter)','order of fries',
                                        'person',
                                        'pill',
                                        'tomato','candy','baseball','apple','doughnut','onigiri','cookie','chestnut','battery','paperclip',
                                        'oden','ruler','dango','paintbrush','pencil','banana',
                                        'sheet of paper','photograph','envelope','shirt','piece of pizza',
                                        'book',
                                        'bicycle','car','computer',
                                        'cat','mouse','dog','bee','insect','fish',
                                        'bird','rabbit',
                                        'box',
                                        'building floor',
                                        'customer (person; polite)',
                                        'hour (duration)'];

	this.KaimonoInput.on("submitted", this.answerListener.bind(this));
	this.KaimonoInput.on("switcheroo", this.switchCharacters.bind(this));

	this.currentScore = 0;
	this.currentStreak = 0;
	this.entryBox = document.querySelector('.game_container');
	this.objectBox = document.querySelector('.objects_container');
	this.descriptionBox = document.querySelector('.description_container');
	this.scoreHolder = document.querySelector('.score_update');
	this.streakHolder = document.querySelector('.score_streak');
	this.kkSwitch = document.querySelector('.kanji_or_kana');
	this.switchCharacters();
	this.currentAttempts = 0;
	this.newQuestion();
}

Kaimono.prototype.newQuestion = function() {
	var self = this;
	while (self.objectBox.firstChild) {
		self.objectBox.removeChild(self.objectBox.firstChild);
	}
	for (i = 1; i <= self.numOfObjects; i++) {
		//var newObject = document.createElement("div");
		//newObject.id = objectSets[objectType];
		//objectBox.appendChild(newObject);
		var newObject = document.createElement("div");
		newObject.id = self.objectSets[self.objectType];
		newObject.className = self.objectIcon[self.objectType];
		self.objectBox.appendChild(newObject);
	}
	if (self.numOfObjects == 1) {
		self.descriptionBox.textContent = self.numOfObjects + ' ' + self.objectDescriptionSingular[self.objectType];
	} else {
		self.descriptionBox.textContent = self.numOfObjects + ' ' + self.objectDescription[self.objectType];
	}
	var textInput = document.getElementById('counter_entry');

    if (textInput.getAttribute('class') == 'kbox1 kbox1_g') {
        textInput.setAttribute('class', 'kbox1 kbox1_g_flip');
    }

};

Kaimono.prototype.newItems = function() {
	var self = this;
	self.objectType = Math.floor((Math.random() * 48));
	self.numOfObjects = Math.floor((Math.random() * 10) + 1);
};

Kaimono.prototype.nextItems = function() {
	var self = this;
	self.newItems();
	self.newQuestion();
};

Kaimono.prototype.answerListener = function() {
	var self = this;
	var textInput = document.getElementById('counter_entry');
	if (textInput.value == '') {
	} else if (textInput.value == self.objectCounters[self.objectType][self.numOfObjects-1]) {
		if (self.currentAttempts == 1) {

		} else {
			self.currentScore++;
			self.currentStreak++;
		}
		textInput.setAttribute('class', 'kbox1 kbox1_g');
		self.scoreHolder.textContent = self.currentScore;
		self.streakHolder.textContent = self.currentStreak;
		self.currentAttempts = 0;
		textInput.value = '';
		textInput.style.color = "black";
		self.nextItems();
	} else {
		textInput.value = self.objectCounters[self.objectType][self.numOfObjects-1];
		self.currentStreak = 0;
		self.streakHolder.textContent = self.currentStreak;
		textInput.style.color = "#d92425";
		textInput.setAttribute('class', 'kbox1 kbox1_r');
		self.currentAttempts = 1;
	}
};

Kaimono.prototype.switchCharacters = function () {
	if (this.kOrK == 0) {
		this.kkSwitch.textContent = '漢字';
		this.kOrK = 1;
		this.objectCounters = [
            ['一度','二度','三度','四度','五度','六度','七度','八度','九度','十度'],					// degrees class
            ['一杯','二杯','三杯','四杯','五杯','六杯','七杯','八杯','九杯','十杯'],					// cups of coffee
            ['一杯','二杯','三杯','四杯','五杯','六杯','七杯','八杯','九杯','十杯'],					// pints of beer
            ['一杯','二杯','三杯','四杯','五杯','六杯','七杯','八杯','九杯','十杯'],					// cups of miso soup
            ['一つ','二つ','三つ','四つ','五つ','六つ','七つ','八つ','九つ','十'],						// bento
            ['一つ','二つ','三つ','四つ','五つ','六つ','七つ','八つ','九つ','十'],						// balloons
            ['一つ','二つ','三つ','四つ','五つ','六つ','七つ','八つ','九つ','十'],						// burgers
            ['一つ','二つ','三つ','四つ','五つ','六つ','七つ','八つ','九つ','十'],						// ramen
            ['一つ','二つ','三つ','四つ','五つ','六つ','七つ','八つ','九つ','十'],						// orders of fries
            ['一人','二人','三人','四人','五人','六人','七人','八人','九人','十人'],					// people
            ['一錠','二錠','三錠','四錠','五錠','六錠','七錠','八錠','九錠','十錠'],					// pills
            ['一個','二個','三個','四個','五個','六個','七個','八個','九個','十個'],					// tomatoes
            ['一個','二個','三個','四個','五個','六個','七個','八個','九個','十個'],					// candies
            ['一個','二個','三個','四個','五個','六個','七個','八個','九個','十個'],					// baseballs
            ['一個','二個','三個','四個','五個','六個','七個','八個','九個','十個'],					// apples
            ['一個','二個','三個','四個','五個','六個','七個','八個','九個','十個'],					// doughnuts
            ['一個','二個','三個','四個','五個','六個','七個','八個','九個','十個'],					// onigiri
            ['一個','二個','三個','四個','五個','六個','七個','八個','九個','十個'],					// cookies
            ['一個','二個','三個','四個','五個','六個','七個','八個','九個','十個'],					// chestnuts
            ['一個','二個','三個','四個','五個','六個','七個','八個','九個','十個'],					// batteries
            ['一個','二個','三個','四個','五個','六個','七個','八個','九個','十個'],					// paperclips
            ['一本','二本','三本','四本','五本','六本','七本','八本','九本','十本'],					// oden
            ['一本','二本','三本','四本','五本','六本','七本','八本','九本','十本'],					// rulers
            ['一本','二本','三本','四本','五本','六本','七本','八本','九本','十本'],					// dango
            ['一本','二本','三本','四本','五本','六本','七本','八本','九本','十本'],					// paintbrushes
            ['一本','二本','三本','四本','五本','六本','七本','八本','九本','十本'],					// pencils
            ['一本','二本','三本','四本','五本','六本','七本','八本','九本','十本'],					// bananas
            ['一枚','二枚','三枚','四枚','五枚','六枚','七枚','八枚','九枚','十枚'],					// papers
            ['一枚','二枚','三枚','四枚','五枚','六枚','七枚','八枚','九枚','十枚'],					// photographs
            ['一枚','二枚','三枚','四枚','五枚','六枚','七枚','八枚','九枚','十枚'],					// envelopes
            ['一枚','二枚','三枚','四枚','五枚','六枚','七枚','八枚','九枚','十枚'],					// shirts
            ['一枚','二枚','三枚','四枚','五枚','六枚','七枚','八枚','九枚','十枚'],					// pieces of pizza
            ['一冊','二冊','三冊','四冊','五冊','六冊','七冊','八冊','九冊','十冊'],					// books
            ['一台','二台','三台','四台','五台','六台','七台','八台','九大','十台'],					// bicycles
            ['一台','二台','三台','四台','五台','六台','七台','八台','九大','十台'],					// cars
            ['一台','二台','三台','四台','五台','六台','七台','八台','九大','十台'],					// computers
            ['一匹','二匹','三匹','四匹','五匹','六匹','七匹','八匹','九匹','十匹'],					// cats
            ['一匹','二匹','三匹','四匹','五匹','六匹','七匹','八匹','九匹','十匹'],					// mice
            ['一匹','二匹','三匹','四匹','五匹','六匹','七匹','八匹','九匹','十匹'],					// dogs
            ['一匹','二匹','三匹','四匹','五匹','六匹','七匹','八匹','九匹','十匹'],					// bees
            ['一匹','二匹','三匹','四匹','五匹','六匹','七匹','八匹','九匹','十匹'],					// insects
            ['一匹','二匹','三匹','四匹','五匹','六匹','七匹','八匹','九匹','十匹'],					// fish
            ['一羽','二羽','三羽','四羽','五羽','六羽','七羽','八羽','九羽','十羽'],					// birds
            ['一羽','二羽','三羽','四羽','五羽','六羽','七羽','八羽','九羽','十羽'],					// rabbits
            ['一箱','二箱','三箱','四箱','五箱','六箱','七箱','八箱','九箱','十箱'],					// boxes
            ['一階','二階','三階','四階','五階','六階','七階','八階','九階','十階'],					// building floors
            ['一名','二名','三名','四名','五名','六名','七名','八名','九名','十名'],					// customers
            ['一時間','二時間','三時間','四時間','五時間','六時間','七時間','八時間','九時間','十時間']	// hours (duration)
        ];
	} else {
		this.kkSwitch.textContent = 'かな';
		this.kOrK = 0;
		this.objectCounters = [
			['いちど','にど','さんど','よんど','ごど','ろくど','ななど','はちど','きゅうど','じゅうど'],					// degrees c
			['いっぱい','にはい','さんばい','よんはい','ごはい','ろっぱい','ななはい','はっぱい','きゅうはい','じゅっぱい'],	// cups of coffee
			['いっぱい','にはい','さんばい','よんはい','ごはい','ろっぱい','ななはい','はっぱい','きゅうはい','じゅっぱい'],	// pints of beer
			['いっぱい','にはい','さんばい','よんはい','ごはい','ろっぱい','ななはい','はっぱい','きゅうはい','じゅっぱい'],	// cups of miso soup
			['ひとつ','ふたつ','みっつ','よっつ','いつつ','むっつ','ななつ','やっつ','ここのつ','とお'],					// bento
			['ひとつ','ふたつ','みっつ','よっつ','いつつ','むっつ','ななつ','やっつ','ここのつ','とお'],					// balloons
			['ひとつ','ふたつ','みっつ','よっつ','いつつ','むっつ','ななつ','やっつ','ここのつ','とお'],					// burgers
			['ひとつ','ふたつ','みっつ','よっつ','いつつ','むっつ','ななつ','やっつ','ここのつ','とお'],					// ramen
			['ひとつ','ふたつ','みっつ','よっつ','いつつ','むっつ','ななつ','やっつ','ここのつ','とお'],					// orders of fries
			['ひとり','ふたり','さんにん','よにん','ごにん','ろくにん','しちにん','はちにん','きゅうにん','じゅうにん'],		// people
			['いちじょう','にじょう','さんじょう','よんじょう','ごじょう','ろくじょう','ななじょう','はちじょう','きゅうじょう','じゅうじょう'],	// pills
			['いっこ','にこ','さんこ','よんこ','ごこ','ろっこ','ななこ','はっこ','きゅうこ','じゅっこ'],					// tomatoes
			['いっこ','にこ','さんこ','よんこ','ごこ','ろっこ','ななこ','はっこ','きゅうこ','じゅっこ'],					// candies
			['いっこ','にこ','さんこ','よんこ','ごこ','ろっこ','ななこ','はっこ','きゅうこ','じゅっこ'],					// baseballs
			['いっこ','にこ','さんこ','よんこ','ごこ','ろっこ','ななこ','はっこ','きゅうこ','じゅっこ'],					// apples
			['いっこ','にこ','さんこ','よんこ','ごこ','ろっこ','ななこ','はっこ','きゅうこ','じゅっこ'],					// doughnuts
			['いっこ','にこ','さんこ','よんこ','ごこ','ろっこ','ななこ','はっこ','きゅうこ','じゅっこ'],					// onigiri
			['いっこ','にこ','さんこ','よんこ','ごこ','ろっこ','ななこ','はっこ','きゅうこ','じゅっこ'],					// cookies
			['いっこ','にこ','さんこ','よんこ','ごこ','ろっこ','ななこ','はっこ','きゅうこ','じゅっこ'],					// chestnuts
			['いっこ','にこ','さんこ','よんこ','ごこ','ろっこ','ななこ','はっこ','きゅうこ','じゅっこ'],					// batteries
			['いっこ','にこ','さんこ','よんこ','ごこ','ろっこ','ななこ','はっこ','きゅうこ','じゅっこ'],					// paperclips
			['いっぽん','にほん','さんぼん','よんほん','ごほん','ろっぽん','ななほん','はっぽん','きゅうほん','じゅっぽん'],	// oden
			['いっぽん','にほん','さんぼん','よんほん','ごほん','ろっぽん','ななほん','はっぽん','きゅうほん','じゅっぽん'],	// rulers
			['いっぽん','にほん','さんぼん','よんほん','ごほん','ろっぽん','ななほん','はっぽん','きゅうほん','じゅっぽん'],	// dango
			['いっぽん','にほん','さんぼん','よんほん','ごほん','ろっぽん','ななほん','はっぽん','きゅうほん','じゅっぽん'],	// paintbrushes
			['いっぽん','にほん','さんぼん','よんほん','ごほん','ろっぽん','ななほん','はっぽん','きゅうほん','じゅっぽん'],	// pencils
			['いっぽん','にほん','さんぼん','よんほん','ごほん','ろっぽん','ななほん','はっぽん','きゅうほん','じゅっぽん'],	// bananas
			['いちまい','にまい','さんまい','よんまい','ごまい','ろくまい','ななまい','はちまい','きゅうまい','じゅうまい'],	// papers
			['いちまい','にまい','さんまい','よんまい','ごまい','ろくまい','ななまい','はちまい','きゅうまい','じゅうまい'],	// photographs
			['いちまい','にまい','さんまい','よんまい','ごまい','ろくまい','ななまい','はちまい','きゅうまい','じゅうまい'],	// envelopes
			['いちまい','にまい','さんまい','よんまい','ごまい','ろくまい','ななまい','はちまい','きゅうまい','じゅうまい'],	// shirts
			['いちまい','にまい','さんまい','よんまい','ごまい','ろくまい','ななまい','はちまい','きゅうまい','じゅうまい'],	// slices of pizza
			['いっさつ','にさつ','さんさつ','よんさつ','ごさつ','ろくさつ','ななさつ','はっさつ','きゅうさつ','じゅっさつ'],	// books
			['いちだい','にだい','さんだい','よんだい','ごだい','ろくだい','ななだい','はちだい','きゅうだい','じゅうだい'],	// bicycles
			['いちだい','にだい','さんだい','よんだい','ごだい','ろくだい','ななだい','はちだい','きゅうだい','じゅうだい'],	// cars
			['いちだい','にだい','さんだい','よんだい','ごだい','ろくだい','ななだい','はちだい','きゅうだい','じゅうだい'],	// computers
			['いっぴき','にひき','さんぴき','よんひき','ごひき','ろっぴき','ななひき','はっぴき','きゅうひき','じゅっぴき'],	// cats
			['いっぴき','にひき','さんぴき','よんひき','ごひき','ろっぴき','ななひき','はっぴき','きゅうひき','じゅっぴき'],	// mice
			['いっぴき','にひき','さんぴき','よんひき','ごひき','ろっぴき','ななひき','はっぴき','きゅうひき','じゅっぴき'],	// dogs
			['いっぴき','にひき','さんぴき','よんひき','ごひき','ろっぴき','ななひき','はっぴき','きゅうひき','じゅっぴき'],	// bees
			['いっぴき','にひき','さんぴき','よんひき','ごひき','ろっぴき','ななひき','はっぴき','きゅうひき','じゅっぴき'],	// insects
			['いっぴき','にひき','さんぴき','よんひき','ごひき','ろっぴき','ななひき','はっぴき','きゅうひき','じゅっぴき'],	// fish ?? (bi)
			['いちわ','にわ','さんわ','よんわ','ごわ','ろくわ','ななわ','はちわ','きゅうわ','じゅうわ'],					// birds
			['いちわ','にわ','さんわ','よんわ','ごわ','ろくわ','ななわ','はちわ','きゅうわ','じゅうわ'],					// rabbits
			['ひとはこ','ふたはこ','さんぱこ','よはこ','ごはこ','ろっぱこ','ななはこ','はっぱこ','きゅうはこ','じゅっぱこ'],	// boxes
			['いっかい','にかい','さんがい','よんかい','ごかい','ろっかい','ななかい','はっかい','きゅうかい','じゅっかい'],	//floors
			['いちめい','にめい','さんめい','よんめい','ごめい','ろくめい','ななめい','はちめい','きゅうめい','じゅうめい'],	// customers
			['いちじかん','にじかん','さんじかん','よじかん','ごじかん','ろくじかん','しちじかん','はちじかん','くじかん','じゅうじかん']	// hours
			//['','','','','','','','','','']
		];
	}
};
