function save (level, input, value, id) {

    if (value != '') {

        // 'level' can be course, module or workshop
        // input can be title, description etc
        // value is whatever is in that field
        // id is database id of the course, module or workshop
        course_id = document.getElementById("course_id").value

        console.log("COURSE:", course_id, level, id, input, value, "-saved")

        fetch("/new_course", {
            method: 'PUT',
            body: JSON.stringify({
                course_id: course_id,
                level: level,
                input: input,
                value: value,
                id: id,
            }),
        })
    }
}

function update_image (value) {
    if (value != '') {
        image = document.getElementById("course_img")
        image.setAttribute("src", value)
    }
}

function new_module() {
    module_form = document.getElementById("new_module")

    // Stop the add new on click function for that module
    module_form.setAttribute("onclick", "")

    // Create a new module in the database and get its id
    fetch("/new_course", {
        method: 'PUT',
        body: JSON.stringify({
            new_module: "True",
            course_id: document.getElementById("course_id").value
        })
    })
    .then(response => response.json())
    .then(module_id => {
        console.log("new module id:", module_id)

        module_form.innerHTML =
            `<div class="module_form">
                <div>
                    <input  class="module_title", type="text", name="module_title", placeholder="Module Title", 
                            onblur="save('module', 'title', value, ${module_id})">
                    <input  class="module_location", type="text", name="location", placeholder="Module Location", 
                            onblur="save('module', 'location', value, ${module_id})">
                    <div>
                        <div>Start Date</div>
                        <input class="module_location", type="date",
                                onblur="save('module', 'start_date', value, ${module_id})">
                        <div>End Date</div>
                        <input class="module_location", type="date"
                                onblur="save('module', 'end_date', value, ${module_id})">
                    </div>
                </div>
                <div>
                    <input class="module_description", type="text", name="module_description", placeholder="Module Description", onblur="save('module', 'description', value, ${module_id})">
                    <i class="fa-solid fa-trash", id="delete_button", onclick="handle_delete('module', ${module_id})"></i>
                </div>
            </div>
            <div id="workshops_${module_id}">
                <div class="workshop_wrapper", id="new_workshop_${module_id}", onclick="new_workshop(${module_id})">+ Workshop</div>
            </div>`

        // Assign the database id to the module in the id tag
        module_form.setAttribute("id",`module_${module_id}`)

        // Creates a new +Module button
        modules = document.getElementById("modules")
        var new_module_button = document.createElement("div");
        new_module_button.innerHTML =
                    `<div class="module_wrapper", id="new_module", onclick="new_module()">+ Module</div>`

        modules.append(new_module_button)
    })
}


function new_workshop (module_id) {

    workshop_form = document.getElementById(`new_workshop_${module_id}`)

    // Stop the add new on click function for that module
    workshop_form.setAttribute("onclick", "")

    // Gets a database id for the newly created workshop (links to the module in question via module_id)
    fetch("/new_course", {
        method: 'PUT',
        body: JSON.stringify({
            new_workshop: "True",
            module_id: module_id,
        })
    })
    .then(response => response.json())
    .then(workshop_id => {
        console.log("new workshop id:", workshop_id)

        workshop_form.innerHTML =
            `<div class="workshop_form">
                <div>Start Time</div>
                <input class="workshop_date_input" type="datetime-local", name="time", onblur="save('workshop', 'start_time', value, ${workshop_id})">
                <div>End Time</div>
                <input class="workshop_date_input" type="datetime-local", name="time", onblur="save('workshop', 'end_time', value, ${workshop_id})">
                <input class="workshop_subject_input" type="text", name="subject", placeholder="Subject", onblur="save('workshop', 'subject', value, ${workshop_id})">
                <i class="fa-solid fa-trash", id="delete_button", onclick="handle_delete('workshop', ${workshop_id})"></i>
            </div>
            `

        // Assign the database id to the workshop in the id tag
        workshop_form.setAttribute("id",`workshop_${workshop_id}`)

        // Adds a new +Workshop button for that module
        workshops_div = document.getElementById(`workshops_${module_id}`)

        var new_workshop_button = document.createElement("div");
        new_workshop_button.innerHTML =
            `<div class="workshop_wrapper", id="new_workshop_${module_id}", onclick="new_workshop(${module_id})">+ Workshop</div>`
        workshops_div.append(new_workshop_button)
    })
}

function handle_delete (level, id) {

    fetch("/new_course", {
        method: 'DELETE',
        body: JSON.stringify({
            level: level,
            id: id
        }),
    })

    if (level == "module") {
        // Removes the module form
        module_form = document.getElementById(`module_${id}`)
        module_form.remove()
        console.log(level, id, "deleted")
        }
    else if (level == "workshop") {
        // Removes the workshop form
        workshop_form = document.getElementById(`workshop_${id}`)
        workshop_form.remove()
        console.log(level, id, "deleted")
    }

}


function publish(course_id) {

    fetch("/new_course", {
        method: 'PUT',
        body: JSON.stringify({
            course_id: course_id,
            published: "True",
        }),
    })
}


function show_details (module_id) {
    extra_details = document.getElementById(`extra_details_${module_id}`)
    chevron = document.getElementById(`chevron_${module_id}`)

    chevron.style.transform = (chevron.style.transform === "rotate(180deg)") ? "" : "rotate(180deg)";
    extra_details.style.display = (extra_details.style.display === "none" || extra_details.style.display === "") ? "block" : "none";
}

    // if (extra_details.style.display == "none") {
    //     extra_details.style.display = "block";
    // } else {
    //     extra_details.style.display = "none";
    // }
