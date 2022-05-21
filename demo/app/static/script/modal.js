$(document).ready(function () {
    
    // example: https://getbootstrap.com/docs/4.2/components/modal/
    // show modal
    $('#add_artist_task_modal').on('show.bs.modal', (function (event) {
        console.log("add artist clicked!");
        const button = $(event.relatedTarget) // Button that triggered the modal
        const content = button.data('content') // Extract info from data-* attributes

        const modal = $(this)
        if (content) {
            modal.find('.form-control').val(content);
        } else {
            modal.find('.form-control').val('');
        }
    }));

    $('#add_song_task_modal').on('show.bs.modal', (function (event) {
        console.log("add song clicked!");
        const button = $(event.relatedTarget) // Button that triggered the modal
        const content = button.data('content') // Extract info from data-* attributes

        const modal = $(this)
        if (content) {
            modal.find('.form-control').val(content);
        } else {
            modal.find('.form-control').val('');
        }
    }));
        
    $('#edit_task_modal').on('show.bs.modal', (function (event) {
        console.log("edit clicked!");
        const button = $(event.relatedTarget) // Button that triggered the modal
        const taskID = button.data('source') // Extract info from data-* attributes
        const content = button.data('content') // Extract info from data-* attributes
        
        console.log("taskID:", taskID);
        const modal = $(this)
        if (content) {
            modal.find('.form-control').val(content);
        } else {
            modal.find('.form-control').val('');
        }
                
        modal.data('source', taskID);
    }));


    $('#save_changes_add_artist').on("click", function () {
        console.log("save changes for add artist modal clicked!");
        $.ajax({
            type: 'POST',
            url: '/create_artist',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                "name": document.getElementById('add_modal_artist_name').value,
                "followers": parseInt(document.getElementById('add_modal_artist_followers').value),
                'image': document.getElementById('add_modal_artist_image').value,
                'popularityRating': parseInt(document.getElementById('add_modal_artist_popularity').value),
            }),
            success: function (res) {
                console.log(res.response)
                location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
    });

    $('#save_changes_add_song').on("click", function () {
        console.log("save changes for add song modal clicked!");
        $.ajax({
            type: 'PUT',
            url: '/insert_song',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                "name": document.getElementById('add_modal_song_name').value,
                "genre": document.getElementById('add_modal_song_genre').value,
                'popularity': parseInt(document.getElementById('add_modal_song_popularity').value),
                'totalDuration': parseFloat(document.getElementById('add_modal_song_duration').value),
            }),
            success: function (res) {
                console.log(res.response)
                location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
    });

    $('#save_changes_edit').click(function (event) {
        console.log("save changes for edit modal clicked!");
        const tID = $("#edit_task_modal").data('source');
        console.log(`submitted changes for edit task modal with ID ${tID}`)
        $.ajax({
            type: 'PATCH',
            url: '/edit/' + tID,
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'popularityRating': parseInt(document.getElementById('edit_modal_popularity').value),
            }),
            success: function (res) {
                console.log(res.response)
                location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
    });
    
    $('.remove').click(function () {
        const remove = $(this)
        console.log("Remove clicked!")
        $.ajax({
            type: 'DELETE',
            url: '/delete/' + remove.data('source'),
            success: function (res) {
                console.log("success")
                console.log(res.response)
                location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
    });


    $('#generate_new_playlist').click(function (event) {
        $.ajax({
            type: 'POST',
            url: '/songs',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'genre': document.getElementById('search-by-genre-playlist').value,
                'start_date': parseInt(document.getElementById('search-by-start-year-playlist').value),
                'end_date':  parseInt(document.getElementById('search-by-end-year-playlist').value),
            }),
            success: function (res) {
                console.log(res.response),
                window.location.href = "playlist";
            },
            error: function (e) {
                console.log(e);
            }
        });
    });

    $('#generate_new_plot').click(function (event) {
        $.ajax({
            type: 'POST',
            url: '/plot',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'genre': document.getElementById('search-by-genre').value,
                'start_date': parseInt(document.getElementById('search-by-start-year').value),
                'end_date':  parseInt(document.getElementById('search-by-end-year').value),
            }),
            success: function (res) {
                console.log(res.response),
                window.location.href = "playlist_plots";
            },
            error: function (e) {
                console.log(e);
            }
        });
    });

    $('#search_artist').click(function (event) {
        console.log("search artist clicked!")
        console.log(document.getElementById('search-by-artist-name').value)
        $.ajax({
            type: 'POST',
            url: '/search',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'artistName': document.getElementById('search-by-artist-name').value
            }),
            success: function (res) {
                console.log(res.response),
                window.location.href = "search_results";
            },
            error: function () {
                console.log('Error');
            }
        });
    });

    $('.edit').click(function () {
        const state = $(this)
        const tID = state.data('source')
        const new_state = state.text();
        $.ajax({
            type: 'PATCH',
            url: '/edit/' + tID,
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'popularityRating': new_state
            }),
            success: function (res) {
                console.log(res)
                location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
    });

});