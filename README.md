# CS50W Capstone

<img src="https://github.com/mikeblochlevermore/setcourse/blob/master/setcourse/static/setcourse/logo.png?raw=true" max-width="400"/>


## Hosting, enrollment and chat for courses
[See the Video](https://youtu.be/tE8i0XUhj_8)<br>

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
![Hosting Example](https://github.com/mikeblochlevermore/setcourse/blob/master/setcourse/static/setcourse/host_example.gif?raw=true)

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

### Filtering posts

Depending on the page that is loaded, the view_posts function can take a "filter" variable:
"all" to view all posts
"following" to view posts from people the user is following
"{username}" to view posts from just that specific user.

For an explanation of the ${page} variable, see 'Pagination' below

```
 fetch(`/view_posts/${filter}/${page}`)
    .then(response => response.json())
    .then(posts => {

      const postList = document.querySelector('#posts');

      // Loop through each post and create HTML elements
      posts.forEach(post => {

            var element = document.createElement("div");
            element.innerHTML =
                `
                <div class="post">
                    <div class="post_wrapper">
                        <div>
                            <img class="avatar" src="${post.bio_image}">
                        </div>
                        <div>
                            <div class="post_details">
                                <strong>
                                    <a href="/profile/${post.user}">${post.user}</a>
                                </strong>
                                <div class="post_time">
                                    ${post.time}
                                </div>
                            </div>
                            <div class="post_content">
                                <div id="post_text_${post.id}">${post.content}</div>
                                <div id="edit_div_${post.id}"></div>
                            </div>
                            <div>
                                <img class="post_image" src=${post.image_url}>
                            </div>
                            <div class="like_display">
                                <div>
                                    <button
                                        onclick="like(${post.id}, ${post.liked})"
                                        id="like_button_${post.id}">
                                        🙌
                                    </button>
                                </div>
                                <div>
                                    <p id="like_count_${post.id}">${post.like_count}</p>
                                <div>
                            </div>
                        </div>
                    </div>
                </div>

                `;
                postList.append(element);
```

### Producing the json response in views.py:
Excerpt shows just the "all" filter, see views.py for the mechanism of the other filters.
To see the serialize function, see 'Liked Status' below.

```
@csrf_exempt
@login_required
def view_posts(request, filter, page):

    if request.method == "GET":

        # Options for the "filter" variable:
        # "all" to view all posts
        # "following" to see posts from people the user is following
        # "{username}" to see posts from just that specific user

            if filter == "all":
                # Query for all posts
                try:
                    posts = Post.objects.all().order_by('-time')

                except Post.DoesNotExist:
                    return JsonResponse({"error": "Posts not found."}, status=404)

        # Returns posts data as defined above
        return JsonResponse([post.serialize(request.user) for post in data], safe=False)
```

## Likes / Giving Kudos

### Liked status
Whether a post has already been 'liked' by the current user is determined below when data is fetched for the post. The 'liked' status (True / False) is sent as part of the json file containing the posts' data.

Note, this also returns whether the current user is the owner of each post, and as such has permission to edit it (can_edit = True).

```
class Post(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post")
   content = models.CharField(max_length=264)
   time = models.DateTimeField(auto_now_add=True)
   like_count = models.IntegerField(default=0)
   image_url = models.CharField(max_length=128)

   def serialize(self, current_user):
        # Includes an image of the user for each post
        bio_image = User_bio.objects.get(user=self.user).bio_image_url

        # Checks to see if the current user has already liked that post and sets a true/false status
        like = Like.objects.filter(post=self.id, user=current_user)
        if like.exists():
            liked = True
        else:
            liked = False

        # If the current user owns the post, send a token that they can edit the post
        if self.user == current_user:
            can_edit = True
        else:
            can_edit = False

        return {
            "id": self.id,
            "user": f"{self.user}",
            "bio_image": bio_image,
            "content": self.content,
            "time": self.time.strftime("%b %d %Y, %I:%M %p"),
            "like_count": self.like_count,
            "image_url": self.image_url,
            "liked": liked,
            "can_edit": can_edit,
        }
```

### Asynchronously updating the like status and count
A post that has *not* been liked by the current user will have a lightgrey hands up emoji (liked == false), indicating the lack of kudos. If the post *has* been liked, the emoji will be in color: 🙌 (liked == true).

### Identifying the like button by post
Note that because 10 posts are rendered on each page, I chose to assign the post id to the like button as part of the element's id i.e. id="like_button_${post_id}"
That way it's easier to determine which button is being clicked.


```
    <button
        onclick="like(${post.id}, ${post.liked})"
        id="like_button_${post.id}">
        🙌
    </button>

    // Set the like button styling based on whether the post is already liked by the current user
    // Onclick triggers the like(post.id, post.liked) function, passing on the id and the true/false status of previous likes

    button = document.getElementById(`like_button_${post.id}`)
    if (post.liked == true) {
        button.style.color = "black";
        button.style.textShadow = "none";
    }
    else {
        button.style.color = "transparent";
        button.style.textShadow = "0 0 0 lightgray";
    }
```

### Clicking the like button
Clicking the button in either state will update the page using JavaScript:
- the button color / styling is updated
- the like count is increased or decreased (liked / unliked)
- the onclick function is updated to reflect whether 'liked = true' or 'false'

```
    function like(post_id, liked) {

    like_counter = document.getElementById(`like_count_${post_id}`)
    button = document.getElementById(`like_button_${post_id}`)

    // if the post was previously liked, decrease the like count, change the button properties to "unliked"
    if (liked == true) {
        like_counter.innerHTML--
        button.style.color = "transparent";
        button.style.textShadow = "0 0 0 lightgray";
        button.setAttribute("onclick", `like(${post_id}, false)`)
        data = -1
    }
    // if the post was not previously liked, increase the like count, change the button properties to "liked"
    else {
        like_counter.innerHTML++
        button.style.color = "black";
        button.style.textShadow = "none";
        button.setAttribute("onclick", `like(${post_id}, true)`)
        data = 1
    }
    // sends a PUT request to the API:
    // - updates the like count via the data above (+1 or -1)
    // - saves new likes or deletes for unlikes
    fetch(`/like/${post_id}`, {
        method: 'PUT',
        body: JSON.stringify({
            like_count: data,
        }),
    })
}
```

## Following another user

On each user's bio page will be a button to follow / unfollow that user's posts.
Note if a user visits their own bio page, this button is simply replaced by an option to log out.

Whether the other user is already followed by the current user is determined via a fetch request, which gives a true/false status.

```
 fetch(`/profile/${username}/follow`)
        .then(response => response.json())
        .then(followed => {

            const follow_button_div = document.getElementById("follow_button_div");
            const button = follow_button_div.querySelector("button");

            if (followed == true) {
                // onclick the button will trigger the like function, passing on the true/false status of previous likes
                button.setAttribute("onclick", `follow('${username}', true)`)
                button.innerHTML = "Following"
                button.setAttribute("id", "unfollow_button");
            }
            else {
                button.setAttribute("onclick", `follow('${username}', false)`)
                button.innerHTML = "Follow"
                button.setAttribute("id", "follow_button");
            }
        })
    }
```

### Clicking the follow button
On activating the follow button, the follow('${username}', true/false) function is called which toggles the button styling and sends a PUT request to update the information.

```
function follow(username, followed) {

    const follow_button_div = document.getElementById("follow_button_div");
    const button = follow_button_div.querySelector("button");

    // if the account is being unfollowed - (already) followed = true:
    if (followed == true) {
        button.innerHTML = "Follow"
        button.setAttribute("id", "follow_button");
        button.setAttribute("onclick", `follow('${username}', false)`)
        // decrease the follower count
        follower_count.innerHTML--
    }
    // if the account is being followed:
    else {
        button.innerHTML = "Following"
        button.setAttribute("id", "unfollow_button");
        button.setAttribute("onclick", `follow('${username}', true)`)
        // increase the follower count
        follower_count.innerHTML++
    }

    // send the follow/unfollow request to the API
    fetch(`/profile/${username}/follow`, {
        method: 'PUT',
    })
}
```
### Registering the follow / unfollow in views.py

```
@csrf_exempt
@login_required
def follow(request, username):

    user = User.objects.get(username=username)

    if request.method == "PUT":

        followed = Follower.objects.filter(user=user, follower=request.user)
        # If the account is already followed by the user, deletes the relationship from the database
        if followed.exists():
            followed.delete()
            print("unfollowed")

        else:
            new_follow = Follower(
            user=user,
            follower=request.user)
            print(f"New Follow: USER:", new_follow.user, "FOLLOWER", new_follow.follower)
            new_follow.save()

    return HttpResponse(status=204)

```

### Follow / Follower relationship pair in models.py:

```
class Follower(models.Model):
    # user = the person being followed
    # follower = the person following this user
    # therefore the follower is FOLLOWING the user
   user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_follower")
   follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")

   def __str__(self):
        return f"{self.user}, {self.follower}"
```

## Pagination
The specification required that posts needed to be displayed on pages of 10 at a time.
I used the Paginator function in python to facilitate this:

```
 # Paginator divides the posts to 10 per page
        paginator = Paginator(posts, 10)
        data = paginator.get_page(page)

        # Returns posts data as defined previously
        return JsonResponse([post.serialize(request.user) for post in data], safe=False)
```
### The pages can be changed via chevrons on the nav bar (prev. / next)

```
function change_page(direction) {

    // Get the current page from the URL (default is page = 1)
    let current_page = parseInt(new URLSearchParams(window.location.search).get("page") || 1);

    if (direction == 'next') {
        page = current_page + 1
        link = document.getElementById("next_page_link")
    } else if (current_page > 1) {
        page = current_page - 1
        link = document.getElementById("prev_page_link")
    }

    // Updates the href to the selected link for the new page number
    link.setAttribute("href", `?page=${page}`)
}
```
## The nav in layout.html

The layout features a footer navigation with large icons.
Options are:
- Previous page
- See posts from those the current user is following
- Add a new post
- See all posts on the network (explore)
- See your personal profile page
- Next Page

```
    {% if user.is_authenticated %}
        <nav>
          <div>
            <a class="nav_item" href="?page=1" onclick="change_page('prev')" id="prev_page_link"><i class="fa-solid fa-chevron-left"></i></a>
          </div>
          <div class="nav_item">
            <a href="{% url 'following' %}"><i class="fa-solid fa-house"></i></a>
          </div>
          <div class="nav_item">
            <a href="{% url 'new_post' %}"><i class="fa-solid fa-square-plus"></i></a>
          </div>
          <div class="nav_item">
            <a href="{% url 'index' %}"><i class="fa-solid fa-earth-americas"></i></a>
          </div>
          <div class="nav_item">
            <a href="/profile/{{ user.username }}"><i class="fa-solid fa-circle-user"></i></a>
          </div>
          <div class="nav_item">
            <a class="page_link" href="?page=2" onclick="change_page('next')" id="next_page_link"><i class="fa-solid fa-chevron-right"></i></a>
          </div>
        </nav>
        {% endif %}
```

## Profile page

Each user has a bio which features a text and an image of their choosing.
On registration they are given a default image and the text 'I'm New!' - these can be changed as desired.

Bio data is stored using the model User_bio (see models.py)

- The bio data and follower/following count is rendered directly by Django
- The posts for that user are fetched via json using view_posts(username) - see above.
- The amount of followers the user has is displayed (follower_count)
- as well as the number of accounts the user follows (following_count)

```
# profile page that displays a bio and that user's posts
def profile(request, username):

    user = User.objects.get(username=username)

    # Get the number of followers the selected user has
    followers = Follower.objects.filter(user=user)
    follower_count = followers.count()

    # Get the number of accounts the selected user follows
    # (i.e. relationships where the user is the follower)
    following = Follower.objects.filter(follower=user)
    following_count = following.count()

    bio = User_bio.objects.filter(user=user)

    # If the account has just been created, set a default bio for the user
    if not bio.exists():
        default_bio = User_bio(
            user=request.user,
            bio="I'm New!",
            bio_image_url="https://emojis.wiki/thumbs/emojis/raising-hands.webp"
        )
        default_bio.save()

    bio = User_bio.objects.get(user=user)

    return render(request, "network/profile.html", {
        "username": username,
        "follower_count": follower_count,
        "following_count": following_count,
        "bio": bio,
    })
```

## Editing Posts

If a user owns a post, a button is displayed that allows them to edit the post.
Note: A similar mechanic is employed to allow users to edit their own bio text and image.

Whether the current user has permission to edit a post is sent as part of the json data when requesting data for posts (see: Liked Status).

JavaScript creates an edit button if 'can_edit == true'

```
// If the user owns the post (true/false from backend via "post.can_edit"), display an edit
edit_div = document.getElementById(`edit_div_${post.id}`)
if (post.can_edit == true) {
    edit_div.innerHTML =
    `<button id="edit_button" onclick="edit(${post.id})">
        <i class="fa-solid fa-pen-to-square"></i>
    </button>`
}
```
### Clicking the edit button
- On click, the button will display the text from the post in a textarea that can be adjusted.
- The edit button is changed to a save button
- On clicking the save button, the new text is displayed without a page refresh
- The updated information is sent via a PUT request to the backend.

```
function edit(post_id) {
    text = document.getElementById(`post_text_${post_id}`)
    old_content = text.textContent

    // Change the text to a textarea, pre-populated with the current content
    text.innerHTML = `<textarea id="editing_textarea">${old_content}</textarea>`

    // Change the edit button to a save button
    edit_div = document.getElementById(`edit_div_${post_id}`)
    edit_div.innerHTML =
    `<button id="save_button">
        <i class="fa-solid fa-circle-check"></i>
    </button>`

    let save_button = document.getElementById("save_button")
    // On clicking save, change the text on the post to the new content, then save to the server
    save_button.addEventListener("click", () => {
        new_content = text.querySelector("textarea").value
        text.innerHTML = `${new_content}`

        // Change the save button back to the edit button
        edit_div.innerHTML =
        `<button id="edit_button" onclick="edit(${post_id})">
            <i class="fa-solid fa-pen-to-square"></i>
        </button>`

        fetch("/new_post", {
            method: 'PUT',
            body: JSON.stringify({
                post_id: post_id,
                content: new_content
            }),
        })
    })
}
```

### Edits are handled by the new_post function in views.py
Note that the backend double-checks the current user is the owner of that post, before updating the post with the new information, which was sent through json data via a PUT request (see above)

```
@csrf_exempt
@login_required
def new_post(request):

    if request.method == "PUT":
        data = json.loads(request.body)
        post_id = data["post_id"]
        post = Post.objects.get(id=post_id)

        # Double-check the post is owned by the current user
        if post.user == request.user:

            post.content = data["content"]
            post.save()
            return HttpResponse(status=204)
        else:
            return JsonResponse({"error": "Current user lacks permission to edit"}, status=500)

```

### Credit to CS50W
- Basic Django setup
- Login / Logout and Registration functions in views.py
- User model in models.py
- register.html

[See Project Specifications](https://cs50.harvard.edu/web/2020/projects/4/network/)
