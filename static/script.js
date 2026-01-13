async function download() {
    const url = document.getElementById("url").value;
    const msg = document.getElementById("msg");
    const player = document.getElementById("player");
    document.querySelector(".loader").style.display = "block";

    msg.textContent = "";
    player.src = "";

    if (!url) {
        msg.textContent = "Please enter a YouTube URL";
        return;
    }

    try {
        const response = await fetch("/download", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ url })
        });

        if (!response.ok) {
            const data = await response.json();
            msg.textContent = data.error || "Download failed";
            return;
        }

        const blob = await response.blob();
        const audioURL = URL.createObjectURL(blob);

        player.src = audioURL;
        player.play();

    } catch (err) {
        msg.textContent = "Server error or network issue";
    }
}
