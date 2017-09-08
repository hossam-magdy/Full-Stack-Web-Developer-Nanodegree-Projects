/* STUDENTS IGNORE THIS FUNCTION
 * All this does is create an initial
 * attendance record if one is not found
 * within localStorage.
 */
(function() {
    if (!localStorage.attendance) {
        console.log('Creating attendance records...');
        function getRandom() {
            return (Math.random() >= 0.5);
        }

        var nameColumns = $('tbody .name-col'),
            attendance = {};

        nameColumns.each(function() {
            var name = this.innerText;
            attendance[name] = [];

            for (var i = 0; i <= 11; i++) {
                attendance[name].push(getRandom());
            }
        });

        localStorage.attendance = JSON.stringify(attendance);
    }
}());


/* STUDENT APPLICATION */
$(function() {

    model = {
        init: function(){
            this.attendance = JSON.parse(localStorage.attendance);
        },
        updateAttendance: function(studentName, day, attendance){
            this.attendance[studentName][day] = attendance;
            localStorage.attendance = JSON.stringify(this.attendance);
        },
    };
    
    octopus = {
        init: function(){
            model.init();
            view.init();
        },
        getNoOfDays: function(){
            return model.attendance[Object.keys(model.attendance)[0]].length;
        },
        getAttendance: function(){
            return model.attendance;
        },
        updateStudent: function(studentName, day, attendance){
            model.updateAttendance(studentName, day, attendance);
            view.render();
        },
        countMissedDays: function(stName){
            var c = 0;
            for(var i=0;i<this.getNoOfDays();i++){
                if(!model.attendance[stName][i]) c++;
            }
            return c;
        },
    };
    
    view = {
        init: function(){
            this.noOfDays = octopus.getNoOfDays();
            this.table = $('table#attendance');
            this.table.html('<thead><tr></tr></thead><tbody></tbody>');
            this.theadTr = this.table.find('thead tr');
            this.tbody = this.table.find('tbody');
            this.table.find('.attend-col').remove();

            this.tbodyTr = $('<tr></tr>');
            this.theadTr.append('<th class="name-col">Student Name</th>');
            this.tbodyTr.append('<td class="name-col"></td>');
            for(var i=0;i<this.noOfDays;i++){
                var elem = $('<th class="attend-col"></th>');
                elem.text(i+1);
                this.theadTr.append(elem);
                //elem.insertBefore(this.theadMissed);
                this.tbodyTr.append('<td class="attend-col"><input type="checkbox"></td>');
            }
            this.theadTr.append('<th class="missed-col">Days Missed</th>');
            this.tbodyTr.append('<td class="missed-col"></td>');
            this.tbodyTr.find('input').on('change', function(){
                var day = $(this).attr('dayN');
                var stName = $(this).closest('tr[stName]').attr('stName');
                var val = $(this).is(":checked");
                octopus.updateStudent(stName, day, val);
            });
            this.render();
        },
        render: function(){
            this.tbody.html('');
            var att = octopus.getAttendance();
            for (var stName in att) {
                var tr = view.tbodyTr.clone(true);
                tr.find('.name-col').text(stName);
                tr.attr('stName', stName);
                for(var i=0;i<this.noOfDays;i++){
                    tr.find('.attend-col:eq(' + i + ') input').attr('dayN', i).prop('checked', att[stName][i]);
                }
                tr.find('.missed-col').text(octopus.countMissedDays(stName));
                this.tbody.append(tr);
            }
        }
    };
    
    octopus.init();

}());
