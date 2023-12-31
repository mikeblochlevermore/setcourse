# CS50W Capstone

<img src="https://github.com/mikeblochlevermore/setcourse/blob/master/setcourse/static/setcourse/logo.png?raw=true" max-width="400"/>


## Watch on YouTube

[![See the Video](https://github.com/mikeblochlevermore/setcourse/blob/master/setcourse/static/setcourse/youtube_thumb.png?raw=true)](https://youtu.be/1Ub4RH4AAMA)

[See the Video](https://youtu.be/1Ub4RH4AAMA)<br>

I've worked in education for 18 years, and scheduling and coordinating courses is still awkward. I wanted to create a platform where you could easily post the details of a course, have students enroll, and then automatically have them collected into a chatroom for course discussions.

🎓 Host courses by posting details and scheduling modules

🤓 Enroll in courses as a student

🤚 Use the chat to coordinate the course


## Host a course

![Hosting Example](https://github.com/mikeblochlevermore/setcourse/blob/master/setcourse/static/setcourse/host_example.gif?raw=true)

After registering, any user can host a course through their profile.

new_course.html works as a single-page for creating courses and editing drafts of unpublished courses.

### Save onblur

During course creation / editing, when any of the input fields are deselected (onblur), a JavaScript function runs to save the contents of the input via a PUT request to the backend.

The save function handles every input by each sending unique information
for example:
```
<input  class="module_title",
        placeholder="Module Title",
        onblur="save('module', 'title', value, ${module_id})">

<input  class="module_description",
        placeholder="Location",
        onblur="save('module', 'location', value, ${module_id})">
```
![SaveExample](https://github.com/mikeblochlevermore/setcourse/blob/master/setcourse/static/setcourse/save_example.gif?raw=true)

```
function save (level, input, value, id) {

    // if new information is entered
    if (value != '') {

        // starts a spinning wheel to indicate the input is saving
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
        // artificial delay before showing the input is saved
        sleep(1500).then(() => toggle_save_status("true"));
    }
}
```
### Handling the save in views.py
The new_course function also handles GET requests to retrieve the form template (pre-populated with draft details if applicable), as well as DELETE requests to delete the course.

```
def new_course(request):

    if request.method == "PUT":
        data = json.loads(request.body)
        level = data["level"]
        input = data["input"]
        value = data["value"]

        if level == "course":
            setattr(course, input, value)
            course.save()

            print(f"COURSE id: {course.id} detail saved: {input} = {value}")

        if level == "module":
            module = Module.objects.get(id=data["id"])
            setattr(module, input, value)
            module.save()

            print(f"MODULE id: {module.id} detail saved: {input} = {value}")
```

## Modules and Workshops

![Module Example](https://github.com/mikeblochlevermore/setcourse/blob/master/setcourse/static/setcourse/module_example.gif?raw=true)

- Modules are a collection of dates (like a weekend or month)

- Workshops are sections within the module (like a day, several hours or a section)

### Adding a module

During course creation or editing, modules can be added easily by clicking on a module div, workshops are added and handled in a similar fashion.

Onclick triggers a JavaScript fuction which creates a new module / workshop element and, via a PUT request, creates the html using the unique module / workshop ID returned by the backend.

```
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
                        placeholder="Location",
                        onblur="save('module', 'location', value, ${module_id})">
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
```
## Chat

When I host an education, it typically requires a chat group to coordinate changes, questions, discussions etc. This typically required setting up a Facebook or Discord group.

- This part was largely inspired by by wife's current education which coordinates its students and all questions with huge amounts of reply-all mails (and it hurts my techie mind) 🤦

I wanted to go directly from enrollment to chatting without setting up a separate platform and avoid the added admin of collecting the students elsewhere and potentially them not having an account for that other platform, as well as other logistic issues.

![Chat Example](https://github.com/mikeblochlevermore/setcourse/blob/master/setcourse/static/setcourse/chat_example.gif?raw=true)


### Divided by module

- Chat threads are automatically divided by course modules. So there's no need to assign topics and setup a complex server (like Discord), and it's not all in one long thread (like Facebook groups).

The chat is automatically loaded at the current module, to nudge users into using the most current module to discuss what's hapenning now, or next.

Messages are loaded via a JavaScript fetch request in dashboard.js

```
function view_messages(module_id) {

    fetch(`/view_messages/${module_id}`)
    .then(response => response.json())
    .then(messages => {

      const chat_main = document.getElementById("chat_main");

    //   Display input field for that module's messages
      chat_main.innerHTML =
      `<div class="host_message">
        <form onsubmit="send_message(event, ${module_id})">
                <input class="message_form" type="text" id="message_input" name="message" placeholder="Message"></input>
                <button class="message_submit" type="submit"><i class="fa-regular fa-paper-plane"></i></button>
        </form>
      </div>`

      // If the JSON response is "No messages", set a default message
      if (messages == "No messages") {
        toggle_selected(module_id)

        var element = document.createElement("div");
        element.innerHTML = `It's still quiet on this module! Add the first post, or look at the other module's message boards`
        chat_main.append(element)

      } else {
        toggle_selected(module_id)
        // Loop through each message and create HTML elements
        messages.forEach(message => {

            var element = document.createElement("div");

            // messages by the host of the course have specific styling
            if (message.by_host == true) {
                element.innerHTML =
                    `<div class="host_message">
                        <p class="host_message_text"><strong>${message.user} (host):</strong> ${message.message}</p>
                        <p class="message_time">${message.time}</p>
                    </div>`;
            }
            else {
                element.innerHTML =
                    `<div class="message">
                        <p class="message_text"><strong>${message.user}:</strong> ${message.message}</p>
                        <p class="message_time">${message.time}</p>
                    </div>`;
            }
            chat_main.append(element);
        })
    }

    })
}
```
### Handling in views.py
```
def view_messages (request, module_id):

    if request.method == "GET":

        module = Module.objects.get(id=module_id)
        messages = Comment.objects.filter(module=module)

        messages = messages.order_by("-time").all()
        if messages:
             return JsonResponse([message.serialize() for message in messages], safe=False)
        else:
             return JsonResponse("No messages", safe=False)
```
## Profile and Enrolment

![Profile Example](https://github.com/mikeblochlevermore/setcourse/blob/master/setcourse/static/setcourse/profile_example.gif?raw=true)

On registration each user is created a profile.

As well as a username, email and password, users can have a school name (for hosting purposes) and assign url to a bio image.

A profile displays (if applicable):
1. courses in which that user is enrolled (linked to the applicable dashboard)
2. courses that user hosts (linked to course info / editing )
3. drafts (courses created but not yet published)
4. link to create a new course

Course information is rendered using a Django template:
```
    <div id="enroll_banner">
        <div>
            <h1>you're enrolled in 👇</h1>
            <h4>click the course for the dashboard and chat</h4>
        </div>
        <div id="course_list">
            {% for course in enrolled_courses %}
            <a href="{% url 'dashboard' course.id %}">
                <div class="card">
                    <div class="card_image_div">
                        <img src="{{ course.image }}">
                        <i id="image_icon" class="fa-solid fa-gauge-high"></i>
                    </div>
                    <div class="card_details">
                        <h2>{{ course.title  }}</h2>
                        <h3>{{ course.host.first_name }}</h3>
                        <div>{{ course.description|slice:":150" }}...</div>
                    </div>
                </div>
            </a>
            {% empty %}
            <p>You aren't enrolled in any courses yet</p>
            {% endfor %}
        </div>
    </div>
```


## Capstone for CS50W

This project was created as a final project for CS50s Web Development with Python and JavaScript.

- Please note there was no template for this project, all files, as well as the concept, are the creation of the author.

[See Project Specifications](https://cs50.harvard.edu/web/2020/projects/final/capstone/)


## Distinctiveness and Complexity

As per the CS50W specification, despite sharing some characteristics, I would argue that this course is neither fundamentally a social network, nor e-commerce site. Instead, this project was inspired from a common difficulty I have faced, and see others in the education industry facing - the complex coordination required to advertise the details of a course, and then gather students in a discussion forum. An issue that, in fact, e-commerce sites and social media platforms aren't great at resolving.

Typically for small educational businesses, course hosting first involves creating a website to display course information, which many outsource, making a barrier to quickly updating information about the schedule / details etc.

Following this, students might need to enroll via email, the teacher would generate an email list, then reroute those students into a discussion group such as Facebook or Discord, or perhaps, they just email back and forth all the time.

Although this project may share some similar features to my previous CS50W projects, I feel I have expanded it in complexity especially in the following areas:

- The project was created with a specific demographic in mind, and as such, I have had greater consideration for its functionallity and actual use. To aid with this thought process, I created a [Figma wireframe](https://www.figma.com/file/0liSzWJsWQoXBTBvKAc3nn/setCourse?type=design&node-id=0%3A1&mode=design&t=Od3aMNjkgxVXdi5g-1).

- This project features 6 models. Since courses, modules and workshops are nested within each other, this format required extra consideration in its implementation, for example, ensuring that when a 'new_workshop' div is clicked, it triggers the correct association to its respective module (and the same for module and course). I spent some time creating a streamlined system that assigns course, module and workshop ids and communicates them effectively between the front and back ends.
- I also devoted extra time to working on the CSS styling, since I wanted courses to appear unique, despite sharing the same template. As such, the course backgrounds are derived from a blurred, extra-saturated version of their cover photos, which preserves a colour scheme and helps each page seem unique. I have also worked more on animations, such as small pops to draw attention to actions, and created custom drop-down boxes.
- The automatic save function was also an innovation for this project - since courses can contain a lot of details, I wanted to ensure that inputs were saved periodically. I feel that this is an upgrade to previous projects that relied more on POST requests of a full form, often linked to a page refresh. I also wanted to indicate the save status via animation, to comfort users that their inputs were retained.

## Mobile Responsiveness

CSS dynamically adjusts to changes in screen dimension. Specific examples are changes to the grid layout on index.html and the reformatting of the chat layout for mobile screens.

![Mobile Example](https://github.com/mikeblochlevermore/setcourse/blob/master/setcourse/static/setcourse/mobile_example.gif?raw=true)

### File contents:
| file | description |
| ---- | ----------- |
| dashboard.js / setcourse.js | JavaScript functions |
| index.html | main landing page |
| dashboard.html | course chat and current module information |
| layout.html | generic layout and nav |
| new_course.html | editing page for courses |
| profile.html | displays enrolled, hosting and draft courses for user |
| register.html | login / registration page |
| models.py | classes for User, Course, Module, Workshop, Comment, Student |
| views.py | main Python backend |
| urls.py | routing |
| dashboard.css / styles.css | CSS styling |
| db.sqlite3 | database |

### How to run

Set up database
- python3 manage.py makemigrations
- python3 manage.py migrate

Run server
- python3 manage.py runserver

### Get in Touch!

Michael Bloch-Levermore <br>
📧 interactivephilosophy@gmail.com <br>
👤 [LinkedIn](https://www.linkedin.com/in/mike-bloch-levermore/)

