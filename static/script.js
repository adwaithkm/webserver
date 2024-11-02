document.getElementById("generate-button").addEventListener("click", async () => {
    const userInput = document.getElementById("user-input").value;

    const response = await fetch("/generate_code/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ description: userInput }),
    });

    if (response.ok) {
        const data = await response.json();
        const generatedCode = data.code;
        document.getElementById("generated-code").textContent = generatedCode;
        document.getElementById("output-container").style.display = "block"; // Show output
    } else {
        alert("Error generating code.");
    }
});

document.getElementById("copy-button").addEventListener("click", () => {
    const code = document.getElementById("generated-code").textContent;
    navigator.clipboard.writeText(code).then(() => {
        alert("Code copied to clipboard!");
    }).catch(err => {
        alert("Failed to copy: ", err);
    });
});
