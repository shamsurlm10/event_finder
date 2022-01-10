function create_reply(profile_id, comment_id) {
    const reply_input = document.getElementById(`reply-box-${comment_id}`)
    const reply_holder = document.getElementById(`reply-holder-${comment_id}`);

    let headers = new Headers();
    headers.append('Accept', 'Application/JSON');
    headers.append('Content-Type', 'Application/JSON');
    headers.append('Authorization', getCookie("access_token"));

    let req = new Request(`/api/v1/replies`, {
        method: 'POST',
        mode: 'cors',
        headers,
        body: JSON.stringify({
            content: reply_input.value,
            profile_id: profile_id,
            comment_id: comment_id,
        })
    });

    fetch(req)
        .then((res) => res.json())
        .then((data) => {
            let replyElement = update_reply_card(data);
            reply_holder.insertBefore(
                replyElement,
                reply_holder.children[reply_holder.children.length]
            );
            reply_input.value = ""
        })
        .catch((e) => {
            console.error(e);
        });
}

function delete_reply(id) {
    let headers = new Headers();
    headers.append('Accept', 'Application/JSON');
    headers.append('Content-Type', 'Application/JSON');
    headers.append('Authorization', getCookie("access_token"));
    let req = new Request(`/api/v1/replies/${id}`, {
        method: 'DELETE',
        mode: 'cors',
        headers,
    });
    fetch(req)
        .then((res) => res.json())
        .then((data) => {
           let reply_card = document.getElementById(`card-reply-${id}`);
           reply_card.remove()
        })
        .catch((e) => {
            console.error(e);
        });
}
function update_reply_card(data) {
    const innerHTML = `
    <div class="vr"></div>
    <div class="d-flex justify-content-between">
        <div class="d-flex align-items-center">
            <img src="${ "http://" + window.location.host + "/static" + data.profile.profile_photo}"
                class="reply-img-post">
            <div class="ms-2">
                <div class="fw-bold my-0" style="font-size: 0.8rem;">
                    ${data.profile.first_name} ${data.profile.last_name}
                </div>
                <div class="text-muted my-0" style="font-size: 0.6rem;">
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
                            <i class="fas fa-pen-nib"></i> Edit reply
                        </a>
                    </li>
                    <li>
                        <button class="dropdown-item dropdown-delete" id="delte-reply-btn"
                            onclick="delete_reply(${data.id})">
                            <i class="fas fa-trash-alt"></i> Delete reply
                        </button>
                    </li>
                </ul>
            </div>
        </div>
    </div>
    <p class="mb-0" style="font-size: 0.9rem;">${data.content}</p>
    `;

    let div = document.createElement("div");
    div.id = `card-reply-${data.id}`
    div.innerHTML = innerHTML;

    return div;
}
