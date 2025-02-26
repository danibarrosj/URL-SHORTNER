function shortenURL() {
    const longUrl = document.getElementById("long_url").value;

    let formData = new URLSearchParams();
    formData.append("long_url", longUrl);

    fetch("/shorten", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: formData.toString()
    })
    .then(response => response.json())
    .then(data => {
        if (data.short_url) {
            // ✅ Display the shortened link and a hidden input field for copying
            document.getElementById("short_url").innerHTML = `
                Short URL: <a href="${data.short_url}" target="_blank">${data.short_url}</a>
                <input type="text" value="${data.short_url}" id="copy_text" readonly style="position:absolute;left:-9999px;">
            `;
        } else {
            document.getElementById("short_url").innerHTML = "Error: " + data.error;
        }
    })
    .catch(error => console.error("Error:", error));
}

// ✅ Function to Copy the URL to Clipboard
function copyToClipboard() {
    const copyText = document.getElementById("copy_text");
    
    if (copyText) {
        copyText.select();
        copyText.setSelectionRange(0, 99999); // For mobile compatibility
        document.execCommand("copy");

        alert("Copied to clipboard: " + copyText.value);
    }
}
