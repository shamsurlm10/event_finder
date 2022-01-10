function create_comment(profile_id, post_id) {
    const comment_input = document.getElementById(`comment-box-${post_id}`)
    const comment_holder = document.getElementById(`comment-holder-${post_id}`);


    let headers = new Headers();
    headers.append('Accept', 'Application/JSON');
    headers.append('Content-Type', 'Application/JSON');
    headers.append('Authorization', getCookie("access_token"));

    let req = new Request(`/api/v1/comments`, {
        method: 'POST',
        mode: 'cors',
        headers,
        body: JSON.stringify({
            content: comment_input.value,
            profile_id: profile_id,
            post_id: post_id,
        })
    });

    fetch(req)
        .then((res) => res.json())
        .then((data) => {
            let commentElement = update_comment_card(data);
            comment_holder.insertBefore(
                commentElement,
                comment_holder.children[comment_holder.children.length]
            );
            comment_input.value = ""
            let comment_len = document.getElementById(`comment-len-${post_id}`)
            comment_len.innerText = `${parseInt(comment_len.innerText[0])+1} comments`
        })
        .catch((e) => {
            console.error(e);
        });
}

function delete_comment(id, post_id) {
    let headers = new Headers();
    headers.append('Accept', 'Application/JSON');
    headers.append('Content-Type', 'Application/JSON');
    headers.append('Authorization', getCookie("access_token"));
    let req = new Request(`/api/v1/comments/${id}`, {
        method: 'DELETE',
        mode: 'cors',
        headers,
    });
    fetch(req)
        .then((res) => res.json())
        .then(() => {
            let comment_len = document.getElementById(`comment-len-${post_id}`)
            let comment_card = document.getElementById(`card-comment-${post_id}`);
            comment_len.innerText = `${parseInt(comment_len.innerText[0])-1} comments`
            comment_card.remove()
        })
        .catch((e) => {
            console.error(e);
        });
}

function active_comment(post_id) {
    const comment_input = document.getElementById(`comment-box-${post_id}`)
    comment_input.focus()
}

function update_comment_card(data) {
    const innerHTML = `
    <div class="vr"></div>
    <div class="mt-2">
    <div class="d-flex justify-content-between">
        <div class="d-flex align-items-center">
            <img src="${ "http://" + window.location.host + "/static" + data.profile.profile_photo}"
                class="comment-img-post">
            <div class="ms-2">
                <div class="fw-bold my-0" style="font-size: 0.9rem;">
                    ${data.profile.first_name} ${data.profile.last_name}
                </div>
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
                            <i class="fas fa-pen-nib"></i> Edit comment
                        </a>
                    </li>
                    <li>
                        <button class="dropdown-item dropdown-delete" onclick="delete_comment(${ data.id }, ${data.post_id})">
                            <i class="fas fa-trash-alt"></i> Delete comment
                        </button>
                    </li>
                </ul>
            </div>
        </div>
        </div>
        <p class="mb-0">${data.content}</p>
    </div>
    <div class="ms-5">
        <div id="reply-holder-${ data.id }">
            <div id="card-reply-${ data.id }"></div>
        </div>
        <div class="d-flex align-items-center mb-2">
            <img src="${ "http://" + window.location.host + "/static" + data.profile.profile_photo}"
                class="reply-img-post">
            <div class="d-flex w-100 px-2">
                <input type="text" name="comment" id="reply-box-${data.id}" class="form-control input-box me-2"
                    style="border-radius: 35px; font-size: 0.8rem;" placeholder="Write a reply..." />               
                <button class="btn btn-sm btn-light px-3" type="submit"
                        onclick="create_reply(${ data.profile.id }, ${ data.id })"><i
                            class="fas fa-paper-plane"></i></button>
            </div>
        </div>
    </div>
    `;

    let div = document.createElement("div");
    div.id = `card-comment-${data.id}`
    div.innerHTML = innerHTML;

    return div;
}
