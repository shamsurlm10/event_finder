function up_vote(post_id, profile_id) {
    let headers = new Headers();
    headers.append('Accept', 'Application/JSON');
    headers.append('Content-Type', 'Application/JSON');
    headers.append('Authorization', getCookie("access_token"));

    let req = new Request(`/api/v1/posts/up-vote/${post_id}`, {
        method: 'PATCH',
        mode: 'cors',
        headers,
        body: JSON.stringify({
            profile_id: profile_id,
        })
    });

    const up_vote_counter = document.getElementById(`up-vote-counter-${post_id}`)
    const down_vote_counter = document.getElementById(`down-vote-counter-${post_id}`)
    const up_vote_btn = document.getElementById(`up-vote-btn-${post_id}`)
    const down_vote_btn = document.getElementById(`down-vote-btn-${post_id}`)

    fetch(req)
        .then((res) => res.json())
        .then((data) => {
            up_vote_counter.innerText = data.up_vote.length
            down_vote_counter.innerText = data.down_vote.length
            up_vote_btn.classList.toggle("btn-clicked")
            down_vote_btn.classList.remove("btn-clicked")
        })
        .catch((e) => {
            console.error(e);
        });
}

function down_vote(post_id, profile_id) {
    let headers = new Headers();
    headers.append('Accept', 'Application/JSON');
    headers.append('Content-Type', 'Application/JSON');
    headers.append('Authorization', getCookie("access_token"));

    let req = new Request(`/api/v1/posts/down-vote/${post_id}`, {
        method: 'PATCH',
        mode: 'cors',
        headers,
        body: JSON.stringify({
            profile_id: profile_id,
        })
    });

    const up_vote_counter = document.getElementById(`up-vote-counter-${post_id}`)
    const down_vote_counter = document.getElementById(`down-vote-counter-${post_id}`)
    const up_vote_btn = document.getElementById(`up-vote-btn-${post_id}`)
    const down_vote_btn = document.getElementById(`down-vote-btn-${post_id}`)

    fetch(req)
        .then((res) => res.json())
        .then((data) => {
            up_vote_counter.innerText = data.up_vote.length
            down_vote_counter.innerText = data.down_vote.length
            down_vote_btn.classList.toggle("btn-clicked")
            up_vote_btn.classList.remove("btn-clicked")
        })
        .catch((e) => {
            console.error(e);
        });
}

