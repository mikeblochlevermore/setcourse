function save (level, input, value, id) {

    // 'level' can be course, module or workshop
    // input can be title, description etc
    // value is whatever is in that field
    // id is the module or workshop id
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
            new_module: "False"
        }),
    })
}


function new_module() {
    module_form = document.getElementById("new_module")

    // Stop the click function
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
                    <input class="module_input", type="text", name="module_title", placeholder="Module Title", onblur="save('module', 'title', value, ${module_id})">
                    <input class="module_input", type="text", name="module_description", placeholder="Module Description", onblur="save('module', 'description', value, ${module_id})">
                    <input class="module_input", type="text", name="location", placeholder="Module Location", onblur="save('module', 'location', value, ${module_id})">
                    <div id="delete_button", onclick="handle_delete('module', ${module_id})"><i class="fa-solid fa-trash"></i></div>
                </form>
            </div>`

        module_form.setAttribute("id",`module_${module_id}`)

        // Append a new +Module button
        modules = document.getElementById("modules")

        var new_module_button = document.createElement("div");
        new_module_button.innerHTML =
                    `<div class="module_wrapper", id="new_module", onclick="new_module()">+ Module</div>`
        modules.append(new_module_button)
    })
}

function handle_delete (level, module_id) {

    fetch("/new_course", {
        method: 'DELETE',
        body: JSON.stringify({
            level: level,
            id: module_id
        }),
    })

    // Removes the form
    module_form = document.getElementById(`module_${module_id}`)
    module_form.remove()
    console.log(level, module_id, "deleted")
}