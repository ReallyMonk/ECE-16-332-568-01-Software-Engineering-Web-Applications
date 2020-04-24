function reset_Form() {
    //window.alert('act');
    document.getElementById("info").reset();
}

function setup_Unit(units) {
    document.getElementById("units_choice").innerHTML = "You select to use " + units + " units";
    if (units == "English") {
        document.getElementById("units_r").innerHTML = '(ft)';
        document.getElementById("units_h").innerHTML = '(ft)';
        document.getElementById("units_v").innerHTML = '(ft^3)';
    } else {
        document.getElementById("units_r").innerHTML = '(m)';
        document.getElementById("units_h").innerHTML = '(m)';
        document.getElementById("units_v").innerHTML = '(m^3)';
    }
}

function setup_Shape(shape) {
    document.getElementById("shape_choice").innerHTML = "You select to find the values for a " + shape + " shape"
    document.getElementById("res_shape").innerHTML = shape
}

function calculate() {
    var PI = 3.14
    var radius = document.getElementById("radius").value;
    var height = document.getElementById("height").value;
    var shape = document.getElementById("shape").value;
    var units = document.getElementsByName("units");

    for (i = 0; i < units.length; i++) {
        console.log(units[i].value)
        if(units[i].checked){
            unit = units[i].value
        }
    }

    var str = " radius " + radius + " height " + height + " shape " + shape + " units " + unit
    //window.alert(str)

    if (shape == 'Cone') {
        volume = PI * radius * radius * height / 3
    } else if (shape == 'Sphere') {
        volume = PI * radius * radius * radius * 4 / 3
    } else if (shape == 'Cylinder') {
        volume = PI * radius * radius * height
    }

    setup_Unit(unit)
    setup_Shape(shape)

    document.getElementById("res_r").innerHTML = radius
    document.getElementById("res_h").innerHTML = height
    document.getElementById("res_v").innerHTML = volume
}
