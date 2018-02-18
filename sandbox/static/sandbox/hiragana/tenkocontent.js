function TenkoContent() {
	this.start_index = 0;
	this.current_level = 1;
	this.level_cap = 9;
	this.level_index_max = 0;
	this.level_index_min = 0;
	this.setA = [];
	this.setB = [];
	this.tenbits = [];
	this.contentSeed();
};

TenkoContent.prototype.contentSeed = function() {
	var self = this;
	self.level_index_max = 4;
	self.level_index_min = 0;
	self.setA = ['あ','い','う','え','お','か','き','く','け','こ','さ','し','す','せ','そ','た','ち','つ','て','と','な','に','ぬ','ね','の','は','ひ','ふ','へ','ほ','ま','み','む','め','も','ら','り','る','れ','ろ','や','ゆ','よ','わ','を','ん'];
	self.setB = ['a','i','u','e','o','ka','ki','ku','ke','ko','sa','shi','su','se','so','ta','chi','tsu','te','to','na','ni','nu','ne','no','ha','hi','fu','he','ho','ma','mi','mu','me','mo','ra','ri','ru','re','ro','ya','yu','yo','wa','wo','n'];
	for (var x = 0; x < self.setA.length; x++) {
		self.tenbits[x] = new Tenbit (self.setA[x], self.setB[x], (100+x), 1, { right: 0, wrong: 0 })
	};
};

// L1 = a (L1-9: 5)
// L2 = ka
// L3 = sa
// L4 = ta
// L5 = na
// L6 = ha
// L7 = ma
// L8 = ra
// L9 = ya/wa (L9: 6)

TenkoContent.prototype.levelUp = function() {
	var self = this;
	if (self.current_level < 10) {
		self.current_level++;
	}
	if (self.current_level < self.level_cap) {
		self.level_index_min += 5;
		self.level_index_max += 5;
	} else if (self.current_level == self.level_cap) {
		self.level_index_min += 5;
		self.level_index_max += 6;
	} else {
		self.level_index_min = 0;
		self.level_index_max = self.setA.length-1;
	}
};

TenkoContent.prototype.makePlants = function(excludeMe,whichSet) {
	var self = this;
	var plants = [];
	excludeMe-=self.level_index_min;		
	if (whichSet == 0) {
		var array = self.setB.slice(self.level_index_min,self.level_index_max+1);
	} else {
		var array = self.setA.slice(self.level_index_min,self.level_index_max+1);
	};
	array.splice(excludeMe,1);
	var currentIndex = array.length, temporaryValue, randomIndex;

	// While there remain elements to shuffle...
	while (0 !== currentIndex) {
		// pick a leftover element
		randomIndex = Math.floor(Math.random() * currentIndex);
		currentIndex -= 1;

		// swap it w/current element
		temporaryValue = array[currentIndex];
		array[currentIndex] = array[randomIndex];
		array[randomIndex] = temporaryValue;
	}
	return array;	
};
