document.addEventListener('DOMContentLoaded', () => {
    const lyricsDiv = document.getElementById('lyrics');
    const afrobeatsSongsDiv = document.getElementById('afrobeats-songs');
    const searchForm = document.getElementById('search-form');

    afrobeatsSongsDiv.addEventListener('click', async (e) => {
        const songDiv = e.target.closest('.song');
        if (songDiv) {
            const artist = songDiv.getAttribute('data-artist');
            const title = songDiv.getAttribute('data-title');
            lyricsDiv.innerHTML = '<div class="spinner-border text-light" role="status"><span class="sr-only">Loading...</span></div>';
            const response = await fetch(`/lyrics?artist=${encodeURIComponent(artist)}&title=${encodeURIComponent(title)}`);
            const data = await response.json();
            if (data.error) {
                lyricsDiv.innerHTML = `<p>Error: ${data.error}</p>`;
            } else if (data.lyrics) {
                lyricsDiv.innerHTML = `<h3>${data.title} by ${data.artist}</h3><p><strong>Sentiment:</strong> ${data.sentiment}</p><p>${data.lyrics}</p>`;
            } else {
                lyricsDiv.innerHTML = `<p>Check artist or song name.</p>`;
            }
        }
    });

    searchForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const artist = document.getElementById('artist-search').value;
        const title = document.getElementById('title-search').value;
        lyricsDiv.innerHTML = '<div class="spinner-border text-light" role="status"><span class="sr-only">Loading...</span></div>';
        const response = await fetch(`/lyrics?artist=${encodeURIComponent(artist)}&title=${encodeURIComponent(title)}`);
        const data = await response.json();
        if (data.error) {
            lyricsDiv.innerHTML = `<p>Error: ${data.error}</p>`;
        } else if (data.lyrics) {
            lyricsDiv.innerHTML = `<h3>${data.title} by ${data.artist}</h3><p><strong>Sentiment:</strong> ${data.sentiment}</p><p>${data.lyrics}</p>`;
        } else {
            lyricsDiv.innerHTML = `<p>Check artist or song name.</p>`;
        }
    });
});