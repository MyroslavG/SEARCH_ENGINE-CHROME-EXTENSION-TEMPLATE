document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("search-input");
    const searchButton = document.getElementById("search-button");
    const resultsContainer = document.getElementById("results-container");

    searchButton.addEventListener("click", function () {
        const userInput = searchInput.value.trim();

        // Make an AJAX request to Flask route /search
        fetch("/search", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: `input=${userInput}`,
        })
        .then((response) => response.json())
        .then((data) => {
            const searchResults = data.results;

            // Clear previous results
            resultsContainer.innerHTML = "";

            if (searchResults.length > 0) {
                // Display search results
                const ul = document.createElement("ul");
                ul.classList.add("search-results");

                searchResults.forEach((result) => {
                    const li = document.createElement("li");
                    li.textContent = result.name; // Assuming 'name' is the attribute of Movie class
                    ul.appendChild(li);
                });

                resultsContainer.appendChild(ul);
            } else {
                // No results found
                const noResults = document.createElement("p");
                noResults.textContent = "No results found.";
                resultsContainer.appendChild(noResults);
            }
        })
        .catch((error) => {
            console.error("Error:", error);
        });
    });
});
