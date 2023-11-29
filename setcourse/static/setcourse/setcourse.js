function save (level, input) {

    // 'level' can be course, module or workshop
    new_value = document.getElementById(input).value
    course_id = document.getElementById("course_id").value

    console.log(course_id, level, input, new_value)

    fetch("/new_course", {
        method: 'PUT',
        body: JSON.stringify({
            course_id: course_id,
            level: level,
            input: input,
            new_value: new_value,
        }),
    })
}