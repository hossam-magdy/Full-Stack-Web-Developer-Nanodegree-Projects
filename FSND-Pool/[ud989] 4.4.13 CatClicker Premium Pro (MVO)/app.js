
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
        {
            name: "Kate",
            clickCount: 0,
            imgSrc: "https://lh3.ggpht.com/cesD31eroFxIZ4IEeXPAJkx_8i5-haU3P9LQosGNfV-GfAPUh2bE4iw4zV6Mc9XobWOR70BQh2JAP57wZlM=s0#w=640&h=480"
        },
    ],
    
    init: function() {},
    
    getCurrentCat: function() {
        return this.cats[this.currentCatKey];
    },
    
    setCurrentCatKey: function(catKey) {
        this.currentCatKey = catKey;
    },
    
    updateCurrentCatProperty: function(property, value) {
        this.cats[this.currentCatKey][property] = value;
    },
};

var octopus = {
    init: function() {
        model.init();
        view_CatList.init();
        view_CatView.init();
        view_CatAdmin.init();
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
        view_CatAdmin.render();
        //return cat.clickCount;
    },
    setCurrentCatKey: function(catKey) {
        model.setCurrentCatKey(catKey);
        view_CatView.render();
        view_CatAdmin.render();
    },
    updateCurrentCat: function(name, imgSrc, clickCount) {
        model.updateCurrentCatProperty('name', name);
        model.updateCurrentCatProperty('imgSrc', imgSrc);
        model.updateCurrentCatProperty('clickCount', clickCount);
        view_CatList.render();
        view_CatView.render();
        view_CatAdmin.render();
    }
};

var view_CatList = {
    init: function() {
        this.catListElem = $('#catList');
        this.render();
    },
    
    render: function() {
        this.catListElem.html('');
        octopus.getAllCats().forEach(function(cat, key) {
            var liElem = $('<li></li>');
            liElem.text(cat.name);
            liElem.on('click', (function(catKey) {
                return function() {
                    octopus.setCurrentCatKey(catKey);
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

var view_CatAdmin = {
    init: function() {
        this.catAdminElem = $('#admin');
        this.catAdminFormElem = this.catAdminElem.find('form');
        this.catAdminFormElem_name = this.catAdminFormElem.find('input[name="name"]');
        this.catAdminFormElem_imgSrc = this.catAdminFormElem.find('input[name="imgSrc"]');
        this.catAdminFormElem_clickCount = this.catAdminFormElem.find('input[name="clickCount"]');
        this.catAdminBtnElem = this.catAdminElem.find('#adminBtn');
        this.catAdminBtnElem.on('click', function() {
            var cat = octopus.getCurrentCat();
            view_CatAdmin.catAdminFormElem_name.val(cat.name);
            view_CatAdmin.catAdminFormElem_imgSrc.val(cat.imgSrc);
            view_CatAdmin.catAdminFormElem_clickCount.val(cat.clickCount);
            view_CatAdmin.catAdminFormElem.show();
        });
        this.catAdminFormElem.on('submit', function() {
            var name = view_CatAdmin.catAdminFormElem_name.val();
            var imgSrc = view_CatAdmin.catAdminFormElem_imgSrc.val();
            var clickCount = view_CatAdmin.catAdminFormElem_clickCount.val();
            octopus.updateCurrentCat(name, imgSrc, clickCount);
            //view_CatAdmin.catAdminFormElem.hide();
            return false;
        });
        this.catAdminFormElem.find('input[type="reset"]').on('click', function() {
            view_CatAdmin.catAdminFormElem.hide();
        });
        this.render();
    },
    
    render: function() {
        this.catAdminFormElem.hide();
    },
};

$(function() { // jQuery: onDocumentReady
    octopus.init();
});
