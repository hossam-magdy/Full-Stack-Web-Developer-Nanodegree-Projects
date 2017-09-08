
var model = {
    currentCatKey: 0,
    cats: [
        {
            name: "Kitty",
            clickCount: 0,
            imgSrc: "https://lh3.ggpht.com/nlI91wYNCrjjNy5f-S3CmVehIBM4cprx-JFWOztLk7vFlhYuFR6YnxcT446AvxYg4Ab7M1Fy0twaOCWYcUk=s0#w=640&h=426"
        },
        {
            name: "Sam",
            clickCount: 0,
            imgSrc: "https://lh3.ggpht.com/kixazxoJ2ufl3ACj2I85Xsy-Rfog97BM75ZiLaX02KgeYramAEqlEHqPC3rKqdQj4C1VFnXXryadFs1J9A=s0#w=640&h=496"
        },
    ],
    
    init: function() {},
    
    getCurrentCat: function() {
        return this.cats[this.currentCatKey];
    },
    
    setCurrentCat: function(catKey) {
        this.currentCatKey = catKey;
    }
};

var octopus = {
    init: function() {
        model.init();
        view_CatList.init();
        view_CatView.init();
    },
    getCurrentCat: function() {
        return model.cats[model.currentCatKey];
    },
    getAllCats: function() {
        return model.cats;
    },
    incrementClickCount: function() {
        var cat = this.getCurrentCat();
        cat.clickCount++;
        view_CatView.render();
        //return cat.clickCount;
    },
    setCurrentCatKey: function(catKey) {
        model.currentCatKey = catKey;
    }
};

var view_CatList = {
    init: function() {
        this.catListElem = $('#catList');
        this.render();
    },
    
    render: function() {
        octopus.getAllCats().forEach(function(cat, key) {
            var liElem = $('<li></li>');
            liElem.text(cat.name);
            liElem.on('click', (function(catKey) {
                return function() {
                    octopus.setCurrentCatKey(catKey);
                    view_CatView.render();
                };
            }) (key) );
            view_CatList.catListElem.append(liElem);
        });
    }
};

var view_CatView = {
    init: function() {
        catViewElem = $('#catView'),
        catNameElem = catViewElem.find('.catName'),
        catCountElem = catViewElem.find('.catCount'),
        catImgElem = catViewElem.find('.catImg'),
        catImgElem.on('click', function() {
            octopus.incrementClickCount();
        });
        octopus.setCurrentCatKey(0);
        this.render();
    },
    
    render: function() {
        currentCat = octopus.getCurrentCat();
        catNameElem.text(currentCat.name);
        catCountElem.text(currentCat.clickCount);
        catImgElem.attr('src', '');
        catImgElem.attr('src', currentCat.imgSrc);
    },
};

$(function() { // jQuery: onDocumentReady
    octopus.init();
});
