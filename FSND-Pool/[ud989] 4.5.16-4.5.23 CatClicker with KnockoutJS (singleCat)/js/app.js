
var myViewModel = function(){
    this.imgSrc = ko.observable('https://lh3.ggpht.com/nlI91wYNCrjjNy5f-S3CmVehIBM4cprx-JFWOztLk7vFlhYuFR6YnxcT446AvxYg4Ab7M1Fy0twaOCWYcUk=s0#w=640&h=426');
    this.catName = ko.observable('Kitty Cat');
    this.clickCount = ko.observable(0);
    this.nickNames = ko.observableArray(['K', 'i', 't', 'C']);
    this.catLevel = ko.computed(function(){
        if(this.clickCount()>=10) return 'Teen';
        if(this.clickCount()>=5) return 'Infant';
        return 'NewBorn';
    }, this);
    
    this.incCount = function(){
        this.clickCount(this.clickCount() + 1);
    };
};

ko.applyBindings(myViewModel);
