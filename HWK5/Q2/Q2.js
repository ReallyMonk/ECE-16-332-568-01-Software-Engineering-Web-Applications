function setup_Unit(units) {
    document.getElementById("units_choice").innerHTML = "You select to use " + units + " units";
    if (units == "English") {
        document.getElementById("units_r").innerHTML = '(ft)';
        document.getElementById("units_h").innerHTML = '(ft)';
        document.getElementById("units_v").innerHTML = '(ft^3)';
    }
    else {
        document.getElementById("units_r").innerHTML = '(m)';
        document.getElementById("units_h").innerHTML = '(m)';
        document.getElementById("units_v").innerHTML = '(m^3)';
    }
}

function setup_Shape(shape) {
    document.getElementById("shape_choice").innerHTML = "You select to find the values for a " + shape + " shape"
    document.getElementById("res_shape").innerHTML = shape
}

function reset_Form() {
    window.alert('act');
    document.getElementById("info").reset();
    setup_Unit('English');
    setup_Shape('Cone')
}

function calculate() {
    
}
