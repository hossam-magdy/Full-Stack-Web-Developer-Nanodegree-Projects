
var initialCats = [
    {
        catName: 'Kitty Cat',
        imgSrc: 'https://lh3.ggpht.com/nlI91wYNCrjjNy5f-S3CmVehIBM4cprx-JFWOztLk7vFlhYuFR6YnxcT446AvxYg4Ab7M1Fy0twaOCWYcUk=s0#w=640&h=426',
        clickCount: 0,
        nickNames: ['K', 'i', 't', 'C'],
    },
    {
        catName: 'Sam Cat',
        imgSrc: 'https://lh3.ggpht.com/kixazxoJ2ufl3ACj2I85Xsy-Rfog97BM75ZiLaX02KgeYramAEqlEHqPC3rKqdQj4C1VFnXXryadFs1J9A=s0#w=640&h=496',
        clickCount: 0,
        nickNames: ['S', 'i', 't', 'C'],
    },
    {
        catName: 'Kit Cat',
        imgSrc: 'https://lh3.ggpht.com/cesD31eroFxIZ4IEeXPAJkx_8i5-haU3P9LQosGNfV-GfAPUh2bE4iw4zV6Mc9XobWOR70BQh2JAP57wZlM=s0#w=640&h=480',
        clickCount: 0,
        nickNames: ['K2', 'i', 't', 'C'],
    },
];

var Cat = function(data){
    this.imgSrc = ko.observable(data.imgSrc);
    this.catName = ko.observable(data.catName);
    this.clickCount = ko.observable(data.clickCount);
    this.nickNames = ko.observableArray(data.nickNames);
    this.catLevel = ko.computed(function(){
        if(this.clickCount()>=10) return 'Teen';
        if(this.clickCount()>=5) return 'Infant';
        return 'NewBorn';
    }, this);
};

var myViewModel = function(){
    var self = this;
    
    this.catList = ko.observable([]);
    initialCats.forEach(function(cat){
        self.catList().push(new Cat(cat));
    });
    
    this.currentCat = ko.observable(self.catList()[2]);
    this.setCurrentCat = function(theCat){
        self.currentCat(theCat);
    };
    
    this.incCount = function(){
        self.currentCat().clickCount(self.currentCat().clickCount() + 1);
    };
};

ko.applyBindings( new myViewModel() );
