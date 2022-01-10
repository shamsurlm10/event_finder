const post_input = document.getElementById("post-input-box");
const post_submit_btn = document.getElementById("post-input-submit");
const post_holder = document.getElementById("post-holder");


post_submit_btn.addEventListener('click', function () {
    let headers = new Headers();
    headers.append('Accept', 'Application/JSON');
    headers.append('Content-Type', 'Application/JSON');
    headers.append('Authorization', getCookie("access_token"));

    let req = new Request(`/api/v1/posts`, {
        method: 'POST',
        mode: 'cors',
        headers,
        body: JSON.stringify({
            content: post_input.value,
            profile_id: post_input.getAttribute("data-profileId"),
            event_id: post_input.getAttribute("data-eventId"),
        })
    });

    fetch(req)
        .then((res) => res.json())
        .then((data) => {
            let commentElement = update_post_card(data);
            post_holder.insertBefore(
                commentElement,
                post_holder.children[0]
            );
            post_input.value = ""
        })
        .catch((e) => {
            console.error(e);
        });
});

function delete_post(id) {
    let headers = new Headers();
    headers.append('Accept', 'Application/JSON');
    headers.append('Content-Type', 'Application/JSON');
    headers.append('Authorization', getCookie("access_token"));
    let req = new Request(`/api/v1/posts/${id}`, {
        method: 'DELETE',
        mode: 'cors',
        headers,
    });
    fetch(req)
        .then((res) => res.json())
        .then((data) => {
           let post_card = document.getElementById(`card-post-${id}`);
           post_card.remove()
        })
        .catch((e) => {
            console.error(e);
        });
}
function update_post_card(data) {
    const innerHTML = `
    <div class="px-1">
            <div class="d-flex justify-content-between">
                <div class="d-flex align-items-center">
                    <img src="${ "http://" + window.location.host + "/static" + data.profile.profile_photo}"
                        class="host-img-post">
                    <div class="ms-2">
                        <div class="fw-bold my-0">${data.profile.first_name} ${data.profile.last_name}</div>
                        <div class="text-muted my-0" style="font-size: 0.7rem;">
                            1 sec ago
                        </div>
                    </div>
                </div>
                <div class="align-self-center">
                    <div class="btn-group dropstart">
                        <button type="button" style="border: 0; background: none;" data-bs-toggle="dropdown"
                            aria-expanded="false">
                            <i class="fas fa-ellipsis-h"></i>
                        </button>
                        <ul class="dropdown-menu">
                            <li>
                                <a class="dropdown-item dropdown-edit" href="#">
                                    <i class="fas fa-pen-nib"></i> Edit post
                                </a>
                            </li>
                            <li>
                            <button class="dropdown-item dropdown-delete" onclick="delete_post(${ data.id })" data-postId="{{ post.id }}">
                                <i class="fas fa-trash-alt"></i> Delete post
                            </button>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
        <p>${data.content}</p>
        <div class="mb-2 d-flex justify-content-between" style="font-size: 0.9rem;">
            <div class="d-flex mt-2">
                <div>
                    <i class="fas fa-arrow-up"></i>
                    <span class="fw-bold">0</span>
                </div>
                <div class="ms-2">
                    <i class="fas fa-arrow-down"></i>
                    <span class="fw-bold">0</span>
                </div>
            </div>
            <div class="fw-bold text-decoration-underline" id="comment-len-${data.id}">
                ${data.comments.length} comments
            </div>
        </div>
        <hr class="my-0" />
        <div class="d-flex">
            <div class="d-flex">
                <a href="#" class="flex-fill btn btn-sm btn-light btn-vote-comment m-2 py-2 px-5">
                    <i class="fas fa-arrow-up"></i>
                    Up Vote
                </a>
                <a href="#" class="flex-fill btn btn-sm btn-light btn-vote-comment m-2 py-2 px-5">
                    <i class="fas fa-arrow-down"></i>
                    Down Vote
                </a>
            </div>
            <a href="#" class="flex-fill btn btn-sm btn-light btn-vote-comment m-2 py-2 px-5">
                <i class="far fa-comment-alt"></i>
                Comment
            </a>
        </div>
        <hr class="my-0 mb-2" />
        <div class="d-flex align-items-center mb-2">
            <img src="${ "http://" + window.location.host + "/static" + data.profile.profile_photo}"
                class="comment-img-post">
            <div class="d-flex w-100 px-2">
                <input type="text" name="comment" id="comment-box-${data.id}" data-postid="${data.id}" class="form-control input-box me-2"
                    style="border-radius: 35px;" placeholder="Write a comment..." />
                <button class="btn btn-sm btn-light px-3" id="comment-box-submit"
                    onclick="create_comment(${data.profile.id}, ${data.id})" type="submit"><i class="fas fa-paper-plane"></i></button>
            </div>
        </div>
        <div id="comment-holder-${ data.id }">
            <div id="card-comment-${data.id}"></div>
        </div>
    `;

    let div = document.createElement("div");
    div.className = "card card-body shadow-card mt-2";
    div.id = `card-post-${data.id}`
    div.innerHTML = innerHTML;

    return div;
}
