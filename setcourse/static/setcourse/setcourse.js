function save (level, input, value, id) {

    if (value != '') {

        toggle_save_status("false")

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
        sleep(1500).then(() => toggle_save_status("true"));
    }
}

// Small delay to simulate longer API response
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }


function toggle_save_status(status) {

    const status_div = document.getElementById("save_status")

    if (status == "false") {
        status_div.innerHTML =`<div class="lds-ring"><div></div><div></div><div></div><div></div></div>Saving...`
    }
    else {
        status_div.innerHTML = `<div id="save_check"><i class="fa-regular fa-circle-check"></i></div> Saved`
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
        console.log("new module, id:", module_id)

        module_form.innerHTML =
        `<div class="module_details">
            <div class="draft_dates">
                <input  class="module_location",
                        type="date"
                        onblur="save('module', 'start_date', value, ${module_id})">
                <input  class="module_location",
                        type="date"
                        onblur="save('module', 'end_date', value, ${module_id})">
            </div>
            <div>
                    <i class="fa-solid fa-trash", id="delete_button", onclick="handle_delete('module', ${module_id})"></i>
            </div>
        </div>
        <div class="draft_details">
            <div class="title_location">
                <input  class="module_title",
                        placeholder="Module Title",
                        onblur="save('module', 'title', value, ${module_id})">
                <input  class="module_description",
                        placeholder="Description",
                        onblur="save('module', 'description', value, ${module_id})">
            </div>
            <div class="module_description">
                <textarea   placeholder="Description",
                            onblur="save('module', 'description', value, ${module_id})"></textarea>
            </div>
        </div>

        <div class="workshop_banner", id="new_workshop_${module_id}", onclick="new_workshop(${module_id})">+ Workshop</div>
        `

        // Assign the database id to the module in the id tag
        module_form.setAttribute("id",`module_${module_id}`)

        // Creates a new +Module button
        var new_module = document.createElement('div');
        new_module.className = 'module_banner';
        new_module.id = 'new_module';
        new_module.textContent = '+ Module';
        new_module.setAttribute("onclick", "new_module()")

        // Append the new element to the content-grid div
        document.getElementById("content_grid").append(new_module);
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
        `<div class="workshop_dates">
            <input  type="datetime-local"
                    class="workshop_date_input", name="time",
                    onblur="save('workshop', 'start_time', value, ${workshop_id})">

            <input  type="datetime-local"
                    class="workshop_date_input", name="time",
                    onblur="save('workshop', 'end_time', value, ${workshop_id})">
        </div>
        <div>
            <input  class="workshop_subject_input" type="text", name="subject",
                    placeholder="Subject",
                    onblur="save('workshop', 'subject', value, ${workshop_id})">

            <i      class="fa-solid fa-trash", id="delete_button",
                    onclick="handle_delete('workshop', ${workshop_id})"></i>
            </div>`

        // Assign the database id to the workshop in the id tag
        workshop_form.setAttribute("id",`workshop_${workshop_id}`)

        // Adds a new +Workshop button for that module
        workshop_module = document.getElementById(`module_${module_id}`)

        var new_workshop_button = document.createElement("div");
        new_workshop_button.innerHTML =
            `<div class="workshop_banner", id="new_workshop_${module_id}", onclick="new_workshop(${module_id})">+ Workshop</div>`
        workshop_module.append(new_workshop_button)
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
    else if (level == "course") {
        // Redirects to profile page if whole course is deleted
        alert("deleted")
        // Delay the navigation to the profile page by 2 seconds to display the alert
        setTimeout(() => {
            window.location.href = "/profile";
        }, 2000);
        }
}


function publish(course_id) {
    fetch("/new_course", {
        method: 'POST',
        body: JSON.stringify({
            course_id: course_id,
            published: "True",
        }),
    })
    .then(response => {
        if (response.ok) {
            alert("published")
            // Delay the navigation to the profile page by 2 seconds to display the alert
            setTimeout(() => {
                window.location.href = "/profile";
            }, 2000);
        }
    })
}


function alert (type) {
    var alert = document.getElementById("alert");
    var alertContainer = document.getElementById('alert-container')
        alertContainer.style.display = 'flex';
    if (type == "published") {
        alert.innerHTML = `
        <div id="save_check"><i class="fa-regular fa-circle-check"></i></div>
        <div>Course Published!</div>`;
    }
    if (type == "deleted") {
        alert.innerHTML = `
        <div id="save_check"><i class="fa-solid fa-trash"></i></div>
        <div>Course Deleted!</div>`;
    }
}

function toggle_details (module_id) {
    extra_details = document.getElementById(`extra_details_${module_id}`)
    chevron = document.getElementById(`chevron_${module_id}`)

    chevron.style.transform = (chevron.style.transform === "scaleY(-1)") ? "scaleY(1)" : "scaleY(-1)";
    extra_details.style.display = (extra_details.style.display === "none" || extra_details.style.display === "") ? "block" : "none";
}
