function getColumn(table_id, col) {
    var tab = document.getElementById(table_id);
    var n = tab.rows.length;
    var i, s = null, tr, td;
    var column = []

    // First check that col is not less then 0
    if (col < 0) {
        return null;
    }

    for (i = 0; i < n; i++) {
        tr = tab.rows[i];
        if (tr.cells.length > col) { // Check that cell exists before you try
            td = tr.cells[col];      // to access it.
            s += ' ' + td.innerText;
            column.push(td.innerText)
        } // Here you could say else { return null; } if you want it to fail
        // when requested column is out of bounds. It depends.
    }
    return column;
}

$('td').click(function () {
    var myCol = $(this).index();
    var txt = getColumn('table', myCol);
    var $tr = $(this).closest('tr');
    var myRow = $tr.index();
    var beforeTime = 1
    var afterTime = 24

    for (let i = myRow; i > 0; i--) {
        if (txt[i] == "X") {
            beforeTime = i
            break
        }
    }

    for (let i = myRow + 1; i < 23; i++) {
        if (txt[i] == "X") {
            afterTime = i
            break
        }
    }

    netTime = (afterTime - 1) - (beforeTime - 1)
    alert("Time between previous and next work orders: " + netTime + " hours")
});